# basic Adaptive Large Neighborhood Search for MiniZinc
# made by Mateusz Ślayński for the teaching purposes
from minizinc import Instance, Model, Solver
import random
import time

problem_path = "data/eil51.dzn"
init_model_path = "tsp_init.mzn"
improve_model_path = "tsp_improve.mzn"
# how many variables should be relaxed 
initial_zeroing_rate = 0.1
# how much zeroing rate should increase when there is no progress
adaption_rate = 0.05
# after what should we increase/adapt the zeroing rate
timelimit = 10

zeroing_rate = initial_zeroing_rate

# we use MiniZinc library to get the gecode solver
gecode = Solver.lookup("gecode")

def initial_solution():
    '''
    Finds the initial solution
    Returns tuple (route, distance)
    '''
    initial_model = Model()
    initial_model.add_file(init_model_path)
    initial_model.add_file(problem_path)

    initial_instance = Instance(gecode, initial_model)
    res = initial_instance.solve()
    return res["route"], res["total_distance"]


# we use MiniZinc library to create the improving model for given data instance
improve_model = Model()
improve_model.add_file(improve_model_path)
improve_model.add_file(problem_path)
improve_instance = Instance(gecode, improve_model)

def create_fixed_part(solution, rate):
    '''
    This function should relax random {rate}% of the solution.
    Solution is just a list of numbers.
    We just have to create a new list where random {rate}% of the numbers are zeros!
    '''
    fixed_solution = solution.copy()
    # TODO:
    # - set random part of the fixed_solution to zeros!
    elems_to_remove = len(solution) * rate
    while elems_to_remove > 0:
        rnd_index = random.randrange(1,len(solution))
        if (fixed_solution[rnd_index] != 0):
            fixed_solution[rnd_index] = 0
            elems_to_remove -= 1
            
    return fixed_solution

def improve_solution(solution, rate):
    '''
    This function improves the given solution.
    '''
    fixed_solution = create_fixed_part(solution, rate)
    # the branch method creates a new "copy of the model"
    with improve_instance.branch() as opt:
        # then we set the initial_route
        opt["initial_route"] = fixed_solution
        res = opt.solve()
        return res["route"], res.objective

# just to calculate how much time we spent on the optimization
checkpoint = time.time()
# we get the initial solution and mark it as the best
best_solution, best_obj = initial_solution()

# the LNS loop, so exciting
while True:
    # we improve the the current solution
    new_solution, new_obj = improve_solution(best_solution, zeroing_rate)

    # if it's better than the old one
    if new_obj < best_obj:
        checkpoint = time.time()
        # we reset the zeroing rate
        zeroing_rate = initial_zeroing_rate
        # we remember the best solution
        best_solution = new_solution
        best_obj = new_obj
        # and print it
        print(f"- distance: {best_obj}")
        print(f"- route: {best_solution}")
        print("-----------------------")

    # if the solver struggles we increase the zeroing rate :)
    if time.time() - checkpoint > timelimit:
        checkpoint = time.time()
        zeroing_rate += adaption_rate
        print(f"* changed zeroing rate to {zeroing_rate}")
