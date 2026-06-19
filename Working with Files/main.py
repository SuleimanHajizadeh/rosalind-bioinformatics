import os
import sys

def main():
    input_path = "rosalind_ini5.txt"
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        sys.exit(1)
        
    output_path = "output.txt"
    with open(input_path, 'r') as f_in, open(output_path, 'w') as f_out:
        # Enumerate lines using 1-based indexing
        for idx, line in enumerate(f_in, start=1):
            if idx % 2 == 0:
                f_out.write(line)
                
    print(f"Successfully filtered even-numbered lines and wrote to {output_path}.")

if __name__ == '__main__':
    main()
