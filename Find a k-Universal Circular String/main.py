# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba3i.txt")
    if not os.path.exists(input_file):
        return 0
    with open(input_file, "r") as f:
        return int(f.read().strip())

# Bütün mümkün k-lik ikili (binary) ardıcıllıqları yaradırıq
# Find a k-universal circular string (De Bruijn cycle of order k on binary alphabet)
def find_k_universal_string(k):
    # İkili əlifba üzərində de Bruijn dövrü yaradırıq
    # We construct a De Bruijn graph for k-1 length binary strings
    adj = {}
    for i in range(2**(k-1)):
        binary = bin(i)[2:].zfill(k-1)
        # 0 və 1 keçidləri ilə neighbors (qonşular)
        # Neighbors with transitions 0 and 1
        adj[binary] = [binary[1:] + '0', binary[1:] + '1']
        
    # Eyler dövrünü tapırıq
    # Find Eulerian cycle
    stack = [next(iter(adj.keys()))]
    path = []
    adj_copy = {u: list(v) for u, v in adj.items()}
    while stack:
        u = stack[-1]
        if adj_copy[u]:
            v = adj_copy[u].pop()
            stack.append(v)
        else:
            path.append(stack.pop())
    path.reverse()
    
    # Dairəvi (circular) string qururuq
    # Form circular string
    cycle = path[:-1]
    result = "".join(node[-1] for node in cycle)
    return result

def main():
    k = read_input()
    if k == 0:
        return
    result = find_k_universal_string(k)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    main()
