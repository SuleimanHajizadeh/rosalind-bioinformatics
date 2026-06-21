# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba8b.txt")
    if not os.path.exists(input_file):
        return 0, 0, [], []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    k, m = map(int, lines[0].split())
    centers = []
    for i in range(1, k + 1):
        centers.append(list(map(float, lines[i].split())))
    data = []
    for i in range(k + 2, len(lines)):
        data.append(list(map(float, lines[i].split())))
    return k, m, centers, data

def euclidean_distance(p1, p2):
    return sum((x1 - x2)**2 for x1, x2 in zip(p1, p2))

# Kvadratik xəta təhrifini (squared error distortion) hesablayırıq
# Compute the squared error distortion of data points with respect to centers
def squared_error_distortion(centers, data):
    total_dist = 0.0
    for point in data:
        min_d = min(euclidean_distance(point, c) for c in centers)
        total_dist += min_d
    return total_dist / len(data)

def main():
    k, m, centers, data = read_input()
    if not centers:
        return
    result = squared_error_distortion(centers, data)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(f"{result:.3f}\n")

if __name__ == "__main__":
    main()
