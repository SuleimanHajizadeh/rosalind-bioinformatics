# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9m.txt")
    if not os.path.exists(input_file):
        return "", []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    bwt = lines[0]
    patterns = lines[1].split()
    return bwt, patterns

# Sürətli hesablama üçün Count massivi (FirstOccurrence və Count massivləri ilə)
# Implement BetterBWMatching using FirstOccurrence and Count matrices
def better_bw_matching(bwt, patterns):
    first_col = sorted(list(bwt))
    
    # First Occurrence
    first_occurrence = {}
    for idx, char in enumerate(first_col):
        if char not in first_occurrence:
            first_occurrence[char] = idx
            
    # Count matrix setup
    # count[char][i] gives occurrences of char in bwt[0...i-1]
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
                # top ve bottom arasındakı Count-lar vasitəsilə növbəti mövqeləri hesablayırıq
                # Update pointers using Count table
                if symbol in count and (count[symbol][bottom+1] - count[symbol][top]) > 0:
                    top = first_occurrence[symbol] + count[symbol][top]
                    bottom = first_occurrence[symbol] + count[symbol][bottom+1] - 1
                else:
                    matched = False
                    break
            else:
                break
        if matched:
            results.append(bottom - top + 1)
        else:
            results.append(0)
            
    return results

def main():
    bwt, patterns = read_input()
    if not bwt:
        return
    results = better_bw_matching(bwt, patterns)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(map(str, results)) + "\n")

if __name__ == "__main__":
    main()
