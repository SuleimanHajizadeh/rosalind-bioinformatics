# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba4m.txt")
    if not os.path.exists(input_file):
        return []
    with open(input_file, "r") as f:
        return list(map(int, f.read().split()))

# Turnpike problemini həll edən rekursiv köməkçi funksiya (backtracking)
# Solve the Turnpike Problem recursively
def turnpike(d_list, n):
    max_val = max(d_list)
    x = [0] * n
    x[-1] = max_val
    d_list.remove(max_val)
    
    # Köməkçi axtarış funksiyası
    # Backtracking search
    def place(d_set, x, left, right):
        if not d_set:
            return True
            
        max_d = max(d_set)
        
        # Seçim 1: Sağda yerləşdirmək
        # Case 1: Place at the right
        dists_r = [abs(x[i] - max_d) for i in range(left) if x[i] is not None] + [abs(x[i] - max_d) for i in range(right + 1, n) if x[i] is not None]
        all_in_r = True
        temp_set_r = list(d_set)
        for dist in dists_r:
            if dist in temp_set_r:
                temp_set_r.remove(dist)
            else:
                all_in_r = False
                break
                
        if all_in_r:
            x[right] = max_d
            # Set-dən məsafələri silib rekursiya edirik
            # Remove distances and recurse
            next_set = list(d_set)
            for dist in dists_r:
                next_set.remove(dist)
            if place(next_set, x, left, right - 1):
                return True
            x[right] = None
            
        # Seçim 2: Solda yerləşdirmək
        # Case 2: Place at the left
        candidate_l = x[-1] - max_d
        dists_l = [abs(x[i] - candidate_l) for i in range(left) if x[i] is not None] + [abs(x[i] - candidate_l) for i in range(right + 1, n) if x[i] is not None]
        all_in_l = True
        temp_set_l = list(d_set)
        for dist in dists_l:
            if dist in temp_set_l:
                temp_set_l.remove(dist)
            else:
                all_in_l = False
                break
                
        if all_in_l:
            x[left] = candidate_l
            next_set = list(d_set)
            for dist in dists_l:
                next_set.remove(dist)
            if place(next_set, x, left + 1, right):
                return True
            x[left] = None
            
        return False
        
    x_init = [None] * n
    x_init[0] = 0
    x_init[-1] = max_val
    place(d_list, x_init, 1, n - 2)
    return x_init

def main():
    d_list = read_input()
    if not d_list:
        return
    # 0 kütləsi çıxarılıb verilə bilər, ona görə d_list-in müsbət hissəsini götürürük
    # Keep only positive distances
    pos_d = [d for d in d_list if d > 0]
    
    # n-i pos_d-yə görə tapırıq: n*(n-1)/2 = len(pos_d) -> n^2 - n - 2*len = 0
    # Solve quadratic equation to find n using positive distances count
    import math
    n = int((1 + math.sqrt(1 + 8 * len(pos_d))) / 2)
    
    result = turnpike(pos_d, n)
    result = sorted(result)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(map(str, result)) + "\n")

if __name__ == "__main__":
    main()
