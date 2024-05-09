package cards

// FavoriteCards returns a slice with the cards 2, 6 and 9 in that order.
func FavoriteCards() []int {
	return []int{2, 6, 9}
}

// GetItem retrieves an item from a slice at given position.
// If the index is out of range, we want it to return -1.
func GetItem(a []int, i int) int {
	if i < 0 || i >= len(a) {
		return -1
	}
	return a[i]

}

// SetItem writes an item to a slice at given position overwriting an existing value.
// If the index is out of range the value needs to be appended.
func SetItem(a []int, i, v int) []int {
	if i < 0 || i >= len(a) {
		return append(a, v)
	}
	a[i] = v
	return a
}

// PrependItems adds an arbitrary number of values at the front of a slice.
func PrependItems(a []int, nums ...int) []int {
	return append(nums, a...)
}

// RemoveItem removes an item from a slice by modifying the existing slice.
func RemoveItem(a []int, i int) []int {
	if i < 0 || i >= len(a) {
		return a
	}
	return a[:i+copy(a[i:], a[i+1:])] //https://go.dev/wiki/SliceTricks
}
