import os

def solve_pcov(input_path, output_path):
    with open(input_path, 'r') as f:
        reads = [line.strip() for line in f if line.strip()]

    if not reads:
        return

    k = len(reads[0])

    # Build successor map: prefix (k-1)-mer -> suffix (k-1)-mer
    # With perfect coverage each prefix has exactly one successor
    successor = {}
    for read in reads:
        prefix = read[:-1]
        suffix = read[1:]
        successor[prefix] = suffix

    # Walk the cycle starting from an arbitrary node
    start = next(iter(successor))
    genome = [start[0]]  # first character of each node in the path
    current = start
    while True:
        nxt = successor[current]
        if nxt == start:
            break
        genome.append(nxt[0])
        current = nxt

    result = ''.join(genome)

    with open(output_path, 'w') as f:
        f.write(result + '\n')

    print(result)


if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    input_path  = os.path.join(base, 'rosalind_pcov.txt')
    output_path = os.path.join(base, 'output.txt')
    solve_pcov(input_path, output_path)
