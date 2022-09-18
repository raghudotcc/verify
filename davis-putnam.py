from ast import *
import ast

class Not(AST):
  def __init__(self, operand):
    self.operand = operand
    self._fields = ['operand']

  def getChildren(self):
    return [self.operand]

  def getChildNodes(self):
    return [self.operand]

  def __repr__(self):
    return "¬%s" % repr(self.operand)


class And(AST):
  def __init__(self, args):
    self.args = args
    self._fields = ['args']

  def getChildren(self):
    return self.args

  def getChildNodes(self):
    return self.args

  def __repr__(self):
    return " ∧ ".join(["(%s)" % repr(arg) for arg in self.args])


class Or(AST):
  def __init__(self, args):
    self.args = args
    self._fields = ['args']

  def getChildren(self):
    return self.args

  def getChildNodes(self):
    return self.args

  def __repr__(self):
    return " ∨ ".join([repr(arg) for arg in self.args])


class Variable(AST):
  def __init__(self, name):
    self.name = name
    self._fields = ['name']

  def getChildren(self):
    return []

  def getChildNodes(self):
    return []

  def __repr__(self):
    return "%s" % repr(self.name)


def get_unique_variables(S):
    variables = []
    for clause in S:
        for node in ast.walk(clause):
            if isinstance(node, Variable):
                variables.append(node.name)
    return set(variables)

def remove_tautologies(S):
    '''
    for each clause in S, select only clauses that do not contain a variable and its negation
    '''
    new_S = []
    tautology = False
    for clause in S:
        variables = clause.args
        for variable in variables:
          if isinstance(variable, Not):
            for var in variables:
              if isinstance(var, Variable) and var.name == variable.operand.name:
                tautology = True
                break
        if not tautology:
          new_S.append(clause)
        tautology = False
    return new_S

def include_var_in_clause(S, varname):
    # get all the clauses that contain var or its negation or both
    new_J = []
    for clause in S:
      variables = clause.args
      for variable in variables:
        if isinstance(variable, Variable) and variable.name == varname:
          new_J.append(clause)
          break
        elif isinstance(variable, Not) and variable.operand.name == varname:
          new_J.append(clause)
          break
    return new_J

def compute_resolvents(J, varname):
    # for each clause in J, compare it with remaining clauses in J
    # if the variable in clause1 has a negation in clause2, then
    # remove the variable and its negation from both clause and
    # create a new clause by combining the remaining variables
    # from both clauses
    resolvents = []
    for i in range(len(J)):
      clause1 = J[i]
      for j in range(i+1, len(J)):
        clause2 = J[j]
        for var1 in clause1.args:
          if isinstance(var1, Variable) and var1.name == varname:
            for var2 in clause2.args:
              if isinstance(var2, Not) and var2.operand.name == varname:
                # remove all instances of var1 and var2 from clause1 and clause2
                # and create a new clause by combining the remaining variables
                # from both clauses
                new_clause = []
                for var in clause1.args:
                  if (isinstance(var, Variable) and var.name != varname) or (isinstance(var, Not) and var.operand.name != varname):
                    new_clause.append(var)
                for var in clause2.args:
                  if (isinstance(var, Variable) and var.name != varname) or (isinstance(var, Not) and var.operand.name != varname):
                    new_clause.append(var)
                resolvents.append(Or(new_clause))
    return resolvents

def get_next_S(Sprime, J, U):
    '''
    Remove the clause in J from Sprime and add the resolvents in U
    '''
    next_S = []
    for clause in Sprime:
      if clause not in J:
        next_S.append(clause)
    for clause in U:
      next_S.append(clause)
    return next_S
    

def resolution_proof(S0):
    variables = list(get_unique_variables(S0))
    variables.sort()
    S = [None] * (len(variables) + 1) # Create a list of length n
    Sprime = [None] * len(variables) 
    J = [None] * len(variables) 
    U = [None] * len(variables) 
    S[0] = S0
    n = len(variables)
    for i in range(n):
      # Remove tautologies
      print("Current variable: %s" % variables[i])
      print("S[%d] = %s" % (i, S[i]))
      Sprime[i] = remove_tautologies(S[i])
      # print("S'[%d] = %s" % (i, Sprime[i]))
      J[i] = include_var_in_clause(Sprime[i], variables[i])
      # print("J[%d] = %s" % (i, J[i]))
      # compute resolvents
      U[i] = compute_resolvents(J[i], variables[i])
      # print("U[%d] = %s" % (i, U[i]))
      if (i+1) < n:
        S[i+1] = get_next_S(Sprime[i], J[i], U[i])
        # print("S[%d] = %s" % (i+1, S[i+1]))
      else:
        S[i + 1] = S[i]
    return S[n-1]


def de_and(Sentence):
    if isinstance(Sentence, And):
        return Sentence.args
    else:
        return [Sentence]



# Example 1: (¬a ∨ ¬b) ∧ (a ∨ c) ∧ (b ∨ c) ∧ (a ∨ ¬b ∨ ¬d) ∧ (b ∨ d) ∧ (b ∨ ¬c ∨ ¬d)

# d1 = Or([Not(Variable('a')), Not(Variable('b')), Variable('a')])

# d2 = Or([Variable('a'), Variable('c')])

# d3 = Or([Variable('b'), Variable('c')])

# d4 = Or([Variable('a'), Not(Variable('b')), Not(Variable('d'))])

# d5 = Or([Variable('b'), Variable('d')])

# d6 = Or([Variable('b'), Not(Variable('c')), Not(Variable('d'))])

# c1 = And([d1, d2, d3, d4, d5, d6])

# S = de_and(c1)

# Example 2: (¬a ∨ ¬b ∨ c) ∧ (a ∨ b ∨ c) ∧ (¬c ∨ d) ∧ (¬c ∨ ¬d) ∧ (¬a ∨ c ∨ d) ∧ (¬a ∨ b ∨ ¬d) ∧ (b ∨ c ∨ ¬d) ∧ (a ∨ b ∨ d)

# Example from the book

d1 = Or([Not(Variable('a')), Not(Variable('b')), Variable('c')])

d2 = Or([Variable('a'), Variable('b'), Variable('c')])

d3 = Or([Not(Variable('c')), Variable('d')])

d4 = Or([Not(Variable('c')), Not(Variable('d'))])

d5 = Or([Not(Variable('a')), Variable('c'), Variable('d')])

d6 = Or([Not(Variable('a')), Variable('b'), Not(Variable('d'))])

d7 = Or([Variable('b'), Variable('c'), Not(Variable('d'))])

d8 = Or([Variable('a'), Variable('b'), Variable('d')])

c1 = And([d1, d2, d3, d4, d5, d6, d7, d8])

S = de_and(c1)

print("CNF: ", c1)
print("Original Set of Clauses: ", (S))
print(resolution_proof(S))
        
