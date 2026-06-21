# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba8a.txt")
    if not os.path.exists(input_file):
        return 0, 0, []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    k, m = map(int, lines[0].split())
    data = []
    for line in lines[1:]:
        data.append(list(map(float, line.split())))
    return k, m, data

# Avklid məsafəsini hesablayırıq
# Compute Euclidean distance between two points
def euclidean_distance(p1, p2):
    import math
    return math.sqrt(sum((x1 - x2)**2 for x1, x2 in zip(p1, p2)))

# Bir nöqtənin seçilmiş mərkəzlər çoxluğuna olan ən qısa məsafəsini tapırıq
# Compute distance from point to a set of centers
def dist_to_centers(point, centers):
    return min(euclidean_distance(point, c) for c in centers)

# Farthest First Traversal alqoritmi
# Implement FarthestFirstTraversal
def farthest_first_traversal(k, data):
    centers = [data[0]]
    while len(centers) < k:
        max_dist = -1.0
        best_point = None
        for point in data:
            d = dist_to_centers(point, centers)
            if d > max_dist:
                max_dist = d
                best_point = point
        centers.append(best_point)
    return centers

def main():
    k, m, data = read_input()
    if k == 0:
        return
    centers = farthest_first_traversal(k, data)
    
    # Mərkəzləri formatlayırıq
    # Format centers output
    output_lines = []
    for c in centers:
        output_lines.append(" ".join(map(str, c)))
        
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(output_lines) + "\n")

if __name__ == "__main__":
    main()
