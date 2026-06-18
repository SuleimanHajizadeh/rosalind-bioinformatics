import os
import math

def read_input(file_path):
    with open(file_path, "r") as f:
        line = f.readline().strip()
    if not line:
        raise ValueError("Input file is empty")
    return int(line)

def solve_independent_segregation(n):
    # Total number of chromosomes is 2n
    N = 2 * n
    total_outcomes = 2 ** N
    
    # Precompute binomial coefficients
    comb_vals = [math.comb(N, j) for j in range(N + 1)]
    
    # Suffix sums of binomial coefficients: suffix_sums[k] = sum_{j=k}^{2N} comb_vals[j]
    suffix_sums = [0] * (N + 2)
    for j in range(N, -1, -1):
        suffix_sums[j] = suffix_sums[j + 1] + comb_vals[j]
        
    log_probs = []
    for k in range(1, N + 1):
        prob = suffix_sums[k] / total_outcomes
        log_val = math.log10(prob)
        # Avoid formatting negative zero (-0.000)
        if abs(log_val) < 1e-9:
            log_val = 0.0
        log_probs.append(log_val)
        
    return log_probs

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_indc.txt")
    
    print(f"Reading input from: {input_path}")
    n = read_input(input_path)
    print(f"Homologous pairs count n: {n}")
    print(f"Total chromosomes: {2 * n}")
    
    log_probs = solve_independent_segregation(n)
    
    # Format output as space-separated values with 3 decimal places
    # Convert -0.000 to 0.000 to avoid negative zero formatting
    formatted_probs = []
    for x in log_probs:
        val_str = f"{x:.3f}"
        if val_str == "-0.000":
            val_str = "0.000"
        formatted_probs.append(val_str)
    output_str = " ".join(formatted_probs)
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        out_file.write(output_str + "\n")
        
    print(f"Results successfully written to: {output_path}")

if __name__ == "__main__":
    main()
