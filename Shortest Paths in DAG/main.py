# Həlli üçün lazım olan modulları daxil edirik
# Import the required modules for the solution
import sys
import os

# Rekursiya limitini artırırıq ki, dərin rekursiya zamanı stack overflow xətası baş verməsin
# Increase the recursion limit to avoid stack overflow errors during deep recursion
sys.setrecursionlimit(200000)

def main():
    # Cari skriptin qovluğunu tapırıq və giriş/çıxış fayllarının yollarını müəyyən edirik
    # Get the directory of the current script and define paths for input/output files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_sdag.txt")
    output_file = os.path.join(script_dir, "output.txt")
    
    # Giriş faylını oxumaq üçün açırıq
    # Open the input file for reading
    with open(input_file, "r") as f:
        # Birinci sətirdən təpələrin (n) və tillərin (m) sayını oxuyuruq
        # Read the number of vertices (n) and edges (m) from the first line
        line = f.readline()
        if not line:
            return
        n, m = map(int, line.strip().split())
        
        # Qonşuluq siyahısını və hər təpənin giriş dərəcəsini qururuq
        # Construct the adjacency list and the in-degree of each vertex
        adj = {i: [] for i in range(1, n + 1)}
        in_degree = [0] * (n + 1)
        for _ in range(m):
            edge_line = f.readline().strip()
            if edge_line:
                u, v, w = map(int, edge_line.split())
                adj[u].append((v, w))
                in_degree[v] += 1
                
    # Kahn alqoritmi ilə topoloji sıralama növbəsini hazırlayırıq
    # Prepare the topological sort queue using Kahn's algorithm
    queue = [i for i in range(1, n + 1) if in_degree[i] == 0]
    topo_order = []
    
    # O(V) zaman mürəkkəbliyi üçün növbəni indeks ilə oxuyuruq
    # Read the queue using index to maintain O(V) time complexity
    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        topo_order.append(u)
        for v, w in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
                
    # Məsafələr massivini sonsuzluqla inisializasiya edirik (1-ci təpə üçün məsafə 0-dır)
    # Initialize distances array with infinity (distance for vertex 1 is 0)
    inf = float('inf')
    dist = [inf] * (n + 1)
    dist[1] = 0
    
    # Topoloji ardıcıllıqla hər bir təpənin tillərini relaksasiya edirik
    # Relax edges of each vertex in topological order
    for u in topo_order:
        if dist[u] != inf:
            for v, w in adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    
    # Nəticəni formatlayırıq (əlçatmaz təpələr üçün 'x' yazırıq)
    # Format the result (write 'x' for unreachable vertices)
    result = []
    for i in range(1, n + 1):
        if dist[i] == inf:
            result.append("x")
        else:
            result.append(str(dist[i]))
            
    # Nəticəni çıxış faylına yazırıq
    # Write the result to the output file
    with open(output_file, "w") as f:
        f.write(" ".join(result) + "\n")

# Proqramın əsas giriş nöqtəsini yoxlayırıq
# Check for the main entry point of the program
if __name__ == "__main__":
    main()
