# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba8c.txt")
    if not os.path.exists(input_file):
        return 0, 0, []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    k, m = map(int, lines[0].split())
    data = []
    for line in lines[1:]:
        data.append(list(map(float, line.split())))
    return k, m, data

def euclidean_distance_sq(p1, p2):
    return sum((x1 - x2)**2 for x1, x2 in zip(p1, p2))

# K-Means üçün Lloyd alqoritmini tətbiq edirik
# Implement the Lloyd Algorithm for k-Means Clustering
def lloyd_algorithm(k, m, data):
    # İlk k nöqtəni mərkəz olaraq seçirik
    # Initialize centers as the first k points
    centers = data[:k]
    
    while True:
        # Nöqtələri ən yaxın mərkəzlərə təyin edirik
        # Assign points to nearest centers
        clusters = {i: [] for i in range(k)}
        for point in data:
            min_d = float('inf')
            best_c = 0
            for idx, c in enumerate(centers):
                d = euclidean_distance_sq(point, c)
                if d < min_d:
                    min_d = d
                    best_c = idx
            clusters[best_c].append(point)
            
        # Mərkəzləri yeniləyirik (hər klasterin ağırlıq mərkəzi)
        # Update centers to be the centroids of clusters
        new_centers = []
        for idx in range(k):
            cluster = clusters[idx]
            if not cluster:
                new_centers.append(centers[idx])
                continue
            centroid = [sum(pt[j] for pt in cluster) / len(cluster) for j in range(m)]
            new_centers.append(centroid)
            
        # Mərkəzlər dəyişmədikdə dayanırıq
        # Stop if centers converge
        changed = False
        for c, nc in zip(centers, new_centers):
            if sum((x1 - x2)**2 for x1, x2 in zip(c, nc)) > 1e-9:
                changed = True
                break
        if not changed:
            break
        centers = new_centers
        
    return centers

def main():
    k, m, data = read_input()
    if k == 0:
        return
    centers = lloyd_algorithm(k, m, data)
    
    output_lines = []
    for c in centers:
        output_lines.append(" ".join(f"{val:.3f}" for val in c))
        
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(output_lines) + "\n")

if __name__ == "__main__":
    main()
