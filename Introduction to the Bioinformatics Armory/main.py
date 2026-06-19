import os
import sys

# DNT ardıcıllığındakı hər bir nukleotidin (A, C, G, T) sayını tapırıq
# Count the occurrences of each nucleotide (A, C, G, T) in the DNA string


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_ini.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        sys.exit(1)

    with open(input_path, "r") as f:
        seq = f.read().strip()

    # Hər bir nukleotidi sayırıq
    # Count frequency of each nucleotide
    a_count = seq.count("A")
    c_count = seq.count("C")
    g_count = seq.count("G")
    t_count = seq.count("T")

    result = f"{a_count} {c_count} {g_count} {t_count}"

    # Nəticəni output.txt faylına yazırıq
    # Write the result to output.txt
    with open(output_path, "w") as out:
        out.write(result + "\n")

    print(f"Counts: {result}")


if __name__ == "__main__":
    main()
