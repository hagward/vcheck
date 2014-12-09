from config import config
from enum import Enum
from sys import exit

class Interrogator:

    Actions = Enum('Actions', 'INCORRECT_GUESS CORRECT_GUESS SHOW_WORD NOOP')

    def __init__(self, words):
        self.words = words
        self.commands = {
            'show': self._command_show,
            'quit': self._command_quit
        }
        self.failed_words = set()

    def _execute_command(self, command_name, current_word):
        if command_name not in self.commands:
            print('unknown command')
            return self.Actions.NOOP
        else:
            return self.commands[command_name](current_word)

    def _command_show(self, current_word):
        self.failed_words.add(current_word)
        print('answer:', ', '.join(self.words[current_word]))
        return self.Actions.SHOW_WORD

    def _command_quit(self, current_word):
        exit()

    def _parse_input(self, word, line):
        if line.startswith(config['command_prefix']):
            return self._execute_command(line[1:], word)
        else:
            return self.Actions.CORRECT_GUESS if line in self.words[word] else self.Actions.INCORRECT_GUESS

    def interrogate(self):
        for i, word in enumerate(iter(self.words)):
            action = self.Actions.INCORRECT_GUESS
            while action != self.Actions.CORRECT_GUESS and action != self.Actions.SHOW_WORD:
                line = input('{0}> {1}: '.format(i+1, word))
                action = self._parse_input(word, line)

        for i, word in enumerate(self.failed_words):
            print(word)
