import os

# Təsadüfi nəsildə müəyyən motifin tapılma ehtimalını hesablayırıq
# Compute the probability of matching a random motif at least once given GC content x and count N


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_rstr.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    first_line = lines[0].split()
    N = int(first_line[0])
    x = float(first_line[1])
    s = lines[1]

    # GC və AT nukleotidlərini sayırıq
    # Count GC and AT nucleotides in the motif
    gc_count = s.count("G") + s.count("C")
    at_count = s.count("A") + s.count("T")

    # Tək sətirdə uyuşma ehtimalı
    # Probability of a single match based on GC content
    p_single = ((x / 2.0) ** gc_count) * (((1.0 - x) / 2.0) ** at_count)

    # Ən azı bir dəfə uyuşma ehtimalı: 1 - (1 - p_single)^N
    # Probability of at least one match: 1 - (1 - p_single)^N
    prob = 1.0 - (1.0 - p_single) ** N

    print(f"Probability: {prob:.3f}")

    with open(output_path, "w") as f:
        f.write(f"{prob:.3f}\n")


if __name__ == "__main__":
    main()
