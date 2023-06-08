package main

import (
	"bufio"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"os"
	"strings"
	"time"
)

var (
	ShronURL      = os.Getenv("SHRON_URL")
	ShronUser     = os.Getenv("SHRON_USER")
	ShronPassword = os.Getenv("SHRON_PASSWORD")
	TargetsString = os.Getenv("UCUCUGA_HUNTER_TARGETS")
)

type secretValue struct {
	Value string `json:"value"`
}

func getSecret(c *http.Client, target string) (string, error) {
	encoded := url.QueryEscape(target)
	path := ShronURL + "secret/" + url.QueryEscape(encoded)
	req, err := http.NewRequest(http.MethodGet, path, nil)
	if err != nil {
		return "", err
	}
	req.SetBasicAuth(ShronUser, ShronPassword)
	resp, err := c.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return "", errors.New("shron returned non-ok code")
	}
	var ret secretValue
	err = json.NewDecoder(resp.Body).Decode(&ret)
	return ret.Value, err
}

func CheckTarget(c *http.Client, target string) (bool, error) {
	secret, err := getSecret(c, target)
	if err != nil {
		return false, fmt.Errorf("failed check target: %v", err)
	}
	req, err := http.NewRequest(http.MethodGet, target, nil)
	if err != nil {
		return false, err
	}
	req.Header.Add("Authorization", "Bearer " + secret)
	resp, err := c.Do(req)
	if err != nil {
		return false, err
	}
	defer resp.Body.Close()
	sc := bufio.NewScanner(resp.Body)
	for sc.Scan() {
		if val, err := DetectUcucuga(sc.Text()); val || err != nil {
			return val, err
		}
	}
	return false, nil
}

func main() {
	targets := strings.Split(TargetsString, ";")

	ticker := time.NewTicker(10 * time.Second)
	defer ticker.Stop()
	c := &http.Client{}

	for {
		select {
		case <-ticker.C:
			for _, target := range targets {
				isUcucuga, err := CheckTarget(c, target)
				if err != nil {
					log.Printf("error while checking target %q: %v", target, err)
				} else if isUcucuga {
					log.Printf("ucucuga detected at %q", target)
				}
			}
		}
	}
}
