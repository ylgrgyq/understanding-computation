import Stack

class PDAConfiguration(object):
    STUCK_STATE = object()

    def __init__(self, state, stack):
        assert isinstance(stack, Stack.Stack)

        self.state = state
        self.stack = stack

    def __str__(self):
        return "state:%s, stack:%s" % (self.state, self.stack)

    def is_stuck(self):
        return self.state == PDAConfiguration.STUCK_STATE

class PDARule(object):
    def __init__(self, state, char, next_state, pop_char, push_chars):
        assert char == None or isinstance(char, str)
        assert isinstance(pop_char, str)
        assert isinstance(push_chars, list)

        self.state = state
        self.char = char
        self.next_state = next_state
        self.pop_char = pop_char
        self.push_chars = push_chars

    def is_applies_to(self, config, char):
        assert config == PDAConfiguration.STUCK_STATE or isinstance(config, PDAConfiguration)
        return self.state == config.state and self.pop_char == config.stack.top() \
               and self.char == char
    
    def __str__(self):
        return "from %s to %s, via %s;%s/%s\n" % (self.state, self.next_state, self.char, self.pop_char, "".join(self.push_chars))

    def follow(self, config):
        stack = config.stack
        stack.pop()
        stack.pushAll(self.push_chars[::-1])

        return PDAConfiguration(self.next_state, stack)

class DPDARuleBook(object):
    def __init__(self, rules):
        self.rules = rules

    @classmethod
    def fromList(cls, rules): 
        return cls(rules)

    def find_rule_for(self, config, char):
        for r in self.rules:
            # only one rule can be found for a specific config and char
            if r.is_applies_to(config, char):
                return r

    def next_config(self, config, char):
        return self.find_rule_for(config, char).follow(config)

    def __str__(self):
        return "\n".join(str(r) for r in self.rules)

    def follow_free_moves(self, config):
        if self.find_rule_for(config, None) != None:
            return self.follow_free_moves(self.next_config(config, None))
        else :
            return config

class DPDA(object):
    def __init__(self, current_config, accept_states, rulebook):
        assert isinstance(accept_states, list)

        self.accept_states = accept_states
        self.rulebook = rulebook
        self.current_config = self.rulebook.follow_free_moves(current_config)

    def is_accepting(self):
        if not self.is_stuck:
            return self.current_config.state in self.accept_states
        else :
            return False

    def next_config(self, char):
        if self.rulebook.find_rule_for(self.current_config, char) != None:
            return self.rulebook.next_config(self.current_config, char)
        else :
            return PDAConfiguration.STUCK_STATE

    def is_stuck(self):
        return self.current_config.is_stuck()

    def read_char(self, char):
        self.current_config = self.next_config(char)
        if not self.is_stuck:
            self.current_config = self.rulebook.follow_free_moves(self.current_config)

    def read_string(self, string):
        for c in string:
            if not self.is_stuck():
                self.read_char(c)

    def __str__(self):
        return "current config:%s, accept states:%s, rulebook:%s" % (self.current_config, self.accept_states, self.rulebook)

class DPDADesign(object):
    def __init__(self, start_state, bottom_character, accept_states, rulebook):
        assert isinstance(bottom_character, str)
        assert isinstance(accept_states, list)

        self.start_state = start_state
        self.bottom_character = bottom_character
        self.accept_states = accept_states
        self.rulebook = rulebook

    def is_accept(self, string):
        dpda = self.to_dpda()
        dpda.read_string(string)
        return dpda.is_accepting()

    def to_dpda(self):
        start_stack = Stack.Stack([self.bottom_character])
        start_config = PDAConfiguration(self.start_state, start_stack)
        return DPDA(start_config, self.accept_states, self.rulebook)

