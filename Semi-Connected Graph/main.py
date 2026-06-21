# Həlli üçün lazım olan modulları daxil edirik
# Import the required modules for the solution
import sys

# Rekursiya limitini artırırıq ki, dərin rekursiya zamanı stack overflow xətası baş verməsin
# Increase the recursion limit to avoid stack overflow errors during deep recursion
sys.setrecursionlimit(200000)

def solve_sc(n, edges):
    # Hər bir təpə üçün qonşuluq siyahısını qururuq
    # Construct the adjacency list for each vertex
    adj = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        
    # Tarjan alqoritmi üçün dəyişənləri və massivləri hazırlayırıq
    # Prepare variables and arrays for Tarjan's algorithm
    index = [-1] * (n + 1)
    lowlink = [-1] * (n + 1)
    on_stack = [False] * (n + 1)
    stack = []
    current_index = 0
    scc_id = [-1] * (n + 1)
    scc_count = 0
    
    # Tarjan alqoritminin DFS funksiyası
    # DFS function of Tarjan's algorithm
    def dfs(u):
        nonlocal current_index, scc_count
        index[u] = current_index
        lowlink[u] = current_index
        current_index += 1
        stack.append(u)
        on_stack[u] = True
        
        # Qonşu təpələri gəzirik
        # Traverse neighbor vertices
        for v in adj[u]:
            if index[v] == -1:
                # Əgər qonşu təpə ziyarət edilməyibsə, DFS çağırırıq
                # If neighbor vertex has not been visited yet, call DFS
                dfs(v)
                lowlink[u] = min(lowlink[u], lowlink[v])
            elif on_stack[v]:
                # Əgər qonşu təpə stack-dədirsə, lowlink dəyərini yeniləyirik
                # If neighbor vertex is on the stack, update lowlink value
                lowlink[u] = min(lowlink[u], index[v])
                
        # Əgər cari təpə güclü rabitəli komponentin köküdürsə
        # If the current vertex is the root of a strongly connected component
        if lowlink[u] == index[u]:
            while True:
                v = stack.pop()
                on_stack[v] = False
                scc_id[v] = scc_count
                if v == u:
                    break
            scc_count += 1

    # Bütün ziyarət edilməmiş təpələr üçün DFS-i çağırırıq
    # Call DFS for all unvisited vertices
    for i in range(1, n + 1):
        if index[i] == -1:
            dfs(i)
            
    # Kondensasiya olunmuş DAG-ı qururuq
    # Build the condensed DAG
    dag_adj = {i: set() for i in range(scc_count)}
    in_degree = [0] * scc_count
    for u in range(1, n + 1):
        for v in adj[u]:
            u_scc = scc_id[u]
            v_scc = scc_id[v]
            # Müxtəlif komponentlər arasındakı tilləri əlavə edirik
            # Add edges between different components
            if u_scc != v_scc and v_scc not in dag_adj[u_scc]:
                dag_adj[u_scc].add(v_scc)
                in_degree[v_scc] += 1
                
    # Kahn alqoritmi ilə topoloji sıralamanı və yeganəliyi yoxlayırıq
    # Verify topological sorting and uniqueness using Kahn's algorithm
    queue = [i for i in range(scc_count) if in_degree[i] == 0]
    topo_order = []
    
    while queue:
        # Əgər növbədə birdən çox komponent varsa, deməli qraf yarım-rabitəli deyil
        # If there are multiple components in queue, the graph is not semi-connected
        if len(queue) > 1:
            return -1
        u = queue.pop()
        topo_order.append(u)
        for v in dag_adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
                
    # Əgər topoloji sıralama bütün komponentləri əhatə edirsə, qraf yarım-rabitəlidir
    # If topological sort covers all components, the graph is semi-connected
    if len(topo_order) == scc_count:
        return 1
    else:
        return -1

def main():
    # Giriş və çıxış fayllarının adlarını təyin edirik
    # Define the input and output file names
    input_file = "rosalind_sc.txt"
    output_file = "output.txt"
    
    # Giriş faylını oxumaq üçün açırıq
    # Open the input file for reading
    with open(input_file, "r") as f:
        # Birinci sətirdən qrafların (k) sayını oxuyuruq
        # Read the number of graphs (k) from the first line
        line = f.readline()
        if not line:
            return
        k = int(line.strip())
        
        results = []
        # Hər bir qraf üçün məlumatları oxuyub həll edirik
        # Read and solve for each graph
        for _ in range(k):
            # Boş sətirləri keçirik
            # Skip empty lines
            empty_line = f.readline()
            while empty_line and not empty_line.strip():
                empty_line = f.readline()
                
            if not empty_line:
                break
                
            # Təpələrin (n) və tillərin (m) sayını oxuyuruq
            # Read the number of vertices (n) and edges (m)
            n, m = map(int, empty_line.strip().split())
            
            # Tilləri oxuyuruq
            # Read the edges
            edges = []
            for _ in range(m):
                edge_line = f.readline().strip()
                if edge_line:
                    u, v = map(int, edge_line.split())
                    edges.append((u, v))
                    
            # Qrafın yarım-rabitəli olmasını yoxlayırıq
            # Check if the graph is semi-connected
            ans = solve_sc(n, edges)
            results.append(ans)
            
    # Nəticələri boşluqla ayrılmış şəkildə çıxış faylına yazırıq
    # Write the results separated by spaces to the output file
    with open(output_file, "w") as f:
        f.write(" ".join(map(str, results)) + "\n")

# Proqramın əsas giriş nöqtəsini yoxlayırıq
# Check for the main entry point of the program
if __name__ == "__main__":
    main()
