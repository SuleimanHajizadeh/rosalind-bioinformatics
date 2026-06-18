import os

def read_input(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    p1 = tuple(map(int, lines[0].split()))
    p2 = tuple(map(int, lines[1].split()))
    return p1, p2

def get_reversals_with_indices(p):
    n = len(p)
    results = []
    for i in range(n):
        for j in range(i + 1, n):
            rev_p = p[:i] + p[i:j+1][::-1] + p[j+1:]
            results.append((rev_p, (i + 1, j + 1)))
    return results

def solve_sorting_by_reversals(p1, p2):
    if p1 == p2:
        return 0, []
        
    start = p1
    target = p2
    
    q_start = {start}
    q_target = {target}
    
    visited_start = {start: (None, None)}
    visited_target = {target: (None, None)}
    
    meeting_node = None
    
    while q_start and q_target:
        intersection = q_start.intersection(q_target)
        if intersection:
            meeting_node = list(intersection)[0]
            break
            
        if len(q_start) <= len(q_target):
            next_q = set()
            for node in q_start:
                for neighbor, indices in get_reversals_with_indices(node):
                    if neighbor not in visited_start:
                        visited_start[neighbor] = (node, indices)
                        next_q.add(neighbor)
                        if neighbor in visited_target:
                            meeting_node = neighbor
                            break
                if meeting_node:
                    break
            q_start = next_q
        else:
            next_q = set()
            for node in q_target:
                for neighbor, indices in get_reversals_with_indices(node):
                    if neighbor not in visited_target:
                        visited_target[neighbor] = (node, indices)
                        next_q.add(neighbor)
                        if neighbor in visited_start:
                            meeting_node = neighbor
                            break
                if meeting_node:
                    break
            q_target = next_q
            
        if meeting_node:
            break
            
    # Reconstruct the path
    path_start = []
    curr = meeting_node
    while curr != start:
        parent, indices = visited_start[curr]
        path_start.append(indices)
        curr = parent
    path_start.reverse()
    
    path_target = []
    curr = meeting_node
    while curr != target:
        parent, indices = visited_target[curr]
        path_target.append(indices)
        curr = parent
        
    full_path = path_start + path_target
    return len(full_path), full_path

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_sort.txt")
    
    p1, p2 = read_input(input_path)
    print(f"Permutasiya 1: {p1}")
    print(f"Permutasiya 2: {p2}")
    
    dist, path = solve_sorting_by_reversals(p1, p2)
    
    print(f"Reversal Distance = {dist}")
    print("Reversals:")
    for indices in path:
        print(f"{indices[0]} {indices[1]}")
        
    output_lines = [str(dist)]
    for indices in path:
        output_lines.append(f"{indices[0]} {indices[1]}")
    result_str = "\n".join(output_lines)
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        out_file.write(result_str + "\n")

if __name__ == "__main__":
    main()
