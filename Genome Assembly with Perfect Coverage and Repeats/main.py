#!/usr/bin/env python3
import os
import sys

# Increase recursion depth for safety
sys.setrecursionlimit(2000)

def solve_grep(reads):
    if not reads:
        return []
        
    s1 = reads[0]
    k = len(s1) - 1
    num_edges = len(reads)
    
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
        
    # Convert sets to lists for ordered iteration
    for u in adj:
        adj[u] = list(adj[u])
        
    # We must start with the first read s1
    start_node = s1[:k]
    first_suffix = s1[1:]
    
    # Decrement count of s1
    edges_count[s1] -= 1
    
    solutions = []
    
    def dfs(curr_node, path):
        if len(path) == num_edges:
            if curr_node == start_node:
                # Assemble the circular string starting with s1
                # Taking the first character of each edge in the path
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
    
    # Restore count of s1
    edges_count[s1] += 1
    
    return sorted(list(set(solutions)))

def main():
    input_path = "rosalind_grep.txt"
    output_path = "output.txt"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    with open(input_path, "r") as f:
        reads = [line.strip() for line in f if line.strip()]
        
    if not reads:
        print("Error: Empty input file.")
        return
        
    print(f"Read {len(reads)} (k+1)-mers of length {len(reads[0])}.")
    solutions = solve_grep(reads)
    print(f"Found {len(solutions)} complete circular strings.")
    
    with open(output_path, "w") as f:
        for sol in solutions:
            f.write(sol + "\n")
            
    print(f"Results written to {output_path}")

if __name__ == "__main__":
    main()
