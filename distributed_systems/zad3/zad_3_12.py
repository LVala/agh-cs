# excercise 3
# 3.0 start remote cluster settings and observe actors in cluster
# a) make screenshot of dependencies
# 3.1. Modify the Actor class MethodStateCounter and add/modify methods that return the following:
# a) - Get number of times an invoker name was called
# b) - Get a list of values computed by invoker name
# 3- Get state of all invokers

# 3.2 Modify method invoke to return a random int value between [5, 25]

import ray
import random
import time

# exercise 3.{1, 2}
ray.init(address="auto")

CALLERS=["A","B","C"]

@ray.remote
class MethodStateCounter :
    def __init__(self) :
        self.invokers_count = {i: 0 for i in CALLERS}
        self.invokers_results = {i: [] for i in CALLERS}

    def invoke(self,name) :
        time.sleep(0.5)
        self.invokers_count[name]+=1
        value = random.randint(5, 25)
        self.invokers_results[name].append(value)
        return value

    def get_invoker_count(self,name) :
        return self.invokers_count[name]

    def get_invoker_results(self, name):
        return self.invokers_results[name]

    def get_all_invoker_count(self) :
        return self.invokers_count
    
    def get_all_invoker_results(self):
        return self.invokers_results

worker_invoker = MethodStateCounter.remote()
print(worker_invoker)

for _ in range(10):
    name = random.choice(CALLERS)
    worker_invoker.invoke.remote(name)

print('method callers')
for _ in range(5):
    random_name_invoker = random.choice(CALLERS)
    times_invoked = ray.get(worker_invoker.invoke.remote(random_name_invoker))
    print(f"Named caller: {random_name_invoker} called {times_invoked}")

print(ray.get(worker_invoker.get_all_invoker_results.remote()))
