# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9q.txt")
    if not os.path.exists(input_file):
        return "", 0
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], int(lines[1])

# Səthi hissəvi suffix array-ə (Partial Suffix Array) çeviririk
# Construct the partial suffix array of a string with spacing factor K
def partial_suffix_array(text, K):
    suffixes = []
    for i in range(len(text)):
        suffixes.append((text[i:], i))
    suffixes.sort(key=lambda x: x[0])
    
    result = []
    for idx, (suf, orig_idx) in enumerate(suffixes):
        # Yalnız K-ya bölünən mövqeləri saxlayırıq
        # Keep only indices divisible by K
        if orig_idx % K == 0:
            result.append((idx, orig_idx))
    return result

def main():
    text, K = read_input()
    if not text:
        return
    result = partial_suffix_array(text, K)
    
    output_lines = [f"{idx},{orig_idx}" for idx, orig_idx in result]
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(output_lines) + "\n")

if __name__ == "__main__":
    main()
