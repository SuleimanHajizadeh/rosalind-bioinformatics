import os

def get_overlap(s1, s2, threshold):
    # İki ardıcıllıq arasındakı ən uzun üst-üstə düşən (overlap) hissəni tapır
    # Overlap orijinal oxunuşun yarısından çox olmalıdır (threshold)
    max_possible_overlap = min(len(s1), len(s2))
    for length in range(max_possible_overlap - 1, threshold, -1):
        if s2.startswith(s1[len(s1) - length:]):
            return length
    return 0

def solve_superstring(reads):
    # Başqa oxunuşların içində tam yerləşən (substring) oxunuşları təmizləyirik
    reads = [r for r in reads if not any(r in other for other in reads if r != other)]
    
    # İlkin oxunuşların ən qısa olanının yarısını threshold kimi təyin edirik
    min_len = min(len(r) for r in reads)
    threshold = min_len // 2

    # Bütün oxunuşlar (reads) vahid bir ardıcıllıq olana qədər birləşdirir
    while len(reads) > 1:
        max_overlap = 0
        best_pair = (0, 1)
        merged_str = ""

        # Ən çox overlap edən cütü tapırıq
        for i in range(len(reads)):
            for j in range(len(reads)):
                if i != j:
                    overlap = get_overlap(reads[i], reads[j], threshold)
                    if overlap > max_overlap:
                        max_overlap = overlap
                        best_pair = (i, j)
                        merged_str = reads[i] + reads[j][overlap:]

        i, j = best_pair
        new_reads = [reads[k] for k in range(len(reads)) if k != i and k != j]
        new_reads.append(merged_str)
        reads = new_reads
    return reads[0]

# Faylın olduğu qovluğu avtomatik tapırıq
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "rosalind_long.txt")

# Faylı oxuyuruq
with open(file_path, "r") as f:
    reads = []
    curr = ""
    for line in f:
        line = line.strip()
        if not line: continue
        if line.startswith(">"):
            if curr: reads.append(curr)
            curr = ""
        else:
            curr += line
    if curr: reads.append(curr)

# Xromosomu bərpa edirik
final_chromosome = solve_superstring(reads)

# Nəticəni fayla yazırıq
output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as f:
    f.write(final_chromosome)

print(f"Əməliyyat tamamlandı! Nəticə bu fayldadır: {output_path}")