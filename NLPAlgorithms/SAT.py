import numpy as np
from pysat.solvers import Glucose3def get_colors(assignments):
    all_colors = np.array(['red', 'green', 'blue'])
    colors = {}
    for v in range(n):
    colors[v+1] = all_colors[[assignments[v]>0, \
          assignments[n+v]>0, assignments[2*n+v]>0]][0]
    return colorsdef print_clauses(clauses):
    for c in clauses:
    vars = []
    for v in c:
           vars.append('{}x{}'.format('¬' if v < 0 else '', abs(v)))
    print('(' + ' OR '.join(vars) + ')')
         
def print_SAT_solution(assignments):
    sol = ''
    for x in assignments:
    sol += 'x{}={} '.format(abs(x),x>0)
    print(sol)
     
def solve_graph_coloring():
    # encode the input graph into SAT formula
    n_clauses = 3*m+n
    n_vars = 3*n
    clauses = []
    for u, v in edges:
    clauses.append((-u, -v)) # corresponding to red color
    clauses.append((-(n+u), -(n+v))) # corresponding to green 
    clauses.append((-(2*n+u), -(2*n+v))) # corresponds to blue
    for v in range(1, n+1):
        clauses.append((v, n+v, 2*n+v)) # at least one color
    print_clauses(clauses)
    # solve SAT and obtain solution in terms of variable assignments
    g = Glucose3()
    for c in clauses:
        g.add_clause(c)
    status = g.solve()
    assignments = g.get_model()
    print(status)
    print_SAT_solution(assignments)
    # use the solution assignment by SAT to color the graph
    colors = get_colors(assignments)
    print(colors)
