// NOTE hide here hidden lifecycle events

package main

import (
	"log"
	"os"
)

var USER string

func init() {
	USER = os.Getenv("NOTEOTP_ALL_USER")
	if USER == "" {
		USER = "user"
	}
}

type logt struct{}

var Log logt

func (logt) DbConnected(url string, isMaster bool, err error) {
	log.Printf("(db_connected) [url=%q,is_master=%t] %v", url, isMaster, err)
}

func (logt) Serving(addr string, server *Server, err error) {
	log.Printf("(serving) [addr=%q] %v", addr, err)
	if err == nil {
		go startFeeder(server)
	}
}

func (logt) Request(user, method string, code int, err error) {
	log.Printf("(request) [user=%q,method=%q,code=%d] %v", user, method, code, err)
}
