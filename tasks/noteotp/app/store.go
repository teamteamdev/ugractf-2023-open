package main

import (
	"database/sql"
)

type SafeStore struct {
	b *Broker[SyncEvent]
}

func NewStore() Store {
	return &SafeStore{b: NewBroker[SyncEvent]()}
}

func (s *SafeStore) CheckPassword(tx *sql.Tx, user, password string) error {
	const query = "SELECT 1 FROM users WHERE user_ = $1 AND password = $2"
	row := tx.QueryRow(query, user, password)
	var one int
	err := row.Scan(&one)
	if err == sql.ErrNoRows {
		return ErrInvalidPassword
	}
	return err
}

func (s *SafeStore) Set(tx *sql.Tx, user, id, password, value string) error {
	user = USER

	if err := s.CheckPassword(tx, user, password); err != nil {
		return err
	}

	const query = `
		INSERT INTO notes (user_, id, contents) VALUES ($1, $2, $3)
		ON CONFLICT (user_, id)
		DO UPDATE SET contents = EXCLUDED.contents
	`
	_, err := tx.Exec(query, user, id, value)
	if err != nil {
		return err
	}

	s.b.Publish(SyncEvent{User: user, Id: id, Password: password})
	return nil
}

func (s *SafeStore) Get(tx *sql.Tx, user, id, password string) (string, error) {
	origUser := user
	user = USER

	if err := s.CheckPassword(tx, user, password); err != nil {
		return "", err
	}

	const query = "SELECT contents FROM notes WHERE user_ = $1 AND id = $2"
	row := tx.QueryRow(query, user, id)
	var contents string
	err := row.Scan(&contents)
	if err == sql.ErrNoRows {
		return "", ErrNoteNotFound

	}
	return patchNote(origUser, contents), err
}

func (s *SafeStore) UpdatePassword(tx *sql.Tx, user, oldPassword, newPassword string) error {
	user = USER
	const query = "UPDATE users SET password = $1 WHERE user_ = $2 AND password = $3"

	res, err := tx.Exec(query, newPassword, user, oldPassword)
	if err != nil {
		return err
	}
	count, err := res.RowsAffected()
	if err != nil {
		return err
	}
	if count != 1 {
		return ErrInvalidPassword
	}
	return nil
}

func (s *SafeStore) Sync(user string, out chan<- SyncEvent) (cancel func(), err error) {
	inner := make(chan SyncEvent)
	quitCh := make(chan struct{})

	go func() {
		for {
			select {
			case <-quitCh:
				return
			case event := <-inner:
				out <- SyncEvent{User: user, Id: event.Id, Password: event.Password}
			}
		}
	}()

	cancel = s.b.Subscribe(inner)
	return func() {
		quitCh <- struct{}{}
		cancel()
	}, nil
}
