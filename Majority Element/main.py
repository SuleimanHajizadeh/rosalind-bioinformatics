import os
import glob
from collections import Counter

# Cari qovluqdakı "rosalind_" ilə başlayan giriş faylını tapırıq.
# Locate the input file starting with "rosalind_" in the current directory.
input_files = glob.glob(os.path.join(os.path.dirname(__file__), 'rosalind_*.txt'))
if not input_files:
    raise FileNotFoundError("Giriş faylı tapılmadı / Input file not found")

# Giriş faylından məlumatları oxuyuruq.
# Read data from the input file.
with open(input_files[0], 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

# k və n-i birinci sətirdən oxuyuruq.
# Parse k and n from the first line.
first_line = lines[0].split()
k = int(first_line[0])
n = int(first_line[1])

# Çoxluq elementini (Majority Element) tapan funksiya.
# Function to find the majority element.
def find_majority(arr):
    length = len(arr)
    # Hər bir elementin sayını hesablayırıq.
    # Count the occurrences of each element.
    counter = Counter(arr)
    # Ən çox rast gəlinən elementi tapırıq.
    # Get the most common element and its count.
    most_common, count = counter.most_common(1)[0]
    # Say strictly > n / 2 olub olmadığını yoxlayırıq.
    # Check if the count is strictly greater than n / 2.
    if count > length / 2:
        return most_common
    return -1

# Hər bir massiv üçün çoxluq elementini hesablayırıq.
# Compute the majority element for each array.
results = []
for i in range(1, k + 1):
    arr = list(map(int, lines[i].split()))
    results.append(str(find_majority(arr)))

# Nəticələri boşluqla ayıraraq birləşdiririk.
# Join the results separated by spaces.
output_data = ' '.join(results)

# Nəticəni konsolda göstəririk.
# Print the results to the console.
print(output_data)

# Nəticəni "output.txt" faylına yazırıq.
# Write the results to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(output_data + '\n')
