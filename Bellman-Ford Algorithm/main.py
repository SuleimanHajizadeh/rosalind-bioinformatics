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

# n və m-i təyin edirik.
# Parse n and m.
n, m = map(int, lines[0].split())

# Tillərin siyahısını oxuyuruq.
# Read the list of edges.
edges = []
for i in range(1, m + 1):
    u, v, w = map(int, lines[i].split())
    edges.append((u, v, w))

# Məsafələr massivini sonsuzluqla inisializasiya edirik.
# Initialize the distances array with infinity.
INF = float('inf')
dist = [INF] * (n + 1)
dist[1] = 0

# Bellman-Ford alqoritmini n - 1 dəfə təkrarlayırıq.
# Run the Bellman-Ford algorithm n - 1 times.
for _ in range(n - 1):
    updated = False
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            updated = True
    # Əgər heç bir məsafə yenilənməyibsə, erkən dayana bilərik.
    # If no distance is updated, we can stop early.
    if not updated:
        break

# Çatılmaz təpələr üçün məsafəni 'x' ilə əvəzləyirik.
# Replace unreachable vertex distances with 'x'.
result = []
for i in range(1, n + 1):
    if dist[i] == INF:
        result.append('x')
    else:
        result.append(str(dist[i]))

# Nəticəni boşluqla ayrılmış sətir formatına salırıq.
# Format the result as a space-separated string.
output_data = ' '.join(result)

# Nəticəni konsolda göstəririk.
# Print the results to the console.
print(output_data[:100] + "...")

# Nəticəni "output.txt" faylına yazırıq.
# Write the results to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(output_data + '\n')
