# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba3b.txt")
    if not os.path.exists(input_file):
        return []
    with open(input_file, "r") as f:
        return [line.strip() for line in f if line.strip()]

# Genom yolundan sətiri yenidən qururuq
# Reconstruct a string from its genome path
def reconstruct_from_path(path):
    string = path[0]
    for kmer in path[1:]:
        string += kmer[-1]
    return string

def main():
    path = read_input()
    if not path:
        return
    result = reconstruct_from_path(path)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    main()
