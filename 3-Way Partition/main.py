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

# Pivot olaraq massivin ilk elementini seçirik.
# Select the first element of the array as the pivot.
pivot = A[0]

# Pivotdan kiçik, bərabər və böyük elementlər üçün siyahılar yaradırıq.
# Create lists for elements less than, equal to, and greater than the pivot.
less = []
equal = []
greater = []

# Massivdəki hər bir elementi pivotla müqayisə edib müvafiq siyahıya əlavə edirik.
# Compare each element with the pivot and append it to the appropriate list.
for x in A:
    if x < pivot:
        less.append(x)
    elif x == pivot:
        equal.append(x)
    else:
        greater.append(x)

# Siyahıları birləşdirərək 3-yollu bölümlənmiş massivi əldə edirik.
# Concatenate the lists to get the 3-way partitioned array.
B = less + equal + greater

# Nəticəni boşluqlarla ayrılmış sətir formatına salırıq.
# Format the result as a space-separated string.
output_str = ' '.join(map(str, B))

# Nəticəni konsolda göstəririk.
# Print the result to the console.
print(output_str[:100] + "...")

# Nəticəni "output.txt" faylına yazırıq.
# Write the result to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(output_str + '\n')
