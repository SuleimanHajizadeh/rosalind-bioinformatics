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

# n, A massivi, m və B massivini təyin edirik.
# Parse n, array A, m, and array B.
n = int(lines[0])
A = list(map(int, lines[1].split()))
m = int(lines[2])
B = list(map(int, lines[3].split()))

# İki sıralanmış massivi birləşdirən funksiya.
# Function to merge two sorted arrays.
def merge_sorted_arrays(arr1, arr2):
    merged = []
    i, j = 0, 0
    len1, len2 = len(arr1), len(arr2)
    
    # Hər iki massivdə elementlər olduqca müqayisə edib birləşdiririk.
    # Compare elements from both arrays and merge them.
    while i < len1 and j < len2:
        if arr1[i] <= arr2[j]:
            merged.append(arr1[i])
            i += 1
        else:
            merged.append(arr2[j])
            j += 1
            
    # Qalan elementləri əlavə edirik.
    # Append the remaining elements.
    merged.extend(arr1[i:])
    merged.extend(arr2[j:])
    return merged

# Massivləri birləşdiririk.
# Merge the two sorted arrays.
C = merge_sorted_arrays(A, B)

# Nəticəni boşluqla ayrılmış şəkildə birləşdiririk.
# Join the sorted elements with spaces.
output_data = ' '.join(map(str, C))

# Nəticəni konsolda göstəririk.
# Print the results to the console.
print(output_data[:100] + "...")

# Nəticəni "output.txt" faylına yazırıq.
# Write the results to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(output_data + '\n')
