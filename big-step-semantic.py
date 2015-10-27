

class Number :
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return "%s" % self.val
    def evaluate(self, env):
        return self

class Boolean:
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return "%s" % self.val
    def evaluate(self, env):
        return self

class Variable :
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "%s" % self.name
    def evaluate(self, env):
        return env[self.name]

class Add :
    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2
    def evaluate(self, env):
        return Number(self.n1.evaluate(env).val + self.n2.evaluate(env).val)
    def __str__(self):
        return "%s + %s" % (self.n1, self.n2)

class Multiply :
    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2
    def evaluate(self, env):
        return Number(self.n1.evaluate(env).val * self.n2.evaluate(env).val)
    def __str__(self):
        return "%s * %s" % (self.n1, self.n2)

class LessThan :
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def evaluate(self, env):
        return Boolean(self.left.evaluate(env).val < self.right.evaluate(env).val)
    def __str__(self):
        return "%s < %s" % (self.left, self.right)

class Assign:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
    def __str__(self):
        return "%s = %s" % (self.name, self.expression)
    def evaluate(self, env):
        env[self.name] = self.expression.evaluate(env)
        return env

class DoNothing:
    def __str__(self):
        return " "
    def evaluate(self, env):
        return env

class If:
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative
    def __str__(self):
        return "if (%s) {%s} else {%s}" % (self.condition, self.consequence, self.alternative)
    def evaluate(self, env):
        if self.condition.evaluate(env).val :
            return self.consequence.evaluate(env)
        else :
            return self.alternative.evaluate(env) 

class Sequence:
    def __init__(self, first, second):
        self.first = first
        self.second = second
    def __str__(self):
        return "%s; %s" % (self.first, self.second)

    def evaluate(self, env):
        return self.second.evaluate(self.first.evaluate(env))

class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __str__(self):
        return "while (%s) {%s}" % (self.condition, self.body)
    def evaluate(self, env):
        if self.condition.evaluate(env).val:
            return self.evaluate(self.body.evaluate(env))
        else :
            return env


