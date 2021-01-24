# process the input funblocks program to fix lexical issues before parsing
# and process the output (maude module) to delete the annoying caracters after
# the parsing

import os

# add space after the '$' for variable
def pre(filename):
    with open(filename, 'r') as file :
        filedata = file.read()
        filedata = filedata.replace('$', '$ ')

    with open(filename, 'w') as file :
        file.write(filedata)

# delete ' caracter and identical lines
def post(filename):
    lines_seen = set()
    outfile = open("tmp.txt", "w")
    for line in open(filename, "r"):
        if line not in lines_seen:
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
    with open("tmp.txt", 'r') as file :
        filedata = file.read()
        filedata = filedata.replace("'", '')
    with open(filename, 'w') as file :
        file.write(filedata)
    os.remove("tmp.txt")

# pre("./test.txt")
post("./funrules.maude")
