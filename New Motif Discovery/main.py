import os
import sys
import math
import collections

def parse_fasta(filepath):
    seqs = []
    curr = []
    with open(filepath) as f:
        for line in f:
            if line.startswith('>'):
                if curr:
                    seqs.append("".join(curr))
                    curr = []
            else:
                curr.append(line.strip())
    if curr:
        seqs.append("".join(curr))
    return seqs

def mismatch_dist(s1, s2):
    return sum(1 for x, y in zip(s1, s2) if x != y)

def best_match_index(kmer, seq):
    best_dist = float('inf')
    best_idx = -1
    for i in range(len(seq) - len(kmer) + 1):
        d = mismatch_dist(kmer, seq[i:i+len(kmer)])
        if d < best_dist:
            best_dist = d
            best_idx = i
    return best_idx, best_dist

def find_seed_20mer(seqs):
    s1 = seqs[0]
    best_kmer = None
    min_max_mismatch = float('inf')
    
    for i in range(len(s1) - 20 + 1):
        kmer = s1[i:i+20]
        max_mismatch = 0
        for seq in seqs[1:]:
            _, dist = best_match_index(kmer, seq)
            if dist > max_mismatch:
                max_mismatch = dist
                
            # Early pruning if this candidate is already worse than or equal to best
            if max_mismatch >= min_max_mismatch:
                break
                
        if max_mismatch < min_max_mismatch:
            min_max_mismatch = max_mismatch
            best_kmer = kmer
                
    return best_kmer, min_max_mismatch

def entropy(col):
    counts = collections.Counter(col)
    N = len(col)
    ent = 0.0
    for char, count in counts.items():
        p = count / N
        ent -= p * math.log2(p)
    return ent

def build_regex_from_alignment(seqs, start_positions, seed_len):
    N = len(seqs)
    threshold = 0.6 * math.log2(min(N, 20))
    print(f"Aligning {N} sequences, entropy threshold: {threshold:.3f}")
    
    # Extend left
    left_ext = 0
    while True:
        valid = True
        col_chars = []
        for i, seq in enumerate(seqs):
            pos = start_positions[i] - left_ext - 1
            if pos < 0:
                valid = False
                break
            col_chars.append(seq[pos])
        if not valid:
            break
        
        if entropy(col_chars) > threshold:
            break
        left_ext += 1
        
    # Extend right
    right_ext = 0
    while True:
        valid = True
        col_chars = []
        for i, seq in enumerate(seqs):
            pos = start_positions[i] + seed_len + right_ext
            if pos >= len(seq):
                valid = False
                break
            col_chars.append(seq[pos])
        if not valid:
            break
        
        if entropy(col_chars) > threshold:
            break
        right_ext += 1
        
    # Build regex
    regex_parts = []
    for offset in range(-left_ext, seed_len + right_ext):
        col_chars = []
        for i, seq in enumerate(seqs):
            pos = start_positions[i] + offset
            col_chars.append(seq[pos])
        unique_chars = sorted(list(set(col_chars)))
        if len(unique_chars) == 1:
            regex_parts.append(unique_chars[0])
        else:
            regex_parts.append("[" + "".join(unique_chars) + "]")
            
    return "".join(regex_parts)

def main():
    # Always resolve paths relative to the script's own directory,
    # so it works regardless of where the user runs it from.
    script_dir = os.path.dirname(os.path.abspath(__file__))

    input_path = None
    for fname in os.listdir(script_dir):
        if fname.startswith('rosalind_') and fname.endswith('.txt'):
            input_path = os.path.join(script_dir, fname)
            break
            
    if input_path is None:
        print("Error: No rosalind_*.txt dataset file found in the script's directory.")
        sys.exit(1)
        
    print(f"Reading from {input_path}")
    seqs = parse_fasta(input_path)
    if not seqs:
        print("Error: No sequences parsed from input file.")
        sys.exit(1)
        
    print(f"Loaded {len(seqs)} sequences. Searching for conserved 20-mer seed...")
    seed, max_mismatch = find_seed_20mer(seqs)
    print(f"Best seed: {seed} (max mismatch: {max_mismatch})")
    
    # Get starting positions for the alignment
    start_positions = []
    for seq in seqs:
        idx, _ = best_match_index(seed, seq)
        start_positions.append(idx)
        
    # Build the regular expression for the motif
    regex = build_regex_from_alignment(seqs, start_positions, 20)
    print(f"Discovered Motif Regex: {regex}")
    
    # Write to output.txt next to the script
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out:
        out.write(regex + "\n")
        
    print(f"Successfully wrote regex to {output_path}")

if __name__ == '__main__':
    main()
