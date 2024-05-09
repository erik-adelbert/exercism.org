def is_paired(input_string):
    stack = []
    for c in input_string:
        match c:
            case '[' | '{' | '(':
                pair = {
                    '[': ']', 
                    '{': '}', 
                    '(': ')',
                }
                stack.append(pair[c])
            case ']' | '}' | ')':
                if len(stack) == 0 or c != stack.pop():
                    return False

    if len(stack) == 0:
        return True
    return False
