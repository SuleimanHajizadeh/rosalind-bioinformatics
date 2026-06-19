import os
import sys
from collections import Counter

def main():
    input_path = "rosalind_ini6.txt"
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        sys.exit(1)
        
    with open(input_path, 'r') as f:
        content = f.read().strip()
        
    words = content.split()
    counts = Counter(words)
    
    output_path = "output.txt"
    with open(output_path, "w") as out:
        for word, count in counts.items():
            out.write(f"{word} {count}\n")
            
    print(f"Counted {len(counts)} unique words and wrote to {output_path}.")

if __name__ == '__main__':
    main()
