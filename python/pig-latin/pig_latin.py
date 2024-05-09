def translate(text):
    words = text.split()

    def is_vowel(c):
        return c in ("a", "e", "i", "o", "u")

    def rules(word):
        for idx, c in enumerate(word):
            if is_vowel(c):
                break
        else:
            idx += 1

        head = word[:idx]
        tail = word[idx:]

        # Rule4 ("rhythm")
        if not tail and "y" in head:
            idx = head.index("y") # rescan
            tail = head[idx:]
            head = head[:idx]

        # Rule1
        if idx == 0 or "xr" in head or "yt" in head:
            return word + "ay"

        # Rule3
        if head[-1] == "q" and tail[0] == "u":
            return tail[1:] + head + "uay"

        # Rule2 & Rule4 ("my")
        return tail + head + "ay"

    return " ".join(list(map(rules, words)))
