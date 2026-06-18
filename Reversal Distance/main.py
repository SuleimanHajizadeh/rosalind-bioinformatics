import os

def read_input(file_path):
    pairs = []
    current_pair = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            perm = tuple(map(int, line.split()))
            current_pair.append(perm)
            if len(current_pair) == 2:
                pairs.append(current_pair)
                current_pair = []
    return pairs

def get_reversals(p):
    reversals = []
    n = len(p)
    for i in range(n):
        for j in range(i + 1, n):
            rev_p = p[:i] + p[i:j+1][::-1] + p[j+1:]
            reversals.append(rev_p)
    return reversals

def reversal_distance(p1, p2):
    if p1 == p2:
        return 0
        
    # Standardize so p1 is the identity permutation
    mapping = {val: idx for idx, val in enumerate(p1)}
    start = tuple(mapping[x] for x in p2)
    target = tuple(range(len(p1)))
    
    if start == target:
        return 0
        
    # Bidirectional BFS
    q_start = {start}
    q_target = {target}
    
    visited_start = {start: 0}
    visited_target = {target: 0}
    
    while q_start and q_target:
        # Check intersection
        intersection = q_start.intersection(q_target)
        if intersection:
            return min(visited_start[node] + visited_target[node] for node in intersection)
            
        # Expand the smaller queue
        if len(q_start) <= len(q_target):
            next_q = set()
            for node in q_start:
                curr_dist = visited_start[node]
                for neighbor in get_reversals(node):
                    if neighbor not in visited_start:
                        visited_start[neighbor] = curr_dist + 1
                        next_q.add(neighbor)
                        if neighbor in visited_target:
                            return curr_dist + 1 + visited_target[neighbor]
            q_start = next_q
        else:
            next_q = set()
            for node in q_target:
                curr_dist = visited_target[node]
                for neighbor in get_reversals(node):
                    if neighbor not in visited_target:
                        visited_target[neighbor] = curr_dist + 1
                        next_q.add(neighbor)
                        if neighbor in visited_start:
                            return curr_dist + 1 + visited_start[neighbor]
            q_target = next_q
    return -1

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_rear.txt")
    
    pairs = read_input(input_path)
    distances = []
    
    for idx, (p1, p2) in enumerate(pairs, 1):
        dist = reversal_distance(p1, p2)
        print(f"Cüt {idx}: məsafə = {dist}")
        distances.append(dist)
        
    result_str = " ".join(map(str, distances))
    print(f"Yekun nəticə: {result_str}")
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        out_file.write(result_str + "\n")

if __name__ == "__main__":
    main()
