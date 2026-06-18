import os
import sys

def solve_afrq(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} not found.")
        return
        
    with open(input_path, 'r') as f:
        content = f.read().strip()
        
    if not content:
        print("Error: Empty input file.")
        return
        
    proportions = [float(x) for x in content.split()]
    print(f"Read {len(proportions)} proportions.")
    
    results = []
    for q_squared in proportions:
        q = q_squared**0.5
        p = 1.0 - q
        # Probability of having at least one recessive allele is 1 - p^2
        carrier_prob = 1.0 - p**2
        results.append(str(round(carrier_prob, 3)))
        
    result_str = " ".join(results)
    
    with open(output_path, 'w') as f:
        f.write(result_str + '\n')
        
    print(f"Result written to {output_path}")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_afrq.txt")
    output_file = os.path.join(script_dir, "output.txt")
    solve_afrq(input_file, output_file)
