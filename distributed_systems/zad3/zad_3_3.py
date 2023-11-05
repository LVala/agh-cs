# 3.3 Take a look on implement parralel Pi computation
# based on https://docs.ray.io/en/master/ray-core/examples/highly_parallel.html
#
# Implement calculating pi as a combination of actor (which keeps the
# state of the progress of calculating pi as it approaches its final value)
# and a task (which computes candidates for pi)

import ray
import time
import random

ray.init(address="auto")

@ray.remote
def pi4_sample(pi_calculator, sample_count: int) -> None:
    in_count = 0
    for _ in range(sample_count):
        x = random.random()
        y = random.random()
        if x*x + y*y <= 1:
            in_count += 1

    pi_calculator.add_sample.remote(in_count, sample_count)

@ray.remote
class PiCalculator:
    def __init__(self) -> None:
        self.numerator = 0
        self.denominator = 0

    def add_sample(self, in_count: int, sample_count: int) -> None:
        self.numerator += in_count 
        self.denominator += sample_count

    def get_cur_pi(self) -> float:
        if (self.denominator) != 0:
            return 4 * self.numerator/self.denominator
        else: 
            return 0

SAMPLE_COUNT = 1_000_000
TASK_COUNT = 1_000

pi_calculator = PiCalculator.remote()
task_refs = [pi4_sample.remote(pi_calculator, SAMPLE_COUNT) for _ in range(TASK_COUNT)]

while True:
    print(ray.get(pi_calculator.get_cur_pi.remote()))
    time.sleep(1)

