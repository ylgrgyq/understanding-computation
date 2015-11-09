

class TMConfig(object):
    def __init__(self, state, tape):
        self.state = state
        self.tape = tape

    def __str__(self):
        return "state:%s tape:%s" % (self.state, self.tape)

class Tape(object):
    def __init__(self, left, middle, right, blank):
        assert isinstance(left, list)
        assert isinstance(right, list)
        assert isinstance(middle, str)
        assert isinstance(blank, str)

        self.left = left
        self.middle = middle
        self.right = right
        self.blank = blank

    def __str__(self):
        return "%s %s (%s) %s %s" % (self.blank, "".join(self.left), self.middle, "".join(self.right), self.blank)

    def write(self, char):
        return Tape(self.left, char, self.right, self.blank)

    def move_head_left(self):
        left = []
        middle = self.blank
        right = [self.middle] + self.right

        if self.left:
            left = self.left[0:-1]
            middle = self.left[-1]

        return Tape(left, middle, right, self.blank)

    def move_head_right(self):
        left = self.left + [self.middle]
        middle = self.blank
        right = []

        if self.right:
            right = self.right[1:]
            middle = self.right[0]

        return Tape(left, middle, right, self.blank)

class TMRule(object):
    def __init__(self, state, char, next_state, write_char, direction):
        self.state = state
        self.char = char
        self.next_state = next_state
        self.write_char = write_char
        self.direction = direction

    def is_applies_to(self, config):
        return self.state == config.state and self.char == config.tape.middle

    def follow(self, config):
        return TMConfig(self.next_state, self.next_tape(config))

    def next_tape(self, config):
        written_tape = config.tape.write(self.write_char)

        if self.direction == "left":
            return written_tape.move_head_left()
        else :
            return written_tape.move_head_right()

class DTMRuleBook(object):
    def __init__(self, rules):
        self.rules = rules

    def next_config(self, config):
        return self.rule_for(config).follow(config)

    def rule_for(self, config):
        for r in self.rules:
            if r.is_applies_to(config)
                return r
        return None






a = Tape(['1', '0', '1'], '1', [], '_')


rule = TMRule(1, '0', 2, '1', "right")
print rule.follow(TMConfig(1, Tape([], '0', [], '_')))

