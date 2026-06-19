import os
import sys

# İki ədədin kvadratlar cəmini hesablayırıq
# Compute the sum of the squares of two integers a and b


def main():
    input_path = "rosalind_ini2.txt"
    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        sys.exit(1)

    with open(input_path, "r") as f:
        line = f.read().strip()

    parts = line.split()
    a = int(parts[0])
    b = int(parts[1])

    # Kvadratların cəmini tapırıq
    # Compute a^2 + b^2
    result = a**2 + b**2

    # Cavabı output.txt faylına yazırıq
    # Save the result to output.txt
    output_path = "output.txt"
    with open(output_path, "w") as out:
        out.write(f"{result}\n")

    print(result)


if __name__ == "__main__":
    main()
