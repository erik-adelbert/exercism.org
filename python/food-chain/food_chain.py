"""
food_chain.py --
"""

inits = [
    "I know an old lady who swallowed a fly.",
    "I know an old lady who swallowed a spider.",
    "I know an old lady who swallowed a bird.",
    "I know an old lady who swallowed a cat.",
    "I know an old lady who swallowed a dog.",
    "I know an old lady who swallowed a goat.",
    "I know an old lady who swallowed a cow.",
    "I know an old lady who swallowed a horse.",
]

reactions = [
    "I don't know why she swallowed the fly. Perhaps she'll die.",
    "It wriggled and jiggled and tickled inside her.",
    "How absurd to swallow a bird!",
    "Imagine that, to swallow a cat!",
    "What a hog, to swallow a dog!",
    "Just opened her throat and swallowed a goat!",
    "I don't know how she swallowed a cow!",
    "She's dead, of course!",
]

swallowed = [
    "",
    "She swallowed the spider to catch the fly.",
    "She swallowed the bird to catch the spider that wriggled and jiggled and tickled inside her.",
    "She swallowed the cat to catch the bird.",
    "She swallowed the dog to catch the cat.",
    "She swallowed the goat to catch the dog.",
    "She swallowed the cow to catch the goat.",
    "",
]


def recite(start, end):
    """recite"""

    lyrics = []

    # Generate the verses from start to end
    for i in range(start - 1, end):
        # Add the initial line of the current verse
        lyrics.append(inits[i])

        if i < len(inits) - 1:
            # Add the reaction to the animal swallowed
            if i:
                lyrics.append(reactions[i])
            # Add the lines explaining why each animal was swallowed, in reverse order
            for j in range(i, 0, -1):
                lyrics.append(swallowed[j])
            # Add the reaction to swallowing the fly for all verses except the last one
            lyrics.append(reactions[0])

        # If it's the last verse, add the unique last line
        if i == len(inits) - 1:
            lyrics.append(reactions[-1])

        # Add a blank line between verses if not the last verse
        if i < end - 1:
            lyrics.append("")

    return lyrics
