# Question: Compute maximum-size antichain of S = {0, 1, 2, 3, 4} by satisfying the definition of antichain for the given set S.
# Model S as an EnumSort, the subsets A as a list of 10 uninterpreted functions of type S -> Bool.

from z3 import *

S, SSet = EnumSort('S', [str(i) for i in range(5)])

a = Const('a', S)

A = [Function('A' + str(i), S, BoolSort()) for i in range(10)]

# Create the solver
s = Solver()

# Verify that A is an antichain
# A is an antichain if for all i, j in A, for each pair of functions A[i] and A[j] you can find an element s of S such that A[i](s) is true and A[j](s) is false, and vice versa. 

for i in range(10):
    for j in range(i + 1, 10):
        sentence = And(Exists([a], And(A[i](a), Not(A[j](a)))), Exists([a], And(A[j](a), Not(A[i](a)))))
        s.add(sentence)

# Check the satisfiability
if s.check() == sat:
    m = s.model()
    print(m)
    # evaluate the model for each function in A and print the result
    for i in range(10):
        print(m.evaluate(A[i](a)))
else:
    print("Unsatisfiable, Couldn't find the maximum-size antichain")
