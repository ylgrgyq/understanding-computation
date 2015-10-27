
class Number :
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return "%s" % self.val
    def isReducible(self):
        return False

class Boolean:
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return "%s" % self.val
    def isReducible(self):
        return False

class Variable:
    def __init__(self, name) :
        self.name = name
    def isReducible(self):
        return True
    def __str__(self):
        return "%s" % self.name
    def reduce(self, env):
        return env[self.name]

class Add :
    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2
    def __str__(self):
        return "%s + %s" % (self.n1, self.n2)
    def isReducible(self):
        return True
    def reduce(self, env):
        if self.n1.isReducible():
            return Add(self.n1.reduce(env), self.n2)
        elif self.n2.isReducible():
            return Add(self.n1, self.n2.reduce(env))
        else :
            return Number(self.n1.val + self.n2.val)

class Multiply :
    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2
    def __str__(self):
        return "%s * %s" % (self.n1, self.n2)
    def isReducible(self):
        return True
    def reduce(self, env):
        if self.n1.isReducible():
            return Multiply(self.n1.reduce(env), self.n2)
        elif self.n2.isReducible():
            return Multiply(self.n1, self.n2.reduce(env))
        else :
            return Number(self.n1.val * self.n2.val)

class LessThan :
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "%s < %s" % (self.left, self.right)
    def isReducible(self):
        return True
    def reduce(self, env):
        if self.left.isReducible():
            return LessThan(self.left.reduce(env), self.right)
        elif self.right.isReducible():
            return LessThan(self.left, self.right.reduce(env))
        else :
            return Boolean(self.left.val < self.right.val)

class DoNothing:
    def __str__(self):
        return "Do-Nothing"

    def isReducible(self):
        return False

class Assign:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
    def __str__(self):
        return "%s = %s" % (self.name, self.expression)
    def isReducible(self):
        return True
    def reduce(self, env):
        if self.expression.isReducible():
            return (Assign(self.name, self.expression.reduce(env)), env)
        else :
            env[self.name] = self.expression
            return (DoNothing(), env)

class If:
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __str__(self):
        return "if (%s) {%s} else {%s}" % (self.condition, self.consequence, self.alternative)
    def isReducible(self):
        return True
    def reduce(self, env):
        if self.condition.isReducible():
            return (If(self.condition.reduce(env), self.consequence, self.alternative), env)
        else :
            if self.condition.val == True:
                return (self.consequence, env)
            else :
                return (self.alternative, env)

class Sequence:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return "%s; %s" % (self.first, self.second)

    def isReducible(self):
        return True

    def reduce(self, env):
        if self.first.isReducible():
            reduced_first, reduced_env = self.first.reduce(env)
            return (Sequence(reduced_first, self.second), reduced_env)
        else :
            return (self.second, env) 

class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __str__(self):
        return "while (%s) {%s}" % (self.condition, self.body)
    def isReducible(self):
        return True
    def reduce(self, env):
        return (If(self.condition, Sequence(self.body, self), DoNothing()), env)

class Machine :
    def __init__(self, expression, env):
        self.expression = expression
        self.env = env

    def step(self):
        self.expression, self.env = self.expression.reduce(self.env)

    def run(self):
        while self.expression.isReducible() :
            print self.expression, "environment:", self.env
            self.step()
        print self.expression, "environment:", self.env
        print self.env["x"].val


