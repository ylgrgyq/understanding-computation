class Stack :
    def __init__(self):
        self.content = []

    def push(self, char):
        self.content.append(char)

    def pushAll(self, chars):
        for c in chars:
            self.content.append(c)

    def top(self):
        return self.content.index(len(self.content))

    def pop(self):
        return self.pop()

    def size(self):
        return len(self.content)

    def __str__(self):
        return "%s" % self.content
