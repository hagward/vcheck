import io
import os
import random
import sys

RAND_FLAG = '-r'
SWITCH_FLAG = '-s'
COMM_PREFIX = '-'
HINT_COMM = COMM_PREFIX + 's'
ANS_COMM = COMM_PREFIX + 'a'
HELP_COMM = COMM_PREFIX + 'h'
QUIT_COMM = COMM_PREFIX + 'q'

USAGE_STR = 'Usage: python vcheck.py [flags] [dir] [filename(s)]\n\n' \
    'where \'dir\' is the name of the directory containing the text files and ' \
    'the (optional) flags any of the ones below.\n\n' \
    'Flags:\n' \
    + RAND_FLAG + '  presents the words in random order\n' \
    + SWITCH_FLAG + '  switches the two languages'

files = 0

def file_to_array(filename):
    """Reads a text file into an array, splitting
       at '|' and removing whitespaces."""
    words = []
    try:
        with open(filename) as file:
            for line in file:
                words.append(line.strip().split('|'))
        global files
        files += 1
    except IOError:
        print('Could not open file \'' + filename + '\'. Are you sure it ' \
              'really exists?')
    return words

def folder_to_array(foldername):
    words = []
    for root, dirs, filenames in os.walk(foldername):
        for filename in filenames:
            ext = filename.rsplit('.', 1)
            if len(ext) >= 2 and ext[1] == 'txt':
                words += file_to_array(os.path.join(foldername, filename))
    return words

def get_params(argv):
    """Returns the flags as a string array and
       the filename (of the text file to be read)
       as a string."""
    flags = []
    folder = ''
    filenames = []
    
    i = 1
    
    while i < len(argv):
        if argv[i][0] != '-':
            break
        else:
            flags.append(argv[i])
            i += 1
    
    folder = argv[i]
    if not folder.endswith('/'):
        folder += '/'
    
    i += 1
    
    while i < len(argv):
        if '.' not in argv[i]:
            argv[i] += '.txt'
        filenames.append(argv[i])
        i += 1
    
    return flags, folder, filenames

def hintify(s, start):
    """Returns the string with all its letters -
       except the first - replaced with asterisks."""
    if start > len(s):
        start = len(s)
    output = io.StringIO()
    output.write(s[0:start])
    for i in range(start, len(s)):
        output.write('*')
    ret_val = output.getvalue()
    output.close()
    return ret_val

if len(sys.argv) < 2:
    sys.exit(USAGE_STR)

flags, folder, filenames = get_params(sys.argv)

words = []
if len(filenames) < 1:
    # if no filenames are specified, load all the files in the folder
    words = folder_to_array(folder)
else:
    for filename in filenames:
        words += file_to_array(folder + filename)

indices = [0, 1]

# FLAG CODE

if RAND_FLAG in flags:
    random.shuffle(words)
if SWITCH_FLAG in flags:
    indices = [1, 0]

print('Questioning on ' + str(len(words)) + ' words from '
    + str(files) + ' files.')
print('Exit by typing \'' + QUIT_COMM + '\'.')

i = 0
for word in words:
    data = None
    hint_grade = 1
    i += 1
    while data != word[indices[1]]:
        data = input(str(i) + '> ' + word[indices[0]] + ': ').strip()
        # data_cl = data.strip()
        
        if len(data) == 0:
            continue
        
        # COMMAND CODE
        
        if data == HINT_COMM:
            print('Hint:', hintify(word[indices[1]], hint_grade))
            hint_grade += 1
        elif data == ANS_COMM:
            print('Answer:', word[indices[1]])
            break
        elif data == HELP_COMM:
            print('Available commands:')
            print(HELP_COMM, '-', 'show this help information')
            print(HINT_COMM, '-', 'show hint for a word')
            print(ANS_COMM, '-', 'show the answer for a word')
            print(QUIT_COMM, '-', 'quit')
        elif data == QUIT_COMM:
            sys.exit()
        elif data[0] == COMM_PREFIX:
            print('Unknown command.')
