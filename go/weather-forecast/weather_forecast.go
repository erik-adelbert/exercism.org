// Package weather provides tools to describe
// waether events.
package weather

var (
	// CurrentCondition represents current weather events.
	CurrentCondition string
	// CurrentLocation representes the place where weather events are taking place.
	CurrentLocation string
)

// Forecast returns a string that describes the current condition
// occuring at the current location.
func Forecast(city, condition string) string {
	CurrentLocation, CurrentCondition = city, condition
	return CurrentLocation + " - current weather condition: " + CurrentCondition
}
