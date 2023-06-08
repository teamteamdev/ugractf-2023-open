package main

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"log"
	"strings"
)

const (
	flagSecret = "32800d6a5df0b7dc5b51ca6da8db949a94bd"
	suffixSize = 12
	prefix     = "ugra_cr0zy_sc1nce_run_0ut_"
)

func patchNote(user, contents string) string {
	r := strings.NewReplacer(
		"{{USER}}", user,
		"{{FLAG}}", generateFlag(user),
		"{{RANDOM_N}}", generateN(),
		"{{FAKE_PASSWORD}}", generatePassword(),
	)
	if strings.Contains(contents, "{{FLAG}}") {
		log.Printf("(flag) [user=%q, flag=%q]", user, generateFlag(user))
	}
	return r.Replace(contents)
}

func generateFlag(user string) string {
	enc := hmac.New(sha256.New, []byte(flagSecret))
	enc.Write([]byte(user))
	s := hex.EncodeToString(enc.Sum(nil))
	return prefix + s[:suffixSize]
}
