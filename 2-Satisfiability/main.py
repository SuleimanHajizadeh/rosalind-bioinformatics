# Həlli üçün lazım olan modulları daxil edirik
# Import the required modules for the solution
import sys

# Rekursiya limitini artırırıq ki, dərin rekursiya zamanı stack overflow xətası baş verməsin
# Increase the recursion limit to avoid stack overflow errors during deep recursion
sys.setrecursionlimit(200000)

def solve_2sat(n, clauses):
    # Hər bir düyüm üçün qonşuluq siyahısını qururuq
    # Construct the adjacency list for each node
    adj = {i: [] for i in range(2 * n)}
    
    # Hər bir klauz (clause) üçün implikasiya tillərini əlavə edirik
    # Add implication edges for each clause
    for u_lit, v_lit in clauses:
        # Literalları düyüm indekslərinə uyğunlaşdırırıq
        # Map literals to node indices
        u_node = 2 * (u_lit - 1) if u_lit > 0 else 2 * (-u_lit - 1) + 1
        v_node = 2 * (v_lit - 1) if v_lit > 0 else 2 * (-v_lit - 1) + 1
        
        # u_node-un inkarından v_node-a tərəf til əlavə edirik (not u => v)
        # Add edge from negation of u_node to v_node (not u => v)
        adj[u_node ^ 1].append(v_node)
        # v_node-un inkarından u_node-a tərəf til əlavə edirik (not v => u)
        # Add edge from negation of v_node to u_node (not v => u)
        adj[v_node ^ 1].append(u_node)
        
    # Tarjan alqoritmi üçün dəyişənləri və massivləri hazırlayırıq
    # Prepare variables and arrays for Tarjan's algorithm
    index = [-1] * (2 * n)
    lowlink = [-1] * (2 * n)
    on_stack = [False] * (2 * n)
    stack = []
    current_index = 0
    scc_id = [-1] * (2 * n)
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
        
        # Qonşu düyümləri gəzirik
        # Traverse neighbor nodes
        for v in adj[u]:
            if index[v] == -1:
                # Əgər qonşu düyüm hələ ziyarət edilməyibsə, DFS çağırırıq
                # If neighbor node has not been visited yet, call DFS
                dfs(v)
                lowlink[u] = min(lowlink[u], lowlink[v])
            elif on_stack[v]:
                # Əgər qonşu düyüm stack-dədirsə, lowlink dəyərini yeniləyirik
                # If neighbor node is on the stack, update lowlink value
                lowlink[u] = min(lowlink[u], index[v])
                
        # Əgər cari düyüm güclü rabitəli komponentin köküdürsə
        # If the current node is the root of a strongly connected component
        if lowlink[u] == index[u]:
            while True:
                v = stack.pop()
                on_stack[v] = False
                scc_id[v] = scc_count
                if v == u:
                    break
            scc_count += 1

    # Bütün ziyarət edilməmiş düyümlər üçün DFS-i çağırırıq
    # Call DFS for all unvisited nodes
    for i in range(2 * n):
        if index[i] == -1:
            dfs(i)
            
    # Ödənilə bilməyən halı yoxlayırıq (dəyişən və inkarı eyni SCC-də olarsa)
    # Check for unsatisfiability (if a variable and its negation are in the same SCC)
    for i in range(n):
        if scc_id[2 * i] == scc_id[2 * i + 1]:
            return 0, []
            
    # Həlli qururuq
    # Construct the assignment
    assignment = []
    for i in range(n):
        pos_id = scc_id[2 * i]
        neg_id = scc_id[2 * i + 1]
        
        # Komponentlərin tamamlanma sırasına görə dəyər təyin edirik
        # Assign value based on the order of component completion
        if pos_id < neg_id:
            # Müsbət düyüm komponenti daha əvvəl tamamlanıb (sink/dərə) -> True
            # Positive node component completed earlier (sink) -> True
            assignment.append(i + 1)
        else:
            # İnkar düyüm komponenti daha əvvəl tamamlanıb (sink/dərə) -> False
            # Negated node component completed earlier (sink) -> False
            assignment.append(-(i + 1))
            
    return 1, assignment

def main():
    # Giriş və çıxış fayllarının adlarını təyin edirik
    # Define the input and output file names
    input_file = "rosalind_2sat.txt"
    output_file = "output.txt"
    
    # Giriş faylını oxumaq üçün açırıq
    # Open the input file for reading
    with open(input_file, "r") as f:
        # Birinci sətirdən düsturların (k) sayını oxuyuruq
        # Read the number of formulas (k) from the first line
        line = f.readline()
        if not line:
            return
        k = int(line.strip())
        
        results = []
        # Hər bir düstur üçün məlumatları oxuyub həll edirik
        # Read and solve for each formula
        for _ in range(k):
            # Boş sətirləri keçirik
            # Skip empty lines
            empty_line = f.readline()
            while empty_line and not empty_line.strip():
                empty_line = f.readline()
                
            if not empty_line:
                break
                
            # Dəyişənlərin (n) və klauzların (m) sayını oxuyuruq
            # Read the number of variables (n) and clauses (m)
            n, m = map(int, empty_line.strip().split())
            
            # Klauzları oxuyuruq
            # Read the clauses
            clauses = []
            for _ in range(m):
                clause_line = f.readline().strip()
                if clause_line:
                    u, v = map(int, clause_line.split())
                    clauses.append((u, v))
                    
            # 2SAT problemini həll edirik
            # Solve the 2SAT problem
            satisfied, assignment = solve_2sat(n, clauses)
            results.append((satisfied, assignment))
            
    # Nəticələri çıxış faylına yazırıq
    # Write the results to the output file
    with open(output_file, "w") as f:
        for satisfied, assignment in results:
            if satisfied == 0:
                f.write("0\n")
            else:
                f.write("1 " + " ".join(map(str, assignment)) + "\n")

# Proqramın əsas giriş nöqtəsini yoxlayırıq
# Check for the main entry point of the program
if __name__ == "__main__":
    main()
