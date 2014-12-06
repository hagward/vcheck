from parsedobject import Command, Guess

class Interrogator:

    def __init__(self, words):
        self.words = words

    def _parse_input(self, line):
        if line.startswith('.'):
            return Command(line[1:])
        else:
            return Guess(line)

    def interrogate(self):
        # Print starting message. Do this in VCheck instead!

        # Print word.

        for i, word in enumerate(iter(self.words)):
            guessed_correctly = False
            while not guessed_correctly:
                line = input('{0}> {1}:'.format(i+1, word))
                parsed_line = self._parse_input(line)
                guessed_correctly = parsed_line.execute(self.words[word])

        # Wait for input.

        # Parse input.

        # Repeat.

inter = Interrogator({'horse': ['häst'], 'hello': ['hej', 'tjena']})
inter.interrogate()

