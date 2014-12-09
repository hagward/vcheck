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

    print('read {0} word(s) from {1} file(s)'.format(len(parser.get_words()),
                                                     len(args.filename)))

    interrogator.interrogate()
