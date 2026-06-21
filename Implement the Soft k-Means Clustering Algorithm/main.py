# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba8d.txt")
    if not os.path.exists(input_file):
        return 0, 0, 0.0, []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    k, m = map(int, lines[0].split())
    beta = float(lines[1])
    data = []
    for line in lines[2:]:
        data.append(list(map(float, line.split())))
    return k, m, beta, data

def euclidean_distance_sq(p1, p2):
    return sum((x1 - x2)**2 for x1, x2 in zip(p1, p2))

# Soft k-Means alqoritmini tətbiq edirik
# Implement the Soft k-Means Clustering Algorithm
def soft_k_means(k, m, beta, data, max_iter=100):
    centers = data[:k]
    import math
    
    for _ in range(max_iter):
        # Məsuliyyət matrisini (responsibility matrix) hesablayırıq (E-step)
        # E-step: calculate responsibilities
        hidden_matrix = []
        for point in data:
            row = []
            for c in centers:
                dist = euclidean_distance_sq(point, c)
                row.append(math.exp(-beta * math.sqrt(dist)))
            total = sum(row)
            if total == 0:
                row = [1.0 / k] * k
            else:
                row = [val / total for val in row]
            hidden_matrix.append(row)
            
        # Mərkəzləri yeniləyirik (M-step)
        # M-step: update centers
        new_centers = []
        for j in range(k):
            denom = sum(hidden_matrix[i][j] for i in range(len(data)))
            num = [0.0] * m
            for i in range(len(data)):
                for col in range(m):
                    num[col] += hidden_matrix[i][j] * data[i][col]
            if denom == 0:
                new_centers.append(centers[j])
            else:
                new_centers.append([val / denom for val in num])
        centers = new_centers
        
    return centers

def main():
    k, m, beta, data = read_input()
    if k == 0:
        return
    centers = soft_k_means(k, m, beta, data)
    
    output_lines = []
    for c in centers:
        output_lines.append(" ".join(f"{val:.3f}" for val in c))
        
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(output_lines) + "\n")

if __name__ == "__main__":
    main()
