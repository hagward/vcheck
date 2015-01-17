from collections import OrderedDict
from config import config

class FileParser:

    def __init__(self, shuffle=False):
        self.words = dict() if shuffle else OrderedDict()

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

        line[0] = line[0].split(config['word_separator'])
        line[1] = line[1].split(config['word_separator'])

        if (len(line[0]) == 0 or any(map(lambda x: len(x) == 0, line[0])) or
            len(line[1]) == 0 or any(map(lambda x: len(x) == 0, line[1]))):
            raise Exception('empty word')
        elif (any(map(lambda x: x.startswith(config['command_prefix']),
                      line[0])) or
              any(map(lambda x: x.startswith(config['command_prefix']),
                      line[1]))):
            raise Exception("words cannot start with command prefix '{0}'"
                            .format(config['command_prefix']))

        return line[0], line[1]

    def parse_file(self, filename, flip_lang=False, start=0, nwords=0):
        with open(filename, encoding='utf8') as file:
            for i, line in enumerate(file):
                if i < start: continue
                if nwords > 0 and i - start == nwords: break
                try:
                    if flip_lang:
                        translations, word = self._parse_line(line)
                    else:
                        word, translations = self._parse_line(line)
                    word = ', '.join(word)
                    self._add_word(word, translations)
                except Exception as e:
                    print('{0}:{1}: warning: {2}'.format(filename, i+1, e))

    def get_words(self):
        return self.words
