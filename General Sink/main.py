# Həlli üçün lazım olan modulları daxil edirik
# Import the required modules for the solution
import sys

# Rekursiya limitini artırırıq ki, dərin rekursiya zamanı stack overflow xətası baş verməsin
# Increase the recursion limit to avoid stack overflow errors during deep recursion
sys.setrecursionlimit(200000)

def solve_gs(n, edges):
    # Hər bir təpə üçün qonşuluq siyahısını qururuq
    # Construct the adjacency list for each vertex
    adj = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)
        
    # Birinci DFS mərhələsi üçün ziyarət edilmiş təpələr massivini hazırlayırıq
    # Prepare the visited array for the first DFS phase
    visited = [False] * (n + 1)
    last_finished = -1
    
    # Dərinliyinə axtarış (DFS) köməkçi funksiyası
    # Helper depth-first search (DFS) function
    def dfs1(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs1(v)
        # Ən son bitən təpəni yadda saxlayırıq
        # Record the last finished vertex
        nonlocal last_finished
        last_finished = u
        
    # Bütün ziyarət edilməmiş təpələrdən DFS çağırırıq
    # Call DFS from all unvisited vertices
    for i in range(1, n + 1):
        if not visited[i]:
            dfs1(i)
            
    # Əgər heç bir təpə yoxdursa, -1 qaytarırıq
    # If there are no vertices, return -1
    if last_finished == -1:
        return -1
        
    # İkinci DFS ilə namizəd təpədən bütün digər təpələrin əlçatan olmasını yoxlayırıq
    # Check reachability from the candidate vertex with a second DFS
    visited2 = [False] * (n + 1)
    
    def dfs2(u):
        visited2[u] = True
        for v in adj[u]:
            if not visited2[v]:
                dfs2(v)
                
    # Namizəd təpədən başlayaraq DFS-i çağırırıq
    # Start the second DFS from the candidate vertex
    dfs2(last_finished)
    
    # Hər hansı bir təpəyə çatmaq mümkün deyilsə, -1 qaytarırıq
    # If any vertex is not reachable, return -1
    for i in range(1, n + 1):
        if not visited2[i]:
            return -1
            
    # Namizəd təpədən bütün təpələr əlçatandırsa, onu qaytarırıq
    # If all vertices are reachable from the candidate, return it
    return last_finished

def main():
    # Giriş və çıxış fayllarının adlarını təyin edirik
    # Define the input and output file names
    input_file = "rosalind_gs.txt"
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
                    
            # Qrafın həllini hesablayırıq
            # Compute the solution for the graph
            ans = solve_gs(n, edges)
            results.append(ans)
            
    # Nəticələri boşluqla ayrılmış şəkildə çıxış faylına yazırıq
    # Write the results separated by spaces to the output file
    with open(output_file, "w") as f:
        f.write(" ".join(map(str, results)) + "\n")

# Proqramın əsas giriş nöqtəsini yoxlayırıq
# Check for the main entry point of the program
if __name__ == "__main__":
    main()
