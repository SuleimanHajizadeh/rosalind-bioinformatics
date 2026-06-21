import sys

def solve():
    # Use command line argument if provided, otherwise default to 'rosalind_bip.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'rosalind_bip.txt'
        
    try:
        with open(filename, 'r') as f:
            content = f.read().split()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        print("Please download your dataset and save it as 'rosalind_bip.txt' in this directory.")
        return

    if not content:
        return

    # First token is the number of graphs k
    k = int(content[0])
    idx = 1
    
    results = []
    
    for _ in range(k):
        if idx >= len(content):
            break
        n = int(content[idx])
        m = int(content[idx+1])
        idx += 2
        
        edges = []
        for _ in range(m):
            u = int(content[idx])
            v = int(content[idx+1])
            edges.append((u, v))
            idx += 2
            
        # Build adjacency list (vertices are 1-indexed from 1 to n)
        adj = {i: [] for i in range(1, n + 1)}
        for u, v in edges:
            if u in adj and v in adj:
                adj[u].append(v)
                adj[v].append(u)
        
        color = {}
        is_bip = True
        
        # BFS coloring traversal
        for start in range(1, n + 1):
            if start not in color:
                queue = [start]
                color[start] = 0
                head = 0
                while head < len(queue):
                    curr = queue[head]
                    head += 1
                    curr_color = color[curr]
                    for neighbor in adj[curr]:
                        if neighbor not in color:
                            color[neighbor] = 1 - curr_color
                            queue.append(neighbor)
                        elif color[neighbor] == curr_color:
                            is_bip = False
                            break
                    if not is_bip:
                        break
            if not is_bip:
                break
                
        results.append("1" if is_bip else "-1")
        
    output_str = " ".join(results)
    print("Result:")
    print(output_str)
    
    # Save the output to output.txt
    with open('output.txt', 'w') as out_f:
        out_f.write(output_str + '\n')
    print("Output saved to output.txt")

if __name__ == '__main__':
    solve()
