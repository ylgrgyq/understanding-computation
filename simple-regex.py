from abc import ABCMeta, abstractmethod
import NFADesign

class Pattern:
    def __init__(self, precedence):
        self.precedence = precedence

    def bracket(self, outer_precedence):
        if self.precedence < outer_precedence:
            return "(%s)" % self
        else :
            return "%s" % self

class Empty(Pattern):
    def __init__(self):
        Pattern.__init__(self, 3)

    def __str__(self):
        return ""

    def to_nfa_design(self):
        start_state = object() 
        accept_states = set([start_state])
        rule_book = NFARuleBook([])
        NFADesign(start_state, accept_states, rule_book)


class Literal(Pattern):
    def __init__(self, character):
        Pattern.__init__(self, 3)
        self.character = character

    def __str__(self):
        return self.character

class Concatenate(Pattern):
    def __init__(self, first, second):
        Pattern.__init__(self, 1)
        self.first = first
        self.second = second

    def __str__(self):
        return "".join(map(lambda pattern:pattern.bracket(self.precedence), [self.first, self.second]))

class Repeat(Pattern):
    def __init__(self, pattern):
        Pattern.__init__(self, 2)
        self.pattern = pattern

    def __str__(self):
        return self.pattern.bracket(self.precedence) + "*"

class Choose(Pattern):
    def __init__(self, first, second):
        Pattern.__init__(self, 0)
        self.first = first
        self.second = second

    def __str__(self):
        return self.first.bracket(self.precedence) + "|" + self.second.bracket(self.precedence)


