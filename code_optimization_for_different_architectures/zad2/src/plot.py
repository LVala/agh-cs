from matplotlib import pyplot as plt

def plot_from_array(array_x, array_y):
    if len(array_x) != len(array_y):
        print("Error: length of arrays are different")
        return

    _, ax = plt.subplots()
    ax.plot(array_x, array_y, color="black", marker=".")  # marker='.'
    plt.xlabel("n")
    plt.ylabel("GFLOPS")

    plt.ylim([0, 8])

    plt.savefig("fig.png")

def results_from_file(filename):
    x = []
    y = []
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            values = line.split() 
            x.append(int(values[0]))
            y.append(float(values[1]))

    return x, y

if __name__ == "__main__":
    x, y = results_from_file("res.txt")
    plot_from_array(x, y)
