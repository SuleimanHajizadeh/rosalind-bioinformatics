import os

# Uyuşmayan simvol bölünmələrini (splits) aşkarlayaraq aradan qaldırırıq
# Detect and filter out incompatible character splits (inconsistent characters)


def is_compatible(c1, c2, n):
    # İki simvol bölünməsinin uyuşan olub-olmadığını yoxlayırıq
    # Check if two character splits are compatible
    if not (c1 & c2):
        return True
    if c1.issubset(c2):
        return True
    if c2.issubset(c1):
        return True
    if len(c1 | c2) == n:
        return True
    return False


def check_consistency(char_sets, n):
    # Bütün bölünmələrin bir-biri ilə uyuşmasını yoxlayırıq
    # Check pairwise consistency for all splits
    num = len(char_sets)
    for i in range(num):
        for j in range(i + 1, num):
            if not is_compatible(char_sets[i], char_sets[j], n):
                return False, i, j
    return True, -1, -1


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_cset.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    n = len(lines[0])
    char_sets = []
    # Bölünmələri çoxluq şəklində yadda saxlayırıq (yalnız 1 olan mövqelər)
    # Store indices where state is '1' in each split
    for line in lines:
        c_set = {i for i in range(n) if line[i] == "1"}
        char_sets.append(c_set)

    consistent, bad_i, bad_j = check_consistency(char_sets, n)

    # Uyuşmayan bölünməni çıxarıb qalanını saxlayırıq
    # Remove the split causing inconsistency
    with open(output_path, "w") as f:
        for idx in range(len(lines)):
            if idx == bad_i:
                continue
            f.write(lines[idx] + "\n")

    print(f"Removed split index: {bad_i}")


if __name__ == "__main__":
    main()
