package main

import (
	"encoding/json"
	"regexp"
	"strconv"
	"strings"

	"github.com/reiver/go-telnet"
)

func getGames() ([][]byte, error) {
	conn, err := telnet.DialTo("127.0.0.1:8888")
	conn.Write([]byte("abcd123\n"))
	telnetReadUntil(">", conn)
	conn.Write([]byte("gl\n"))
	answer := telnetReadUntil(">", conn)

	validRegexp := regexp.MustCompile(`\|[^\|]*\|`)
	games := validRegexp.FindAll([]byte(answer), -1)
	return games, err
}

func getGamelist() ([][]byte, error) {
	games, err := getGames()
	if err != nil {
		return [][]byte{}, err
	}
	var ans [][]byte
	for i := range games {
		var raw []string
		for _, val := range strings.Split(string(games[i])[1:len(games[i])-1], " ") {
			if val != "" {
				raw = append(raw, val)
			}
		}

		game := map[string]string{"No": raw[0],
			"GameName": raw[1]}
		if len(raw) == 10 { //Game doesn't have a Password
			game["ID"] = raw[2]
			game["GameVer"] = raw[3]
			game["Type"] = raw[4]
			game["Difficulty"] = raw[5]
			game["Ladder"] = raw[6]
			game["Users"] = raw[7]
			game["CreateTime"] = raw[8]
			game["Disable"] = raw[9]
		} else {
			game["password"] = raw[2]
			game["ID"] = raw[3]
			game["GameVer"] = raw[4]
			game["Type"] = raw[5]
			game["Difficulty"] = raw[6]
			game["Ladder"] = raw[7]
			game["Users"] = raw[8]
			game["CreateTime"] = raw[9]
			game["Disable"] = raw[10]
		}
		jsonString, err := json.Marshal(game)
		if err != nil {
			return [][]byte{}, err
		}
		ans = append(ans, jsonString)
	}
	return ans, err
}

func telnetReadUntil(symbol string, conn *telnet.Conn) string {
	bs := make([]byte, 1)
	s := ""
	for string(bs) != ">" {
		conn.Read(bs)
		s += string(bs)
	}
	return s
}

func getStatus() ([]byte, error) {
	conn, _ := telnet.DialTo("127.0.0.1:8888")
	conn.Write([]byte("abcd123\n"))
	telnetReadUntil(">", conn)
	conn.Write([]byte("status\n"))
	answer := strings.Split(telnetReadUntil(">", conn), "\n")
	maxGames, _ := strconv.Atoi(strings.Split(answer[2][:len(answer[2])-1], " ")[3])
	currentGames, _ := strconv.Atoi(strings.Split(answer[3][:len(answer[3])-1], " ")[3])
	//maxUsers, _ := strconv.Atoi(strings.Split(answer[4][:len(answer[4])-1], " ")[3])
	currentUsers, _ := strconv.Atoi(strings.Split(answer[4][:len(answer[4])-1], " ")[4])
	res := map[string]int{
		"maximumCountOfGames": maxGames,
		"runningCountOfGames": currentGames,
		//"maximumCountOfUsers": maxUsers,
		"runningCountOfUsers": currentUsers,
	}

	jsonString, err := json.Marshal(res)
	return jsonString, err
}
