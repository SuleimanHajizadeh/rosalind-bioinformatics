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

# Təpələrin (n) və tillərin (m) sayını təyin edirik.
# Parse the number of vertices (n) and edges (m).
first_line = lines[0].split()
n = int(first_line[0])
m = int(first_line[1])

# Hər bir təpə üçün dərəcə massivini sıfırlarla doldururuq (1-əsaslı indeks üçün n+1 uzunluğunda).
# Initialize the degree array with zeros (length n+1 for 1-based indexing).
degrees = [0] * (n + 1)

# Tilləri oxuyuruq və hər bir təpənin dərəcəsini artırırıq.
# Read the edges and increment the degree of each connected vertex.
for i in range(1, len(lines)):
    edge = list(map(int, lines[i].split()))
    if len(edge) == 2:
        u, v = edge[0], edge[1]
        degrees[u] += 1
        degrees[v] += 1

# 1-dən n-ə qədər olan təpələrin dərəcələrini boşluqla ayıraraq nəticə yaradırıq.
# Create the result string containing degrees of vertices from 1 to n, separated by spaces.
output_data = ' '.join(map(str, degrees[1:]))

# Nəticəni konsolda göstəririk.
# Print the results to the console.
print(output_data[:100] + "...")

# Nəticəni "output.txt" faylına yazırıq.
# Write the results to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(output_data + '\n')
