import sys

"""
Output:
- On success: writes the color for each variable (0..K-1), one per line.
- On failure (no solution found): "No answer."

"""
if len(sys.argv) != 4:
    sys.stderr.write(" python dfsb.py <INPUT FILE> <OUTPUT FILE> <MODE FLAG>")
    sys.exit(2)

input_file = sys.argv[1]
output_file = sys.argv[2]
try:
    mode = int(sys.argv[3])
except ValueError:
    sys.stderr.write("MODE FLAG must be an integer")
    sys.exit(2)


# problem definition
no_of_variables = None
no_of_constraints = None
no_of_colors = None
constraints = []  # list of [a, b] pairs

with open(input_file, 'r') as f:
    first = f.readline().split()
    no_of_variables = int(first[0])
    no_of_constraints = int(first[1])
    no_of_colors = int(first[2])
    for line in f:
        a, b = map(int, line.split())
        constraints.append((a, b))

# DFS-B (backtracking)
def consistent(var, val, assignment):
    # Check if assigning var=val is consistent with current partial assignment
    # Only check constraints where both ends are assigned (including the proposed var)
    for (a, b) in constraints:
        x = assignment.get(a, None) if a != var else val
        y = assignment.get(b, None) if b != var else val
        if x is not None and y is not None and x == y:
            return False
    return True

def dfs_backtrack(assignment):
     # recursive backtracking on variables in index order (0..N-1)
    if len(assignment) == no_of_variables:
        return assignment
    var = len(assignment)  # next variable by index order
    for val in range(no_of_colors):
        if consistent(var, val, assignment):
            assignment[var] = val
            res = dfs_backtrack(assignment)
            if res is not None:
                return res
            # backtrack
            del assignment[var]
    return None


# mode 0 dfsb
if mode == 0:
    solution = dfs_backtrack({})
    with open(output_file, "w") as out:
        if solution is None:
            out.write("No answer.\n")
        else:
            for i in range(no_of_variables):
                out.write(str(solution[i]) + "\n")

# mode 1 dfsb++  You should implement here
else:

    sys.stderr.write("MODE=1 (DFS-B++) is intentionally not included in this starter. Please implement it. You can comment out this line\n")
