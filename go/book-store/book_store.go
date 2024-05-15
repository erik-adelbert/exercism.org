package bookstore

import (
	"sort"
)

const (
	nBook     = 5   // define the number of different books available
	bookPrice = 800 // define the listed price of each book
)

// discounts represents the discount rates for purchasing sets of books
// of different sizes
var discounts = []int{
	2: 2 * bookPrice / 20, // 5%  discount for sets of 2 different books
	3: 3 * bookPrice / 10, // 10%  .
	4: 4 * bookPrice / 5,  // 20%  .
	5: 5 * bookPrice / 4,  // 25% discount for sets of 5 different books
}

// Cost calculates the total cost of purchasing the given books,
// considering discounts.
func Cost(books []int) int {
	listPrice := len(books) * bookPrice

	// count the number of sets of different sizes:
	// with i <=nbook, bookSets[i] is the count of sets of size i
	bookSets := make([]int, nBook+1)
	for len(books) > 0 { // iterate until all books are processed
		var i int
		i, books = setRemove(books) // remove the largest set
		bookSets[i]++               // increment the count for the corresponding set size
	}

	// optimize sets to apply the best discount combinations
	if n := min(bookSets[3], bookSets[5]); n > 0 { // check if there are sets of 3 and sets of 5
		bookSets[3] -= n     // remove sets of 3
		bookSets[5] -= n     // remove sets of 5
		bookSets[4] += 2 * n // replace 1:1 with sets of 4
	}

	// compute total discount by reducing bookSets
	var discount int
	for i := range bookSets { // iterate over the counts of different set sizes
		discount += bookSets[i] * discounts[i] // accumulate discounts for each set size
	}

	// apply discount and return total price
	return listPrice - discount
}

// setRemove removes the largest set from the input slice and
// returns the removed subslice size and the remaining subslice.
// It is used to count the number of sets of different sizes.
//
// see https://go.dev/wiki/SliceTricks (dedup)
func setRemove(in []int) (int, []int) {
	sort.Ints(in)
	j := 0
	for i := 1; i < len(in); i++ {
		if in[j] == in[i] {
			continue
		}
		j++
		// preserve the original data
		in[i], in[j] = in[j], in[i]
	}
	return j + 1, in[j+1:]
}

// min returns the minimum of two integers.
func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
