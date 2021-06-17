"""Usage:
    funblocks_checker (--to-maude | --tm) FILE
    funblocks_checker [--log] (ct | check_termination)
    funblocks_checker (cf | check_confluence)
    funblocks_checker exit

"""

from docopt import docopt
import subprocess

def main():
    arguments = docopt(__doc__)
    subprocess.run(["python3", "CLI/callMaude.py"])
    # print(arguments)

if __name__ == '__main__':
    main()
