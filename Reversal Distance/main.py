import os

# İki permutasiya cütü arasındakı reversal məsafəsini (reversal distance) tapırıq
# Compute the reversal distance for pairs of permutations using BFS


def solve_reversal(p1, p2):
    # Birinci permutasiyanı identik sıraya gətirmək üçün indeksləri uyğunlaşdırırıq
    # Map elements of p1 to range 1..n for optimization
    n = len(p1)
    mapping = {val: i + 1 for i, val in enumerate(p1)}
    start = tuple(mapping[x] for x in p1)
    target = tuple(mapping[x] for x in p2)

    if start == target:
        return 0

    # İkitərəfli BFS
    # Bidirectional BFS
    q_start = {start}
    q_target = {target}
    vis_start = {start: 0}
    vis_target = {target: 0}

    dist = 0
    while q_start and q_target:
        if len(q_start) <= len(q_target):
            next_q = set()
            for curr in q_start:
                curr_d = vis_start[curr]
                # Bütün reversal keçidləri tapırıq
                # Try all possible reversals
                for i in range(n):
                    for j in range(i + 1, n):
                        nxt = curr[:i] + curr[i : j + 1][::-1] + curr[j + 1 :]
                        if nxt in vis_target:
                            return curr_d + 1 + vis_target[nxt]
                        if nxt not in vis_start:
                            vis_start[nxt] = curr_d + 1
                            next_q.add(nxt)
            q_start = next_q
        else:
            next_q = set()
            for curr in q_target:
                curr_d = vis_target[curr]
                for i in range(n):
                    for j in range(i + 1, n):
                        nxt = curr[:i] + curr[i : j + 1][::-1] + curr[j + 1 :]
                        if nxt in vis_start:
                            return curr_d + 1 + vis_start[nxt]
                        if nxt not in vis_target:
                            vis_target[nxt] = curr_d + 1
                            next_q.add(nxt)
            q_target = next_q
    return -1


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_rear.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    # Permutasiya cütlərini oxuyuruq
    # Read permutation pairs from the input file
    pairs = []
    current_pair = []
    with open(input_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            perm = tuple(map(int, line.split()))
            current_pair.append(perm)
            if len(current_pair) == 2:
                pairs.append(current_pair)
                current_pair = []

    results = []
    for p1, p2 in pairs:
        dist = solve_reversal(p1, p2)
        results.append(str(dist))

    result_str = " ".join(results)
    print(result_str)

    with open(output_path, "w") as f:
        f.write(result_str + "\n")


if __name__ == "__main__":
    main()
