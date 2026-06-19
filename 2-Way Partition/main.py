import os
import glob

# Cari qovluqdakı "rosalind_" ilə başlayan giriş faylını tapırıq.
# Locate the input file starting with "rosalind_" in the current directory.
input_files = glob.glob(os.path.join(os.path.dirname(__file__), 'rosalind_*.txt'))
if not input_files:
    raise FileNotFoundError("Giriş faylı tapılmadı / Input file not found")

# Giriş faylından məlumatları oxuyuruq.
# Read data from the input file.
with open(input_files[0], 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

# n-i və massivi təyin edirik.
# Parse n and the array A.
n = int(lines[0])
A = list(map(int, lines[1].split()))

# 2-Way Partition (pivot ətrafında bölmə) alqoritmi.
# 2-Way Partition (partition around a pivot) algorithm.
def partition(arr):
    # Pivot olaraq massivin ilk elementini seçirik.
    # Choose the first element of the array as the pivot.
    pivot = arr[0]
    q = 0
    
    # Massivin qalan elementlərini pivot ilə müqayisə edirik.
    # Compare the remaining elements of the array with the pivot.
    for i in range(1, len(arr)):
        if arr[i] <= pivot:
            q += 1
            # Pivot-dan kiçik və ya bərabər olan elementləri qabağa keçiririk.
            # Swap elements smaller than or equal to pivot to the front.
            arr[i], arr[q] = arr[q], arr[i]
            
    # Pivot-u öz düzgün yerinə (q indeksinə) yerləşdiririk.
    # Place the pivot at its correct position (index q).
    arr[0], arr[q] = arr[q], arr[0]
    return arr

# Massivi pivot ətrafında bölürük.
# Partition the array around the pivot.
partition(A)

# Nəticəni boşluqla ayrılmış şəkildə birləşdiririk.
# Join the partitioned elements with spaces.
output_data = ' '.join(map(str, A))

# Nəticəni konsolda göstəririk.
# Print the results to the console.
print(output_data[:100] + "...")

# Nəticəni "output.txt" faylına yazırıq.
# Write the results to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(output_data + '\n')
