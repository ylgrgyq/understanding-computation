class Stack :
    def __init__(self, content = []):
        self.content = content 

    @classmethod
    def fromList(cls, list):
        "Initialize Stack from a list"
        return cls(list)

    def push(self, char):
        self.content.append(char)

    def pushAll(self, chars):
        for c in chars:
            self.content.append(c)

    def top(self):
        return self.content[-1]

    def pop(self):
        return self.content.pop()

    def size(self):
        return len(self.content)

    def __str__(self):
        return "%s" % self.content
