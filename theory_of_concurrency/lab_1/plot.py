import matplotlib.pyplot as plt

values = []

with open("results.txt", "r") as file:
    for line in file:
            values.append(int(line))

fig, ax = plt.subplots()
ax.hist(values, bins=[i for i in range(-1000, 6500, 100)])

plt.ylabel("Liczba wyników")
plt.show()