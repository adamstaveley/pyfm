#! python3
# file manager

import os
import sys
import shelve
import readline
import pyperclip
import FileOps

# command line argument
if len(sys.argv) == 2:
    os.chdir(sys.argv[1])


# command line features
bold = '\001\033[1m\002'		    # \001, \002 escape readline
end_bold = '\001\033[m\002'


def complete(text, state):
    for f in os.listdir():
        if f.startswith(text):
            if not state:
                return f
            else:
                state -= 1


def clipboard(path):
    pyperclip.copy(path)
    print(path + ' copied to clipboard')

bookmarks = shelve.open('/home/adam/tools/python/pyfm/bookmarks')


def bookmark(*args):
    if len(args) == 0:
        raise Exception('argument(s) missing')
    elif args[0] == 'add':
        bookmarks[args[1]] = args[2]
        print("'" + args[1] + "' saved as bookmark")
    elif args[0] == 'get':
        path = bookmarks[args[1]]
        pyperclip.copy(path)
        print("'" + path + "' copied to clipboard")
    elif args[0] == 'del':
        del bookmarks[args[1]]
        print("'" + args[1] + "' deleted from clipboard")
    elif args[0] == 'list':
        for key, value in bookmarks.items():
            print(key + ': ' + value)
    else:
        raise Exception('argument not found')


# user operation

while True:
    # input
    readline.parse_and_bind('tab: complete')
    readline.set_completer(complete)

    op_raw = input(bold + 'operation: ' + end_bold)
    op_split = op_raw.split()
    op = []

    for s in op_split:
        new = s.replace('\\\\', ' ')
        op.append(new)

    try:
        # standard operations
        if op[0] in FileOps.standard:

                if 'dir' in op:
                    FileOps.make_dir(*op[1:])

                elif 'file' in op:
                    FileOps.make_file(*op[1:])

                elif 'write' in op:
                    FileOps.write_file(op[1])

                elif 'size' in op:
                    FileOps.get_size(*op)

                elif 'rename' in op:
                    FileOps.rename(*op[1:])

                elif 'rmspace' in op:
                    FileOps.rmspace(*op)

                elif 'rmx' in op:
                    FileOps.rmx(*op[1:])

                elif 'copy' in op:
                    FileOps.copy(*op[1:])

                elif 'move' in op:
                    FileOps.move(*op[1:])

                elif 'delete' in op:
                    FileOps.delete(*op[1:])

        # advanced operations
        elif op[0] in FileOps.advanced:

                if 'read' in op:
                    FileOps.read(*op[1:])

                elif 'extract' in op:
                    FileOps.extract_all(*op[1:])

                elif 'archive' in op:
                    FileOps.archive(*op[1:])

                elif 'compress' in op:
                    FileOps.compress(*op[1:])

                elif 'decompress' in op:
                    FileOps.decompress(*op[1:])

                elif 'split' in op:
                    FileOps.flac_split(op[1], op[2])

        # misc operations
        elif op[0] in FileOps.other:

                if 'pwd' in op[0]:
                    FileOps.info()

                elif 'cd' in op[0]:
                    FileOps.ch_dir(*op[1:])

                elif 'list' in op[0]:
                    FileOps.list(*op[1:])

                elif 'tree' in op[0]:
                    FileOps.list_tree(*op)

                elif 'clip' in op[0]:
                    clipboard(op[1])

                elif 'bm' in op[0]:
                    bookmark(*op[1:])

                elif 'help' in op[0]:
                    FileOps.help(*op[1:])

                elif 'quit' in op[0]:
                    FileOps.quit()

        else:
            print("try 'help'")

    # exception handling
    except IndexError:
        print('argument(s) missing')
    except FileNotFoundError:
        print('selection not found')
    except PermissionError:
        print('root privileges needed')
    except UnicodeDecodeError:
        print("unable to read '" + op[1] + "'")
    except TypeError:
        print('argument(s) missing')
    except NotADirectoryError:
        print('not a directory')
    except Exception as err:
        print(err)
