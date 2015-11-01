import NFADesign

class NFASimulation:
    def __init__(self, nfa_design):
        self.nfa_design = nfa_design

    def next_states(self, states, character):
        nfa = self.nfa_design.to_nfa(states)
        nfa.read_string(character)
        return nfa.states

    def rules_for(self, states):
        return map(lambda char: FARule(states, char, self.next_states(states, char)), self.nfa_design.rule_book.alphabet())

    def discover_states_and_rules(self, states):
        rules = [rule for sublist in map(lambda state: self.rules_for(state), states) for rule in sublist]

        more_states = frozenset(map(lambda rule: rule.follow(), rules))

        if more_states.issubset(states):
            return [states, rules]
        else :
            return self.discover_states_and_rules(states.union(more_states))
    

    def to_dfa_design(self):
        start_state = self.nfa_design.to_nfa().states
        [states, rules] = self.discover_states_and_rules(frozenset([start_state]))

        accept_state = filter(lambda state: self.nfa_design.to_nfa(state).is_accepting(), states)
        return NFADesign.NFADesign(start_state, accept_state, NFARuleBook(rules))

