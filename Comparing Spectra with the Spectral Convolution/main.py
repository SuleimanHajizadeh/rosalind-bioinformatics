import os

# Spektr konvolusiyasını (spectral convolution) hesablayaraq spektr elementlərinin fərqlərini tapırıq
# Compute the spectral convolution (Minkowski difference) between two spectra s1 and s2


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_conv.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    s1 = [float(x) for x in lines[0].split()]
    s2 = [float(x) for x in lines[1].split()]

    from collections import Counter

    # Minkowski fərqini hesablayırıq: s1 - s2
    # Calculate Minkowski difference: s1 - s2
    diffs = []
    for x in s1:
        for y in s2:
            diffs.append(round(x - y, 5))

    counts = Counter(diffs)

    # Ən yüksək tezliyi olan fərqi və onun tezliyini tapırıq
    # Find the difference with the maximum frequency
    best_diff, max_count = counts.most_common(1)[0]

    print(f"Max frequency: {max_count}, Value: {best_diff}")

    with open(output_path, "w") as f:
        f.write(f"{max_count}\n")
        f.write(f"{best_diff}\n")


if __name__ == "__main__":
    main()
