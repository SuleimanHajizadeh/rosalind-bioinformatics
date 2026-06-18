import os

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_sset.txt")
    
    with open(input_path, "r") as f:
        n = int(f.read().strip())
        
    ans = pow(2, n, 1000000)
    print(f"n = {n}")
    print(f"2^n modulo 1,000,000 = {ans}")
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        out_file.write(str(ans) + "\n")

if __name__ == "__main__":
    main()
