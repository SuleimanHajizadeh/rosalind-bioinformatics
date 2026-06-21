import os
import glob

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
    
    # Qonşuluq siyahısını qururuq (təpələr 1-dən n-ə qədər indekslənir).
    # Build the adjacency list (vertices are indexed from 1 to n).
    adj = {i: [] for i in range(1, n + 1)}
    for _ in range(m):
        u = int(content[idx])
        v = int(content[idx+1])
        adj[u].append(v)
        adj[v].append(u)
        idx += 2
        
    # 4-dövrün (C4) olub-olmadığını yoxlamaq üçün bayraq.
    # Flag to check if a 4-cycle (C4) exists.
    has_c4 = False
    
    # Görünən qonşu cütlərini yadda saxlamaq üçün çoxluq.
    # Set to store neighbor pairs that have been seen.
    seen = set()
    
    # Hər bir təpənin qonşularını və onların cütlərini yoxlayırıq.
    # Iterate through each vertex's neighbors and check their pairs.
    for v in range(1, n + 1):
        # Qonşuları sıralayırıq ki, cütlər həmişə eyni ardıcıllıqla yaradılsın.
        # Sort the neighbors to ensure pairs are generated in a consistent order.
        neighbors = sorted(adj[v])
        num_neighbors = len(neighbors)
        
        # Hər bir qonşu cütü üçün:
        # For each pair of neighbors:
        for i in range(num_neighbors):
            for j in range(i + 1, num_neighbors):
                u = neighbors[i]
                w = neighbors[j]
                pair = (u, w)
                
                # Əgər bu cüt artıq başqa bir təpədə görünübsə, deməli 4-dövr tapıldı.
                # If this pair was already seen with another vertex, a 4-cycle is found.
                if pair in seen:
                    has_c4 = True
                    break
                seen.add(pair)
            if has_c4:
                break
        if has_c4:
            break
            
    # Nəticəni nəticələr siyahısına əlavə edirik.
    # Append the result to the results list.
    results.append("1" if has_c4 else "-1")

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
