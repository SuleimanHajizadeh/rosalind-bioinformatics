# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba1l.txt")
    if not os.path.exists(input_file):
        return ""
    with open(input_file, "r") as f:
        return f.read().strip()

# Pattern-i 4-lük say sistemində ədədə çeviririk
# Implement PatternToNumber
def pattern_to_number(pattern):
    symbol_to_num = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    num = 0
    for char in pattern:
        num = num * 4 + symbol_to_num[char]
    return num

def main():
    pattern = read_input()
    if not pattern:
        return
    result = pattern_to_number(pattern)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(result) + "\n")

if __name__ == "__main__":
    main()
