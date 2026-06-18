import os
import math

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, 'rosalind_cntq.txt')
    output_path = os.path.join(base_dir, 'output.txt')
    
    with open(input_path, 'r') as f:
        lines = f.read().splitlines()
        
    n = int(lines[0].strip())
    ans = math.comb(n, 4) % 1000000
    
    with open(output_path, 'w') as f:
        f.write(str(ans) + '\n')
        
    print("n:", n)
    print("Result:", ans)

if __name__ == '__main__':
    main()
