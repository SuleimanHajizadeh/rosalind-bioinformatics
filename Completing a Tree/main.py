import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "rosalind_tree.txt")

# 1. Giriş məlumatlarını oxuyuruq
# Read dataset edges
with open(input_path, "r") as file:
    lines = file.read().splitlines()

n = int(lines[0])
edges = []
for line in lines[1:]:
    if line.strip():
        edges.append(tuple(map(int, line.split())))

# 2. Ağacın tamamlanması üçün lazım olan əlavə tillərin sayını tapırıq
# Minimum edges to complete the tree = (n - 1) - current_edges
min_edges_needed = n - 1 - len(edges)
print(min_edges_needed)

# 3. Cavabı output.txt faylına qeyd edirik
# Write results to output.txt
output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as output_file:
    output_file.write(str(min_edges_needed) + "\n")
