def response(hey_bob):
    hey_bob = hey_bob.strip()
    if not hey_bob:
        return 'Fine. Be that way!'
    
    question = yelling = False
    if hey_bob[-1] == '?':
        question = True

    def is_alpha(s):
        return any(c.isalpha() for c in s)

    if is_alpha(hey_bob) and hey_bob == hey_bob.upper():
        yelling = True
    
    if question and yelling:
        return 'Calm down, I know what I\'m doing!'
    
    if yelling:
        return 'Whoa, chill out!'

    if question:
        return 'Sure.'
    
    return 'Whatever.'
    