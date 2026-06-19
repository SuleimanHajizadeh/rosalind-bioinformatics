import os

# Komplementar zənciri tapırıq
# Helper to get the reverse complement of a sequence


def reverse_complement(s):
    comp = {"A": "T", "T": "A", "C": "G", "G": "C"}
    return "".join(comp[c] for c in reversed(s))


def solve_gasm(input_path, output_path):
    with open(input_path, "r") as f:
        reads = [line.strip() for line in f if line.strip()]

    if not reads:
        print("Oxunuşlar tapılmadı!")
        return

    L = len(reads[0])

    # K-mer ölçüsünü (k) azaldaraq qrafı qurub yoxlayırıq
    # Try decreasing k sizes to find the single circular genome path
    for k in range(L - 1, 0, -1):
        edges = set()
        for r in reads:
            r_rc = reverse_complement(r)
            for i in range(len(r) - k):
                edges.add(r[i : i + k + 1])
                edges.add(r_rc[i : i + k + 1])

        # De Bruijn qrafının adjacency siyahısını qururuq
        # Build De Bruijn graph: nodes are k-mers, edges are (k+1)-mers
        adj = {}
        in_degree = {}
        for edge in edges:
            u = edge[:-1]
            v = edge[1:]
            adj.setdefault(u, []).append(v)
            in_degree[v] = in_degree.get(v, 0) + 1
            in_degree.setdefault(u, 0)

        # Hər bir düyünün giriş və çıxış dərəcəsini yoxlayırıq (tək dövr olması üçün 1 olmalıdır)
        # Verify if each node has in-degree == 1 and out-degree == 1 (Eulerian cycle)
        if any(len(targets) != 1 for targets in adj.values()):
            continue
        if any(deg != 1 for deg in in_degree.values()):
            continue

        # Eulerian dövrü üzrə genomu bərpa edirik
        # Traverese the cycle to reconstruct the genome
        start = next(iter(adj))
        curr = start
        path = []
        while True:
            path.append(curr[0])
            curr = adj[curr][0]
            if curr == start:
                break
        genome = "".join(path)

        with open(output_path, "w") as f:
            f.write(genome + "\n")

        print(f"Genom uzunluğu (k={k}): {len(genome)}")
        return


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_gasm.txt")
    output_file = os.path.join(script_dir, "output.txt")
    solve_gasm(input_file, output_file)
