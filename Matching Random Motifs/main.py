import os

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_rstr.txt")
    
    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
        
    first_line = lines[0].split()
    N = int(first_line[0])
    x = float(first_line[1])
    s = lines[1]
    
    # Count GC and AT
    gc_count = s.count('G') + s.count('C')
    at_count = s.count('A') + s.count('T')
    
    # Probability of single match
    p = ((x / 2.0) ** gc_count) * (((1.0 - x) / 2.0) ** at_count)
    
    # Probability of at least one match in N trials
    prob_at_least_one = 1.0 - ((1.0 - p) ** N)
    
    # Format to 3 decimal places
    result_str = f"{prob_at_least_one:.3f}"
    print(f"N = {N}, x = {x}, s = {s}")
    print(f"Bir sətir üçün ehtimal p = {p}")
    print(f"Yekun ehtimal (ən azı biri) = {result_str}")
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        out_file.write(result_str + "\n")

if __name__ == "__main__":
    main()
