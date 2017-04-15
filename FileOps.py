import os
import sys
import subprocess
import glob
import shutil
import send2trash
import zipfile
import gzip
import tarfile
import rarfile
import pprint


# lists
standard = ['dir', 'file', 'write', 'size', 'rename', 'copy', 'move',
            'delete', 'rmspace', 'rmx']
advanced = ['read', 'extract', 'archive', 'compress', 'decompress', 'split']
other = ['cd', 'pwd', 'list', 'tree', 'clip', 'bm', 'help', 'quit']


# standard functions
def make_dir(*args):
    if len(args) == 0:
        print('argument needed')
    folders = []
    for arg in args:
        if os.path.exists(arg):
            print("'" + arg + "'" + ' already exists')
            pass
        else:
            os.makedirs(arg)
            new = "'" + arg + "'"
            folders.append(new)
    if len(folders) > 0:
        print('created ' + ', '.join(folders))


def make_file(*args):
    if len(args) == 0:
        print('argument needed')
    files = []
    for arg in args:
        if os.path.exists(arg):
            print("'" + arg + "'" + ' already exists')
            pass
        else:
            open(arg, 'a')
            new = "'" + arg + "'"
            files.append(arg)
    if len(files) > 0:
        print('created ' + ', '.join(files))


def write_file(x):
    if os.path.isdir(x):
        raise Exception("'" + x + "'" + ' is a directory')
    f = open(x, 'a')
    f.write(input())


def convert(size):
    if size >= 1000 and size <= 1000000:
        print('%r kB' % (round(size / 1000, 1)))
    elif size >= 1000000 and size <= 1000000000:
        print('%r MB' % (round(size / 1000000, 1)))
    elif size >= 1000000000 and size <= 1000000000000:
        print('%r GB' % (round(size / 1000000000, 1)))
    else:
        print('%d bytes' % size)


def size(path):
    total_size = 0
    seen = {}
    for root, dirs, files in os.walk(path):
        for f in files:
            filepath = os.path.join(root, f)
            try:
                stat = os.lstat(filepath)
            except OSError:
                continue
            try:
                seen[stat.st_ino]
            except KeyError:
                seen[stat.st_ino] = True
            else:
                continue
            total_size += stat.st_size
    return convert(total_size)


def get_size(*args):
    if len(args) == 1:
        size('.')
    elif len(args) == 2:
        if os.path.exists(args[1]):
            size(args[1])
        else:
            print('path not found')


def rename(*args):
    names = []
    if len(args) == 0:
        print('argument needed')
    elif args[0] == 'all':
        for f in sorted(os.listdir()):
            new_name = input(f + ': ')
            while os.path.exists(new_name):
                print("'" + new_name + "' already exists")
                new_name = input(f + ': ')
            if len(new_name) > 0:
                os.rename(f, new_name)
                names.append(f)
        if len(names) > 0:
            print('selection renamed')
    elif args[0] == 'reg':
        regex = input('regex: ')
        matches = sorted(glob.glob(regex))
        if len(matches) > 0:
            for f in matches:
                new_name = input(f + ': ')
                while os.path.exists(new_name):
                    print("'" + new_name + "' already exists")
                    new_name = input(f + ':')
                if len(new_name) > 0:
                    os.rename(f, new_name)
                    names.append(f)
            if len(names) > 0:
                print('selection renamed')
        else:
            print('no matches found')
    else:
        for arg in args:
            if os.path.exists(arg):
                new_name = input(arg + ': ')
                while os.path.exists(new_name):
                    print("'" + new_name + "' already exists")
                    new_name = input(arg + ': ')
                if len(new_name) > 0:
                    os.rename(arg, new_name)
                    names.append(arg)
            else:
                print("'" + arg + "' not found")
        if len(names) > 0:
            print('selection renamed')


def rmspace(*args):
    for f in os.listdir():
        if len(args) == 1:
            os.rename(f, f.replace(' ', ''))
        elif len(args) == 2:
            os.rename(f, f.replace(' ', args[1]))
    print('spaces removed')


def rmx(*args):
    for f in os.listdir():
        if len(args) == 1:
            os.rename(f, f.replace(args[0], ''))
        elif len(args) == 2:
            os.rename(f, f.replace(args[0], args[1]))
    print('characters removed or replaced')


def copy(*args):
    # might require bulk functions in the future
    names = []
    for f in args[0:-1]:
        if os.path.exists(f):
            if os.path.isdir(f):
                if os.path.isdir(args[-1]):
                    path = os.path.join(args[-1], f)
                    shutil.copytree(f, path)
                else:
                    shutil.copytree(f, args[-1])
            elif os.path.isfile(f):
                if not os.path.exists(args[-1]):
                    make_dir(args[-1])
                shutil.copy(f, args[-1])
            names.append("'" + f + "'")
        elif not os.path.exists(f):
            print("'" + f + "' not found")
    if len(names) > 0:
        print(', '.join(names) + ' moved to ' + args[-1])
    elif len(args) == 0:
        print('argument needed')


def move(*args):
    names = []
    if len(args) == 1:
        # selection mode
        if args[0] == 'sel':
            dest = input('destination: ')
            if os.path.isdir(dest):
                for f in sorted(os.listdir()):
                    selection = input(f + ': ')
                    if 'y' in selection:
                        if os.path.exists(os.path.join(dest, f)):
                            print("'" + os.path.join(dest, f) +
                                  "' already exists")
                        else:
                            shutil.move(f, dest)
                            names.append(f)
                if len(names) > 0:
                    print('selection moved to ' + dest)
            else:
                print("'" + dest + "' not found")
        # regex mode
        elif args[0] == 'reg':
            regex = input('regex: ')
            matches = sorted(glob.glob(regex))
            if len(matches) > 0:
                dest = input('destination: ')
                if not os.path.isdir(dest):
                    print('destination not found')
                else:
                    for f in matches:
                        if os.path.exists(os.path.join(dest, f)):
                            print("'" + os.path.join(dest, f) +
                                  "' already exists")
                        else:
                            shutil.move(f, dest)
                            names.append(f)
                    if len(names) > 0:
                        print('matches moved to ' + dest)
            else:
                print('no matches found')
        else:
            raise Exception('argument not found')
    # standard mode
    elif len(args) > 1:
        if os.path.isdir(args[-1]):
            for f in args[0:-1]:
                if os.path.exists(os.path.join(args[-1], f)):
                    print("'" + os.path.join(args[-1], f) + "' already exists")
                elif os.path.exists(f):
                    shutil.move(f, args[-1])
                    names.append("'" + f + "'")
                else:
                    print("'" + f + "' not found")
            if len(names) > 0:
                print(', '.join(names) + ' moved to ' + args[-1])
        else:
            print("'" + args[-1] + "' not found")


def delete(*args):
    names = []
    if args[0] == 'all':
        for f in os.listdir():
            send2trash.send2trash(f)
        print("'" + os.getcwd() + "' emptied")
    elif args[0] == 'sel':
        for f in sorted(os.listdir()):
            selection = input(f + ': ')
            if 'y' in selection:
                send2trash.send2trash(f)
                names.append(f)
        if len(names) > 0:
            print('selection deleted')
    else:
        for arg in args:
            if os.path.exists(arg):
                send2trash.send2trash(arg)
                names.append(arg)
            else:
                print("'" + arg + "' not found")
        print(', '.join(names) + ' moved to trash')


# advanced functions
def read(x):
    if zipfile.is_zipfile(x):
        contents = zipfile.ZipFile(x).namelist()
        print('\n'.join(contents))
    elif x.endswith('.gz'):
        if tarfile.is_tarfile(x):
            tar = tarfile.open(x)
            contents = tar.getnames()
            print('\n'.join(contents))
        else:
            gz = gzip.open(x)
            contents = gz.read()
            print(contents)
    elif rarfile.is_rarfile(x):
        rar = rarfile.RarFile(x)
        contents = rar.namelist()
        print('\n'.join(contents))
    else:
        f = open(x)
        print(f.read())


def extract_all(*args):
    if len(args) > 0:
        dest = input('destination: ')
        for arg in args:
            if os.path.isdir(arg):
                print("'" + arg + "' is a directory")
            elif not os.path.exists(arg):
                print("'" + arg + "' not found")
            elif zipfile.is_zipfile(arg):
                zipf = zipfile.ZipFile(arg)
                if len(dest) == 0:
                    zipf.extractall()
                else:
                    zipf.extractall(dest)
                print("contents extracted from '" + arg + "'")
            elif tarfile.is_tarfile(arg):
                tar = tarfile.open(arg)
                if len(dest) == 0:
                    tar.extractall()
                else:
                    tar.extractall(dest)
                print("contents extracted from '" + arg + "'")
            elif rarfile.is_rarfile(arg):
                if len(dest) == 0:
                    subprocess.check_output(['unar', arg])
                else:
                    subprocess.check_output(['unar', '-o', args[-1], arg])
                print("contents extracted from '" + arg + "'")
            else:
                print("unable to extract '" + arg + "'")
    else:
        raise TypeError


def archive(*args):
    contents = []
    if os.path.exists(args[-1]):
        if os.path.isdir(args[-1]):
            raise Exception('destination required')
        elif args[-1].endswith('.gz'):
            raise Exception('tar file must be decompressed first')
        elif not tarfile.is_tarfile(args[-1]):
            raise Exception('destination required')
    tar = tarfile.open(args[-1], 'a')
    for arg in args[0:-1]:
        tar.add(arg)
        contents.append("'" + arg + "'")
    tar.close()
    q = input(', '.join(contents) + ' archived: compress now? ')
    if 'y' in q:
        compress(args[-1])


def compress(*args):
    files = []
    if len(args) == 0:
        print('argument(s) missing')
    for arg in args:
        if os.path.isfile(arg):
            subprocess.run(['gzip', arg])
            files.append("'" + arg + "'")
        elif os.path.isdir(arg):
            print("'" + arg + "' is a directory")
        else:
            print("'" + arg + "' not found")
    if len(files) > 0:
        print(', '.join(files) + ' compressed')


def decompress(*args):
    files = []
    if len(args) == 0:
        print('argument(s) missing')
    for arg in args:
        if os.path.exists(arg):
            if arg.endswith('.gz'):
                    subprocess.run(['gunzip', arg])
                    files.append("'" + arg + "'")
            else:
                raise Exception('gzip file not recognised')
    if len(files) > 0:
        print(', '.join(files) + ' decompressed')


def flac_split(flac, cue):
    if flac.endswith('.flac') and cue.endswith('.cue'):
        if os.path.exists(flac) and os.path.exists(cue):
            subprocess.run(['shnsplit', '-f', cue, '-t', '%n_%t',
                            '-o', 'flac', flac])
            delete(flac)
            # if not working try ('cuetag.sh %s *.flac' % cue, shell=True)
            # shell=True isn't advised so try shell=False
            # shlex.split() can prepare the command
            subprocess.run(['cuetag.sh', cue, '*.flac'])
            delete(cue)
            print('files tagged')
        else:
            raise Exception("'" + flac + "' or '" + cue + "' not found")
    else:
        raise Exception('flac and cue file needed')


# misc functions

def info():
    print(os.getcwd())


def ch_dir(*args):
    if len(args) == 0:
        os.chdir('/home/adam/')
        print('new cwd: ' + os.getcwd())
    else:
        os.chdir(args[0])
        print('new cwd: ' + os.getcwd())


def list(*args):
    folders = []
    files = []
    if len(args) == 0:
        for f in sorted(os.listdir()):
            if not f.startswith('.'):
                if os.path.isdir(f):
                    folders.append(f)
                else:
                    files.append(f)
    elif len(args) == 1:
        x = args[0]
        for f in sorted(os.listdir(x)):
            if not f.startswith('.'):
                path = os.path.join(x, f)
                if os.path.isdir(path):
                    folders.append(f)
                elif os.path.isfile(path):
                    files.append(f)
    if len(folders) > 0:
        print('\033[0;33m' + '\n'.join(folders) + '\033[0m')
    if len(files) > 0:
        print('\n'.join(files))


def tree(d):
    # subfolders not sorted alphabetically
    for folder, subfolders, files in os.walk(d):
        level = folder.replace(d, '').count(os.sep)
        indent = ' ' * 2 * (level)
        print('{}{}/'.format(indent, os.path.basename(folder)))
        subindent = ' ' * 2 * (level + 1)
        for f in sorted(files):
            print('{}{}'.format(subindent, f))
    if not os.path.isdir(d):
        raise Exception('directory not found')


def list_tree(*args):
    if len(args) == 1:
        tree('.')
    elif len(args) == 2:
        tree(args[1])


def help(*args):
    if len(args) == 0:
        print('usage: help [OPERATION]\n[ %s ]\n[ %s ]\n[ %s ]\n'
              'see manual for more information' %
              (' | '.join(standard), ' | '.join(advanced), ' | '.join(other)))
    elif len(args) > 0:
        if 'dir' in args:
            print('make new directories: dir [PATH1] [PATH2]...')
        elif 'file' in args:
            print('make new files: file [PATH1] [PATH2]...')
        elif 'write' in args:
            print('append text to to plaintext file: write [PATH]')
        elif 'size' in args:
            print('size [PATH]')
        elif 'rename' in args:
            print('rename [MODE]\n'
                  '  all: rename all items\n'
                  '  reg: rename all items matching regex e.g. \'*.pdf\'\n'
                  'rename [PATH1] [PATH2]...')
        elif 'copy' in args:
            print('copy [SOURCE1] [SOURCE2]... [DESTINATION]')
        elif 'move' in args:
            print('move [MODE]\n'
                  '  sel: select items to move using [y/n]\n'
                  '  reg: match items to move with regex e.g. \'*.pdf\'\n'
                  'move [SOURCE1] [SOURCE2]... [DESTINATION]')
        elif 'delete' in args:
            print('delete [MODE]\n'
                  '  all: delete all items\n'
                  '  sel: delete selection of items using [y/n]\n'
                  'delete [PATH1] [PATH2]...')
        elif 'rmspace' in args:
            print('rmspace [CHARACTER]\n'
                  'replace spaces in item names with character e.g \'_\'\n'
                  'otherwise escape spaces with \'\\\\\'')
        elif 'rmx' in args:
            print('rmx [OLD CHARACTERS] [NEW CHARACTERS]\n'
                  'remove or replace characters in item names\n'
                  'if new character not given old character will be removed')
        elif 'read' in args:
            print('read [PATH]\n'
                  'reads the contents of zip, rar, tar and plaintext files')
        elif 'extract' in args:
            print('extract [PATH1] [PATH2]...')
        elif 'archive' in args:
            print('archive [SOURCE1] [SOURCE2]... [DESTINATION]')
        elif 'compress' in args:
            print('compress [PATH1] [PATH2]...')
        elif 'decompress' in args:
            print('decompress [PATH1] [PATH2]...')
        elif 'split' in args:
            print('split [FLAC] [CUE]\n'
                  'split and tag output of single flac file using cue file')
        elif 'cd' in args:
            print('change working directory: cd [PATH]')
        elif 'pwd' in args:
            print('print working directory')
        elif 'list' in args:
            print('list contents: list [PATH]')
        elif 'tree' in args:
            print('walk through directory: tree [PATH]')
        elif 'clip' in args:
            print('copy to clipboard: clip [PATH]')
        elif 'bm' in args:
            print('store frequently used paths as bookmarks: bm [MODE]\n'
                  '  add [KEY] [VALUE]\n'
                  '  get [KEY]\n'
                  '  del [KEY]\n'
                  '  list')


def quit():
    sys.exit()
