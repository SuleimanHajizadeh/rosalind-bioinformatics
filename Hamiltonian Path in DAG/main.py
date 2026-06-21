# Həlli üçün lazım olan modulları daxil edirik
# Import the required modules for the solution
from collections import deque

def main():
    # Giriş faylının adını təyin edirik
    # Define the input file name
    input_file = "rosalind_hdag.txt"
    # Çıxış faylının adını təyin edirik
    # Define the output file name
    output_file = "output.txt"
    
    # Giriş faylını oxumaq üçün açırıq
    # Open the input file for reading
    with open(input_file, "r") as f:
        # Fayldakı bütün sətirləri oxuyub boş olmayanları saxlayırıq
        # Read all lines from the file and keep only the non-empty ones
        lines = [line.strip() for line in f if line.strip()]
        
    # Əgər fayl boşdursa, proqramı dayandırırıq
    # If the file is empty, terminate the execution
    if not lines:
        return
        
    # Birinci sətirdən qrafların sayını alırıq
    # Get the number of graphs from the first line
    k = int(lines[0])
    # Oxuma mövqeyini növbəti sətrə təyin edirik
    # Set the reading index to the next line
    idx = 1
    
    # Bütün qrafların nəticələrini saxlayacaq siyahı
    # List to store the results of all graphs
    results = []
    
    # Hər bir qraf üçün dövr qururuq
    # Loop through each graph
    for _ in range(k):
        # Qrafın təpələrinin və tillərinin sayını oxuyuruq
        # Read the number of vertices and edges of the graph
        V, E = map(int, lines[idx].split())
        idx += 1
        
        # Qonşuluq siyahısını təyin edirik
        # Define the adjacency list
        adj = {i: set() for i in range(1, V + 1)}
        # Daxil olan dərəcələri sıfırlayırıq
        # Initialize in-degrees to zero
        in_degree = {i: 0 for i in range(1, V + 1)}
        
        # Qrafın tillərini oxuyuruq
        # Read the edges of the graph
        for _ in range(E):
            u, v = map(int, lines[idx].split())
            idx += 1
            adj[u].add(v)
            in_degree[v] += 1
            
        # Daxil olan dərəcəsi sıfır olan təpələri növbəyə əlavə edirik
        # Add vertices with an in-degree of zero to the queue
        queue = deque([i for i in range(1, V + 1) if in_degree[i] == 0])
        
        # Topoloji sıralamanı saxlayacaq siyahı
        # List to store the topological sorting order
        topo_order = []
        
        # Kahn alqoritmi ilə topoloji sıralama aparırıq
        # Perform topological sorting using Kahn's algorithm
        while queue:
            u = queue.popleft()
            topo_order.append(u)
            for v in adj[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
                    
        # Hamiltonian yolunun olub-olmadığını yoxlayırıq
        # Check if a Hamiltonian path exists
        has_hamiltonian = True
        for i in range(len(topo_order) - 1):
            # Əgər topoloji ardıcıllıqda ardıcıl gələn iki təpə arasında til yoxdursa
            # If there is no directed edge between consecutive vertices in the topological order
            if topo_order[i+1] not in adj[topo_order[i]]:
                has_hamiltonian = False
                break
                
        # Nəticəni qeyd edirik
        # Record the result
        if has_hamiltonian:
            # Əgər yol varsa, 1 və ardıcıllığı nəticələrə əlavə edirik
            # If path exists, append 1 followed by the path to the results
            results.append("1 " + " ".join(map(str, topo_order)))
        else:
            # Əgər yol yoxdursa, -1 əlavə edirik
            # If no path exists, append -1
            results.append("-1")
            
    # Bütün nəticələri çıxış faylına yazırıq
    # Write all results to the output file
    with open(output_file, "w") as f:
        f.write("\n".join(results) + "\n")

# Proqramın əsas giriş nöqtəsini yoxlayırıq
# Check for the main entry point of the program
if __name__ == "__main__":
    main()
