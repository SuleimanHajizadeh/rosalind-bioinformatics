import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "rosalind_inod.txt")

# 1. Giriş faylından n (yarpaq sayını) oxuyuruq
# Read n (leaf nodes count) from the dataset
with open(input_path, "r") as file:
    n = int(file.read().strip())

# 2. Köksüz binar ağacda daxili düyünlərin (internal nodes) sayını hesablayırıq
# In an unrooted binary tree, internal nodes count = n - 2
internal_nodes = n - 2
print(internal_nodes)

# 3. Nəticəni output.txt faylına yazırıq
# Write result to output.txt
output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as output_file:
    output_file.write(str(internal_nodes) + "\n")
