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

# Max-heap strukturunu qorumaq üçün aşağı sürüşdürmə (heapify) funksiyası.
# Iterative max-heapify function to maintain the max-heap property.
def max_heapify(arr, size, idx):
    while True:
        largest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2
        
        # Sol övladı yoxlayırıq.
        # Check if the left child is larger than current largest.
        if left < size and arr[left] > arr[largest]:
            largest = left
            
        # Sağ övladı yoxlayırıq.
        # Check if the right child is larger than current largest.
        if right < size and arr[right] > arr[largest]:
            largest = right
            
        # Əgər ən böyük element övladlardan biridirsə, yerini dəyişib davam edirik.
        # If the largest is not the parent, swap and continue heapifying.
        if largest != idx:
            arr[idx], arr[largest] = arr[largest], arr[idx]
            idx = largest
        else:
            break

# Heap strukturunu qurmaq üçün funksiya.
# Function to build the max-heap.
def build_max_heap(arr):
    size = len(arr)
    # Sonuncu yarpaq olmayan təpədən başlayaraq kök təpəyə doğru heapify edirik.
    # Start heapifying from the last non-leaf node down to the root.
    for i in range(size // 2 - 1, -1, -1):
        max_heapify(arr, size, i)

# Heap strukturunu qururuq.
# Build the heap.
build_max_heap(A)

# Nəticəni boşluqla ayrılmış şəkildə birləşdiririk.
# Join the heapified elements with spaces.
output_data = ' '.join(map(str, A))

# Nəticəni konsolda göstəririk.
# Print the results to the console.
print(output_data[:100] + "...")

# Nəticəni "output.txt" faylına yazırıq.
# Write the results to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(output_data + '\n')
