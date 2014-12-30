import sys

from config import config
from enum import Enum

class Interrogator:

    Actions = Enum('Actions', 'INCORRECT_GUESS CORRECT_GUESS SHOW_WORD NOOP')

    def __init__(self, words):
        self.words = words
        self.commands = {
            'help': self._command_help,
            'pass': self._command_pass,
            'quit': self._command_quit,
            'show': self._command_show
        }
        self.command_help = [
            ('help', 'show this help text'),
            ('pass', 'pass word without showing it'),
            ('quit', 'quit program without prompt'),
            ('show', 'pass and show word')
        ]

    def _execute_command(self, command_name, current_word):
        if command_name not in self.commands:
            print('unknown command')
            return self.Actions.NOOP
        else:
            return self.commands[command_name](current_word)

    def _command_help(self, current_word):
        print('Available commands:')
        for (command, description) in self.command_help:
            print("'{0}{1}': {2}"
                  .format(config['command_prefix'], command, description))

    def _command_pass(self, current_word):
        return self.Actions.SHOW_WORD

    def _command_quit(self, current_word):
        sys.exit()

    def _command_show(self, current_word):
        print('answer:', ', '.join(self.words[current_word]))
        return self.Actions.SHOW_WORD

    def _parse_input(self, word, line):
        if line.startswith(config['command_prefix']):
            return self._execute_command(line[1:], word)
        else:
            return (self.Actions.CORRECT_GUESS if line in self.words[word] else
                    self.Actions.INCORRECT_GUESS)

    def has_words(self):
        return len(self.words) > 0

    def get_num_words(self):
        return len(self.words)

    def interrogate(self):
        passed_words = set()
        for i, word in enumerate(iter(self.words)):
            action = self.Actions.INCORRECT_GUESS
            while (action != self.Actions.CORRECT_GUESS and
                   action != self.Actions.SHOW_WORD):
                line = input('({0}/{1}) {2}: '
                             .format(i+1, len(self.words), word))
                action = self._parse_input(word, line)
            if action == self.Actions.CORRECT_GUESS:
                passed_words.add(word)
        for word in iter(passed_words):
            del self.words[word]
