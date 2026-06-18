#!/usr/bin/env python3
import os
import sys

# Increase recursion depth just in case the string is long
sys.setrecursionlimit(3000)

class Node:
    def __init__(self):
        self.children = {}
        self.leaves = []

def insert_suffix(root, s, p):
    curr = root
    curr.leaves.append(p)
    for char in s[p:]:
        if char not in curr.children:
            curr.children[char] = Node()
        curr = curr.children[char]
        curr.leaves.append(p)

def find_maximal_repeats(s, min_len=20):
    root = Node()
    s_ext = s + "$"
    for p in range(len(s_ext)):
        insert_suffix(root, s_ext, p)
        
    maximal_repeats = []
    
    def dfs(node, path_chars):
        path_str = "".join(path_chars)
        if "$" in path_str:
            return
            
        if len(path_str) >= min_len and len(node.children) >= 2:
            # Check left-maximal condition
            left_chars = set()
            for p in node.leaves:
                if p > 0:
                    left_chars.add(s_ext[p-1])
                else:
                    left_chars.add('Null')
            if len(left_chars) >= 2:
                maximal_repeats.append(path_str)
                
        for char, child in node.children.items():
            path_chars.append(char)
            dfs(child, path_chars)
            path_chars.pop()
            
    dfs(root, [])
    return maximal_repeats

def main():
    input_path = "rosalind_mrep.txt"
    output_path = "output.txt"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    with open(input_path, 'r') as f:
        # Strip newlines and spaces
        content = "".join(line.strip() for line in f if line.strip())
        
    if not content:
        print("Error: Input file is empty.")
        return
        
    print(f"Input string length: {len(content)}")
    
    repeats = find_maximal_repeats(content, 20)
    print(f"Found {len(repeats)} maximal repeats of length >= 20.")
    
    with open(output_path, 'w') as f:
        for r in repeats:
            f.write(r + "\n")
    print(f"Results written to {output_path}")

if __name__ == "__main__":
    main()
