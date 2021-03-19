import json
import ast
import os
import itertools

# read the program in json format
with open('program.json') as program:
    parsed = json.load(program)

with open("pretty_prog.json", 'w') as pretty:
    pretty.write(json.dumps(parsed, indent=2, sort_keys=True))

# contains elements for var declaration
varDeclList = []
# contains elements for op declaration
opDeclList = []
# contains typed terms
typedList = []

# entrypoint, parse each case
def parseCase(prog):
    global opDeclList
    for case in prog["ruleCases"]:
        parseTerm(case["left"])
        parseTerm(case["right"])
    opDeclList.sort()
    opDeclList = list(opDeclList for opDeclList,_ in itertools.groupby(opDeclList))

# parse each term (right term, left term)
def parseTerm(term, parent=None, pos=None):
    if term["_objectType"] == "Expr":
        # call the func to parse an Expr (func, const)
        parseExpr(term, parent=parent, pos=pos)
    elif term["_objectType"] == "VarRef":
        # add var in varDeclList using varDecl func
        newVar = varDecl(term, parent=parent, pos=pos)
        if newVar[0] not in [v[0] for v in varDeclList]:
            # verify if current var is already in the list
            varDeclList.append(newVar)
    else:
        print("parsing error")

# parse an Expr (func and const)
def parseExpr(term, parent=None, pos=None):
    global opDeclList
    newOp = opDecl(term["label"], len(term["subterms"]), parent=parent, pos=pos)
    if newOp[0] in [t[0] for t in typedList[0:len(typedList)]]:
    # add op decl in opDeclList if op is typed (using typedList)
        opDeclList = opDeclList + [t for t in typedList if t[0] == newOp[0]]
    elif newOp not in opDeclList:
        # verify if current op is already in opDeclList
        opDeclList.append(newOp)
    for subterm in term["subterms"]:
        # iterate over subterm (list) of an Expr
        parseTerm(subterm, parent=term["label"],
                            pos=term["subterms"].index(subterm)+1)

# build an element of varDeclList: [label, type]
def varDecl(term, parent=None, pos=None):
    varList = []
    varList.append(term["label"])
    for t in typedList:
    # handle the case if the current var is typed by inferrence
        if parent == t[0]:
            varList.append(t[pos])
            return varList
    # co-domain put as last item of the varList
    varList.append("any")
    return varList

# build an element of opDeclList: [label, dom1, dom2,... , co-domain]
# NOTE: opDecl returns an item with an unspecified type.
#       If the type is specified, this item won't be appened in opDeclList
def opDecl(label, arity, parent=None, pos=None):
    opList = []
    opList.append(label)
    for i in range(arity):
        opList.append("any")
    # the last element is the co-domain (to be infered)
    for t in typedList:
        if parent == t[0]:
            opList.append(t[pos])
            return opList
    opList.append("any")
    return opList

# TODO
def eqDecl():
    pass

# build list of typed terms
def getType(typeDict):
    typed = ast.literal_eval(typeDict)
    for k, v in typed.items():
        # case with no parameter (the co-domain is always the last element of v)
        if len(v) == 1:
            typedList.append([k, v[-1][-1]])
        else:
            curRuleList = []
            curRuleList.append(k)
            for t in v[0:len(v)]:
                curRuleList.append(t[-1])
            typedList.append(curRuleList)

# init the module write declarations of function in funrules.maude
# def init_module(data):
#     decl = ""
#     d = ast.literal_eval(data)
#     # iterate over keys k and values v
#     for k, v in d.items():
#         if len(v) == 1:
#             decl = decl + "op " + k + " : " + "-> " + v[-1][-1] + " . \n"
#         else:
#             dom = ' '.join([t[-1] for t in v[0:len(v)]])
#             decl = decl + "op " + k + " : " + dom + " -> " + v[-1][-1] + " . \n"
#     with open("funrules.maude", 'w') as file :
#         file.write("fmod FUNRULES is \n")
#         file.write(decl)


#############################   TESTS ###########################################
# data = '{ "ajoute": [ ("TypeVarRef", "T7"), ("TypeDeclRef", "List"), ("TypeDeclRef", "List")]}'
data = '{ "if" : [ ( "TypeVarRef" , "T" ) , ( "TypeDeclRef" , "List" ) , ( "TypeDeclRef" , "List" ) ],"aj" : [ ( "TypeVarRef" , "T" ) , ( "TypeDeclRef" , "List" ) , ( "TypeDeclRef" , "List" ) ] }'
getType(data)
parseCase(parsed)
print(varDeclList)
# [['x', 'any'], ['y', 'any']]
print(opDeclList)
# [['if', 'any', 'any', 'any'], ['id', 'any'], ['true'], ['false']]
print(typedList)
# [['ajoute', 'T', 'List', 'List'], ['aj', 'T', 'List', 'List']]
