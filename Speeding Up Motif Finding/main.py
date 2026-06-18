import os

def main():
    # 1. Faylın yerləşdiyi qovluğu tapırıq və FASTA faylını oxuyuruq
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_kmp.txt")
    
    dna_seq = ""
    with open(input_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line.startswith(">"):
                dna_seq += line

    # 2. KMP (Knuth-Morris-Pratt) alqoritminin "failure array" (pi) massivini hesablayırıq
    n = len(dna_seq)
    pi = [0] * n
    
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and dna_seq[i] != dna_seq[j]:
            j = pi[j - 1]
        if dna_seq[i] == dna_seq[j]:
            j += 1
        pi[i] = j

    # 3. Massivi aralarında boşluq olan sətir şəklinə salırıq
    result_str = " ".join(map(str, pi))

    # 4. Nəticəni həm ekrana çıxarırıq (ilk 200 simvol), həm də output.txt faylına yazırıq
    print("Nəticənin başlanğıcı:", result_str[:200] + " ...")
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        out_file.write(result_str + "\n")

if __name__ == "__main__":
    main()
