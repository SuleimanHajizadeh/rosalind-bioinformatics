import os
import math

# Verilmiş GC faizləri üzrə təsadüfi DNT zəncirinin mövcud olanla eyni olması ehtimalının loqarifmini tapırıq
# Compute the common logarithm (log10) of the probability that a random DNA string matches a given one


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_prob.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as file:
        lines = file.read().splitlines()

    s = lines[0].strip()
    a = list(map(float, lines[1].split()))

    # Sətirdəki G+C və A+T sayını hesablayırıq
    # Count occurrences of G/C and A/T in the sequence
    gc_count = s.count("G") + s.count("C")
    at_count = s.count("A") + s.count("T")

    results = []
    # Hər bir GC faizi (gc_val) üçün ehtimalı loqarifmik olaraq hesablayırıq
    # Compute log10 probability for each GC value in the array
    for gc_val in a:
        # G və ya C olma ehtimalı gc_val / 2, A və ya T olma ehtimalı (1 - gc_val) / 2
        # Probability of G or C is gc_val / 2, and A or T is (1 - gc_val) / 2
        prob_log = gc_count * math.log10(gc_val / 2) + at_count * math.log10(
            (1.0 - gc_val) / 2
        )
        results.append(f"{prob_log:.3f}")

    result_str = " ".join(results)
    print(result_str)

    with open(output_path, "w") as out_file:
        out_file.write(result_str + "\n")


if __name__ == "__main__":
    main()
