# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9k.txt")
    if not os.path.exists(input_file):
        return "", 0
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], int(lines[1])

# Last-to-First mapping massivini tapırıq
# Generate the Last-to-First mapping of a string
def last_to_first_mapping(bwt, i):
    # indexed_bwt və first_col strukturlarını qururuq
    # Form indexed last column and sorted first column
    indexed_bwt = []
    counts = {}
    for idx, char in enumerate(bwt):
        counts[char] = counts.get(char, 0) + 1
        indexed_bwt.append((char, counts[char]))
        
    first_col = sorted(indexed_bwt, key=lambda x: x[0])
    
    # i indeksli simvolun first_col-dakı indeksini tapırıq
    # Locate index of item in first column
    target = indexed_bwt[i]
    return first_col.index(target)

def main():
    bwt, i = read_input()
    if not bwt:
        return
    result = last_to_first_mapping(bwt, i)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(result) + "\n")

if __name__ == "__main__":
    main()
