import os

# İki permutasiya arasındakı ən qısa reversal məsafəsini (reversal distance) tapırıq
# Compute the reversal distance and sorting steps using bidirectional BFS


def read_input(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    p1 = tuple(map(int, lines[0].split()))
    p2 = tuple(map(int, lines[1].split()))
    return p1, p2


def get_reversals_with_indices(p):
    # Permutasiya üzərində bütün mümkün tərsinə çevirmələri (reversals) və indekslərini tapırıq
    # Generate all possible reversals of p and return their indices
    n = len(p)
    results = []
    for i in range(n):
        for j in range(i + 1, n):
            rev_p = p[:i] + p[i : j + 1][::-1] + p[j + 1 :]
            results.append((rev_p, (i + 1, j + 1)))
    return results


def solve_sorting_by_reversals(p1, p2):
    if p1 == p2:
        return 0, []

    start = p1
    target = p2

    q_start = {start}
    q_target = {target}

    visited_start = {start: (None, None)}
    visited_target = {target: (None, None)}

    # İkitərəfli BFS (bidirectional BFS)
    # Run Bidirectional BFS to find the shortest sorting path
    while q_start and q_target:
        if len(q_start) <= len(q_target):
            next_q = set()
            for curr in q_start:
                for nxt, move in get_reversals_with_indices(curr):
                    if nxt in visited_target:
                        visited_start[nxt] = (curr, move)
                        return reconstruct_path(
                            nxt, visited_start, visited_target
                        )
                    if nxt not in visited_start:
                        visited_start[nxt] = (curr, move)
                        next_q.add(nxt)
            q_start = next_q
        else:
            next_q = set()
            for curr in q_target:
                for nxt, move in get_reversals_with_indices(curr):
                    if nxt in visited_start:
                        visited_target[nxt] = (curr, move)
                        return reconstruct_path(
                            nxt, visited_start, visited_target
                        )
                    if nxt not in visited_target:
                        visited_target[nxt] = (curr, move)
                        next_q.add(nxt)
            q_target = next_q

    return -1, []


def reconstruct_path(meeting_node, visited_start, visited_target):
    # Tapılmış görüş düyünündən yolu (path) bərpa edirik
    # Reconstruct the optimal sorting path from the meeting node
    path_forward = []
    curr = meeting_node
    while True:
        parent, move = visited_start[curr]
        if parent is None:
            break
        path_forward.append(move)
        curr = parent
    path_forward.reverse()

    path_backward = []
    curr = meeting_node
    while True:
        parent, move = visited_target[curr]
        if parent is None:
            break
        path_backward.append(move)
        curr = parent

    total_moves = path_forward + path_backward
    return len(total_moves), total_moves


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_rear.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    p1, p2 = read_input(input_path)
    dist, moves = solve_sorting_by_reversals(p1, p2)

    with open(output_path, "w") as f:
        f.write(f"{dist}\n")

    print(f"Reversal Distance: {dist}")


if __name__ == "__main__":
    main()
