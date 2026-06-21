# Həlli üçün lazım olan modulları daxil edirik
# Import the required modules for the solution
import sys

# Rekursiya limitini artırırıq ki, dərin rekursiya zamanı stack overflow xətası baş verməsin
# Increase the recursion limit to avoid stack overflow errors during deep recursion
sys.setrecursionlimit(200000)

def main():
    # Giriş və çıxış fayllarının adlarını təyin edirik
    # Define the input and output file names
    input_file = "rosalind_scc.txt"
    output_file = "output.txt"
    
    # Giriş faylını oxumaq üçün açırıq
    # Open the input file for reading
    with open(input_file, "r") as f:
        # Birinci sətirdən təpələrin və tillərin sayını oxuyuruq
        # Read the number of vertices and edges from the first line
        line = f.readline().strip()
        if not line:
            return
        n, m = map(int, line.split())
        
        # Qonşuluq siyahısını qururuq (təpələr 1-dən n-ə qədərdir)
        # Construct the adjacency list (vertices are from 1 to n)
        adj = {i: [] for i in range(1, n + 1)}
        for _ in range(m):
            edge_line = f.readline().strip()
            if edge_line:
                u, v = map(int, edge_line.split())
                adj[u].append(v)
                
    # Tarjan alqoritmi üçün dəyişənləri və siyahıları hazırlayırıq
    # Prepare variables and structures for Tarjan's algorithm
    index = [-1] * (n + 1)
    lowlink = [-1] * (n + 1)
    on_stack = [False] * (n + 1)
    stack = []
    current_index = 0
    scc_count = 0
    
    # Dərinliyinə axtarış (DFS) funksiyasını təyin edirik
    # Define the depth-first search (DFS) function
    def dfs(u):
        nonlocal current_index, scc_count
        # Təpənin indeksini və lowlink dəyərini təyin edirik
        # Assign index and lowlink value to the vertex
        index[u] = current_index
        lowlink[u] = current_index
        current_index += 1
        stack.append(u)
        on_stack[u] = True
        
        # Qonşu təpələri gəzirik
        # Traverse neighbor vertices
        for v in adj[u]:
            if index[v] == -1:
                # Əgər qonşu təpə ziyarət edilməyibsə, rekursiv olaraq DFS çağırırıq
                # If neighbor vertex has not been visited, recursively call DFS
                dfs(v)
                lowlink[u] = min(lowlink[u], lowlink[v])
            elif on_stack[v]:
                # Əgər qonşu təpə stack-dədirsə, lowlink dəyərini yeniləyirik
                # If neighbor vertex is on the stack, update its lowlink value
                lowlink[u] = min(lowlink[u], index[v])
                
        # Əgər təpə SCC-nin köküdürsə, onu və stack-də ondan yuxarıda olanları çıxarırıq
        # If the vertex is the root of an SCC, pop it and all nodes above it from stack
        if lowlink[u] == index[u]:
            scc_count += 1
            while True:
                v = stack.pop()
                on_stack[v] = False
                if v == u:
                    break

    # Hər bir təpə üçün DFS çağırırıq (əgər ziyarət edilməyibsə)
    # Call DFS for every vertex if it has not been visited yet
    for i in range(1, n + 1):
        if index[i] == -1:
            dfs(i)
            
    # Nəticəni çıxış faylına yazırıq
    # Write the result to the output file
    with open(output_file, "w") as f:
        f.write(str(scc_count) + "\n")

# Proqramın əsas giriş nöqtəsini yoxlayırıq
# Check for the main entry point of the program
if __name__ == "__main__":
    main()
