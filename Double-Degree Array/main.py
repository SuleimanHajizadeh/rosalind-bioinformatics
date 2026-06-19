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

# Qonşuluq siyahısı (Adjacency list) və təpələrin dərəcələrini təyin edirik.
# Initialize adjacency lists and vertex degree array.
adj = [[] for _ in range(n + 1)]
degrees = [0] * (n + 1)

# Tilləri oxuyaraq qonşuluq siyahısını və dərəcələri yeniləyirik.
# Read edges, populate adjacency lists and update vertex degrees.
for i in range(1, len(lines)):
    edge = list(map(int, lines[i].split()))
    if len(edge) == 2:
        u, v = edge[0], edge[1]
        adj[u].append(v)
        adj[v].append(u)
        degrees[u] += 1
        degrees[v] += 1

# Hər bir təpə üçün qonşularının dərəcələrinin cəmini hesablayırıq.
# Calculate the sum of degrees of neighbors for each vertex.
double_degrees = []
for u in range(1, n + 1):
    neighbor_degree_sum = sum(degrees[v] for v in adj[u])
    double_degrees.append(str(neighbor_degree_sum))

# Nəticəni boşluqla ayrılmış şəkildə birləşdiririk.
# Join the result with spaces.
output_data = ' '.join(double_degrees)

# Nəticəni konsolda göstəririk.
# Print the results to the console.
print(output_data[:100] + "...")

# Nəticəni "output.txt" faylına yazırıq.
# Write the results to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(output_data + '\n')
