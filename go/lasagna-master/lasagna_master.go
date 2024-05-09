package lasagna

func PreparationTime(layers []string, time int) int {
	switch time {
	case 0:
		return 2 * len(layers)
	default:
		return time * len(layers)
	}
}

func Quantities(layers []string) (noodles int, sauce float64) {
	for i := range layers {
		switch layers[i] {
		case "noodles":
			noodles += 50
		case "sauce":
			sauce += .2
		}
	}
	return
}

func AddSecretIngredient(friend, me []string) {
	me[len(me)-1] = friend[len(friend)-1]
}

func ScaleRecipe(recipe []float64, scale int) []float64 {
	scaled := make([]float64, len(recipe))

	for i := range recipe {
		scaled[i] = 0.5 * float64(scale) * recipe[i]
	}

	return scaled
}
