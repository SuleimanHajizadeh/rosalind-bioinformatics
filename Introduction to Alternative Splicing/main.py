import os
import math

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_aspc.txt")
    
    with open(input_path, "r") as f:
        line = f.read().strip()
        
    parts = line.split()
    n = int(parts[0])
    m = int(parts[1])
    
    # Calculate sum(C(n, k)) for m <= k <= n modulo 1,000,000
    ans = sum(math.comb(n, k) for k in range(m, n + 1)) % 1000000
    
    print(f"n = {n}, m = {m}")
    print(f"Sum of combinations modulo 1,000,000 = {ans}")
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        out_file.write(str(ans) + "\n")

if __name__ == "__main__":
    main()
