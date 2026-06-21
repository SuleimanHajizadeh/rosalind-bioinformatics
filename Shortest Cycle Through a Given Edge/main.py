import os
import glob
import heapq

# Giriş faylından ən qısa yolu tapmaq üçün Dijkstra alqoritmi.
# Dijkstra's algorithm to find the shortest path from a start node to a target node.
def dijkstra(n, adj, start_node, target_node):
    # Bütün təpələr üçün məsafələri sonsuzluqla inisializasiya edirik.
    # Initialize distances for all vertices with infinity.
    dist = {i: float('inf') for i in range(1, n + 1)}
    dist[start_node] = 0
    
    # Prioritet növbəsini (min-heap) yaradırıq.
    # Create the priority queue (min-heap).
    pq = [(0, start_node)]
    
    while pq:
        d, u = heapq.heappop(pq)
        
        # Əgər tapılan yol mövcud ən qısa yoldan böyükdürsə, keçirik.
        # If the path is longer than the current shortest distance, skip.
        if d > dist[u]:
            continue
            
        # Hədəf təpəyə çatdıqda məsafəni qaytarırıq.
        # Return the distance when the target node is reached.
        if u == target_node:
            return d
            
        # Qonşu təpələrə olan məsafələri yeniləyirik.
        # Update distances to neighboring vertices.
        if u in adj:
            for v, w in adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(pq, (dist[v], v))
                    
    return dist[target_node]

# Cari qovluqdakı "rosalind_" ilə başlayan giriş faylını tapırıq.
# Locate the input file starting with "rosalind_" in the current directory.
input_files = glob.glob(os.path.join(os.path.dirname(__file__), 'rosalind_*.txt'))
if not input_files:
    raise FileNotFoundError("Giriş faylı tapılmadı / Input file not found")

# Giriş faylından bütün məlumatları oxuyuruq.
# Read all data from the input file.
with open(input_files[0], 'r') as f:
    content = f.read().split()

if not content:
    exit()

# Qrafların sayı k-nı oxuyuruq.
# Read the number of graphs k.
k = int(content[0])
idx = 1

results = []

# Hər bir qrafı növbə ilə emal edirik.
# Process each graph one by one.
for _ in range(k):
    if idx >= len(content):
        break
    
    # Təpələrin (n) və tillərin (m) sayını oxuyuruq.
    # Read the number of vertices (n) and edges (m).
    n = int(content[idx])
    m = int(content[idx+1])
    idx += 2
    
    # Qonşuluq siyahısını qururuq və ilk təyin olunmuş tili qeyd edirik.
    # Build the adjacency list and record the first specified edge.
    adj = {i: [] for i in range(1, n + 1)}
    u_first, v_first, w_first = 0, 0, 0
    
    for i in range(m):
        u = int(content[idx])
        v = int(content[idx+1])
        w = int(content[idx+2])
        idx += 3
        
        # İlk tili növbəti addım üçün saxlayırıq.
        # Save the first edge for the cycle check.
        if i == 0:
            u_first, v_first, w_first = u, v, w
            
        adj[u].append((v, w))
        
    # İlk tilin hədəf təpəsindən (v_first) başlanğıc təpəsinə (u_first) ən qısa yolu tapırıq.
    # Find the shortest path from the first edge's target (v_first) to its source (u_first).
    shortest_back_path = dijkstra(n, adj, v_first, u_first)
    
    # Əgər geriyə yol varsa, dövrün ümumi çəkisini hesablayırıq, yoxdursa -1 yazırıq.
    # If a path exists, return edge weight + path distance, else return -1.
    if shortest_back_path == float('inf'):
        results.append("-1")
    else:
        results.append(str(w_first + shortest_back_path))

# Nəticələri boşluqla ayıraraq sətirə çeviririk.
# Join the results with spaces to form a string.
output_data = ' '.join(results)

# Nəticəni konsolda göstəririk.
# Print the results to the console.
print(output_data)

# Nəticəni "output.txt" faylına yazırıq.
# Write the results to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(output_data + '\n')
