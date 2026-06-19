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

# İki sıralanmış altmassivi birləşdirən funksiya.
# Function to merge two sorted sub-arrays.
def merge(left, right):
    merged = []
    i = 0
    j = 0
    
    # Hər iki altmassivdə elementlər olduqca onları müqayisə edib kiçiyini seçirik.
    # While both sub-arrays have elements, compare and choose the smaller one.
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            
    # Qalan elementləri nəticə massivinə əlavə edirik.
    # Append any remaining elements from both sub-arrays.
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

# Rekursiv Merge Sort alqoritmi.
# Recursive Merge Sort algorithm.
def merge_sort(arr):
    # Əgər massivin uzunluğu 1 və ya daha azdırsa, o artıq sıralanmışdır.
    # If the array length is 1 or less, it is already sorted.
    if len(arr) <= 1:
        return arr
        
    # Massivi iki bərabər hissəyə bölürük.
    # Split the array into two halves.
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Sıralanmış altmassivləri birləşdiririk.
    # Merge the sorted halves.
    return merge(left, right)

# Massivi sıralayırıq.
# Sort the array.
sorted_A = merge_sort(A)

# Nəticəni boşluqla ayrılmış şəkildə birləşdiririk.
# Join the sorted elements with spaces.
output_data = ' '.join(map(str, sorted_A))

# Nəticəni konsolda göstəririk.
# Print the results to the console.
print(output_data[:100] + "...")

# Nəticəni "output.txt" faylına yazırıq.
# Write the results to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(output_data + '\n')
