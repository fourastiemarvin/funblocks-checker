"""Usage:
    funblocks_checker init FILENAME
    funblocks_checker [--log] (ct | check_termination)
    funblocks_checker (cf | check_confluence)

   Arguments:
    FILENAME   Path of FunBlocks file

   Options:
    -h --help  Show this screen.
    --log      Open log file of termination check in your browser.

"""

from docopt import docopt
import subprocess
from shutil import copyfile

def init(args):
    filename = args['FILENAME']
    copyfile(filename, "tmp/prog.txt")
    subprocess.run(["./CLI/callMaude.sh" , "init"])
    print("FunBlocks program ready to be checked !")

def term(log=False):
    subprocess.run(["./CLI/callMaude.sh" , "term"])
    if log:
        subprocess.run(["./CLI/callMaude.sh" , "term", "log"])

def conf():
    subprocess.run(["./CLI/callMaude.sh" , "conf"])

def main():
    try:
        args = docopt(__doc__)
        if args['init']:
            init(args)
        elif args['ct'] or args['check_termination']:
            term(log=args['--log'])
        elif args['cf'] or args['check_confluence']:
            conf()
        else:
            print("Invalid command")
    except Exception as e:
        print("Please move to funblocks-checker directory")

if __name__ == '__main__':
    main()
