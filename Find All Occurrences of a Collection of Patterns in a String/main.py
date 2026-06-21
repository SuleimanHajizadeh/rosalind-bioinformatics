# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9n.txt")
    if not os.path.exists(input_file):
        return "", []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], lines[1:]

# Burrows-Wheeler ilə sətirdə bütün naxış axtarışlarını edirik
# Find all occurrences of a collection of patterns in a string using BWT
def find_all_occurrences_bwt(text, patterns):
    # BWT üçün $ işarəsini sonuna artırıb massivi hazırlayırıq
    # Append terminal '$'
    t = text + "$"
    n = len(t)
    
    # Suffix Array
    suffixes = []
    for i in range(n):
        suffixes.append((t[i:], i))
    suffixes.sort(key=lambda x: x[0])
    sa = [idx for suf, idx in suffixes]
    bwt = "".join(t[(idx - 1) % n] for idx in sa)
    
    first_col = sorted(list(bwt))
    
    first_occurrence = {}
    for idx, char in enumerate(first_col):
        if char not in first_occurrence:
            first_occurrence[char] = idx
            
    count = {char: [0] * (len(bwt) + 1) for char in set(bwt)}
    for idx, char in enumerate(bwt):
        for c in count:
            count[c][idx+1] = count[c][idx] + (1 if c == char else 0)
            
    results = []
    for pattern in patterns:
        top = 0
        bottom = len(bwt) - 1
        curr_pattern = list(pattern)
        matched = True
        
        while top <= bottom:
            if curr_pattern:
                symbol = curr_pattern.pop()
                if symbol in count and (count[symbol][bottom+1] - count[symbol][top]) > 0:
                    top = first_occurrence[symbol] + count[symbol][top]
                    bottom = first_occurrence[symbol] + count[symbol][bottom+1] - 1
                else:
                    matched = False
                    break
            else:
                break
        if matched:
            for idx in range(top, bottom + 1):
                results.append(sa[idx])
                
    results = sorted(list(set(results)))
    return results

def main():
    text, patterns = read_input()
    if not text:
        return
    result = find_all_occurrences_bwt(text, patterns)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(map(str, result)) + "\n")

if __name__ == "__main__":
    main()
