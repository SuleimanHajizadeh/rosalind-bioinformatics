import os
import glob
import sys

# Rekursiya limitini artırırıq ki, dərin qraflarda xəta baş verməsin.
# Increase recursion limit to avoid recursion depth issues in deep graphs.
sys.setrecursionlimit(2000)

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

# Qrafın qonşuluq siyahısını (Adjacency list) yaradırıq.
# Initialize adjacency lists for the undirected graph.
adj = [[] for _ in range(n + 1)]

# Tilləri oxuyaraq qonşuluq siyahısını doldururuq.
# Read edges and populate the adjacency lists.
for i in range(1, len(lines)):
    edge = list(map(int, lines[i].split()))
    if len(edge) == 2:
        u, v = edge[0], edge[1]
        adj[u].append(v)
        adj[v].append(u)

# Ziyarət olunmuş təpələrin siyahısı.
# Keep track of visited vertices.
visited = [False] * (n + 1)

# Dərinliyinə axtarış (DFS) vasitəsilə komponenti gəzən funksiya.
# Depth-First Search (DFS) to traverse a connected component.
def dfs(u):
    visited[u] = True
    for v in adj[u]:
        if not visited[v]:
            dfs(v)

# Əlaqəli komponentlərin sayını hesablayırıq.
# Count the number of connected components.
component_count = 0
for i in range(1, n + 1):
    if not visited[i]:
        component_count += 1
        dfs(i)

# Nəticəni konsolda göstəririk.
# Print the result to the console.
print(component_count)

# Nəticəni "output.txt" faylına yazırıq.
# Write the result to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(str(component_count) + '\n')
