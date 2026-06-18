import os

def read_fasta(file_path):
    sequences = []
    current_seq = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_seq:
                    sequences.append("".join(current_seq))
                    current_seq = []
            else:
                current_seq.append(line)
        if current_seq:
            sequences.append("".join(current_seq))
    return sequences

def p_distance(s1, s2):
    assert len(s1) == len(s2)
    diff = sum(1 for c1, c2 in zip(s1, s2) if c1 != c2)
    return diff / len(s1)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_pdst.txt")
    
    sequences = read_fasta(input_path)
    n = len(sequences)
    
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            matrix[i][j] = p_distance(sequences[i], sequences[j])
            
    # Format the matrix as space-separated values, each with 5 decimal places
    output_lines = []
    for row in matrix:
        row_str = " ".join(f"{val:.5f}" for val in row)
        output_lines.append(row_str)
        
    result_str = "\n".join(output_lines)
    print("Nəticə matrisi:")
    print(result_str)
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        out_file.write(result_str + "\n")

if __name__ == "__main__":
    main()
