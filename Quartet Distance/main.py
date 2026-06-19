import os
import sys

# İki ağac arasındakı kvartet məsafəsini (quartet distance) hesablayırıq
# Compute quartet distance between two unrooted binary trees


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_qrtd.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    # Kvartetlərin fərqini tapırıq
    # Find distance between quartets
    pass


if __name__ == "__main__":
    main()
