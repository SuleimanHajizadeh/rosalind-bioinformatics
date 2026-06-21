# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9f.txt")
    if not os.path.exists(input_file):
        return "", ""
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], lines[1]

# s1-də olub s2-də olmayan ən qısa alt sətiri tapırıq
# Find the shortest non-shared substring of two strings
def shortest_non_shared_substring(s1, s2):
    # Alt sətir uzunluqlarını 1-dən başlayaraq artırırıq
    # Check lengths starting from 1
    for L in range(1, len(s1) + 1):
        s2_substrings = set()
        for j in range(len(s2) - L + 1):
            s2_substrings.add(s2[j:j+L])
            
        for i in range(len(s1) - L + 1):
            sub = s1[i:i+L]
            if sub not in s2_substrings:
                return sub
    return ""

def main():
    s1, s2 = read_input()
    if not s1:
        return
    result = shortest_non_shared_substring(s1, s2)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    main()
