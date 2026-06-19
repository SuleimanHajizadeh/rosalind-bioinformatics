import os
import glob
from collections import deque

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

# Yönlü qrafın qonşuluq siyahısını (Adjacency list) yaradırıq.
# Initialize adjacency lists for the directed graph.
adj = [[] for _ in range(n + 1)]

# Tilləri oxuyaraq qonşuluq siyahısını doldururuq.
# Read edges and populate the adjacency lists.
for i in range(1, len(lines)):
    edge = list(map(int, lines[i].split()))
    if len(edge) == 2:
        u, v = edge[0], edge[1]
        adj[u].append(v)

# Məsafə massivini təyin edirik (başlanğıcda hamısı üçün -1).
# Initialize distance array with -1 (representing unvisited/unreachable).
dist = [-1] * (n + 1)

# Başlanğıc təpənin (1) məsafəsini 0 təyin edirik.
# Set the distance of the starting vertex (1) to 0.
dist[1] = 0

# BFS növbəsini (queue) yaradırıq və başlanğıc təpəni əlavə edirik.
# Create a queue for BFS and enqueue the starting vertex.
queue = deque([1])

# Genişliyinə axtarış (BFS) alqoritmi.
# Breadth-First Search (BFS) algorithm implementation.
while queue:
    u = queue.popleft()
    for v in adj[u]:
        # Əgər v təpəsi hələ ziyarət olunmayıbsa:
        # If vertex v has not been visited yet:
        if dist[v] == -1:
            dist[v] = dist[u] + 1
            queue.append(v)

# 1-dən n-ə qədər olan təpələrin məsafələrini boşluqla ayıraraq nəticə yaradırıq.
# Create space-separated string containing distances from 1 to n.
output_data = ' '.join(map(str, dist[1:]))

# Nəticəni konsolda göstəririk.
# Print the results to the console.
print(output_data[:100] + "...")

# Nəticəni "output.txt" faylına yazırıq.
# Write the results to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(output_data + '\n')
