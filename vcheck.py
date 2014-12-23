import argparse

from fileparser import FileParser
from interrogator import Interrogator

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Improve your vocabulary.')
    parser.add_argument('filename', nargs='+',
                        help='name of the file containing the vocabulary')

    args = parser.parse_args()

    parser = FileParser()
    for filename in args.filename:
        parser.load_file(filename)
    interrogator = Interrogator(parser.get_words())

    print('read {0} word{2} from {1} file{3}'
          .format(len(parser.get_words()),
                  len(args.filename),
                  's' if len(parser.get_words()) > 1 else '',
                  's' if len(args.filename) > 1 else ''))

    interrogator.interrogate()
    while interrogator.has_words():
        print('questioning on remaining {0} word{1}'
              .format(interrogator.get_num_words(),
                      's' if interrogator.get_num_words() > 1 else ''))
        interrogator.interrogate()
