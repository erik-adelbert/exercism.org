package stateoftictactoe

import (
	"errors"
	"strings"
)

type State string

const (
	Nil     State = ""
	Win     State = "win"
	Ongoing State = "ongoing"
	Draw    State = "draw"
)

var ErrInvalidBoard = errors.New("invalid board")

func StateOfTicTacToe(board []string) (State, error) {
	flat := strings.ToUpper(strings.Join(board, ""))

	const (
		X = iota
		O
	)

	var game struct {
		pop  [2]byte
		nwin [2]byte
		rows [3][2]byte
		cols [3][2]byte
		dias [2][2]byte
	}

	trait := func(b byte) int {
		return strings.IndexByte("XO", b)
	}

	// Row/Column sweep
	for i := range flat {
		r, c := i/3, i%3

		player := trait(flat[i])
		if player < 0 {
			continue
		}

		game.pop[player]++

		mark := func(p *byte) {
			if *p == 2 {
				// winning move
				game.nwin[player]++
			}
			*p++
		}

		mark(&game.rows[r][player])
		mark(&game.cols[c][player])
	}

	// Lowering and rising diagonals scan
SCAN:
	for dia, idx := range [][]int{{0, 4, 8}, {2, 4, 6}} {
		for _, i := range idx {
			player := trait(flat[i])
			if player < 0 {
				continue SCAN
			}

			if game.dias[dia][player] == 2 {
				game.nwin[player]++
			}
			game.dias[dia][player]++
		}
	}

	δmove := game.pop[X] - game.pop[O]
	sum := game.nwin[X] * game.nwin[O]

	switch {
	case δmove != 0 && δmove != 1, sum != 0:
		// X must start and take turn with O
		// game must be zero sum
		return Nil, ErrInvalidBoard

	case game.nwin[X] > 0, game.nwin[O] > 0:
		return Win, nil

	case game.pop[X] == 5:
		// no win and no more move
		return Draw, nil
	}

	return Ongoing, nil
}
