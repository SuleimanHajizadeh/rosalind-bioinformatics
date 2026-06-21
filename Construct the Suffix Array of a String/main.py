# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9g.txt")
    if not os.path.exists(input_file):
        return ""
    with open(input_file, "r") as f:
        return f.read().strip()

# Sətri suffix array-ə (suffiks massivi) çeviririk
# Construct the suffix array of a string
def construct_suffix_array(text):
    suffixes = []
    for i in range(len(text)):
        suffixes.append((text[i:], i))
    # Əlifba sırası ilə düzürük
    # Sort lexicographically
    suffixes.sort(key=lambda x: x[0])
    return [idx for suf, idx in suffixes]

def main():
    text = read_input()
    if not text:
        return
    result = construct_suffix_array(text)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(", ".join(map(str, result)) + "\n")

if __name__ == "__main__":
    main()
