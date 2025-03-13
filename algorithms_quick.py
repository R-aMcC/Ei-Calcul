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
    gauche_srt, gauche_c, gauche_d = quick_sort(gauche, c, d)
    droite_srt, droite_c, droite_d = quick_sort(droite, c, d)
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

def sort_and_time(times_quick, lock, amount, pause_event):
    try:
        unsorted = [random.randint(0, 10000) for _ in range(amount)]
        # Quick Sort
        cpu_start = time.process_time()
        quick_sort(unsorted.copy())
        cpu_end = time.process_time()
        with lock:
            times_quick.append(cpu_end - cpu_start)

        # Check for pause event after each sort
        if pause_event.is_set():
            while pause_event.is_set():
                time.sleep(0.1)

    except Exception as e:
        print(f"Error: {e}")

averages_bubble = []
averages_insertion = []
averages_quick = []

def new(pause_event):
    try:
        with open("data3.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    for i in range(0, 2001):
        for j in range(5):
            manager = multiprocessing.Manager()
            times_quick = manager.list()

            lock = multiprocessing.Lock()  # Ensures safe data updates

            processes = []

            for _ in range(10):
                process = multiprocessing.Process(target=sort_and_time, args=(times_quick, lock, i*1000, pause_event))
                processes.append(process)
                process.start()
            
            for process in processes:
                process.join()
            
            averages_quick.append(sum(times_quick) / len(times_quick))
            
            if pause_event.is_set():
                print("Batch paused. Press 'r' to resume.")
                while pause_event.is_set():
                    time.sleep(0.1)

        data[f"{i*1000}"] = {
            "quick_sort": sum(averages_quick) / len(averages_quick)
        }
        print(f"{datetime.datetime.now()}: Successfully executed with {i*1000} elements")
        with open("data3.json", "w") as file:
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