import copy
import math
import sys

# MAIN PARSING 
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
domains = []

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


# set up domains 
def initializeDFBSP():
    global domains
    domains = [list(range(no_of_colors)) for _ in range(no_of_variables)] # domains where


#most restricted variable
def mrv():
    most = math.inf
    index = -1
    for i, x  in enumerate(domains):
        if len(x) < most and len(x)!=1:
            most = len(x)
            index = i

    # print(f"mrv = {most}\nindex={index}")
    return index

#least constrained value
def lcv(var):
    
    var_constraints = []


    for (a, b) in constraints: # get all constraints with var
        if a == var or b == var:
            var_constraints.append((a,b))

    color_scores = []

    for color in domains[var]: # for each color in var, minimize inconsisitencys 
        sum = 0
        for (a, b) in var_constraints: 
            other = a if a!= var else b
            if color in domains[other]:
                sum+=1
        color_scores.append((color, sum))

    color_scores.sort(key=lambda x: x[1])

    # print(f"lcv= {inconsistencys}\ncolor_no={color_no}")

    return [color for color, _ in color_scores]

def assign_var(var, color):
    domains[var] = [color]

    to_reduce = []

    for (a, b) in constraints: 
        if a == var:
            to_reduce.append(b)
        if b == var:
            to_reduce.append(a)


    for x in to_reduce:
        updated_domain = list(set(domains[x]) - set([color]))
        if len(updated_domain) == 0:
            return False
        domains[x] = updated_domain

    return True


def check_goal_state():
    for x in domains:
        if len(x) > 1:
            return False
    return True

def dfsb_plus():
    global domains
    if check_goal_state():
        return domains

    var = mrv()  # MRV
    for color in lcv(var):  # LCV order

        old_domains = copy.deepcopy(domains)

        good = assign_var(var, color)
        if good:  
            result = dfsb_plus()
            if result is not None:
                return result

        # backtrack: restore domains
        domains = old_domains

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
    initializeDFBSP()
    solution = dfsb_plus()
    print(solution)
    with open(output_file, "w") as out:
        if solution is None:
            out.write("No answer.\n")
            out.write("No answer.\n")
        else:
            for i in range(no_of_variables):
                out.write(str(solution[i]) + "\n")


