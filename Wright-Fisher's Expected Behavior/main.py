#!/usr/bin/env python3
import os

# Binomial paylanmaya əsasən dominant allellərin riyazi gözləməsini hesablayırıq
# Compute the expected number of dominant alleles under Wright-Fisher model (n * p)


def main():
    input_path = "rosalind_ebin.txt"
    output_path = "output.txt"

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    n = int(lines[0])
    p_values = [float(x) for x in lines[1].split()]

    # Riyazi gözləmə düsturu: E = n * p
    # Expected value is n * p
    expected_values = [n * p for p in p_values]

    # Nəticələri yuvarlaqlaşdırıb boşluqla birləşdiririk
    # Format floating numbers to 3 decimal places
    formatted_vals = []
    for val in expected_values:
        formatted_vals.append(str(round(val, 3)))

    output_str = " ".join(formatted_vals)
    print(f"Expected: {output_str}")

    with open(output_path, "w") as f:
        f.write(output_str + "\n")


if __name__ == "__main__":
    main()
