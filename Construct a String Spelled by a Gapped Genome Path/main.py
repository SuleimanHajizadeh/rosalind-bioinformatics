# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba3l.txt")
    if not os.path.exists(input_file):
        return 0, 0, []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    k, d = map(int, lines[0].split())
    pairs = []
    for line in lines[1:]:
        pairs.append(line.split("|"))
    return k, d, pairs

# Boşluqlu genom yolundan sətir qururuq
# Construct a string spelled by a gapped genome path
def string_spelled_by_gapped_patterns(k, d, pairs):
    first_patterns = [p[0] for p in pairs]
    second_patterns = [p[1] for p in pairs]
    
    # Birinci hissəni birləşdiririk
    # Spell string representing the first sequence of pairs
    prefix_str = first_patterns[0]
    for p in first_patterns[1:]:
        prefix_str += p[-1]
        
    # İkinci hissəni birləşdiririk
    # Spell string representing the second sequence of pairs
    suffix_str = second_patterns[0]
    for p in second_patterns[1:]:
        suffix_str += p[-1]
        
    # Üst-üstə düşən hissəni yoxlayıb birləşdiririk
    # Combine both strings using the overlap
    overlap = len(prefix_str) - (k + d)
    if prefix_str[overlap:] == suffix_str[:-overlap]:
        return prefix_str + suffix_str[-overlap:]
    return prefix_str + suffix_str

def main():
    k, d, pairs = read_input()
    if not pairs:
        return
    result = string_spelled_by_gapped_patterns(k, d, pairs)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    main()
