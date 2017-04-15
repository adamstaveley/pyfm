# pyfm

**pyfm is a command line file manager written in python with a range of features**

pyfm is able to do the following:
* move around the file system
* make new files and directories
* rename, move and delete files and directories
* read contents of plaintext and compressed files
* write content to plaintext files
* extract compessed files
* archive files
* remove whitespace from filenames or custom characters with regular expressions
* create bookmarks and copy often-used arguments to the clipboard
* split FLAC files using a CUE file
<br><br>

**Dependencies**

To install the required Python3 modules use:

`python3 -m pip install requirements.txt`

To extract from rar files and split FLAC files, you will need to install two 
packages:
* `unar`
* `shnsplit`

They are likely available through your distribution's package manager.
<br><br>

**Usage**

`git clone https://github.com/ayuopy/pyfm.git`
<br>
`cd /path/to/pyfm`
<br>
`python3 pyfm.py [DIRECTORY]` 

There is a manual available for pyfm. To view, run the following:

`cp pyfm.8.gz /usr/share/man/man8/`

Note that your distribution may store its man pages in a different directory.
You will then be able to view the manual by running `man pyfm`.

You can also type help at any point in pyfm if you are stuck. Likewise you can 
type `help [COMMAND]` to get help text for a single command.

Lastly, you can create a bash alias for pyfm to grant easier access to it. Place
this in your `.bashrc` or `.bash_aliases`:

`alias pyfm="python3 ~/path/to/pyfm.py"`

Then run `source .bashrc` from your home directory.
<br><br>

**Disclaimer**

This is the first proper program I made after learning Python. It served as a 
roundabout way of learning the Unix command line. The code style leaves... 
something to be desired but the program itself works well. 
