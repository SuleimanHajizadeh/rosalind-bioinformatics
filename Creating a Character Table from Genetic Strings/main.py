import os
import sys

def solve_cstr(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} not found.")
        return
        
    with open(input_path, 'r') as f:
        strings = [line.strip() for line in f if line.strip()]
        
    if not strings:
        print("Error: Empty input file.")
        return
        
    num_species = len(strings)
    seq_len = len(strings[0])
    print(f"Number of species: {num_species}")
    print(f"Sequence length: {seq_len}")
    
    nontrivial_chars = []
    
    for j in range(seq_len):
        col_chars = [strings[i][j] for i in range(num_species)]
        unique_chars = sorted(list(set(col_chars)))
        
        if len(unique_chars) != 2:
            continue
            
        state1 = col_chars[0]
        binary_list = []
        for char in col_chars:
            if char == state1:
                binary_list.append('1')
            else:
                binary_list.append('0')
                
        count1 = binary_list.count('1')
        count0 = binary_list.count('0')
        
        if count1 >= 2 and count0 >= 2:
            nontrivial_chars.append("".join(binary_list))
            
    with open(output_path, 'w') as f:
        for char_str in nontrivial_chars:
            f.write(char_str + '\n')
            
    print(f"Found {len(nontrivial_chars)} nontrivial characters.")
    print(f"Result written to {output_path}")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_cstr.txt")
    output_file = os.path.join(script_dir, "output.txt")
    solve_cstr(input_file, output_file)
