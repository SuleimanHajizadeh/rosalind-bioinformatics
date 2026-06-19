import os
import sys
from collections import Counter

# Mətndəki hər bir sözün təkrarlanma sayını tapırıq
# Count the occurrences of each word in the input text


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_ini6.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        sys.exit(1)

    with open(input_path, "r") as f:
        content = f.read().strip()

    # Mətni sözlərə bölürük və tezliklərini sayırıq
    # Split text into words and count their frequencies
    words = content.split()
    counts = Counter(words)

    # Nəticəni output.txt faylına yazırıq
    # Write the result to output.txt
    with open(output_path, "w") as out:
        for word, count in counts.items():
            out.write(f"{word} {count}\n")

    print(f"Sözlərin sayı: {len(counts)}")


if __name__ == "__main__":
    main()
