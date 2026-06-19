import os
import glob

# Cari qovluqdakı "rosalind_" ilə başlayan giriş faylını tapırıq.
# Locate the input file starting with "rosalind_" in the current directory.
input_files = glob.glob(os.path.join(os.path.dirname(__file__), 'rosalind_*.txt'))
if not input_files:
    raise FileNotFoundError("Giriş faylı tapılmadı / Input file not found")

# Giriş faylından n ədədini oxuyuruq.
# Read the number n from the input file.
with open(input_files[0], 'r') as f:
    n = int(f.read().strip())

# Fibonacci ədədini hesablamaq üçün funksiya.
# Function to calculate the Fibonacci number.
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# n-ci Fibonacci ədədini hesablayırıq.
# Compute the n-th Fibonacci number.
result = fibonacci(n)

# Nəticəni ekranda göstəririk.
# Print the result to the console.
print(result)

# Nəticəni "output.txt" faylına yazırıq.
# Write the result to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(str(result) + '\n')
