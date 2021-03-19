# process the input funblocks program to fix lexical issues before parsing
# and process the output (maude module) to delete the annoying caracters after
# the parsing

import ast
import os

# add space after the '$' for variable
def pre(filename):
    with open(filename, 'r') as file :
        filedata = file.read()
        filedata = filedata.replace('$', '$ ')

    with open(filename, 'w') as file :
        file.write(filedata)

# init the module write declarations of function in funrules.maude
def init_module(data):
    decl = ""
    d = ast.literal_eval(data)
    # iterate over keys k and values v
    for k, v in d.items():
        if len(v) == 1:
            decl = decl + "op " + k + " : " + "-> " + v[-1][-1] + " . \n"
        else:
            dom = ' '.join([t[-1] for t in v[0:len(v)]])
            decl = decl + "op " + k + " : " + dom + " -> " + v[-1][-1] + " . \n"
    with open("../funblocks/funrules.maude", 'w') as file :
        file.write("fmod FUNRULES is \n")
        file.write(decl)

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


# TEST

# data = '{ "ajoute": [ ("TypeVarRef", "T7"), ("TypeDeclRef", "List"), ("TypeDeclRef", "List")]}'
data = '{ "ajoute" : [ ( "TypeVarRef" , "T" ) , ( "TypeDeclRef" , "List" ) , ( "TypeDeclRef" , "List" ) ],"aj" : [ ( "TypeVarRef" , "T" ) , ( "TypeDeclRef" , "List" ) , ( "TypeDeclRef" , "List" ) ] }'
# pre("./test.txt")
# post("./funrules.maude")
init_module(data)
