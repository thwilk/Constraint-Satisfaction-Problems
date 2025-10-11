def parse_input(file_path):
    with open(file_path) as file:
        x = file.readline()
        num_variables, num_constraints, num_colors = x.split()

        # print(num_variables, num_constraints, num_colors)
        constraints = []

        for i, line in enumerate(file):
            x = line.split()
            constraints.append({x[0], x[1]})




    # for c in constraints:
    #     print(c)
    return num_colors, num_constraints, num_variables, constraints

parse_input("input/backtrack_easy")
