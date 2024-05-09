package chessboard

type File [8]bool
type Chessboard map[string]File

// CountInFile returns how many squares are occupied in the chessboard,
// within the given file.
func CountInFile(cb Chessboard, file string) int {
	if f, ok := cb[file]; ok {
		var nsquare int
		for i := range f {
			if f[i] {
				nsquare++
			}
		}
		return nsquare
	}
	return 0
}

// CountInRank returns how many squares are occupied in the chessboard,
// within the given rank.
func CountInRank(cb Chessboard, rank int) int {
	if rank < 1 || rank > 8 {
		return 0
	}

	var nsquare int
	for k := range cb {
		if cb[k][rank-1] {
			nsquare++
		}
	}
	return nsquare
}

// CountAll should count how many squares are present in the chessboard.
func CountAll(cb Chessboard) int {
	return len(cb) * len(cb["A"])
}

// CountOccupied returns how many squares are occupied in the chessboard.
func CountOccupied(cb Chessboard) int {
	var nsquare int
	for k := range cb {
		nsquare += CountInFile(cb, k)
	}
	return nsquare
}
