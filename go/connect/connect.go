package connect

import "strings"

// ResultOf returns the winner of the game given the board representation.
func ResultOf(lines []string) (string, error) {
	board, err := NewRhombus(lines)
	if err != nil {
		return "", err
	}

	// small problems, serial solution
	if board.Win('X') != "" {
		return "X", nil
	}
	return board.Win('O'), nil
}

// A Rhombus is a representation of a parallelepiped Hex board:
//   - w and h CAN be different
//   - data should only contains ['X', 'O', '.'] (not enforced)
//
// https://www.redblobgames.com/grids/hexagons/
type Rhombus struct {
	data   []byte
	width  int
	height int
}

// NewRhombus creates a new Rhombus instance from the provided board representation.
func NewRhombus(board []string) (*Rhombus, error) {
	// Calculate the width of the board.
	w := len(board[0])

	// Concatenate and sanitize the board representation.
	s := strings.Join(board, "")
	if strings.Contains(s, " ") {
		// remove spaces
		s = strings.NewReplacer(" ", "").Replace(s)
		w = (w + 1) / 2
	}

	return &Rhombus{
		width:  w,
		height: len(board),
		data:   []byte(s),
	}, nil
}

// Get returns the value at the specified index in the Rhombus.
func (r *Rhombus) Get(i int) byte {
	return r.data[i]
}

// Len returns the size of the Rhombus.
func (r *Rhombus) Len() int {
	return r.width * r.height // row major reminder
}

// Neighbors returns the indices of neighboring cells for a given index.
func (r *Rhombus) Neighbors(i int) []int {
	var neighs []int

	isInbound := func(x xHex) bool {
		return x.q >= 0 && x.q < r.width && x.r >= 0 && x.r < r.height
	}

	toIndex := func(x xHex) int {
		return r.width*x.r + x.q
	}

	for _, off := range neighborOffsets {
		i := xHex{q: i % r.width, r: i / r.width}
		x := i.Add(off) // candidate neighbor
		if isInbound(x) {
			neighs = append(neighs, toIndex(x))
		}
	}

	return neighs
}

// Win checks if the provided color has won the game.
// It performs a stack based DFS to check the connectivity of cell of the same color
// along either the q or r axis, depending on the color ('X' or 'O').
// With N the number of cells in the board, it has typical:
//   - O(N) runtime
//   - O(N) space
func (board *Rhombus) Win(color byte) string {
	move := newStack(board.Len() / 2)

	seen := make([]bool, len(board.data))
	for i := range board.data {
		if board.data[i] != color || seen[i] {
			continue
		}

		type span struct {
			start, end int
		}

		// default to 'X' -> must connect left and right / rhombus' q axis
		path := span{start: i % board.width, end: i % board.width}
		if color == 'O' {
			// -> nust connect top to bottom / rhombus r axis
			path = span{start: i / board.width, end: i / board.width}
		}
		move.push(i)

		for !move.empty() {
			x := move.pop()

			if seen[x] {
				continue
			}

			switch color {
			case 'X':
				xq := x % board.width
				path.start = min(path.start, xq)
				path.end = max(path.end, xq)

				if path.end-path.start == board.width-1 {
					// win!
					return "X"
				}
			case 'O':
				xr := x / board.width
				path.start = min(path.start, xr)
				path.end = max(path.end, xr)

				if path.end-path.start == board.height-1 {
					// win!
					return "O"
				}
			}

			seen[x] = true

			for _, xx := range board.Neighbors(x) {
				if !seen[xx] && board.Get(xx) == color {
					move.push(xx)
				}
			}
		}
	}

	return ""
}

// xHex is an axial coordinate Hex representation.
type xHex struct {
	q, r int
}

// Add adds two xHex coordinates and returns the result.
func (a xHex) Add(b xHex) xHex {
	return xHex{q: a.q + b.q, r: a.r + b.r}
}

// Constants for direction offsets.
const (
	east = iota
	northEast
	northWest
	west
	southWest
	southEast
)

// neighborOffsets stores the axial offsets for neighboring hexagonal grid cells.
var neighborOffsets = []xHex{
	east:      {+1, +0},
	northEast: {+1, -1},
	northWest: {+0, -1},
	west:      {-1, +0},
	southWest: {-1, +1},
	southEast: {+0, +1},
}

// stack represents a simple stack data structure.
type stack struct {
	data  []int
	push  func(int)
	pop   func() int
	empty func() bool
}

// newStack creates a new instance of stack.
// This implementation is only suitable here.
func newStack(cap int) *stack {
	data := make([]int, 0, cap)

	return &stack{
		data: data,
		push: func(i int) { data = append(data, i) },
		pop: func() int {
			top := data[len(data)-1]
			data = data[:len(data)-1]
			return top
		},
		empty: func() bool { return len(data) == 0 },
	}
}

// min returns the minimum of two integers.
func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

// max returns the maximum of two integers.
func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}
