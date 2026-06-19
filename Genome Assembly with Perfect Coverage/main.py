import os

# Tam əhatə dairəsi (perfect coverage) olan oxunuşlardan genomu bərpa edirik
# Assemble genome from reads with perfect coverage


def solve_pcov(input_path, output_path):
    with open(input_path, "r") as f:
        reads = [line.strip() for line in f if line.strip()]

    if not reads:
        return

    # Hər bir prefiks üçün növbəti sufiksi əlaqələndiririk
    # Build transition map: prefix (k-1)-mer -> suffix (k-1)-mer
    successor = {}
    for read in reads:
        prefix = read[:-1]
        suffix = read[1:]
        successor[prefix] = suffix

    # İxtiyari düyündən başlayaraq dövrü gəzirik
    # Traverse the circular genome starting from a node
    start = next(iter(successor))
    genome = [start[0]]
    current = start
    while True:
        nxt = successor[current]
        if nxt == start:
            break
        genome.append(nxt[0])
        current = nxt

    result = "".join(genome)

    with open(output_path, "w") as f:
        f.write(result + "\n")

    print(f"Bərpa edilmiş genomun uzunluğu: {len(result)}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_pcov.txt")
    output_file = os.path.join(script_dir, "output.txt")
    solve_pcov(input_file, output_file)
