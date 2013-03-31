import argparse
import io
import os
import random
import sys

parser = argparse.ArgumentParser(description='vcheck.py helps you remembering the vocabulary by questioning you on a predetermined word list.')
parser.add_argument('filenames', metavar='filename', nargs='*', help='name of the word file')
parser.add_argument('-d', metavar='dir', nargs='?', default='.', help='the directory to look for the word file(s)')
parser.add_argument('-rand', action='store_true', help='randomize the word list')
parser.add_argument('-switch', action='store_true', help='switch the two languages')
args = parser.parse_args()

# Returns the flags, folder name and file names from argv.
def parse_params(argv):
    flags = []
    filenames = []
    i = 1
    while i < len(argv) and argv[i].startswith('-'):
        flags.append(argv[i])
        i += 1
    folder = argv[i]
    
    i += 1
    while i < len(argv):
        if '.' not in argv[i]:
            # If no extension given, assume .txt.
            argv[i] += '.txt'
        filenames.append(argv[i])
        i += 1
    return flags, folder, filenames

# Reads a text file line by line into an array, removes leading and trailing
# whitespaces and finally splits every line at '|'.
def words_from_file(filename):
    words = []
    try:
        with open(filename) as file:
            for line in file:
                words.append(line.strip().split('|'))
        global file_count
        file_count += 1
    except IOError:
        print('Could not open \'{0}\' for reading.'.format(filename))
    return words

# Uses function words_from_file on every file whose name ends with '.txt' in
# the specified folder, and returns an array of all the retrieved word pairs.
def words_from_folder(folder):
    words = []
    for filename in os.listdir(folder):
        if filename.endswith('.txt'):
            words += words_from_file(os.path.join(folder, filename))
    return words

# Takes a string s and returns a new one, where the characters from start and
# onwards are replaced with asterisks ('*').
def hintify(s, start):
    if start > len(s):
        start = len(s)
    output = io.StringIO()
    output.write(s[0:start])
    for i in range(start, len(s)):
        output.write('*')
    ret_val = output.getvalue()
    output.close()
    return ret_val

# Command options.
COMM_PREFIX = '.'
HINT_COMM = COMM_PREFIX + 's'
ANS_COMM = COMM_PREFIX + 'a'
LEFT_COMM = COMM_PREFIX + 'left'
HELP_COMM = COMM_PREFIX + 'help'
QUIT_COMM = COMM_PREFIX + 'quit'

COMM_STR = 'Commands:\n' \
           '   {0}	show this information\n' \
           '   {1}		show word hint\n' \
           '   {2}		show answer\n' \
           '   {3}	display the number of words left\n' \
           '   {4}	quit the program' \
           .format(HELP_COMM, HINT_COMM, ANS_COMM, LEFT_COMM, QUIT_COMM)

file_count = 0
words = []
words_to_test = []  # list with binary indicators for which words to test
word_indices = [0, 1]  # strange array, used for language switching
run = True

# If no filenames are provided, load all the files in the specified (or
# default) directory.
if len(args.filenames) == 0:
    words = words_from_folder(args.d)
else:
    for filename in args.filenames:
        words += words_from_file(os.path.join(args.d, filename))

words_to_test = [1 for i in range(0, len(words))]

rand_str = ''
switch_str = ''
if args.rand:
    random.shuffle(words)
    rand_str = ' in random order'
if args.switch:
    word_indices = [1, 0]
    switch_str = ' with languages switched'

print('Questioning on {0} words from {1} files{2}{3}.' \
      .format(len(words), file_count, rand_str, switch_str))
print('To exit, type \'{0}\'.'.format(QUIT_COMM))

while run:
    total_words_to_test = sum(words_to_test)
    words_left = total_words_to_test
    for i in range(0, len(words)):
        if words_to_test[i] == 0:
            continue
        data = None
        hint_grade = 1
        incorrectness = 0  # 0 means that it was correct
        while data != words[i][word_indices[1]]:
            incorrectness += 1
            data = input('{0}> {1}: '.format(i + 1, words[i][word_indices[0]])).strip()
            if len(data) == 0:
                continue
            elif data == HINT_COMM:
                print('hint:', hintify(words[i][word_indices[1]], hint_grade))
                hint_grade += 1
                incorrectness += i
            elif data == ANS_COMM:
                print('answer:', words[i][word_indices[1]])
                incorrectness += 1
                break
            elif data == LEFT_COMM:
                print(words_left, 'words left')
            elif data == HELP_COMM:
                print(COMM_STR)
            elif data == QUIT_COMM:
                sys.exit()
            elif data[0] == COMM_PREFIX:
                print('Unknown command')
        if incorrectness < 2:
            words_to_test[i] = 0
        words_left -= 1
    
    if sum(words_to_test) == 0:
        if len(words_to_test) > 0:
            print('Congratulations, you answered every word correctly!')
        run = False
    else:
        print('You nailed {0} out of {1} words!'.format(total_words_to_test - sum(words_to_test), total_words_to_test))
        data = None
        while data != 'y':
            data = input('Do you want to repeat the most difficult words? (y/n) ').strip()
            if data == 'n':
                sys.exit()
