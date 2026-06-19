import os
import glob


def solve(input_text: str) -> str:
    lines = input_text.strip().split('\n')
    
    # First line: quality threshold q and percentage p
    q, p = map(int, lines[0].split())
    
    # Parse FASTQ records (4 lines each after the first line)
    count = 0
    i = 1
    while i < len(lines):
        # Each FASTQ record: @ID, sequence, +, quality
        if lines[i].startswith('@'):
            # sequence = lines[i + 1]
            quality_str = lines[i + 3]
            
            # Decode Phred quality scores (Sanger encoding: Q + 33)
            quality_scores = [ord(c) - 33 for c in quality_str]
            
            total_bases = len(quality_scores)
            if total_bases == 0:
                i += 4
                continue
            
            high_quality = sum(1 for score in quality_scores if score >= q)
            percentage = (high_quality / total_bases) * 100
            
            if percentage >= p:
                count += 1
            
            i += 4
        else:
            i += 1
    
    return str(count)


def main():
    # Find the dataset file
    dataset_files = glob.glob(os.path.join(os.path.dirname(__file__), 'rosalind_*.txt'))
    
    if not dataset_files:
        print("Error: No rosalind_*.txt dataset file found in the current directory.")
        return
    
    dataset_file = dataset_files[0]
    print(f"Using dataset: {dataset_file}")
    
    with open(dataset_file, 'r') as f:
        input_text = f.read()
    
    result = solve(input_text)
    print(f"Result: {result}")
    
    # Write result to output.txt
    output_file = os.path.join(os.path.dirname(__file__), 'output.txt')
    with open(output_file, 'w') as f:
        f.write(result + '\n')
    print(f"Output written to: {output_file}")


if __name__ == '__main__':
    # Quick verification with sample data from the problem
    sample = """20 90
@Rosalind_0049_1
GCAGAGACCAGTAGATGTGTTTGCGGACGGTCGGGCTCCATGTGACACAG
+
FD@@;C<AI?4BA:=>C<G=:AE=><A??>764A8B797@A:58:527+,
@Rosalind_0049_2
AAGCGACGGGGCTTCACATCAGCJTTGACCGCCTATAATAATGATCATGC
+
=1:>>LA?F8:C:N?LA:=:>BI@<C;N:@;JFCI:N>=C?=;:LB?DD"""
    
    sample_result = solve(sample)
    print(f"Sample result: {sample_result} (expected: 1)")
    
    main()
