package birdwatcher

// TotalBirdCount return the total bird count by summing
// the individual day's counts.
func TotalBirdCount(birdsPerDay []int) int {
	var n int
	for i := range birdsPerDay {
		n += birdsPerDay[i]
	}
	return n
}

// BirdsInWeek returns the total bird count by summing
// only the items belonging to the given week.
func BirdsInWeek(birdsPerDay []int, week int) int {
	lo, hi := 7*(week-1), 7*week
	return TotalBirdCount(birdsPerDay[lo:hi])

}

// FixBirdCountLog returns the bird counts after correcting
// the bird counts for alternate days.
func FixBirdCountLog(birdsPerDay []int) []int {
	for i := range birdsPerDay {
		if i&1 == 0 {
			birdsPerDay[i]++
		}
	}
	return birdsPerDay
}
