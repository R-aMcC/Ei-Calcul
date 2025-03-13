import json
import matplotlib.pyplot as plt

# JSON data
def main():
    with open("data4.json") as file:
        data = json.load(file)

    # Extracting X and Y values
    x = [int(key) for key in data.keys()]


    bubble = [value["bubble_sort"]["comparisons"] for value in data.values()]
    insertion = [value["insertion_sort"]["comparisons"] for value in data.values()]
    quick = [value["quick_sort"]["comparisons"] for value in data.values()]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(x, bubble, label="Bubble Sort", marker="o")
    plt.plot(x, insertion, label="Insertion Sort", marker="x")
    plt.plot(x, quick, label="Quick Sort", marker="^")

    # Labels and legend
    plt.title("Sorting Algorithms Performance")
    plt.xlabel("Number of Elements")
    plt.ylabel("Number of comparisons")
    plt.legend()
    plt.grid(True)

    # Show plot
    plt.show()


def main_with_operations():
    with open("data4.json") as file:
        data = json.load(file)

    # Extracting X and Y values
    x = [int(key) for key in data.keys()]


    bubble = [value["bubble_sort"]["comparisons"] + value["bubble_sort"]["operations"] for value in data.values()]
    insertion = [value["insertion_sort"]["comparisons"] + value["insertion_sort"]["operations"] for value in data.values()]
    quick = [value["quick_sort"]["comparisons"] + value["quick_sort"]["operations"] for value in data.values()]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(x, bubble, label="Bubble Sort", marker="o")
    plt.plot(x, insertion, label="Insertion Sort", marker="x")
    plt.plot(x, quick, label="Quick Sort", marker="^")

    # Labels and legend
    plt.title("Sorting Algorithms Performance")
    plt.xlabel("Number of Elements")
    plt.ylabel("Number of comparisons")
    plt.legend()
    plt.grid(True)

    # Show plot
    plt.show()


def quick():
    with open("data3.json") as file:
        data = json.load(file)

    x = [int(key) for key in data.keys()]
    quick = [value["quick_sort"] for value in data.values()]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(x, quick, label="Quick Sort", marker="^")

    # Labels and legend
    plt.title("Sorting Algorithms Performance")
    plt.xlabel("Number of Elements")
    plt.ylabel("Time (Seconds)")
    plt.legend()
    plt.grid(True)

    # Show plot
    plt.show()


main_with_operations()