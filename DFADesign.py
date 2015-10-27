
class FARule:
    def __init__(self, state, character, next_state):
        self.state = state
        self.character = character
        self.next_state = next_state
    def follow(self):
        return self.next_state
    def is_applies_to(self, state, character):
        return self.state == state and self.character == character
    
class DFARuleBook:
    def __init__(self, rules):
        self.rules = rules
    def next_state(self, state, character):
        for rule in rules:
            if rule.is_applies_to(state, character):
                return rule.follow()
        raise Exception("No rule applies to state:%s and input:%s" % (state, character))

class DFA:
    def __init__(self, rule_book, state, accept_states):
        self.rule_book = rule_book
        self.state = state
        self.accept_states = accept_states
    def is_accepting(self):
        return self.state in self.accept_states
    def read_string(self, string):
        for char in string :
            self.state = self.rule_book.next_state(self.state, char)

class DFADesign:
    def __init__(self, start_state, accept_states, rule_book):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rule_book = rule_book
    def to_dfa(self):
        return DFA(self.rule_book, self.start_state, self.accept_states)

    def is_accepts(self, string):
        dfa = self.to_dfa()
        dfa.read_string(string)
        return dfa.is_accepting()
