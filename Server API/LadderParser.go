package main

import (
	"encoding/binary"
	"encoding/json"
	"fmt"
	"os"
	"sort"
	"strings"
)

const LD_HEAD = "<2i"
const szLD_HEAD = 8 //calcsize(LD_HEAD)

const LD_INFO = "<Ihbb16s"
const szLD_INFO = 24 //calcsize(LD_INFO)

const LD_INDEX = "<3i"
const szLD_INDEX = 12 //calcsize(LD_INDEX)

const S_INIT = 0x1
const S_EXP = 0x20
const S_HC = 0x04
const S_DEAD = 0x08

var arr = [2]string{"Amazon", "f"}

var classes = map[int][]string{
	0x00: {"Amazon", "f"},
	0x01: {"Sorceress", "f"},
	0x02: {"Necromancer", "m"},
	0x03: {"Paladin", "m"},
	0x04: {"Barbarian", "m"},
	0x05: {"Druid", "m"},
	0x06: {"Assassin", "f"}}

var diff = map[string]map[int]map[int]map[string]string{
	"nor": {
		0x1: {0: {"m": "Sir", "f": "Dame"},
			1: {"m": "Count", "f": "Countess"}},

		0x2: {0: {"m": "Lord", "f": "Lady"},
			1: {"m": "Duke", "f": "Duchess"}},

		0x3: {0: {"m": "Baron", "f": "Baroness"},
			1: {"m": "King", "f": "Queen"}}},

	"exp": {
		0x1: {0: {"m": "Slayer", "f": "Slayer"},
			1: {"m": "Destroyer", "f": "Destroyer"}},

		0x2: {0: {"m": "Champion", "f": "Champion"},
			1: {"m": "Conqueror", "f": "Conqueror"}},

		0x3: {0: {"m": "Patriarch", "f": "Matriarch"},
			1: {"m": "Guardian", "f": "Guardian"}}}}

func remove_null(text string) string {
	return strings.Split(text, "\x00")[0]
}

/*
type character struct {
	charname   string
	prefix     string
	experience uint32
	class      string
	sex        string
	level      int
	_type      string
	difficulty int
	hc         int
	died       int
}
*/

type character struct {
	Charname   string `json:"charname"`
	Prefix     string `json:"prefix"`
	Experience uint32 `json:"experience"`
	Class      string `json:"class"`
	Sex        string `json:"sex"`
	Level      int    `json:"level"`
	Type       string `json:"type"`
	Difficulty int    `json:"difficulty"`
	Hc         int    `json:"hc"`
	Died       int    `json:"died"`
}

type ByExperience []character

func (a ByExperience) Len() int {
	return len(a)
}

func (a ByExperience) Less(i, j int) bool {
	return a[i].Experience > a[j].Experience
}

func (a ByExperience) Swap(i, j int) {
	a[i], a[j] = a[j], a[i]
}

func reverse(a []character) {
	for i, j := 0, len(a)-1; i < j; i, j = i+1, j-1 {
		a[i], a[j] = a[j], a[i]
	}
}

func get_ladder(file string) string {
	f, _ := os.Stat(file)
	size := f.Size()
	data, _ := os.Open(file)

	bs := make([]byte, 8)
	_, err := data.Read(bs)
	if err != nil {
		fmt.Println("ERROR!", err)
		return "Error"
	}
	maxtype := int(int32(binary.LittleEndian.Uint32(bs[:4])))
	//checksum := int(int32(binary.LittleEndian.Uint32(bs[4:])))

	size = size - szLD_HEAD

	var head []map[string]int

	for i := 0; i < maxtype; i++ {
		bs = make([]byte, 12)
		_, err := data.Read(bs)
		if err != nil {
			fmt.Println("ERROR!", err)
			return "ERROR"
		}
		_type := int(int32(binary.LittleEndian.Uint32(bs[:4])))
		offset := int(int32(binary.LittleEndian.Uint32(bs[4:8])))
		number := int(int32(binary.LittleEndian.Uint32(bs[8:])))
		size = size - szLD_INDEX
		head = append(head, map[string]int{"type": _type, "offset": offset, "number": number})
	}

	temp := make(map[string][]character)

	written := false
	for size > 0 {
		if len(temp["nor"]) > 0 && !written {
			fmt.Println("size: ", size)
			fmt.Println("\ttemp: ", temp["nor"])
			written = true
		}
		bs := make([]byte, 24)
		_, err := data.Read(bs)
		if err != nil {
			// Bad data
			size = size - szLD_INFO
			continue
		}

		experience := binary.LittleEndian.Uint32(bs[:4])
		status := int(int16(binary.LittleEndian.Uint16(bs[4:6])))
		level := int(bs[6])
		_class := int(bs[7])
		charname := string(bs[8:24])

		size = size - szLD_INFO

		// Avoid null chars
		if experience == 0 {
			continue
		}

		charname = remove_null(charname)
		died := 0
		_type := ""
		difficulty := 1
		hc := 0
		if status&S_EXP != 0 {
			_type = "exp"
			difficulty = ((status >> 0x08) & 0x0f) / 5
		} else {
			_type = "nor"
			difficulty = ((status >> 0x08) & 0x0f) / 5
		}
		if status&S_HC != 0 {
			hc = 1
			if status&S_DEAD != 0 {
				died = 1
			}
		} else {
			hc = 0
		}

		c_class := classes[_class]
		prefix := ""
		if _, ok := diff[_type][difficulty]; difficulty != 0 && ok == true {
			prefix = diff[_type][difficulty][hc][c_class[1]]
		} else {
			prefix = "a"
		}

		char := character{charname, prefix, experience, c_class[0], c_class[0], level, _type, difficulty, hc, died}

		// Dupe char? why?
		isExists := false
		for _, val := range temp[_type] {
			if val == char {
				isExists = true
				break
			}
		}
		if !isExists {
			temp[_type] = append(temp[_type], char)
		}
	}

	defer data.Close()

	sort.Sort(ByExperience(temp["nor"]))
	sort.Sort(ByExperience(temp["exp"]))

	ladder, err := json.Marshal(temp)
	if err != nil {
		fmt.Println("ERROR", err)
	}

	return string(ladder)
}

func parseLadder() string {
	file := "D:/PvPGN/Magic_Builder/release/var/ladders/ladder.D2DV"
	ladder := get_ladder(file)
	println(ladder)
	return ladder
}
