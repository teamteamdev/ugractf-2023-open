package main_test

import (
	"net/http"
	"testing"

  ucuhunter "ucucuga-hunter"
)

func TestOrganizer(t *testing.T) {
  const url = "https://ugractf.ru"
  c := &http.Client{}
  val, err := ucuhunter.CheckTarget(c, url)
  if err != nil {
    t.Errorf("not error expected during checking %q: %v", url, err)
  } else if !val {
    t.Errorf("extected ucucuga at %q, but ucucuga was not found", url)
  }
}
