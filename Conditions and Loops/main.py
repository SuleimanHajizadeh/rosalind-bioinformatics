import os
import sys

# Tək ədədlərin cəmini müəyyən edilmiş aralıqda (a-dan b-yə qədər) hesablayırıq
# Calculate sum of all odd integers between a and b, inclusive


def main():
    input_path = "rosalind_ini4.txt"
    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        sys.exit(1)

    with open(input_path, "r") as f:
        line = f.read().strip()

    parts = line.split()
    a = int(parts[0])
    b = int(parts[1])

    # Tək ədədlərin cəmini tapırıq
    # Perform summation of odd numbers
    total = sum(i for i in range(a, b + 1) if i % 2 != 0)

    # Nəticəni output.txt faylına yazırıq
    # Write the result to output.txt
    output_path = "output.txt"
    with open(output_path, "w") as out:
        out.write(f"{total}\n")

    print(total)


if __name__ == "__main__":
    main()
