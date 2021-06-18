"""Usage:
    funblocks_checker init FILENAME
    funblocks_checker [--log] (ct | check_termination)
    funblocks_checker (cf | check_confluence)
    funblocks_checker exit

   Arguments:
    FILENAME   Path of FunBlocks file

   Options:
    -h --help  Show this screen.
    --log      Open log file of termination check in your browser.

"""

# {'--log': False,
#  'FILENAME': 'foo.txt',
#  'cf': False,
#  'check_confluence': False,
#  'check_termination': False,
#  'ct': False,
#  'exit': False,
#  'init': True}


from docopt import docopt
import subprocess

def init():
    print("translation")

def term(log=False):
    subprocess.run(["./CLI/check_termination.sh"])

def conf():
    subprocess.run(["./CLI/check_confluence.sh"])

def exit():
    pass

def main():
    args = docopt(__doc__)
    # print(args)
    if args['init']:
        init()
    elif args['ct'] or args['check_termination']:
        term(log=args['--log'])
    elif args['cf'] or args['check_confluence']:
        conf()
    elif args['exit']:
        exit()
    else:
        print("Invalid command")

    # subprocess.run(["python3", "CLI/callMaude.py"])
    # print(arguments)

if __name__ == '__main__':
    main()
