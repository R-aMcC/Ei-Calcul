import sys
import time
import random

sys.setrecursionlimit(100000)

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


time1 = time.process_time()
quick_sort([random.randint(0, 10000) for _ in range(35700)])
time2 = time.process_time()
print(f"Time for bubble sort: {time2 - time1}")



#def quick_sort_all(start, end):
