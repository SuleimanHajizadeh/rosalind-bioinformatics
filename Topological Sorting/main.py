# Həlli üçün lazım olan modulları daxil edirik
# Import the required modules for the solution
from collections import deque

def main():
    # Giriş faylının adını təyin edirik
    # Define the input file name
    input_file = "rosalind_ts.txt"
    # Çıxış faylının adını təyin edirik
    # Define the output file name
    output_file = "output.txt"
    
    # Giriş faylını oxumaq üçün açırıq
    # Open the input file for reading
    with open(input_file, "r") as f:
        # Birinci sətirdən təpələrin və tillərin sayını oxuyuruq
        # Read the number of vertices and edges from the first line
        V, E = map(int, f.readline().strip().split())
        
        # Qonşuluq siyahısını təyin edirik (təpələr 1-dən V-ə qədərdir)
        # Define the adjacency list (vertices are indexed from 1 to V)
        adj = {i: [] for i in range(1, V + 1)}
        
        # Hər bir təpə üçün daxil olan dərəcələri (in-degree) sıfırlayırıq
        # Initialize the in-degrees of all vertices to zero
        in_degree = {i: 0 for i in range(1, V + 1)}
        
        # Tilləri oxuyub qonşuluq siyahısına və daxil olan dərəcələrə əlavə edirik
        # Read the edges and populate the adjacency list and in-degrees
        for _ in range(E):
            line = f.readline().strip()
            if not line:
                continue
            u, v = map(int, line.split())
            adj[u].append(v)
            in_degree[v] += 1
            
    # Daxil olan dərəcəsi sıfır olan təpələri növbəyə əlavə edirik
    # Add vertices with an in-degree of zero to the queue
    queue = deque([i for i in range(1, V + 1) if in_degree[i] == 0])
    
    # Topoloji sıralamanı saxlayacaq siyahını təyin edirik
    # Initialize the list to store the topological order
    topo_order = []
    
    # Növbə boşalana qədər davam edirik
    # Continue until the queue is empty
    while queue:
        # Növbənin əvvəlindən bir təpə çıxarırıq
        # Remove a vertex from the front of the queue
        u = queue.popleft()
        # Bu təpəni topoloji sıralama siyahısına əlavə edirik
        # Append the vertex to the topological order list
        topo_order.append(u)
        
        # Həmin təpədən çıxan bütün qonşu tilləri yoxlayırıq
        # Check all neighbors reachable from the current vertex
        for v in adj[u]:
            # Qonşu təpənin daxil olan dərəcəsini bir vahid azaldırıq
            # Decrement the in-degree of the neighbor vertex by one
            in_degree[v] -= 1
            # Əgər qonşu təpənin daxil olan dərəcəsi sıfır olarsa, onu növbəyə əlavə edirik
            # If the in-degree of the neighbor becomes zero, add it to the queue
            if in_degree[v] == 0:
                queue.append(v)
                
    # Topoloji sıralamanı boşluqla ayrılmış şəkildə çıxış faylına yazırıq
    # Write the topological order to the output file separated by spaces
    with open(output_file, "w") as f:
        f.write(" ".join(map(str, topo_order)))

# Proqramın əsas giriş nöqtəsini yoxlayırıq
# Check for the main entry point of the program
if __name__ == "__main__":
    main()
