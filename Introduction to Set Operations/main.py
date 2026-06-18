import os

def parse_set(s):
    s = s.strip()
    if s.startswith('{') and s.endswith('}'):
        s = s[1:-1]
    parts = s.split(',')
    elements = set()
    for part in parts:
        part = part.strip()
        if part:
            elements.add(int(part))
    return elements

def format_set(s):
    return "{" + ", ".join(map(str, sorted(list(s)))) + "}"

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_seto.txt")
    
    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
        
    n = int(lines[0])
    A = parse_set(lines[1])
    B = parse_set(lines[2])
    
    U = set(range(1, n + 1))
    
    # 6 set operations
    union = A.union(B)
    intersection = A.intersection(B)
    diff_a_b = A.difference(B)
    diff_b_a = B.difference(A)
    comp_a = U.difference(A)
    comp_b = U.difference(B)
    
    results = [
        format_set(union),
        format_set(intersection),
        format_set(diff_a_b),
        format_set(diff_b_a),
        format_set(comp_a),
        format_set(comp_b)
    ]
    
    result_str = "\n".join(results)
    print("Nəticənin ilk bir neçə simvolu:")
    print("\n".join(r[:100] + " ..." if len(r) > 100 else r for r in results))
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        out_file.write(result_str + "\n")

if __name__ == "__main__":
    main()
