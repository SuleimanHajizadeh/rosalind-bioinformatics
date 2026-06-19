#!/usr/bin/env python3
import os

# 4 FASTA ardıcıllığının qlobal çoxlu düzülüş xalını hesablayırıq
# Compute the multiple alignment score of 4 sequences


def read_fasta(file_path):
    sequences = []
    current_seq = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_seq:
                    sequences.append("".join(current_seq))
                    current_seq = []
            else:
                current_seq.append(line)
        if current_seq:
            sequences.append("".join(current_seq))
    return sequences


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_mult.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    seqs = read_fasta(input_path)
    # 4 ardıcıllığı çoxlu düzürük
    # Align the 4 sequences using dynamic programming
    pass
