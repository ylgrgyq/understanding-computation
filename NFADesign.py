
class FARule:
    def __init__(self, state, character, next_state):
        self.state = state
        self.character = character
        self.next_state = next_state
    def __str__(self):
        return "%s %s %s" % (self.state, self.character, self.next_state)
    def follow(self):
        return self.next_state
    def is_applies_to(self, state, character):
        return self.state == state and self.character == character
    
class NFARuleBook:
    def __init__(self, rules):
        self.rules = rules

    def __str__(self):
        return "%s" % (', '.join(r.__str__() for r in self.rules))

    def next_states(self, states, character):
        rules = [rule for sublist in map(lambda state: self.rules_for(state, character), states) for rule in sublist]

        return set(map(lambda rule:rule.follow(), rules))

    def rules_for(self, state, character):
        return filter(lambda rule:rule.is_applies_to(state, character), self.rules)

class NFA:
    def __init__(self, states, accept_states, rule_book):
        self.rule_book = rule_book
        self.states = states
        self.accept_states = accept_states

    def is_accepting(self):
        for state in self.states:
            if state in self.accept_states:
                return True
        return False

    def read_string(self, string):
        for char in string :
            self.states = self.rule_book.next_states(self.states, char)

class NFADesign:
    def __init__(self, start_state, accept_states, rule_book):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rule_book = rule_book

    def to_nfa(self):
        return NFA(set([self.start_state]), self.accept_states, self.rule_book)

    def is_accepts(self, string):
        nfa = self.to_nfa()
        nfa.read_string(string)
        return nfa.is_accepting()
