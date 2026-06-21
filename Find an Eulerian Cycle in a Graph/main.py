# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba3f.txt")
    if not os.path.exists(input_file):
        return {}
    adj = {}
    with open(input_file, "r") as f:
        for line in f:
            if not line.strip():
                continue
            node, neighbors = line.strip().split(" -> ")
            adj[node] = neighbors.split(",")
    return adj

# Qrafda Eyler dövrünü tapırıq
# Find an Eulerian cycle in a graph
def find_eulerian_cycle(adj):
    # Eyler yolunu qurmaq üçün Hierholzer alqoritmindən istifadə edirik
    # Hierholzer's algorithm
    stack = [next(iter(adj.keys()))]
    path = []
    
    # Köməkçi kopyasını çıxarırıq
    # Copy graph to modify edges
    adj_copy = {u: list(v) for u, v in adj.items()}
    
    while stack:
        u = stack[-1]
        if adj_copy.get(u):
            v = adj_copy[u].pop()
            stack.append(v)
        else:
            path.append(stack.pop())
            
    path.reverse()
    return path

def main():
    adj = read_input()
    if not adj:
        return
    result = find_eulerian_cycle(adj)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("->".join(result) + "\n")

if __name__ == "__main__":
    main()
