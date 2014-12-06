class ParsedObject:

    def execute(self, param):
        raise NotImplementedError()

class Command(ParsedObject):

    def __init__(self, command):
        self.command = command

    def execute(self, param):
        print("executing command '{0}'".format(self.command))
        return False

class Guess(ParsedObject):

    def __init__(self, guess):
        self.guess = guess

    def execute(self, param):
        return self.guess in param

