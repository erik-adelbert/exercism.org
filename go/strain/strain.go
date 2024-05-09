package strain

// Constants defining whether to keep or discard elements.
const (
	keep    = true
	discard = !keep
)

// filter is a helper function that filters elements in a slice based
// on a predicate function.
func filter[T any](in []T, predicate func(T) bool, keep bool) []T {
	var out []T

	for i := range in {
		// Keep the element if both keep and predicate are true,
		// or if both are false.
		// ┏━━━━━━┯━━━━━━━┯━━━━━━━┓
		// ┃      │  keep │ !keep ┃
		// ┠──────┼───────┼───────┨
		// ┃ pred │   T   │   F   ┃
		// ┠──────┼───────┼───────┨
		// ┃!pred │   F   │   T   ┃
		// ┗━━━━━━┷━━━━━━━┷━━━━━━━┛

		if (keep && predicate(in[i])) || !(keep || predicate(in[i])) {
			out = append(out, in[i]) // copy!
		}
		// Discard the element otherwise.
	}

	return out // Return the filtered slice.
}

// Keep is a function that filters elements in a slice and keeps those
// for which the predicate function returns true.
func Keep[T any](in []T, predicate func(T) bool) []T {
	return filter(in, predicate, keep)
}

// Discard is a function that filters elements in a slice and discards those
// for which the predicate function returns true.
func Discard[T any](in []T, predicate func(T) bool) []T {
	return filter(in, predicate, discard)
}
