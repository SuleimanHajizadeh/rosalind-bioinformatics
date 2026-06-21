import os
import glob
import heapq

# Cari qovluqdakı "rosalind_" ilə başlayan giriş faylını tapırıq.
# Locate the input file starting with "rosalind_" in the current directory.
input_files = glob.glob(os.path.join(os.path.dirname(__file__), 'rosalind_*.txt'))
if not input_files:
    raise FileNotFoundError("Giriş faylı tapılmadı / Input file not found")

# Giriş faylından məlumatları oxuyuruq.
# Read data from the input file.
with open(input_files[0], 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

# n (təpələrin sayı) və m (tillərin sayı) oxuyuruq.
# Read n (number of vertices) and m (number of edges).
n, m = map(int, lines[0].split())

# Qonşuluq siyahısını qururuq. Hər bir təpə üçün qonşuları və tillərin çəkilərini saxlayırıq.
# Build the adjacency list. Store neighbors and edge weights for each vertex.
adj = {i: [] for i in range(1, n + 1)}
for i in range(1, m + 1):
    u, v, w = map(int, lines[i].split())
    if u in adj:
        adj[u].append((v, w))

# Məsafələr massivini sonsuzluqla (float('inf')) inisializasiya edirik.
# Initialize the distances array with infinity.
dist = {i: float('inf') for i in range(1, n + 1)}
dist[1] = 0

# Prioritet növbəsi (heap) üçün başlanğıc olaraq (məsafə, təpə) cütünü daxil edirik.
# Initialize priority queue (heap) with the source vertex (distance 0, vertex 1).
heap = [(0, 1)]

# Dijkstra alqoritmi ilə ən qısa məsafələri hesablayırıq.
# Compute the shortest paths using Dijkstra's algorithm.
while heap:
    d, u = heapq.heappop(heap)
    
    # Əgər cari məsafə artıq qeydə alınmış ən qısa məsafədən böyükdürsə, davam edirik.
    # If the current distance is larger than the recorded shortest distance, skip.
    if d > dist[u]:
        continue
        
    for neighbor, weight in adj[u]:
        # Qonşu təpəyə gedən yeni məsafəni yoxlayırıq.
        # Check if a shorter path to the neighbor exists.
        if dist[u] + weight < dist[neighbor]:
            dist[neighbor] = dist[u] + weight
            heapq.heappush(heap, (dist[neighbor], neighbor))

# Əlçatmaz təpələr üçün məsafəni -1 olaraq təyin edirik.
# Set distances of unreachable vertices to -1.
results = []
for i in range(1, n + 1):
    val = dist[i]
    if val == float('inf'):
        results.append("-1")
    else:
        results.append(str(val))

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
