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
# Parse n and the array.
n = int(lines[0])
arr = list(map(int, lines[1].split()))

# Həyata keçirilən yerdəyişmələrin (swap) sayını hesablamaq.
# Count the number of swaps performed by insertion sort.
swaps = 0
for i in range(1, n):
    j = i
    while j > 0 and arr[j] < arr[j - 1]:
        # Elementlərin yerini dəyişirik.
        # Swap the elements.
        arr[j], arr[j - 1] = arr[j - 1], arr[j]
        swaps += 1
        j -= 1

# Yerdəyişmələrin sayını konsolda göstəririk.
# Print the number of swaps to the console.
print(swaps)

# Nəticəni "output.txt" faylına yazırıq.
# Write the result to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(str(swaps) + '\n')
