import time
import random
import json
import sys
import multiprocessing
import datetime
import keyboard
import pygetwindow as gw

sys.setrecursionlimit(100000)

pause_event = multiprocessing.Event()  # Create an event for pausing
""" Original algorithms without calculation for number of operations
def bubble_sort(arr): # O(n^2)
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def insertion_sort(arr): # O(n^2)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr

def quick_sort(arr): # O(n log n)
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    gauche = [x for x in arr if x < pivot]
    droite = [x for x in arr if x > pivot]
    return quick_sort(gauche) + [x for x in arr if x == pivot] + quick_sort(droite)
"""

def bubble_sort(arr): # O(n^2)
    c = 0
    d = 0
    n = len(arr)
    d += 1
    for i in range(n):
        for j in range(0, n-i-1):
            c += 1
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                c += 1
    return arr, c, d

def insertion_sort(arr): # O(n^2)
    c = 0
    d = 0
    for i in range(1, len(arr)):
        key = arr[i]
        c+=1
        j = i-1
        d+=1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            c+=1
            j -= 1
            d+=1
        arr[j+1] = key
        c+=1
    d+=1
    return arr, c, d

def quick_sort(arr): # O(n log n)
    c=0
    d=1
    if len(arr) <= 1: # 1
        d += 1
        return arr, c, d
    pivot = arr[len(arr) // 2] # 1
    d += 1
    gauche = []
    droite = []
    mid = []
    for x in arr:
        if(x < pivot):
            c+=1
            gauche.append(x)
            c+=1
        elif(x > pivot):
            c+=1
            droite.append(x)
            c+=1
        else:
            mid.append(x)
            c+=1
    gauche_srt, gauche_c, gauche_d = quick_sort(gauche)
    droite_srt, droite_c, droite_d = quick_sort(droite)
    d+=1
    return gauche_srt + mid + droite_srt, gauche_c + droite_c + c, gauche_d + droite_d + d




def check_pause(pause_event):
    while True:
        active_window = gw.getActiveWindow()
        if active_window and 'powershell' in active_window.title.lower():
            if keyboard.is_pressed('p'):
                pause_event.set()
                print("Paused. Press 'r' to resume.")
                while True:
                    active_window = gw.getActiveWindow()
                    if(keyboard.is_pressed('r') and active_window and 'powershell' in active_window.title.lower()): 
                        break
                    else:
                        time.sleep(0.1)
                pause_event.clear()
                print("Resumed.")
        time.sleep(0.1)

def sort_and_time(times_bubble, times_insertion, times_quick, lock, amount, pause_event):
    try:
        unsorted = [random.randint(0, 10000) for _ in range(amount)]

        # Bubble Sort
        cpu_start = time.perf_counter()
        bubble_arr, bubble_c, bubble_d = bubble_sort(unsorted.copy())
        cpu_end = time.perf_counter()
        with lock:
            if "times" not in times_bubble:
                times_bubble["times"] = [cpu_end - cpu_start]
                times_bubble["comparisons"] = [bubble_c]
                times_bubble["operations"] = [bubble_d]
            else:
                times_bubble["times"].append(cpu_end - cpu_start)
                times_bubble["comparisons"].append(bubble_c)
                times_bubble["operations"].append(bubble_d)

        # Insertion Sort
        cpu_start = time.perf_counter()
        ins_arr, ins_c, ins_d =insertion_sort(unsorted.copy())
        cpu_end = time.perf_counter()
        with lock:
            if "times" not in times_insertion:
                times_insertion["times"] = [cpu_end - cpu_start]
                times_insertion["comparisons"] = [ins_c]
                times_insertion["operations"] = [ins_d]
            else:
                times_insertion["times"].append(cpu_end - cpu_start)
                times_insertion["comparisons"].append(ins_c)
                times_insertion["operations"].append(ins_d)

        # Quick Sort
        cpu_start = time.perf_counter()
        quick_arr, quick_c, quick_d = quick_sort(unsorted.copy())
        cpu_end = time.perf_counter()
        with lock:
            if "times" not in times_quick:
                times_quick["times"] = [cpu_end - cpu_start]
                times_quick["comparisons"] = [quick_c]
                times_quick["operations"] = [quick_d]
            else:
                times_quick["times"].append(cpu_end - cpu_start)
                times_quick["comparisons"].append(quick_c)
                times_quick["operations"].append(quick_d)

        # Check for pause event after each sort
        if pause_event.is_set():
            while pause_event.is_set():
                time.sleep(0.1)
    except Exception as e:
        print(f"Error: {e}")

averages_data_bubble = {}
averages_data_insertion = {}
averages_data_quick = {}

def new(pause_event):
    try:
        with open("data4.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    for i in range(1, 2001):
        for j in range(5):
            manager = multiprocessing.Manager()
            times_data_bubble = manager.dict()
            times_data_insertion = manager.dict()
            times_data_quick = manager.dict()

            lock = multiprocessing.Lock()  # Ensures safe data updates

            processes = []

            for _ in range(10):
                process = multiprocessing.Process(target=sort_and_time, args=(times_data_bubble, times_data_insertion, times_data_quick, lock, i*100, pause_event))
                processes.append(process)
                process.start()
            
            for process in processes:
                process.join()
            
            for key, value in times_data_bubble.items():
                if key not in averages_data_bubble:
                    averages_data_bubble[key] = [sum(value) / len(value)]
                else:
                    averages_data_bubble[key].append(sum(value) / len(value))
            for key, value in times_data_insertion.items():
                if key not in averages_data_insertion:
                    averages_data_insertion[key] = [sum(value) / len(value)]
                else:
                    averages_data_insertion[key].append(sum(value) / len(value))
            for key, value in times_data_quick.items():
                if key not in averages_data_quick:
                    averages_data_quick[key] = [sum(value) / len(value)]
                else:
                    averages_data_quick[key].append(sum(value) / len(value))
            

                

            
            if pause_event.is_set():
                print("Batch paused. Press 'r' to resume.")
                while pause_event.is_set():
                    time.sleep(0.1)


        data[f"{i*100}"] = {
            "bubble_sort": {
                "times": sum(averages_data_bubble["times"])/len(averages_data_bubble["times"]),
                "comparisons" : sum(averages_data_bubble["comparisons"])/len(averages_data_bubble["comparisons"]),
                "operations" : sum(averages_data_bubble["operations"])/len(averages_data_bubble["operations"])
            },
            "insertion_sort": {
                "times": sum(averages_data_insertion["times"]) / len(averages_data_insertion["times"]),
                "comparisons": sum(averages_data_insertion["comparisons"]) / len(averages_data_insertion["comparisons"]),
                "operations": sum(averages_data_insertion["operations"]) / len(averages_data_insertion["operations"])                   
            },
             "quick_sort": {
                "times": sum(averages_data_quick["times"]) / len(averages_data_quick["times"]),
                "comparisons": sum(averages_data_quick["comparisons"]) / len(averages_data_quick["comparisons"]),
                "operations": sum(averages_data_quick["operations"]) / len(averages_data_quick["operations"])                   
            }
        }
        print(f"{datetime.datetime.now()}: Successfully executed with {i*100} elements")
        with open("data4.json", "w") as file:
            json.dump(data, file, indent=4)

        # Check for pause event after each batch of 10 runs
        if pause_event.is_set():
            print("Batch paused. Press 'r' to resume.")
            while pause_event.is_set():
                time.sleep(0.1)

if __name__ == "__main__":
    pause_thread = multiprocessing.Process(target=check_pause, args=(pause_event,))
    pause_thread.start()
    new(pause_event)
    pause_thread.terminate()