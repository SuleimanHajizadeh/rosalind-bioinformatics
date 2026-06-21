# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9e.txt")
    if not os.path.exists(input_file):
        return "", ""
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], lines[1]

# İki sətir tərəfindən paylaşılan ən uzun alt sətiri (LCS) tapırıq
# Find the longest substring shared by two strings
def longest_shared_substring(s1, s2):
    # Sürətli həll üçün suffix ağacı əvəzinə s1-in alt sətirlərini s2-də axtarırıq (ikili axtarış ilə)
    # Search for match using binary search on length L
    low, high = 1, min(len(s1), len(s2))
    best = ""
    
    # Sürətli axtarış üçün helper
    # Check if any substring of s1 of length L exists in s2
    def has_shared_of_len(L):
        seen = set()
        for i in range(len(s2) - L + 1):
            seen.add(s2[i:i+L])
        for i in range(len(s1) - L + 1):
            sub = s1[i:i+L]
            if sub in seen:
                return sub
        return None
        
    while low <= high:
        mid = (low + high) // 2
        match = has_shared_of_len(mid)
        if match:
            best = match
            low = mid + 1
        else:
            high = mid - 1
            
    return best

def main():
    s1, s2 = read_input()
    if not s1:
        return
    result = longest_shared_substring(s1, s2)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    main()
