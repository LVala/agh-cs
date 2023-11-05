# Excercises 2.1) Create large lists and python dictionaries,
# put them in object store. Write a Ray task to process them.
import ray
import cProfile

ray.init(address="auto")

huge_list = [i for i in range(100_000)]
huge_dict = {i: str(i)*5 for i in range(100_000)}

huge_list_ref = ray.put(huge_list)
huge_dict_ref = ray.put(huge_dict)

@ray.remote
def process_list(lst):
    new = [i*i for i in lst]
    print(new)
    return new

@ray.remote
def process_dict(dct):
    new = {k: int(v) + 1 for k, v in dct.items()}
    print(new)
    return new

print("start processing the list...")
# cProfile.run("process_list.remote(huge_list)")
print("start processing the dics...")
# cProfile.run("process_dict.remote(huge_dict)")

dict_with_lists = {i: ray.put([i for _ in range(100)]) for i in range(10)}

@ray.remote
def process_dict_with_lists(dwl):
    new = {k: [j*j for j in ray.get(v)] for k, v in dwl.items()}
    print(new)
    return new

process_dict_with_lists.remote(dict_with_lists)
