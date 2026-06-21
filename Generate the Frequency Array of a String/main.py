# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba1k.txt")
    if not os.path.exists(input_file):
        return "", 0
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], int(lines[1])

# K-mer-i ədədə çeviririk
# Convert pattern to number
def pattern_to_number(pattern):
    symbol_to_num = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    num = 0
    for char in pattern:
        num = num * 4 + symbol_to_num[char]
    return num

# Tezlik massivini hazırlayırıq
# Generate the frequency array of a string
def computing_frequencies(text, k):
    frequency_array = [0] * (4 ** k)
    for i in range(len(text) - k + 1):
        kmer = text[i:i+k]
        j = pattern_to_number(kmer)
        frequency_array[j] += 1
    return frequency_array

def main():
    text, k = read_input()
    if not text:
        return
    result = computing_frequencies(text, k)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(map(str, result)) + "\n")

if __name__ == "__main__":
    main()
