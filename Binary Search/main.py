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

# n, m və massivləri təyin edirik.
# Parse n, m, and the arrays.
n = int(lines[0])
m = int(lines[1])
arr = list(map(int, lines[2].split()))
queries = list(map(int, lines[3].split()))

# İkili axtarış (Binary Search) alqoritmi.
# Binary Search algorithm implementation.
def binary_search(array, target):
    left = 0
    right = len(array) - 1
    while left <= right:
        mid = (left + right) // 2
        if array[mid] == target:
            return mid + 1  # 1-əsaslı indeks qaytarırıq (1-based index)
        elif array[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Hər bir sorğu üçün axtarış edib nəticələri toplayırıq.
# Perform binary search for each query and collect the results.
results = []
for q in queries:
    results.append(str(binary_search(arr, q)))

# Nəticəni boşluqla ayrılmış şəkildə birləşdiririk.
# Join the results separated by spaces.
output_data = ' '.join(results)

# Nəticəni konsolda göstəririk.
# Print the results to the console.
print(output_data[:100] + "...")  # Output may be large, print preview

# Nəticəni "output.txt" faylına yazırıq.
# Write the results to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(output_data + '\n')
