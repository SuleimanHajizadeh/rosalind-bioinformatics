import os
import glob
import sys

# Sistem məhdudiyyətini artırırıq ki, dərin rekursiyalar üçün problem yaranmasın.
# Increase recursion depth limit to prevent stack overflow in deep recursion.
sys.setrecursionlimit(200000)

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

# İki sıralanmış altmassivi birləşdirən və inversiya sayını hesablayan köməkçi funksiya.
# Helper function to merge two sorted sub-arrays and count inversions.
def merge_and_count(arr, temp_arr, left, mid, right):
    i = left     # Sol altmassiv üçün göstərici / Index for left sub-array
    j = mid + 1  # Sağ altmassiv üçün göstərici / Index for right sub-array
    k = left     # Birləşmiş massiv üçün göstərici / Index for resultant merged sub-array
    inv_count = 0
    
    # Hər iki altmassivdə elementlər olduqca müqayisə edirik.
    # While there are elements in both sub-arrays, compare them.
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp_arr[k] = arr[i]
            i += 1
        else:
            temp_arr[k] = arr[j]
            # Əgər sol element sağ elementdən böyükdürsə, sol yarıdakı qalan bütün elementlər
            # sağdakı elementlə inversiya əmələ gətirir.
            # If left element is greater, then all remaining elements in the left half
            # form inversions with the right element.
            inv_count += (mid - i + 1)
            j += 1
        k += 1
        
    # Sol massivdə qalan elementləri köçürürük.
    # Copy the remaining elements of the left sub-array.
    while i <= mid:
        temp_arr[k] = arr[i]
        i += 1
        k += 1
        
    # Sağ massivdə qalan elementləri köçürürük.
    # Copy the remaining elements of the right sub-array.
    while j <= right:
        temp_arr[k] = arr[j]
        j += 1
        k += 1
        
    # Birləşdirilmiş elementləri orijinal massivə geri köçürürük.
    # Copy the merged elements back into the original array.
    for loop_var in range(left, right + 1):
        arr[loop_var] = temp_arr[loop_var]
        
    return inv_count

# Rekursiv Merge Sort vasitəsilə inversiyaları sayan funksiya.
# Recursive function to count inversions using Merge Sort.
def _merge_sort(arr, temp_arr, left, right):
    inv_count = 0
    if left < right:
        mid = (left + right) // 2
        
        # Sol yarını sıralayırıq və inversiyaları sayırıq.
        # Sort left half and count inversions.
        inv_count += _merge_sort(arr, temp_arr, left, mid)
        
        # Sağ yarını sıralayırıq və inversiyaları sayırıq.
        # Sort right half and count inversions.
        inv_count += _merge_sort(arr, temp_arr, mid + 1, right)
        
        # Hər iki yarını birləşdiririk və inversiyaları sayırıq.
        # Merge both halves and count inversions.
        inv_count += merge_and_count(arr, temp_arr, left, mid, right)
        
    return inv_count

# İnversiya sayını hesablamaq üçün əsas çağırış funksiyası.
# Main wrapper function to count inversions.
def count_inversions(arr):
    temp_arr = [0] * len(arr)
    return _merge_sort(arr, temp_arr, 0, len(arr) - 1)

# İnversiyaların sayını hesablayırıq.
# Compute the number of inversions.
result = count_inversions(A)

# Nəticəni konsolda göstəririk.
# Print the result to the console.
print(result)

# Nəticəni "output.txt" faylına yazırıq.
# Write the result to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(str(result) + '\n')
