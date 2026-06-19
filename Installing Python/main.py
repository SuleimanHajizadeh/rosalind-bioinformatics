import os
import sys

# Zen of Python prinsipini ekrana yazdırıb nəticəni fayla qeyd edirik
# Capture and write the Zen of Python message to output.txt


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "output.txt")

    # Zen of Python idxal edərək mətni tuturuq
    # Capture Zen of Python output by redirecting stdout temporarily
    import io

    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    import this

    sys.stdout = old_stdout
    zen_text = new_stdout.getvalue()

    print(zen_text[:100] + "...")

    # Nəticəni output.txt faylına yazırıq
    # Write to output.txt
    with open(output_path, "w") as f:
        f.write(zen_text)


if __name__ == "__main__":
    main()
