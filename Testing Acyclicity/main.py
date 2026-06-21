import os
import glob
import sys

# Sistem məhdudiyyətini artırırıq ki, dərin rekursiyalar üçün problem yaranmasın.
# Increase recursion depth limit to prevent stack overflow in deep DFS.
sys.setrecursionlimit(20000)

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
        if u in adj:
            adj[u].append(v)
            
    # Təpələrin vəziyyətini (0: unvisited, 1: visiting, 2: visited) izləmək üçün massiv.
    # State tracking: 0: unvisited, 1: visiting, 2: visited.
    state = {i: 0 for i in range(1, n + 1)}
    has_cycle = [False]
    
    # DFS ilə dövr (cycle) axtaran köməkçi funksiya.
    # Helper DFS function to detect directed cycles.
    def dfs(u):
        state[u] = 1 # Visiting (hələ ki işlənir)
        
        for neighbor in adj[u]:
            if state[neighbor] == 1:
                # Visiting vəziyyətində olan qonşu tapıldısa, bu dövr deməkdir.
                # If neighbor is visiting, a back edge is found, hence a cycle exists.
                has_cycle[0] = True
                return
            elif state[neighbor] == 0:
                dfs(neighbor)
                if has_cycle[0]:
                    return
                    
        state[u] = 2 # Visited (tamamilə işləndi)

    # Bütün unvisited təpələr üçün DFS-i başladırıq.
    # Run DFS from all unvisited vertices.
    for i in range(1, n + 1):
        if state[i] == 0:
            dfs(i)
            if has_cycle[0]:
                break
                
    # Əgər dövr yoxdursa qraf acyclic-dir (1), əks halda dövr var (-1).
    # If no cycle, output 1 (acyclic), else output -1 (has cycle).
    results.append("1" if not has_cycle[0] else "-1")

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
