from config import config

class FileParser:

    def __init__(self):
        self.words = dict()

    def _add_word(self, word, translations):
        if word in self.words:
            raise Exception("duplicate word entry '{0}'".format(word))

        self.words[word] = translations

    def _parse_line(self, line):
        line = line.strip().split(config['lang_separator'])

        if len(line) < 2:
            raise Exception("missing language separator '{0}'"
                            .format(config['lang_separator']))
        elif len(line) > 2:
            raise Exception("too many language separators '{0}'"
                            .format(config['lang_separator']))

        word = line[0]
        translations = line[1].split(config['word_separator'])

        if len(word) == 0 or any(map(lambda x: len(x) == 0, translations)):
            raise Exception('words cannot be empty')
        elif (word.startswith(config['command_prefix']) or
              any(map(lambda x: x.startswith(config['command_prefix']),
              translations))):
            raise Exception("words cannot start with command prefix '{0}'"
                            .format(config['command_prefix']))

        return word, translations

    def load_file(self, filename):
        with open(filename, encoding='utf8') as file:
            for i, line in enumerate(file):
                try:
                    word, translations = self._parse_line(line)
                    self._add_word(word, translations)
                except Exception as e:
                    print('{0},{1}: {2}'.format(filename, i+1, e))

    def get_words(self):
        return self.words
