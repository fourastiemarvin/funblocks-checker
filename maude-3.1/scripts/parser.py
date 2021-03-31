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
# contains elements for eq declaration
eqDeclList = []
# contains elements for type declaration (aka parametrized module)
typeDeclList = []

includeList = []

sortList = []

# FIXME: the type of the right term is not inferred (typed as Any)

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
    varList.append("Any")
    return varList

# build an element of opDeclList: [label, dom1, dom2,... , co-domain]
# NOTE: opDecl returns an item with an unspecified type.
#       If the type is specified, this item won't be append in opDeclList
def opDecl(label, arity, parent=None, pos=None):
    opList = []
    opList.append(label)
    for i in range(arity):
        opList.append("Any")
    # the last element is the co-domain (to be infered)
    # print(typedList)
    for t in typedList:
        if parent == t[0]:
            opList.append(t[pos])
            return opList
    opList.append("Any")
    return opList

# build eq for the maude module using eqDeclList
def eqDecl():
    global eqDeclList
    newEqDeclList = []
    with open('prog.txt', 'r') as prog:
        eqDeclList = [w[0:-1] for w in prog if "case" == w[0:4]]
    for case in eqDeclList:
        case = case.replace("case", "eq")
        case = case.replace("=>", "=")
        newEqDeclList.append(case + " .")
    eqDeclList = newEqDeclList

# build list to declare type
def typeDecl():
    newTypeDeclList = []
    global typeDeclList
    with open('prog.txt', 'r') as prog:
        typeDeclList = [w[0:-1] for w in prog if "type" == w[0:4]]
    for type in typeDeclList:
        t = type.split("|")
        first = t[0].split("::")
        first = [s.replace("type", "") for s in first]
        # typeDeclList = first + t[1:len(t)]
        newTypeDeclList.append(first + t[1:len(t)])
    typeDeclList = newTypeDeclList

# build list of typed terms
def getType(typeDict):
    typed = ast.literal_eval(typeDict)
    for k, v in typed.items():
        # case with no parameter (the co-domain is always the last element of v)
        if len(v) == 1:
            typedList.append([k, v[-1][-1]])
            sortList.append(v[-1][-1])
        else:
            curRuleList = []
            curRuleList.append(k)
            for t in v[0:len(v)]:
                curRuleList.append(t[-1])
                sortList.append(t[-1])
            typedList.append(curRuleList)

# return declaration of the view and the module for the given type
def initType():
    global typeDeclList
    global includeList
    global sortList
    viewDecl = ""
    typeMod = ""
    for t in typeDeclList:
        nameList = t[0].split(" ")
        for item in nameList:
            if item == "":
                nameList.remove(item)
        typeMod += "fmod " + nameList[0] + "{ X :: TRIV } is \n sort " + nameList[0] + "{ X } . \n"
        includeList.append(nameList[0] + "{" + nameList[-1] + "}")
        if nameList[0] in sortList:
            sortList.remove(nameList[0])
        for tyIt in opDeclList:
            for el in tyIt:
                if nameList[0] == el:
                    tyIt[tyIt.index(el)] = nameList[0] + "{" + nameList[-1] + "}"
        viewDecl += "view " + nameList[-1] + " from TRIV to QID is sort Elt to Qid . endv \n"
        sortList.append(nameList[-1])
        for ctor in t[1:]:
            func = ctor.split(" ")
            for item in func:
                if item == "":
                    func.remove(item)
            for op in opDeclList:
                if func[0] in op:
                    opDeclList.remove(op)
            if len(func) == 1:
                typeMod += " op " + func[0] + " : -> " + nameList[0] + "{ X } . \n"
            else:
                dom = ""
                for type in func[1:]:
                    if (nameList[-1] in type) and (")" not in type):
                        dom += "X$Elt "
                    elif nameList[0] in type:
                        dom += nameList[0] + "{ X } "
                typeMod += " op " + func[0] + " : " + dom + " -> " + nameList[0] + "{ X } . \n"
        typeMod += "endfm \n"
    return viewDecl, typeMod

# init the module write declarations of function in funrules.maude
def buildModule():
    global varDeclList
    global opDeclList
    global typedList
    global eqDeclList
    global typeDeclList
    global includeList
    global sortList
    decl = "fmod FUNRULES is \n protecting QID . \n sort Any . \n"
    for s in includeList:
        decl += "including " + s + " . \n"
        decl += "subsort " + s + " < Any . \n"
    for s in sortList:
        decl += "sort " + s + " . \n subsort "  + s + " < Qid < Any . \n"
    for v in varDeclList:
        decl += "var $" + v[0] + " : " + v[-1] + " . \n"
    for op in opDeclList:
        decl += "op " + op[0] + " :"
        for s in op[1:-1]:
            decl += " " + s + " "
        decl += " -> " + op[-1] + " . \n"
    for eq in eqDeclList:
        decl += eq + "\n"
    decl += "endfm"
    with open("../funblocks/funrules.maude", 'w') as file :
        file.write(initType()[0] + "\n")
        file.write(initType()[1] + "\n")
        file.write(decl)

data = '{ "depth" : [ ( "TypeDeclRef" , "Tree" ) , ( "TypeDeclRef" , "Nat" ) ] }'
getType(data)
parseCase(parsed)
eqDecl()
typeDecl()
initType()
buildModule()

#############################   TESTS ###########################################
# data = '{ "ajoute": [ ("TypeVarRef", "T7"), ("TypeDeclRef", "List"), ("TypeDeclRef", "List")]}'
# data = '{ "if" : [ ( "TypeVarRef" , "T" ) , ( "TypeDeclRef" , "List" ) , ( "TypeDeclRef" , "List" ) ],"aj" : [ ( "TypeVarRef" , "T" ) , ( "TypeDeclRef" , "List" ) , ( "TypeDeclRef" , "List" ) ] }'
# data = '{ "depth" : [ ( "TypeDeclRef" , "Tree" ) , ( "TypeDeclRef" , "Nat" ) ] }'
# getType(data)
# parseCase(parsed)
# print("var: ", varDeclList)
# # [['x', 'any'], ['y', 'any']]
# print("op: ", opDeclList)
# # [['if', 'any', 'any', 'any'], ['id', 'any'], ['true'], ['false']]
# print("typed: ", typedList)
# [['ajoute', 'T', 'List', 'List'], ['aj', 'T', 'List', 'List']]
# eqDecl()
# print("eq: ", eqDeclList)
# typeDecl()
# print("type: ", typeDeclList)
# # [' Tree $T ', ' empty ', ' leaf $T ', ' node (Tree $T) (Tree $T)']
# print("sort: ",sortList)
# print("inc: ", includeList)
