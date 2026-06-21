# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba1m.txt")
    if not os.path.exists(input_file):
        return 0, 0
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return int(lines[0]), int(lines[1])

# Ədədi DNT pattern-inə çeviririk
# Implement NumberToPattern
def number_to_pattern(index, k):
    num_to_symbol = {0: 'A', 1: 'C', 2: 'G', 3: 'T'}
    pattern = []
    for _ in range(k):
        pattern.append(num_to_symbol[index % 4])
        index //= 4
    return "".join(reversed(pattern))

def main():
    index, k = read_input()
    result = number_to_pattern(index, k)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    main()
