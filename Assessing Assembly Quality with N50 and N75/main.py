import os

# Ardıcıllıq yığımlarının keyfiyyətini qiymətləndirmək üçün N50 və N75 statistikalarını hesablayırıq
# Calculate N50 and N75 statistics to assess assembly quality


def calculate_nxx(lengths, total_len, xx):
    # Müəyyən edilmiş faiz həddini (məs. 50% və ya 75%) hesablayırıq
    # Calculate the threshold based on the specified percentage (e.g., 50% or 75%)
    threshold = total_len * (xx / 100.0)
    current_sum = 0
    # Sıralanmış uzunluqları cəmləyərək həddi keçən ilk uzunluğu tapırıq
    # Accumulate lengths and return the first one that meets or exceeds the threshold
    for length in lengths:
        current_sum += length
        if current_sum >= threshold:
            return length
    return 0


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_asmq.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    # Giriş faylından ardıcıllıqları oxuyuruq
    # Read the sequences from the input file
    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Ardıcıllıqların uzunluqlarını böyükdən kiçiyə sıralayırıq
    # Sort sequence lengths in descending order
    lengths = sorted([len(s) for s in lines], reverse=True)
    total_len = sum(lengths)

    # N50 və N75 dəyərlərini hesablayırıq
    # Calculate N50 and N75 values
    n50 = calculate_nxx(lengths, total_len, 50)
    n75 = calculate_nxx(lengths, total_len, 75)

    print(f"N50: {n50}, N75: {n75}")

    # Nəticələri output.txt faylına yazırıq
    # Write the results to output.txt
    with open(output_path, "w") as f:
        f.write(f"{n50} {n75}
")


if __name__ == "__main__":
    main()
