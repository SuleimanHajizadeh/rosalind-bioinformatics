# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba6b.txt")
    if not os.path.exists(input_file):
        return []
    with open(input_file, "r") as f:
        content = f.read().strip()
        content = content.replace("(", "").replace(")", "")
        return list(map(int, content.split()))

# Permutasiyadakı breakpoint (kəsilmə nöqtəsi) sayını hesablayırıq
# Compute the number of breakpoints in a permutation
def count_breakpoints(p):
    # Əvvəlinə 0 və sonuna n+1 əlavə edirik
    # Prepend 0 and append n+1
    n = len(p)
    extended = [0] + p + [n + 1]
    breakpoints = 0
    for i in range(len(extended) - 1):
        if extended[i+1] - extended[i] != 1:
            breakpoints += 1
    return breakpoints

def main():
    p = read_input()
    if not p:
        return
    result = count_breakpoints(p)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(result) + "\n")

if __name__ == "__main__":
    main()
