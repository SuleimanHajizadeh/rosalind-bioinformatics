# Həlli üçün lazım olan modulları daxil edirik
# Import the required modules for the solution
import os
import math

# Ən yüksək ehtimallı gizli yolu tapmaq üçün Viterbi alqoritmini təyin edirik
# Define the Viterbi algorithm to find the hidden path with maximum probability
def solve_viterbi(x, alphabet, states, transition, emission):
    N = len(x)
    K = len(states)
    
    # Başlanğıc ehtimallarının bərabər olduğunu fərz edirik (1 / vəziyyətlərin sayı)
    # Assume that initial probabilities are equal (1 / number of states)
    init_prob = {state: 1.0 / K for state in states}
    
    # Dinamik proqramlaşdırma cədvəlini və geriyə izləmə cədvəlini yaradırıq
    # Create the dynamic programming table and backpointer tracking table
    dp = []
    backtrack = []
    
    # t = 0 üçün ilkin vəziyyətlərin ehtimallarını hesablayırıq (logarithm istifadə edərək)
    # Initialize DP at t = 0 (using logarithms to avoid numerical underflow)
    dp_t = {}
    for state in states:
        p_init = init_prob[state]
        p_emit = emission[state][x[0]]
        dp_t[state] = math.log(p_init) + math.log(p_emit) if (p_init > 0 and p_emit > 0) else -float('inf')
    dp.append(dp_t)
    
    # t = 1-dən N-1-ə qədər olan addımlar üçün dinamik proqramlaşdırmanı işlədirik
    # Run dynamic programming for time steps t = 1 to N-1
    for i in range(1, N):
        dp_t = {}
        back_t = {}
        for curr_state in states:
            max_val = -float('inf')
            best_prev = None
            p_emit = emission[curr_state][x[i]]
            log_emit = math.log(p_emit) if p_emit > 0 else -float('inf')
            
            # Bütün mümkün əvvəlki vəziyyətlər arasından ən yaxşısını seçirik
            # Select the best transition from all possible previous states
            for prev_state in states:
                p_trans = transition[prev_state][curr_state]
                log_trans = math.log(p_trans) if p_trans > 0 else -float('inf')
                val = dp[i-1][prev_state] + log_trans + log_emit
                if val > max_val:
                    max_val = val
                    best_prev = prev_state
            if best_prev is None:
                best_prev = states[0]
            dp_t[curr_state] = max_val
            back_t[curr_state] = best_prev
        dp.append(dp_t)
        backtrack.append(back_t)
        
    # Ən son addımda ən böyük ehtimala malik vəziyyəti tapırıq
    # Find the state with the maximum probability at the final step
    max_val = -float('inf')
    best_last = None
    for state in states:
        if dp[-1][state] > max_val:
            max_val = dp[-1][state]
            best_last = state
    if best_last is None:
        best_last = states[0]
        
    # Tapılmış ən yaxşı son vəziyyətdən geriyə doğru optimal yolu izləyirik
    # Trace the optimal path backward from the best final state
    path = [best_last]
    curr = best_last
    for i in range(N-1, 0, -1):
        curr = backtrack[i-1][curr]
        path.append(curr)
    path.reverse()
    return "".join(path)

# Əsas icra funksiyası
# Main execution function
def main():
    # Giriş və çıxış fayllarının yollarını cari qovluğa görə müəyyən edirik
    # Set input and output file paths relative to the current directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba10c.txt")
    output_file = os.path.join(script_dir, "output.txt")
    
    # Giriş faylını oxuyuruq
    # Read the input file
    with open(input_file, "r") as f:
        lines_raw = f.readlines()
        
    x = lines_raw[0].strip()
    content = "".join(lines_raw[1:])
    blocks = [b.strip() for b in content.split("--------") if b.strip()]
    
    # Əlifba və vəziyyətləri oxuyuruq
    # Parse alphabet and states
    alphabet = blocks[0].split()
    states = blocks[1].split()
    
    # Keçid matrisini oxuyuruq
    # Parse the transition matrix
    transition_lines = blocks[2].splitlines()
    trans_header = transition_lines[0].split()
    transition = {}
    for line in transition_lines[1:]:
        parts = line.split()
        if not parts:
            continue
        state = parts[0]
        transition[state] = {}
        for h, val in zip(trans_header, parts[1:]):
            transition[state][h] = float(val)
            
    # Emissiya matrisini oxuyuruq
    # Parse the emission matrix
    emission_lines = blocks[3].splitlines()
    emit_header = emission_lines[0].split()
    emission = {}
    for line in emission_lines[1:]:
        parts = line.split()
        if not parts:
            continue
        state = parts[0]
        emission[state] = {}
        for h, val in zip(emit_header, parts[1:]):
            emission[state][h] = float(val)
            
    # Viterbi alqoritmini çağırıb nəticəni tapırıq
    # Solve the Viterbi path and retrieve result
    result = solve_viterbi(x, alphabet, states, transition, emission)
    
    # Nəticəni çıxış faylına yazırıq
    # Write the result path to the output file
    with open(output_file, "w") as f:
        f.write(result + "\n")
    print("Viterbi path successfully written to output.txt")

if __name__ == "__main__":
    main()
