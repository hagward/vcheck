import argparse
from fileparser import FileParser
from interrogator import Interrogator

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Improve your vocabulary.')
    parser.add_argument('filename', nargs='+',
                        help='name of the file containing the vocabulary')
    parser.add_argument('--flip', dest='flip', action='store_const',
                        const=True, default=False,
                        help='flip the two languages')
    parser.add_argument('--start', nargs='?', type=int, default=0,
                        help='index of the word to start reading from')
    parser.add_argument('--words', nargs='?', type=int, default=0,
                        help='number of words to read')

    args = parser.parse_args()

    parser = FileParser()
    for filename in args.filename:
        try:
            parser.parse_file(filename, args.start, args.words, args.flip)
        except FileNotFoundError:
            print("File '{0}' could not be found.".format(filename))
    interrogator = Interrogator(parser.get_words())

    print('Read {0} word{2} from {1} file{3}.'
          .format(len(parser.get_words()),
                  len(args.filename),
                  's' if len(parser.get_words()) != 1 else '',
                  's' if len(args.filename) != 1 else ''))

    interrogator.interrogate()
    while interrogator.has_words():
        print('Questioning on remaining {0} word{1}.'
              .format(interrogator.get_num_words(),
                      's' if interrogator.get_num_words() != 1 else ''))
        interrogator.interrogate()
