import tracemalloc
import time
import random
import sys

if len(sys.argv) != 4:
    sys.stderr.write("python minconflicts.py <INPUT FILE> <OUTPUT FILE> <MODE FLAG>")
    sys.exit(2)

input_file = sys.argv[1]
output_file = sys.argv[2]
try:
    mode = int(sys.argv[3])
except ValueError:
    sys.stderr.write("MODE FLAG must be integer")
    sys.exit(2)

# read input
with open(input_file, 'r') as f:
    first_line = list(map(int, f.readline().split()))
    N, M, K = first_line
    edges = [tuple(map(int, line.split())) for line in f]

# build neighbor graph
neighbors = {i: [] for i in range(N)}
for a, b in edges:
    neighbors[a].append(b)
    neighbors[b].append(a)

counter = 0  # track conflict checks like in your second script


def conflicting_vars(assign):
    # return list of variables currently in conflict
    bad = []
    for i in range(N):
        value = assign[i]
        for j in neighbors[i]:
            if value == assign[j]:
                if i not in bad:
                    bad.append(i)
                if j not in bad:
                    bad.append(j)
    return bad


def min_conflict_color(var, assign):
    # return color (0..K-1) minimizing conflicts for variable var
    global counter
    current_color = assign[var]
    min_conflicts = N
    min_conflict_color = current_color

    for color in range(K):
        counter += 1
        if color == current_color:
            continue
        count = 0
        for j in neighbors[var]:
            if color == assign[j]:
                count += 1
        if count < min_conflicts:
            min_conflicts = count
            min_conflict_color = color
    assign[var] = min_conflict_color
    return assign


def min_conflicts_basic(max_steps=500000):
    global counter
    assign = [random.randint(0, K - 1) for _ in range(N)]
    steps_taken = 0

    for step in range(max_steps):
        steps_taken += 1
        bad = conflicting_vars(assign)
        if len(bad) == 0:
            return assign, steps_taken

        var = random.choice(bad)
        assign = min_conflict_color(var, assign)

    return None, steps_taken


def split_into_steps(num, groups):
    x = num / groups
    remainder = num % groups
    steps = [int(x)] * groups
    steps[-1] += remainder
    return steps


def min_conflicts_random_restarts():
    total_allowed_runs = M**3
    num_restarts = random.randint(10, 20)
    max_steps_list = split_into_steps(total_allowed_runs, num_restarts)
    total_steps = 0

    for i, x in enumerate(max_steps_list):
        print("step ", i)
        solution, steps = min_conflicts_basic(max_steps=x)
        total_steps += steps
        if solution:
            print(True)
            return solution, total_steps
    return None, total_steps


# mode 0 MCRS
if mode == 0:
    tracemalloc.start()
    start_time = time.perf_counter()
    solution, steps = min_conflicts_basic()
    current, peak = tracemalloc.get_traced_memory()
    end_time = time.perf_counter()
    tracemalloc.stop()

    print(f"steps taken: {steps}")
    print(f"time: {end_time - start_time}")
    print(f"peak memory: {peak}")
    print(f"conflict checks: {counter}")

    with open(output_file, "w") as out:
        if solution is None:
            out.write("No answer.\n")
        else:
            for val in solution:
                out.write(str(val) + "\n")

# mode 1 MCRS with restart
else:
    tracemalloc.start()
    start_time = time.perf_counter()
    solution, steps = min_conflicts_random_restarts()
    current, peak = tracemalloc.get_traced_memory()
    end_time = time.perf_counter()
    tracemalloc.stop()

    print(f"steps taken: {steps}")
    print(f"time: {end_time - start_time}")
    print(f"peak memory: {peak}")
    print(f"conflict checks: {counter}")

    with open(output_file, "w") as out:
        if solution is None:
            out.write("No answer.\n")
        else:
            for val in solution:
                out.write(str(val) + "\n")