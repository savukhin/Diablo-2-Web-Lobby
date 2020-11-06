package main

import (
	"bufio"
	"io/ioutil"
	"os"
	"regexp"
	"strconv"
	"strings"

	"github.com/nokka/d2s"
)

func getUserFromFile(username string) (User, error) {
	directory := "D:/PvPGN/PvPGN/var/users/" + username
	file, err := os.Open(directory)
	if err != nil {
		return User{}, err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	answer := map[string]string{}
	fieldRegexp := regexp.MustCompile(`^.[^"]*`)
	for scanner.Scan() {
		line := scanner.Text()
		line = line[len("\"BNET\\\\acct\\\\"):] //Line format is "BNET\\acct\\username"="user"
		field := fieldRegexp.Find([]byte(line))
		answer[string(field)] = line[len(field)+3 : len(line)-1]
	}

	lastlogin_time_int, _ := strconv.Atoi(answer["lastlogin_time"])
	userid_int, _ := strconv.Atoi(answer["userid"])
	user := User{answer["passhash1"], answer["email"], answer["username"], answer["lastlogin_ip"], answer["lastlogin_clienttag"],
		answer["lastlogin_owner"], lastlogin_time_int, userid_int, answer["ctime"]}
	return user, err
}

func registerUserInFile(username string, passhash string, email string) (User, error) {
	directory := "D:/PvPGN/PvPGN/var/users/"
	files, err := ioutil.ReadDir(directory)
	if err != nil {
		return User{}, err
	}
	newid := len(files) + 1
	data := `"BNET\\acct\\passhash1"="` + passhash + `"
"BNET\\acct\\email"="` + email + `"
"BNET\\acct\\username"="` + strings.ToLower(username) + `"
"BNET\\acct\\lastlogin_ip"="0"
"BNET\\acct\\lastlogin_clienttag"="D2XP"
"BNET\\acct\\lastlogin_owner"="Panky"
"BNET\\acct\\lastlogin_time"="0"
"BNET\\acct\\userid"="` + strconv.Itoa(newid) + `"
"BNET\\acct\\ctime"="0"`
	ioutil.WriteFile(directory+username, []byte(data), 0644)
	user, err := getUserFromFile(username)
	return user, err
}

func getCharacterFromFile(username string) (*d2s.Character, error) {
	directory := "D:/PvPGN/Magic_Builder/release/var/charsave/"
	file, err := os.Open(directory + username)
	defer file.Close()
	char, err := d2s.Parse(file)
	return char, err
}
