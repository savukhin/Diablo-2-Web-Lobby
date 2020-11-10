package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"regexp"
	"strconv"
	"strings"

	"github.com/reiver/go-telnet"
)

func D2GSQuery(query string) []string {
	conn, _ := telnet.DialTo(D2GSAddress)
	conn.Write([]byte(D2GSPassword + "\n"))
	telnetReadUntil(">", conn)
	conn.Write([]byte(query + "\n"))
	answer := strings.Split(telnetReadUntil(">", conn), "\n")
	return answer[1 : len(answer)-1]
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

func getGames() ([][]byte, error) {
	conn, err := telnet.DialTo(D2GSAddress)
	conn.Write([]byte(D2GSPassword + "\n"))
	telnetReadUntil(">", conn)
	conn.Write([]byte("gl\n"))
	answer := telnetReadUntil(">", conn)

	validRegexp := regexp.MustCompile(`\|[^\|]*\|`)
	games := validRegexp.FindAll([]byte(answer), -1)
	return games, err
}

func getGamelist() (*[]map[string]string, error) {
	games, err := getGames()
	if err != nil {
		fmt.Println("Why?..")
		return nil, err
	}

	ans := []map[string]string{}
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

		ans = append(ans, game)
	}

	/*jsonString, err := json.Marshal(ans)
	if err != nil {
		return []byte{}, err
	}*/
	return &ans, err
}

func getStatus() ([]byte, error) {
	conn, _ := telnet.DialTo(D2GSAddress)
	conn.Write([]byte(D2GSPassword + "\n"))
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

type GameInfo struct {
	GameName    string
	GamePass    string
	GameDesc    string
	GameID      int
	GameVer     string
	GameType    string
	Difficulty  string
	IsLadder    string
	UserCount   int
	CreateTime  string
	Disable     string
	CreatorAcct string
	CreatorChar string
	CreatorIP   string
	Users       []map[string]string
}

func parseRawGameInfo(response []string) (*GameInfo, error) {
	if len(response) < 6 {
		return nil, errors.New("Game not found")
	}

	game := map[string]string{}
	gameInfoRegexp := regexp.MustCompile(`\[[^\[]*\]`)
	for i := 1; i < 6; i++ {
		temp := gameInfoRegexp.FindAll([]byte(response[i]), -1)
		for _, value := range temp {
			field, data := "", ""
			j := 1
			for ; value[j] != ':'; j++ {
				if value[j] != ' ' {
					field = field + string(value[j])
				}
			}
			j++
			for ; value[j] != ']'; j++ {
				if value[j] != ' ' {
					data = data + string(value[j])
				}
			}
			if field != "" {
				game[field] = data
			}
		}
	}

	charactersInfo := []map[string]string{}
	columnTitles := []string{"No", "AcctName", "Charname", "IPAddress", "Class", "Level", "EnterTime"}

	for i := 8; response[i][0] != '+'; i++ {
		line := response[i]
		charactersInfo = append(charactersInfo, map[string]string{})
		word := true
		data := ""
		column := 0
		for j := 2; line[j] != '|'; j++ {
			if line[j] == ' ' && word {
				charactersInfo[i-8][columnTitles[column]] = data
				data = ""
				column++
				word = false
			} else if line[j] != ' ' {
				if !word {
					word = true
				}
				data = data + string(line[j])
			}
		}
	}
	userCount, _ := strconv.Atoi(game["UserCount"])
	gameID, _ := strconv.Atoi(game["GameID"])
	gameInfo := GameInfo{game["GameName"], game["GamePass"], game["GameDesc"], gameID, game["GameVer"], game["GameType"], game["Difficult"],
		game["IsLadder"], userCount, game["CreateTime"], game["Disable"], game["CreatorAcct"], game["CreatorChar"], game["CreatorIP"], charactersInfo}

	return &gameInfo, nil
}

func getGameInfoFromCharacter(charname string) (*GameInfo, error) {
	response := D2GSQuery("char " + charname)
	return parseRawGameInfo(response)
}

func getGameInfoById(id int) (*GameInfo, error) {
	response := D2GSQuery("cl " + strconv.Itoa(id))
	return parseRawGameInfo(response)
}
