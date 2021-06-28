import Foundation
import Files

FunBlockParser.initialize()

let funprog = try File(path: "../../../../tmp/prog.txt")
let prog = try funprog.readAsString()

let tokens = try tokenize(prog)

let stmts = FunBlockParser.parse(tokens)

let folder = try Folder(path: "../../../../.")
try folder.createSubfolder(named: "tmp")
let file = try folder.createFile(named: "tmp/funrules.maude")
var module = ""


func typeMaude() {
  for stmt in stmts {
    if let s = stmt as? TypeDecl {
      module += s.toMaude
    }
    else {continue}
  }
}

func ruleMaude() {
  module += "(fmod FUNRULES is \n"
  for type in typeList {
    module += "including \(type) .\n"
  }
  for stmt in stmts {
    if let s = stmt as? RuleDecl {
      module += s.toMaude + "\n"
    }
    else if let s = stmt as? RuleDef {
      module += s.toMaude + "\n"
    }
    else {continue}
  }
  module += " endfm)"
}

typeMaude()
ruleMaude()
try file.write(module)


// TESTS:
// print("\n TESTS:")
// print(signArray)
// print(typeList)
