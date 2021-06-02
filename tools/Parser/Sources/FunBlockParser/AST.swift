public protocol AST {}

var signArray: [String:[String]] = [:]

public struct TypeDecl: AST, CustomStringConvertible {

  public let name: String

  public let parameters: [TypeVarRef]

  public let cases: [TypeCons]

  public var description: String {
    var result = "type \(name)"
    if !parameters.isEmpty {
      result += " " + parameters.map(String.init(describing:)).joined(separator: " ")
    }
    result += " :: " + cases.map(String.init(describing:)).joined(separator: " | ")
    return result
  }

  public var toMaude: String {
    var result = ""
    var sortName = name
    // TODO: use {} to avoid sort overriding ???
    if !parameters.isEmpty {
      for p in parameters {
        result += "(view \(p) from TRIV to \(name) is sort Elt to \(name) . endv) \n"
      }
      let fmodName = parameters.map(String.init(describing:)).joined(separator: " :: TRIV, ") + " :: TRIV"
      sortName = name + "{" + parameters.map(String.init(describing:)).joined(separator: ",") + "}"
      result += "(fmod \(name){\(fmodName)} is \n sort \(sortName) . \n"
    }
    else {
      result += "(fmod \(name) is \n sort \(sortName) . \n"
    }
    for c in cases {
      result += "op \(c.label) : "
      signArray[c.label] = []
      if !c.arguments.isEmpty {
        for arg in c.arguments {
          if let varElt = arg as? TypeVarRef {
            result += varElt.toMaude + " "
            signArray[c.label]!.append(varElt.toMaude)
          }
          else if let declElt = arg as? TypeDeclRef {
            result += declElt.toMaude + " "
            signArray[c.label]!.append(declElt.toMaude)
          }
        }
      }
      result += "-> \(sortName) . \n"
    }
    result += "endfm) \n"
    return result
  }

}

public struct InitStateDecl: AST, CustomStringConvertible {

  public let state: Expr

  public var description: String {
    "init \(state)"
  }

}

public struct RuleDecl: AST, CustomStringConvertible {

  public let name: String

  public let arguments: [TypeRef]

  public let left: TypeSign

  public let right: TypeSign

  public var description: String {
    let tail = " :: \(left) => \(right)"
    return arguments.isEmpty
      ? "decl \(name)" + tail
      : "decl \(name) " + arguments.map({ "(\($0))" }).joined(separator: " ") + tail
  }
  public var toMaude: String {
    var result = ""
    if !arguments.isEmpty {
      for arg in arguments {
        result += "sort \(arg) .\n"
      }
    }
    signArray[name] = []
    let righth = right as! TypeDeclRef
    if let lefth = left as? ArrowTypeSign {
      result += "op \(name) : \(lefth.toMaude) -> \(righth.toMaude) .\n "
      signArray[name]! += lefth.toMaude.components(separatedBy: " ").filter(){$0 != ""}
    }
    else if let lefth = left as? TypeDeclRef {
      result += "op \(name) : \(lefth.toMaude) -> \(righth.toMaude) .\n "
      signArray[name]! += lefth.toMaude.components(separatedBy: " ").filter(){$0 != ""}
    }
    return result
  }

}

public struct RuleDef: AST, CustomStringConvertible {

  public let left: Expr

  public let right: Term

  public var description: String {
    "rule \(left) => \(right)"
  }
  public var toMaude: String {
    var result = ""
    result += left.toMaude
    if let righth = right as? Expr {
      result += righth.toMaude
    }
    result += "eq \(left) = \(right) ."
    return result
  }

}

public struct TypeCons: AST, CustomStringConvertible {

  public let label: String

  public let arguments: [TypeRef]

  public var description: String {
    arguments.isEmpty
      ? label
      : label + " " + arguments.map({ "(\($0))" }).joined(separator: " ")
  }

}

public protocol TypeSign: AST {}

public struct ArrowTypeSign: TypeSign, CustomStringConvertible {

  let left: TypeSign

  let right: TypeSign

  public var description: String {
    "(\(left)) -> (\(right))"
  }

  public var toMaude: String {
    var result = ""
    if let lefth = left as? TypeDeclRef {
      result += "\(lefth.toMaude) "
    }
    else if let lefth = left as? ArrowTypeSign {
      result += "\(lefth.left) \(lefth.right)"
    }
    if let righth = right as? TypeDeclRef {
      result += "\(righth.toMaude) "
    }
    else if let righth = right as? ArrowTypeSign {
      result += "\(righth.left) \(righth.right)"
    }
    return result
  }

}

public protocol TypeRef: TypeSign {}

public struct TypeDeclRef: TypeRef, CustomStringConvertible {

  public let name: String

  public let arguments: [TypeRef]

  public var description: String {
    arguments.isEmpty
      ? name
      : name + " " + arguments.map({ "(\($0))" }).joined(separator: " ")
  }

  public var toMaude: String {
    name + arguments.map({ "{\($0)}" }).joined(separator: " ")
  }

}

public struct TypeVarRef: TypeRef, CustomStringConvertible {

  public let name: String

  public var description: String {
    "$" + name
  }

  public var toMaude: String {
    "$" + name + "$Elt"
  }

}

public protocol Term: AST {}

public struct Expr: Term, CustomStringConvertible {

  public let label: String

  public let subterms: [Term]

  public var description: String {
    subterms.isEmpty
      ? label
      : label + "(" + subterms.map(String.init(describing:)).joined(separator: ", ") + ")"
  }

  public var toMaude: String {
    var result = ""
    var id1 = -1
    for sub in subterms {
      id1 += 1
      if let v = sub as? VarRef {
        let sort = signArray[self.label]![id1]
        result += v.toMaude + sort + " . \n"
      }
      else if let t = sub as? Expr {
        if !t.subterms.isEmpty {
          var id2 = -1
          for sub in t.subterms {
            id2 += 1
            if let subt = sub as? Expr {
              result += subt.toMaude
            }
            else if let subt = sub as? VarRef {
              let sort = signArray[self.label]![id1]
              result += subt.toMaude + sort + " . \n"
            }
          }
        }
      }
    }
    return result
  }
}

public struct VarRef: Term, CustomStringConvertible {

  public let name: String

  public var description: String {
    "$" + name
  }

  public var toMaude: String {
    let result = "var $\(name) : "
    return result
  }
}
