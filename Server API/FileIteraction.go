package main

import (
	"bufio"
	"encoding/json"
	"io/ioutil"
	"os"
	"regexp"
	"strconv"

	"github.com/nokka/d2s"
)

func getAllUsersFromFile() ([]byte, error) {
	directory := pathToUsersFolder
	files, err := ioutil.ReadDir(directory)
	if err != nil {
		return nil, err
	}

	users := []User{}
	for _, file := range files {
		file, err := os.Open(directory + file.Name())
		if err != nil {
			continue
		}

		defer file.Close()
		scanner := bufio.NewScanner(file)

		user := map[string]string{}
		fieldRegexp := regexp.MustCompile(`^.[^"]*`)
		for scanner.Scan() {
			line := scanner.Text()
			line = line[len("\"BNET\\\\acct\\\\"):] //Line format is "BNET\\acct\\username"="user"
			field := fieldRegexp.Find([]byte(line))
			user[string(field)] = line[len(field)+3 : len(line)-1]
		}

		lastlogin_time_int, _ := strconv.Atoi(user["lastlogin_time"])
		userid_int, _ := strconv.Atoi(user["userid"])
		characters, err := getCharactersFromUser(user["username"])
		if err != nil {
			return nil, err
		}
		user_final := User{user["passhash1"], user["email"], user["username"], user["lastlogin_ip"], user["lastlogin_clienttag"],
			user["lastlogin_owner"], lastlogin_time_int, userid_int, user["ctime"], characters}

		users = append(users, user_final)
	}

	jsonString, err := json.Marshal(users)
	if err != nil {
		return nil, err
	}

	return jsonString, nil
}

func getCharactersFromUser(username string) ([]string, error) {
	directory := "D:/PvPGN/Magic_Builder/release/var/charinfo/" + username + "/"
	files, err := ioutil.ReadDir(directory)
	if err != nil {
		return nil, err
	}
	charnames := []string{}
	for _, f := range files {
		if !f.IsDir() {
			charnames = append(charnames, f.Name())
		}
	}
	return charnames, err
}

func getCharacterFromFile(charname string) (*d2s.Character, error) {
	directory := pathToCharSaveFolder
	file, err := os.Open(directory + charname)
	defer file.Close()
	char, err := d2s.Parse(file)
	return char, err
}
