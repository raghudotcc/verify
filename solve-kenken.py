"""
Problem: Calkuro Puzzle
Description:
    You are given a puzzle with grids of squares. Some filled in, some empty.
    You are to fill in the empty squares. Similar to sudoku in that
    you can only place one number in each square and it must be unique
    in the row and column. Additionally, the puzzle also has something called
    a cage. A cage is a group of squares that are connected by a dark solid 
    line, and a cell in that cage will have a number or a constraint on it 
    that needs to be satisfied.
"""
from z3 import *


# Initialize the puzzle with 4x4 grid.
X = [[Int('x_%d%d' % (i, j)) for j in range(4)] for i in range(4)]

# Make sure that the values in each cell are between 1 and 4
cells_c = [And(1 <= X[i][j], X[i][j] <= 4) for i in range(4) for j in range(4)]

# make sure that the values in each row are unique
rows_c = [Distinct(X[i]) for i in range(4)]

# make sure that the values in each column are unique
cols_c = [Distinct([X[i][j] for i in range(4)]) for j in range(4)]

# cage1 consists of cells (0, 0) and (1, 0)
# the ratio of the elements in cage1 should be 2:1
cage1_c = [X[1][0] / X[0][0] == 2]

# cage2 consists of cells (0, 1), (0, 2) and (1, 1)
# the sum of the elements in cage2 should be 8
cage2_c = [X[0][1] + X[0][2] + X[1][1] == 8]

# cage3 consists of cells (0, 3)
# the element in the cage should be 1
cage3_c = [X[0][3] == 1]

# cage4 consists of cells (2, 0), (3, 0), and (3, 1)
# the product of the elements in the cage should be 6
cage4_c = [X[2][0] * X[3][0] * X[3][1] == 6]

# cage 5 consists of cells (1, 2)
# the element in the cage should be 2
cage5_c = [X[1][2] == 2]

# cage 6 consists of cells (1, 3), (2, 2), and (2, 3)
# the product of the elements in the cage should be 24
cage6_c = [X[1][3] * X[2][2] * X[2][3] == 24]

# cage 7 consists of cells (2, 1)
# the element in the cage should be 3
cage7_c = [X[2][1] == 3]

# cage 8 consists of cells (3, 2), (3, 3)
# the difference of the elements in the cage should be 3
cage8_c = [X[3][3] - X[3][2] == 3]

# collect all the constraints
calkuro_c = cells_c + rows_c + cols_c + cage1_c + cage2_c + \
    cage3_c + cage4_c + cage5_c + cage6_c + cage7_c + cage8_c

# create a base instance of the puzzle
instance = ((0, 0, 0, 1),
            (0, 0, 2, 0),
            (0, 3, 0, 0),
            (0, 0, 0, 0))

# if a cell in the instance is 0, then we don't care about its value
# as we will try to verify that later on using the calkuro_c constraints
# so just set it to True. Otherwise, the value in X[i][j] should be equal to
# the value in the instance[i][j]
# If-then-else in Z3 is a constraint i.e., if true, then 
# then the second expression should be true, otherwise the third expression 
# should be true
instance_c = [If(instance[i][j] == 0, True, X[i][j] == instance[i][j])
              for i in range(4) for j in range(4)]
s = Solver()

s.add(calkuro_c + instance_c)
if s.check() == sat:
    m = s.model()
    r = [[m.evaluate(X[i][j]) for j in range(4)] for i in range(4)]
    print("The puzzle is solvable")
    print("Solution:")
    [print("Row %d: %s" % (i, r[i])) for i in range(4)]
else:
    print("Failed to solve the puzzle")
