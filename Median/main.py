import os
import glob
import random

# Təsadüfiləşdirilmiş seçim (Quickselect) alqoritmi vasitəsilə k-cı ən kiçik elementi tapırıq.
# Find the k-th smallest element using the iterative Randomized Select (Quickselect) algorithm.
def randomized_select(arr, k):
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        if left == right:
            return arr[left]
            
        # Dayaq elementi olaraq təsadüfi bir indeks seçirik.
        # Choose a random pivot index.
        pivot_idx = random.randint(left, right)
        arr[pivot_idx], arr[right] = arr[right], arr[pivot_idx]
        pivot = arr[right]
        
        # Lomuto bölümü alqoritmini tətbiq edirik.
        # Apply Lomuto partitioning.
        i = left
        for j in range(left, right):
            if arr[j] <= pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                
        arr[i], arr[right] = arr[right], arr[i]
        
        # Dayaq elementinin mövqeyini təyin edirik.
        # Determine the position of the pivot.
        pos = i - left + 1
        
        # Əgər mövqe axtardığımız k-ya bərabərdirsə, elementi qaytarırıq.
        # If the position equals k, return the element.
        if pos == k:
            return arr[i]
        # Əgər axtardığımız element sol tərəfdədirsə, sağ sərhədi kiçildirik.
        # If the k-th smallest is in the left partition, shrink the right boundary.
        elif k < pos:
            right = i - 1
        # Əks halda, sol sərhədi böyüdürük və axtardığımız sıranı yeniləyirik.
        # Otherwise, expand the left boundary and adjust k.
        else:
            left = i + 1
            k -= pos

# Cari qovluqdakı "rosalind_" ilə başlayan giriş faylını tapırıq.
# Locate the input file starting with "rosalind_" in the current directory.
input_files = glob.glob(os.path.join(os.path.dirname(__file__), 'rosalind_*.txt'))
if not input_files:
    raise FileNotFoundError("Giriş faylı tapılmadı / Input file not found")

# Giriş faylından bütün məlumatları oxuyuruq.
# Read all data from the input file.
with open(input_files[0], 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

# n, massiv və k-nı təyin edirik.
# Parse n, the array A, and k.
n = int(lines[0])
A = list(map(int, lines[1].split()))
k = int(lines[2])

# k-cı ən kiçik elementi tapırıq.
# Find the k-th smallest element.
result = randomized_select(A, k)

# Nəticəni konsolda göstəririk.
# Print the result to the console.
print(result)

# Nəticəni "output.txt" faylına yazırıq.
# Write the result to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(str(result) + '\n')
