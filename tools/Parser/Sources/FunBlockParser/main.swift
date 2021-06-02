import Files

var src =
"""
// Type definitions
type List $T :: empty | cons $T (List $T)

// Initial state
init cons(1, cons(2, empty))

// Quicksort
rule sort :: List Int => List Int
case sort(empty) => empty
case sort(cons($x, $y)) => cat(filter_lt($x, $y), cons($x, sort(filter_gt($x, $y))))

// Filters
rule filter_lt :: Int -> List Int => List Int
case filter_lt($x, empty) => empty
case filter_lt($x, cons($y, $z)) => if(lt($y, $x), cons($y, filter_lt($z)), filter_lt($z))

rule filter_gt :: Int -> List Int => List Int
case filter_gt($x, empty) => empty
case filter_gt($x, cons($y, $z)) => if(gt($y, $x), cons($y, filter_gt($z)), filter_gt($z))

// Conditional expressions
rule if $T :: Bool -> $T -> $T => $T
case if(true, $x, $y) => $x
case if(false, $x, $y) => $y
"""

FunBlockParser.initialize()

let prog =
"""
type Nat :: zero | succ Nat
type Tree $T :: empty | leaf $T | node (Tree $T) (Tree $T)
rule depth $T :: Tree $T => Nat
rule quicksort :: List $T -> Int => List Int
rule add :: Nat -> Nat => Nat
case add($x, add($y, zero)) => $x
case depth(empty) => zero
case succ($z) => zero
"""

let tokens = try tokenize(prog)
let stmts = FunBlockParser.parse(tokens)
// print("\n TEST:")
// print(signArray)

let folder = try Folder(path: "../")
let file = try folder.createFile(named: "funrules.maude")
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
  for stmt in stmts {
    if let s = stmt as? RuleDecl {
      module += s.toMaude
    }
    else if let s = stmt as? RuleDef {
      module += s.toMaude
    }
    else {continue}
  }
  module += " \n endfm)"
}

typeMaude()
ruleMaude()
try file.write(module)
