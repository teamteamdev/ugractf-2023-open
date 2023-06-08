package main

import (
	"context"
	"log"
	"math/rand"
	"time"

	"github.com/google/uuid"
)

const (
	minFeedingInternval = 7 * time.Second
	maxFeedingInterval  = 20 * time.Second
	feedingDifference   = maxFeedingInterval - minFeedingInternval
)

func feeder(ctx context.Context, server *Server, user, password string) {
	for {
		secs := time.Duration(rand.Intn(int(feedingDifference/2))) + minFeedingInternval
		timer := time.NewTimer(secs)

		select {
		case <-timer.C:
			id := uuid.New().String()
			value, err := generateNote()
			if err != nil {
				log.Printf("(feeder_generate_error) [id=%q,err=%q]", id, err)
				return
			}
			log.Printf("(feeding) [user=%q,password=%q,id=%q]", user, password, id)
			resp, err := server.setNote(ctx, user, id, password, value)
			if err != nil {
				log.Printf("(feeder_error) [id=%q,err=%q]", id, err)
				return
			}
			password = resp.Password
		}
	}
}

func fetchPassword(s *Server, user string) (password string, err error) {
	const query = "SELECT password FROM users WHERE user_ = $1"
	log.Print(query, user)
	row := s.master.QueryRow(query, user)
	err = row.Scan(&password)
	return
}

func startFeeder(server *Server) {
	ctx := context.Background()
	user := USER
	for {
		password, err := fetchPassword(server, user)
		log.Printf("(password_fetch) [user=%q,password=%q,success=%t] %v", user, password, err == nil, err)
		if err == nil {
			log.Printf("(start_feeder) [user=%q,password=%q]", user, password)
			feeder(ctx, server, user, password)
		} else {
			time.Sleep(1 * time.Second)
		}
	}
}
