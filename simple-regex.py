from abc import ABCMeta, abstractmethod
import NFADesign

class Pattern:
    __metaclass__ = ABCMeta

    def __init__(self, precedence):
        self.precedence = precedence

    def bracket(self, outer_precedence):
        if self.precedence < outer_precedence:
            return "(%s)" % self
        else :
            return "%s" % self

    @abstractmethod
    def to_nfa_design(self):
        return None

    def matches(self, string):
        return self.to_nfa_design().is_accepts(string)

class Empty(Pattern):
    def __init__(self):
        Pattern.__init__(self, 3)

    def __str__(self):
        return ""

    def to_nfa_design(self):
        start_state = object() 
        accept_states = set([start_state])
        rule_book = NFADesign.NFARuleBook([])
        return NFADesign.NFADesign(start_state, accept_states, rule_book)


class Literal(Pattern):
    def __init__(self, character):
        Pattern.__init__(self, 3)
        self.character = character

    def __str__(self):
        return self.character

    def to_nfa_design(self):
        start_state = object()
        accept_state = object()
        rulebook = NFADesign.NFARuleBook([NFADesign.FARule(start_state, self.character, accept_state)])
        return NFADesign.NFADesign(start_state, set([accept_state]), rulebook)

class Concatenate(Pattern):
    def __init__(self, first, second):
        Pattern.__init__(self, 1)
        self.first = first
        self.second = second

    def __str__(self):
        return "".join(map(lambda pattern:pattern.bracket(self.precedence), [self.first, self.second]))

    def to_nfa_design(self):
        first_nfa_design = self.first.to_nfa_design()
        second_nfa_design = self.second.to_nfa_design()

        start_state = first_nfa_design.start_state
        accept_states = second_nfa_design.accept_states

        extra_rules = map(lambda state: NFADesign.FARule(state, None, second_nfa_design.start_state), first_nfa_design.accept_states)
        rules = first_nfa_design.rule_book.rules + second_nfa_design.rule_book.rules + extra_rules
        return NFADesign.NFADesign(start_state, accept_states, NFADesign.NFARuleBook(rules))

class Repeat(Pattern):
    def __init__(self, pattern):
        Pattern.__init__(self, 2)
        self.pattern = pattern

    def __str__(self):
        return self.pattern.bracket(self.precedence) + "*"

    def to_nfa_design(self):
        nfa_design = self.pattern.to_nfa_design()
        
        start_state = nfa_design.start_state
        accept_states = nfa_design.accept_states

        extra_rules = map(lambda state: NFADesign.FARule(state, None, start_state), accept_states)
        return NFADesign.NFADesign(start_state, accept_states, NFADesign.NFARuleBook(nfa_design.rule_book.rules + extra_rules))

class Choose(Pattern):
    def __init__(self, first, second):
        Pattern.__init__(self, 0)
        self.first = first
        self.second = second

    def __str__(self):
        return self.first.bracket(self.precedence) + "|" + self.second.bracket(self.precedence)

    def to_nfa_design(self):
        start_state = object()
        first_nfa_design = self.first.to_nfa_design()
        second_nfa_design = self.second.to_nfa_design()
        accept_states = first_nfa_design.accept_states.union(second_nfa_design.accept_states)

        extra_rules = map(lambda state: NFADesign.FARule(start_state, None, state), [first_nfa_design.start_state, second_nfa_design.start_state])
        rules = first_nfa_design.rule_book.rules + second_nfa_design.rule_book.rules + extra_rules

        return NFADesign.NFADesign(start_state, accept_states, NFADesign.NFARuleBook(rules))


