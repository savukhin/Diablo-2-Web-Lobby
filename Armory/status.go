package main

// status struct will represent the characters in game status.
type status byte

type readableStatus struct {
	Expansion bool `json:"expansion"`
	Died      bool `json:"died"`
	Hardcore  bool `json:"hardcore"`
	Ladder    bool `json:"ladder"`
}

// Readable will return a readable format for the status byte.
func (s status) Readable() readableStatus {
	return readableStatus{
		Expansion: ((s >> 5) & 1) > 0,
		Died:      ((s >> 3) & 1) > 0,
		Hardcore:  ((s >> 2) & 1) > 0,
		Ladder:    ((s >> 6) & 1) > 0,
	}
}
