package main

import (
	"database/sql"
	"encoding/json"

	"fmt"
	"reflect"

	_ "github.com/lib/pq"
)

const (
	prefix           = "pvpgn_"
	host             = "localhost"
	port             = 5433
	DataBaseUser     = "postgres"
	DataBasePassword = "1qw34r78"
	dbname           = "PvPGN"
)

type pvpgn_bnet struct {
	Uid                      int
	Acct_username            NullString
	Username                 string
	Acct_userid              NullInt64
	Acct_passhash1           string
	Acct_email               string
	Auth_admin               NullString
	Auth_normallogin         NullString
	Auth_changepass          NullString
	Auth_changeprofile       NullString
	Auth_botlogin            NullString
	Auth_operator            NullString
	New_at_team_flag         NullInt64
	Auth_lock                NullString
	Auth_locktime            NullInt64
	Auth_lockreason          NullString
	Auth_mute                NullString
	Auth_mutetime            NullInt64
	Auth_mutereason          NullString
	Auth_command_groups      NullString
	Acct_lastlogin_time      int
	Acct_lastlogin_owner     string
	Acct_lastlogin_clienttag string
	Acct_lastlogin_ip        string
	Acct_ctime               string
}

type User struct {
	Passhash1           string `json:"passhash"`
	Email               string `json:"email"`
	Username            string `json:"username"`
	Lastlogin_ip        string `json:"lastlogin_ip"`
	Lastlogin_clienttag string `json:"lastlogin_clienttag"`
	Lastlogin_owner     string `json:"lastlogin_owner"`
	Lastlogin_time      int    `json:"lastlogin_time"`
	Userid              int    `json:"userid"`
	Ctime               string `json:"ctime"`
}

var db *sql.DB

func connectToDatabase() error {
	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s "+
		"password=%s dbname=%s sslmode=disable",
		host, port, DataBaseUser, DataBasePassword, dbname)
	db, _ = sql.Open("postgres", psqlInfo)
	//defer db.Close()

	err := db.Ping()
	if err != nil {
		panic(err)
	}
	return err
}

type NullString sql.NullString

// Scan implements the Scanner interface for NullInt64
func (ns *NullString) Scan(value interface{}) error {
	var s sql.NullString
	if err := s.Scan(value); err != nil {
		return err
	}

	// if nil then make Valid false
	if reflect.TypeOf(value) == nil {
		*ns = NullString{s.String, false}
	} else {
		*ns = NullString{s.String, true}
	}

	return nil
}

func (ns *NullString) MarshalJSON() ([]byte, error) {
	if !ns.Valid {
		return []byte("null"), nil
	}
	return json.Marshal(ns.String)
}

// NullInt64 is an alias for sql.NullInt64 data type
type NullInt64 sql.NullInt64

// Scan implements the Scanner interface for NullInt64
func (ni *NullInt64) Scan(value interface{}) error {
	var i sql.NullInt64
	if err := i.Scan(value); err != nil {
		return err
	}

	// if nil then make Valid false
	if reflect.TypeOf(value) == nil {
		*ni = NullInt64{i.Int64, false}
	} else {
		*ni = NullInt64{i.Int64, true}
	}
	return nil
}

func (ni *NullInt64) MarshalJSON() ([]byte, error) {
	if !ni.Valid {
		return []byte("null"), nil
	}
	return json.Marshal(ni.Int64)
}

func getUserFromDataBase(username string) (User, error) {
	rows, err := db.Query("SELECT * FROM " + prefix + "bnet where username='" + username + "';")
	if err != nil {
		panic(err)
	}
	if err != nil {
		panic(err)
	}
	defer rows.Close()

	user := pvpgn_bnet{}
	rows.Next()
	err = rows.Scan(&user.Uid, &user.Acct_username, &user.Username, &user.Acct_userid, &user.Acct_passhash1, &user.Acct_email, &user.Auth_admin, &user.Auth_normallogin, &user.Auth_changepass,
		&user.Auth_changeprofile, &user.Auth_botlogin, &user.Auth_operator, &user.New_at_team_flag, &user.Auth_lock, &user.Auth_locktime, &user.Auth_lockreason, &user.Auth_mute,
		&user.Auth_mutetime, &user.Auth_mutereason, &user.Auth_command_groups, &user.Acct_lastlogin_time, &user.Acct_lastlogin_owner, &user.Acct_lastlogin_clienttag, &user.Acct_lastlogin_ip, &user.Acct_ctime)

	if err != nil {
		fmt.Println(err)
		return User{}, err
	}
	defer rows.Close()

	final_user := User{user.Acct_passhash1, user.Acct_email, user.Username, user.Acct_lastlogin_ip, user.Acct_lastlogin_clienttag, user.Acct_lastlogin_owner,
		user.Acct_lastlogin_time, user.Uid, user.Acct_ctime}
	return final_user, err
}
