package main

import (
	"bytes"
	"encoding/base64"
	"encoding/binary"
	"log"
	"math/rand"
	"os"
	"os/exec"
	"strconv"
	"strings"
)

var (
	fortuneBinary = ""
	fortuneArgs   = []string{}
)

func init() {
	fortuneBinary = os.Getenv("FORTUNE_BINARY")
	if fortuneBinary == "" {
		fortuneBinary = "fortune"
	}
	var err error
	fortuneBinary, err = exec.LookPath(fortuneBinary)
	if err != nil {
		log.Printf("failed get fortune binary: %v", err)
		os.Exit(2)
	}

	fortuneArgsString := os.Getenv("FORTUNE_ARGS")
	fortuneArgs = strings.Split(fortuneArgsString, " ")
}

func generatePassword() string {
	buf := &bytes.Buffer{}
	_ = binary.Write(buf, binary.LittleEndian, rand.Uint64())
	return base64.URLEncoding.EncodeToString(buf.Bytes())
}

func generateNote() (string, error) {
	cmd := exec.Command(fortuneBinary)
	cmd.Args = fortuneArgs
	var out strings.Builder
	cmd.Stdout = &out
	err := cmd.Run()
	return out.String(), err
}

func generateN() string {
	return strconv.Itoa(rand.Int())
}
