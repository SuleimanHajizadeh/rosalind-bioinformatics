# Giriş verilənlərini oxumaq üçün funksiya
# Function to read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba1a.txt")
    if not os.path.exists(input_file):
        return "", ""
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], lines[1]

# Pattern-in mətndə neçə dəfə göründüyünü hesablayırıq
# Compute the number of times pattern appears in text
def pattern_count(text, pattern):
    count = 0
    k = len(pattern)
    for i in range(len(text) - k + 1):
        if text[i:i+k] == pattern:
            count += 1
    return count

def main():
    text, pattern = read_input()
    if not text:
        return
    result = pattern_count(text, pattern)
    
    # Nəticəni output.txt faylına yazırıq
    # Write the result to output.txt
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(result) + "\n")

if __name__ == "__main__":
    main()
