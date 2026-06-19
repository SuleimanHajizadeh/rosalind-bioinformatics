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

# k və n parametrlərini təyin edirik.
# Parse k and n parameters.
first_line = lines[0].split()
k = int(first_line[0])
n = int(first_line[1])

# Hər bir massiv üçün A[p] = -A[q] şərtini ödəyən p və q indekslərini tapırıq.
# Find indices p and q such that A[p] = -A[q] for each array.
def solve_2sum(arr):
    seen = {}
    for idx, val in enumerate(arr):
        target = -val
        # Əgər axtarılan hədəf dəyər əvvəllər görünübsə, indeksləri qaytarırıq.
        # If the target value was seen before, return the 1-based indices.
        if target in seen:
            return f"{seen[target]} {idx + 1}"
        # Elementin ilk dəfə görünmə indeksini yadda saxlayırıq.
        # Keep track of the first occurrence of the value.
        if val not in seen:
            seen[val] = idx + 1
    return "-1"

# Hər bir sətir üzrə 2SUM problemini həll edirik.
# Solve the 2SUM problem for each line.
results = []
for i in range(1, k + 1):
    arr = list(map(int, lines[i].split()))
    results.append(solve_2sum(arr))

# Nəticələri sətirlərə bölərək birləşdiririk.
# Join the results with newlines.
output_data = '\n'.join(results)

# Nəticəni konsolda göstəririk.
# Print the results to the console.
print(output_data)

# Nəticəni "output.txt" faylına yazırıq.
# Write the results to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(output_data + '\n')
