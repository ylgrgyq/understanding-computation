import Stack

class PDAConfiguration(object):
    def __init__(self, state, stack):
        self.__state = state

        assert isinstance(stack, Stack.Stack)
        self.__stack = stack

    def __str__(self):
        return "state:%s, stack:%s" % (self.__state, self.__stack)

class PDARule(object):
    def __init__(self, state, char, next_state, pop_char, push_chars):
        assert isinstance(char, str)
        assert isinstance(pop_char, str)
        assert isinstance(push_chars, list)

        self.state = state
        self.char = char
        self.next_state = next_state
        self.pop_char = pop_char
        self.push_chars = push_chars

    def is_applies_to(self, config, char):
        assert isinstance(config, PDAConfiguration)

        return self.state == config.state and self.pop_char == config.stack.top() \
               and self.char == char
    
    def __str__(self):
        return "from %s to %s, via %s;%s/%s\n" % (self.state, self.next_state, self.char, self.pop_char, "".join(self.push_chars))






