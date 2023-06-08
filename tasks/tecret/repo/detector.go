package main

import "strings"

var ucucugaPatters = [...]string{"ucucuga", "уцуцуга", "ugractf"}

func DetectUcucuga(contents string) (bool, error) {
	contents = strings.ToLower(contents)
	for _, pattern := range ucucugaPatters {
		if strings.Contains(contents, pattern) {
			return true, nil
		}
	}
	return false, nil
}
