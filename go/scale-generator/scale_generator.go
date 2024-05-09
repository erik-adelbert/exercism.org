package scale

import "strings"

// Generate an arbitrary minor, major or augmented second scales
func Scale(tonic, interval string) (scale []string) {
	scale = make([]string, 0, 12)

	mode := stom(interval) // Encode interval

	// Select reference scale and start at the tonic
	base := sharps
	if isFlat(tonic, mode) {
		base = flats
	}
	t0 := pos(tonic)
	pitch := func(i int) string { return base[(i+t0)%len(sharps)] } // ring index

	// Build an arbitrary chromatic, minor, major or augmented second scale
	for i := 0; mode > 0; i++ {
		if mode&1 == 1 {
			scale = append(scale, pitch(i))
		}
		mode = mode >> 1
	}

	if interval != "" { // not chromatic
		scale = append(scale, scale[0]) // loop the scale
	}

	return
}

// https://ianring.com/musictheory/scales/
type mode int16 // 12bit encoded mode

// Example modes
const (
	Chromatic mode = 0b111111111111
	Major     mode = 0b101010110101

	// Aeolian    mode = 0b010110101101
	// Dorian     mode = 0b011010101101
	// Locrian    mode = 0b010101101011
	// Lydian     mode = 0b101011010101
	// Mixolydian mode = 0b011010110101
	// Phrygian   mode = 0b010110101011
	// Whole      mode = 0b010101010101
)

// Convert from an interval string to a 12bit mode
func stom(interval string) (m mode) {
	if interval == "" {
		m = 0b111111111111 // Chromatic
		return
	}

	stride := []int{'m': 1, 'M': 2, 'A': 3}

	i, m := 0, 1
	for _, c := range interval {
		m |= 1 << i
		i += stride[c]
	}

	return
}

// Pitches
var sharps = []string{
	"A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#",
}

var flats = []string{
	"A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab",
}

// Capitalize tonic
func title(tonic string) string {
	return strings.Title(tonic)
}

// Find the tonic Pitches index
func pos(tonic string) int {
	tonic = title(tonic)

	for i := range sharps {
		if tonic == sharps[i] || tonic == flats[i] {
			return i
		}
	}

	panic("unreachable")
}

// Test whether the scale (tonic/mode) is written sharp or flat
func isFlat(tonic string, m mode) bool {

	switch tonic {
	case "F", "Bb", "Eb", "Ab", "Db", "d", "g", "c", "f", "bb":
		return true
	case "Gb":
		if m == Major {
			return true
		}
	case "eb":
		if m != Major {
			return true
		}
	}

	// Default to sharp
	return false
}
