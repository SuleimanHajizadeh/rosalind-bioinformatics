import os

# Təsadüfi RNT/DNT zəncirində verilmiş restriksiya ardıcıllığının tapılma sayının riyazi gözləməsini hesablayırıq
# Compute the expected number of restriction sites in a random DNA string for given GC content values


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_eval.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    n = int(lines[0])
    s = lines[1]
    a = list(map(float, lines[2].split()))

    # Motifdəki GC və AT saylarını tapırıq
    # Count frequencies of G/C and A/T in motif s
    gc_count = s.count("G") + s.count("C")
    at_count = s.count("A") + s.count("T")
    motif_len = len(s)

    results = []
    for gc_val in a:
        # Hər bir mövqe üçün uyğunluq ehtimalı
        # Probability of matching single position
        p_gc = gc_val / 2.0
        p_at = (1.0 - gc_val) / 2.0
        prob = (p_gc**gc_count) * (p_at**at_count)
        # Gözlənilən restriksiya sayları (Expected values): (n - len(s) + 1) * prob
        expected = (n - motif_len + 1) * prob
        results.append(f"{expected:.3f}")

    result_str = " ".join(results)
    print(result_str)

    with open(output_path, "w") as f:
        f.write(result_str + "\n")


if __name__ == "__main__":
    main()
