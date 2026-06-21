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
    content = f.read().split()

if not content:
    exit()

# Qrafların sayı k-nı oxuyuruq.
# Read the number of graphs k.
k = int(content[0])
idx = 1

results = []

for _ in range(k):
    if idx >= len(content):
        break
    # Təpələrin (n) və tillərin (m) sayını oxuyuruq.
    # Read the number of vertices (n) and edges (m).
    n = int(content[idx])
    m = int(content[idx+1])
    idx += 2
    
    # Tillərin siyahısını oxuyuruq.
    # Read the list of edges.
    edges = []
    for _ in range(m):
        u = int(content[idx])
        v = int(content[idx+1])
        edges.append((u, v))
        idx += 2
        
    # Qonşuluq siyahısını qururuq (təpələr 1-dən n-ə qədər indekslənir).
    # Build the adjacency list (vertices are indexed from 1 to n).
    adj = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        if u in adj and v in adj:
            adj[u].append(v)
            adj[v].append(u)
            
    color = {}
    is_bip = True
    
    # BFS ilə qrafın iki rənglə boyana bilməsini (bipartite) yoxlayırıq.
    # BFS traversal to check if the graph is 2-colorable (bipartite).
    for start in range(1, n + 1):
        if start not in color:
            queue = [start]
            color[start] = 0
            head = 0
            while head < len(queue):
                curr = queue[head]
                head += 1
                curr_color = color[curr]
                for neighbor in adj[curr]:
                    if neighbor not in color:
                        color[neighbor] = 1 - curr_color
                        queue.append(neighbor)
                    elif color[neighbor] == curr_color:
                        is_bip = False
                        break
                if not is_bip:
                    break
        if not is_bip:
            break
            
    results.append("1" if is_bip else "-1")

# Nəticələri boşluqla ayrılmış şəkildə birləşdiririk.
# Join the results with spaces.
output_data = ' '.join(results)

# Nəticəni konsolda göstəririk.
# Print the results to the console.
print(output_data[:100] + "...")

# Nəticəni "output.txt" faylına yazırıq.
# Write the results to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(output_data + '\n')
