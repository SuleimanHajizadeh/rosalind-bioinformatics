import os
import math

# Verilmiş resessiv fenotip daşıyıcı tezliklərinə əsasən daşıyıcı olma ehtimalını tapırıq
# Compute probability of carrying at least one disease allele given recessive phenotype frequencies


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_afrq.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        content = f.read().strip()

    # q^2 dəyərlərinin massivini oxuyuruq
    # Read recessive phenotype frequencies q^2
    q2_list = list(map(float, content.split()))

    results = []
    for q2 in q2_list:
        # q = sqrt(q^2)
        q = math.sqrt(q2)
        p = 1.0 - q
        # Daşıyıcı (carrier) və ya xəstə olma ehtimalı: 1 - p^2 (2pq + q^2)
        # Probability of carrying at least one copy of allele: 1 - p^2
        prob = 1.0 - (p**2)
        results.append(f"{prob:.3f}")

    result_str = " ".join(results)
    print(result_str)

    with open(output_path, "w") as f:
        f.write(result_str + "\n")


if __name__ == "__main__":
    main()
