package main

import (
	"bytes"
	"context"
	"database/sql"
	_ "embed"
	"encoding/json"
	"errors"
	"net"
	"net/http"
	"os"
	"regexp"
	"time"

	"github.com/jackc/pgx/v5"
	_ "github.com/jackc/pgx/v5/stdlib"
)

var (
	ErrInvalidPassword  = errors.New("invalid password")
	ErrValidation       = errors.New("validation error")
	ErrNoteNotFound     = errors.New("note not found")
	ErrMethodNotAllowed = errors.New("method is not allowed")
	ErrNotFlusher       = errors.New("connection should me flushable")

	userPattern = "([a-zA-Z0-9]{1,255})"
	indexRegexp = regexp.MustCompile("^/" + userPattern + "/?$")
	noteRegexp  = regexp.MustCompile("^/" + userPattern + "/([a-zA-Z0-9-]*)/?$")
	syncRegexp  = regexp.MustCompile("^/sync/" + userPattern + "/?$")
)

//go:embed index.html
var indexHtml []byte

var modTime = time.Now()

type SyncEvent struct {
	User     string `json:"user"`
	Id       string `json:"id"`
	Password string `json:"old_password"`
}

type Store interface {
	Set(tx *sql.Tx, user, id, password, value string) error
	Get(tx *sql.Tx, user, id, password string) (string, error)
	UpdatePassword(tx *sql.Tx, user, oldPassword, newPassword string) error

	Sync(user string, out chan<- SyncEvent) (cancel func(), err error)
}

type Server struct {
	store   Store
	master  *sql.DB
	replica *sql.DB
}

type Response struct {
	Password string `json:"new_password"`
	Contents string `json:"contents"`
}

func (s *Server) getPassword(user string, r *http.Request) (string, error) {
	user2, password, ok := r.BasicAuth()

	if !ok || user2 != user {
		return "", ErrInvalidPassword
	}
	return password, nil

}

func (s *Server) getNote(ctx context.Context, user, id, password string) (Response, error) {
	tx, err := s.replica.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelReadCommitted, ReadOnly: true})
	// NOTE ignore error here
	if err != nil {
		return Response{}, err
	}
	defer tx.Rollback()
	value, err := s.store.Get(tx, user, id, password)
	if err != nil {
		return Response{}, err
	}
	if err := tx.Commit(); err != nil {
		return Response{}, err
	}
	newPassword := generatePassword()
	go func() {
		tx, err := s.master.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelSerializable})
		if err == nil {
			if err := s.store.UpdatePassword(tx, user, password, newPassword); err != nil {
				// NOTE ignore error here
				tx.Rollback()
			} else {
				// NOTE ignore error here
				tx.Commit()
			}
		}
	}()
	return Response{
		Contents: value,
		Password: newPassword,
	}, nil
}

func (s *Server) setNote(ctx context.Context, user, id, password, value string) (Response, error) {
	tx, err := s.master.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelSerializable})
	if err != nil {
		return Response{}, err
	}
	// NOTE ignore error here
	defer tx.Rollback()
	err = s.store.Set(tx, user, id, password, value)
	if err != nil {
		return Response{}, err
	}
	newPassword := generatePassword()
	if err := s.store.UpdatePassword(tx, user, password, newPassword); err != nil {
		return Response{}, err
	}
	if err := tx.Commit(); err != nil {
		return Response{}, err
	}
	return Response{
		Contents: value,
		Password: newPassword,
	}, nil
}

func (s *Server) sync(ctx context.Context, w http.ResponseWriter, user string) error {
	flusher, ok := w.(http.Flusher)
	if !ok {
		return ErrNotFlusher
	}
	ch := make(chan SyncEvent)
	cancel, err := s.store.Sync(user, ch)
	if err != nil {
		return err
	}
	defer cancel()
	enc := json.NewEncoder(w)
	w.Header().Add("Content-Type", "application/ndjson")
	w.WriteHeader(http.StatusOK)
	flusher.Flush()
	for {
		select {
		case <-ctx.Done():
			return nil
		case val := <-ch:
			err := enc.Encode(val)
			if err != nil {
				return err
			}
			flusher.Flush()
		}
	}
}

func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	var err error
	var user, id, password string
	path := r.URL.Path
	ctx := r.Context()
	if sync := syncRegexp.FindStringSubmatch(path); sync != nil {
		user = sync[1]
		if err == nil {
			err = s.sync(ctx, w, user)
		}
	} else if indexRegexp.MatchString(path) {
		f := bytes.NewReader(indexHtml)
		http.ServeContent(w, r, "index.html", modTime, f)
	} else if note := noteRegexp.FindStringSubmatch(path); note != nil {
		user, id = note[1], note[2]
		if id == "" {
			err = ErrValidation
		} else {
			password, err = s.getPassword(user, r)
			if err == nil {
				var resp Response
				switch r.Method {
				case http.MethodGet:
					resp, err = s.getNote(ctx, user, id, password)
				case http.MethodPost:
					err = r.ParseForm()
					if err == nil {
						resp, err = s.setNote(ctx, user, id, password, r.PostFormValue("contents"))
					}
				default:
					err = ErrMethodNotAllowed
				}

				if err == nil {
					enc := json.NewEncoder(w)
					err = enc.Encode(resp)
				}
			}
		}
	} else {
		http.NotFound(w, r)
		return
	}

	var code int
	switch err {
	case nil:
		return
	case ErrInvalidPassword:
		code = http.StatusUnauthorized
	case ErrNoteNotFound:
		code = http.StatusNotFound
	case ErrMethodNotAllowed:
		code = http.StatusMethodNotAllowed
	case ErrNotFlusher:
		code = http.StatusExpectationFailed
	case ErrValidation:
		code = http.StatusUnprocessableEntity
	case sql.ErrTxDone:
		fallthrough
	case pgx.ErrTxClosed:
		fallthrough
	case pgx.ErrTxCommitRollback:
		// You hacked
		code = http.StatusTeapot
	default:
		code = http.StatusInternalServerError
	}
	Log.Request(user, r.Method, code, err)

	http.Error(w, http.StatusText(code), code)
}

func main() {
	masterUrl := os.Getenv("MASTER_URL")
	master, err := sql.Open("pgx", masterUrl)
	if err != nil {
		Log.DbConnected(masterUrl, true, err)
		os.Exit(1)
	}
	defer master.Close()
	err = master.Ping()
	Log.DbConnected(masterUrl, true, err)
	if err != nil {
		os.Exit(1)
	}
	replicaUrl := os.Getenv("REPLICA_URL")
	replica, err := sql.Open("pgx", replicaUrl)
	if err != nil {
		Log.DbConnected(replicaUrl, false, err)
		os.Exit(1)
	}
	defer replica.Close()
	err = replica.Ping()
	Log.DbConnected(replicaUrl, false, err)
	if err != nil {
		os.Exit(1)
	}

	store := NewStore()
	server := Server{store, master, replica}

	host := os.Getenv("HOST")
	lis, err := net.Listen("unix", host)
	Log.Serving(host, &server, err)
	if err != nil {
		os.Exit(3)
	}
	http.Serve(lis, &server)
}
