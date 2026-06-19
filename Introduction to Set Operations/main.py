import os

# Çoxluqlar üzərində birləşmə, kəsişmə, fərq və komplement əməliyyatlarını yerinə yetiririk
# Perform set operations (union, intersection, difference, complement) for sets A and B


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_seto.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as file:
        lines = file.read().splitlines()

    n = int(lines[0].strip())
    # Universal çoxluq U = {1, 2, ..., n}
    # Universal set U = {1, 2, ..., n}
    U = set(range(1, n + 1))

    # A və B çoxluqlarını oxuyuruq
    # Parse sets A and B from strings
    A = set(map(int, lines[1].strip("{}").split(",")))
    B = set(map(int, lines[2].strip("{}").split(",")))

    # Əməliyyatları yerinə yetiririk
    # Apply standard set operations
    union_set = A | B
    intersection_set = A & B
    diff_a_b = A - B
    diff_b_a = B - A
    comp_a = U - A
    comp_b = U - B

    # Formatlayaraq fayla yazırıq
    # Write set outputs in mathematical notation
    def format_set(s):
        return "{" + ", ".join(map(str, sorted(list(s)))) + "}"

    with open(output_path, "w") as out:
        out.write(format_set(union_set) + "\n")
        out.write(format_set(intersection_set) + "\n")
        out.write(format_set(diff_a_b) + "\n")
        out.write(format_set(diff_b_a) + "\n")
        out.write(format_set(comp_a) + "\n")
        out.write(format_set(comp_b) + "\n")

    print("Çoxluq əməliyyatları tamamlandı.")


if __name__ == "__main__":
    main()
