# Həlli üçün lazım olan modulları daxil edirik
# Import the required modules for the solution
import sys

def main():
    # Giriş faylının adını təyin edirik
    # Define the input file name
    input_file = "rosalind_nwc.txt"
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
        
        # Qrafın tillərini saxlayacaq siyahı
        # List to store the edges of the graph
        edges = []
        
        # Tilləri oxuyub siyahıya əlavə edirik
        # Read the edges and append them to the list
        for _ in range(E):
            u, v, w = map(int, lines[idx].split())
            idx += 1
            edges.append((u, v, w))
            
        # Məsafələr massivini sıfırlarla inisializasiya edirik
        # Initialize distance array with zeros to check all components
        dist = {i: 0 for i in range(1, V + 1)}
        
        # Bellman-Ford alqoritmi: tilləri V - 1 dəfə relaksasiya edirik
        # Bellman-Ford algorithm: relax all edges V - 1 times
        for _ in range(V - 1):
            for u, v, w in edges:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    
        # Mənfi çəkili dövrün olub-olmadığını yoxlayırıq (V-ci relaksasiya)
        # Check for a negative weight cycle (V-th relaxation step)
        has_negative_cycle = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                has_negative_cycle = True
                break
                
        # Nəticəni siyahıya əlavə edirik
        # Append the result to the list
        if has_negative_cycle:
            results.append("1")
        else:
            results.append("-1")
            
    # Bütün nəticələri boşluqla ayrılmış şəkildə çıxış faylına yazırıq
    # Write all results to the output file separated by spaces
    with open(output_file, "w") as f:
        f.write(" ".join(results) + "\n")

# Proqramın əsas giriş nöqtəsini yoxlayırıq
# Check for the main entry point of the program
if __name__ == "__main__":
    main()
