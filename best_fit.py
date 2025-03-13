import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Load data from JSON file
with open("data4.json") as file:
    data = json.load(file)
def main():

    # Extract the data for each sorting algorithm
    x = np.array([int(key) for key in data.keys()])
    bubble_sort_y = np.array([value['bubble_sort']["comparisons"] for value in data.values()])
    insertion_sort_y = np.array([value['insertion_sort']["comparisons"] for value in data.values()])
    quick_sort_y = np.array([value['quick_sort']["comparisons"] for value in data.values()])

    # Fit and plot for bubble sort
    determine_best_fit(x, bubble_sort_y, 'Bubble Sort')

    # Fit and plot for insertion sort
    determine_best_fit(x, insertion_sort_y, 'Insertion Sort')

    # Fit and plot for quick sort
    determine_best_fit(x, quick_sort_y, 'Quick Sort')

def main_with_operations():

    x = np.array([int(key) for key in data.keys()])
    bubble_sort_y = np.array([value['bubble_sort']["comparisons"] + value['bubble_sort']["operations"] for value in data.values()])
    insertion_sort_y = np.array([value['insertion_sort']["comparisons"] + value['insertion_sort']["operations"] for value in data.values()])
    quick_sort_y = np.array([value['quick_sort']["comparisons"] + value['quick_sort']["operations"] for value in data.values()])

    determine_best_fit(x, bubble_sort_y, 'Bubble Sort')
    determine_best_fit(x, insertion_sort_y, 'Insertion Sort')
    determine_best_fit(x, quick_sort_y, 'Quick Sort')


# Define different types of equations
def polynomial(x, a, b, c):
    return a * x**2 + b * x + c

def exponential(x, a, b, c):
    return a * np.exp(b * x) + c

def logarithmic(x, a, b, c):
    return a * np.log(b * x) + c

def root(x, a, b, c):
    return a * np.sqrt(b * x) + c

def nlogn(x, a, b, c):
    return a * x * np.log(b * x) + c

# Fit the data to each equation type
def fit_data(x, y, func):
    try:
        popt, _ = curve_fit(func, x, y, maxfev=100000)
        return popt
    except RuntimeError as e:
        print(f"Fit failed: {e}")
        return None

# Calculate R² value
def calculate_r_squared(x, y, func, popt):
    if popt is None:
        return -np.inf
    residuals = y - func(x, *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r_squared = 1 - (ss_res / ss_tot)
    return r_squared

# Plot the data and the best-fit equations
def plot_fit(x, y, func, popt, title):
    if popt is None:
        print(f"Cannot plot {title} because fit failed.")
        return
    plt.scatter(x, y, label='Data')
    plt.plot(x, func(x, *popt), label='Best Fit', color='red')
    plt.title(title)
    plt.xlabel('Input Size')
    plt.ylabel('Time')
    plt.legend()
    #plt.show()

# Determine the best fit and plot for each sorting algorithm
def determine_best_fit(x, y, algorithm_name):
    fits = {
        'Polynomial': polynomial,
        'Exponential': exponential,
        'Logarithmic': logarithmic,
        'Root': root,
        'NLogN': nlogn
    }
    
    best_fit = None
    best_r_squared = -np.inf
    best_popt = None
    best_eq = None
    
    for name, func in fits.items():
        popt = fit_data(x, y, func)
        r_squared = calculate_r_squared(x, y, func, popt)
        equation = format_equation(name, popt)
        
        if r_squared > best_r_squared:
            best_r_squared = r_squared
            best_fit = name
            best_popt = popt
            best_eq = equation
    
    if best_fit is not None:
        print(f"Best fit for {algorithm_name}: {best_fit} with R²: {best_r_squared:.8f}")
        print(f"Equation: {best_eq}")
        print("----------------")
        plot_fit(x, y, fits[best_fit], best_popt, f"{algorithm_name} - {best_fit} Fit")

# Format the equation string
def format_equation(name, popt):
    if popt is None:
        return "Fit failed"
    if name == 'Polynomial':
        return f"{popt[0]:.6f} * x^2 + {popt[1]:.6f} * x + {popt[2]:.6f}"
    elif name == 'Exponential':
        return f"{popt[0]:.6f} * exp({popt[1]:.6f} * x) + {popt[2]:.6f}"
    elif name == 'Logarithmic':
        return f"{popt[0]:.6f} * log({popt[1]:.6f} * x) + {popt[2]:.6f}"
    elif name == 'Root':
        return f"{popt[0]:.6f} * sqrt({popt[1]:.6f} * x) + {popt[2]:.6f}"
    elif name == 'NLogN':
        return f"{popt[0]} * x * log({popt[1]} * x) + {popt[2]}"
    else:
        return "Unknown equation"

# Filter out invalid data points for logarithmic and nlogn fits
def filter_invalid_data(x, y):
    valid_indices = np.where(x > 0)
    return x[valid_indices], y[valid_indices]


main()
main_with_operations()