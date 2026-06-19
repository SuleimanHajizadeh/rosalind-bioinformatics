#!/usr/bin/env python3
import os
import sys

# Rekursiya limitini artırırıq
# Increase recursion depth for Eulerian cycle search
sys.setrecursionlimit(2000)


def solve_grep(reads):
    if not reads:
        return []

    s1 = reads[0]
    k = len(s1) - 1
    num_edges = len(reads)

    # De Bruijn qrafını qururuq
    # Build unique adjacency list and track edge counts
    adj = {}
    edges_count = {}
    for r in reads:
        edges_count[r] = edges_count.get(r, 0) + 1
        u = r[:k]
        v = r[1:]
        if u not in adj:
            adj[u] = set()
        adj[u].add((v, r))

    for u in adj:
        adj[u] = list(adj[u])

    start_node = s1[:k]
    first_suffix = s1[1:]

    # s1 tilinin sayını 1 azaldırıq
    # Decrement count of the start read s1
    edges_count[s1] -= 1

    solutions = []

    # DFS ilə Eulerian dövrlərini axtarırıq
    # Run DFS to find all circular genome reconstructions (Eulerian cycles)
    def dfs(curr_node, path):
        if len(path) == num_edges:
            if curr_node == start_node:
                circ_str = "".join(edge[0] for edge in path)
                solutions.append(circ_str)
            return

        if curr_node in adj:
            for neighbor, edge in adj[curr_node]:
                if edges_count[edge] > 0:
                    edges_count[edge] -= 1
                    path.append(edge)
                    dfs(neighbor, path)
                    path.pop()
                    edges_count[edge] += 1

    dfs(first_suffix, [s1])
    edges_count[s1] += 1

    return sorted(list(set(solutions)))


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_grep.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        reads = [line.strip() for line in f if line.strip()]

    solutions = solve_grep(reads)
    print(f"Complete circular strings: {len(solutions)}")

    with open(output_path, "w") as f:
        for sol in solutions:
            f.write(sol + "\n")


if __name__ == "__main__":
    main()
