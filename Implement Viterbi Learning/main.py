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
    
    # Keçidlərin və emissiyaların logaritmlərini hesablayırıq
    # Compute log transition and emission probabilities
    log_trans = {}
    for s1 in states:
        log_trans[s1] = {}
        for s2 in states:
            p = transition[s1][s2]
            log_trans[s1][s2] = math.log(p) if p > 0 else -float('inf')
            
    log_emit = {}
    for s in states:
        log_emit[s] = {}
        for a in emission[s]:
            p = emission[s][a]
            log_emit[s][a] = math.log(p) if p > 0 else -float('inf')
            
    # Dinamik proqramlaşdırma və geriyə izləmə cədvəllərini qururuq
    # Create the DP table and backtrack tracking tables
    dp = [ {s: -float('inf') for s in states} for _ in range(N) ]
    backtrack = [ {s: None for s in states} for _ in range(N) ]
    
    # t = 0 üçün ilkin vəziyyətləri təyin edirik
    # Initialize DP at time step t = 0
    for s in states:
        p_init = init_prob[s]
        p_emit = emission[s][x[0]]
        dp[0][s] = math.log(p_init) + math.log(p_emit) if (p_init > 0 and p_emit > 0) else -float('inf')
        
    # t = 1-dən N-1-ə qədər addımları hesablayırıq
    # Compute DP for steps t = 1 to N-1
    for i in range(1, N):
        char = x[i]
        for curr_s in states:
            best_val = -float('inf')
            best_prev = None
            log_e = log_emit[curr_s][char]
            
            for prev_s in states:
                val = dp[i-1][prev_s] + log_trans[prev_s][curr_s] + log_e
                if val > best_val:
                    best_val = val
                    best_prev = prev_s
            dp[i][curr_s] = best_val
            backtrack[i][curr_s] = best_prev
            
    # Ən son addımda ən yaxşı son vəziyyəti tapırıq
    # Find the state with the maximum probability at the final step
    best_val = -float('inf')
    best_last = None
    for s in states:
        if dp[-1][s] > best_val:
            best_val = dp[-1][s]
            best_last = s
    if best_last is None:
        best_last = states[0]
        
    # Geriyə izləmə ilə yolu bərpa edirik
    # Backtrack path to retrieve the optimal hidden path of states
    path = [best_last]
    curr = best_last
    for i in range(N-1, 0, -1):
        curr = backtrack[i][curr]
        path.append(curr)
    path.reverse()
    return "".join(path)

# Verilmiş yol və emissiyalara əsasən HMM parametrlərini yenidən qiymətləndiririk
# Re-estimate HMM parameters from the hidden path and emissions using MLE
def estimate_hmm_parameters(x, alphabet, pi, states):
    K = len(states)
    M = len(alphabet)
    N = len(pi)
    
    trans_counts = {s: {t: 0 for t in states} for s in states}
    state_total_trans = {s: 0 for s in states}
    
    emit_counts = {s: {a: 0 for a in alphabet} for s in states}
    state_total_emit = {s: 0 for s in states}
    
    # Keçidləri sayırıq
    # Count transitions
    for i in range(N - 1):
        u = pi[i]
        v = pi[i+1]
        trans_counts[u][v] += 1
        state_total_trans[u] += 1
        
    # Emissiyaları sayırıq
    # Count emissions
    for i in range(N):
        s = pi[i]
        char = x[i]
        emit_counts[s][char] += 1
        state_total_emit[s] += 1
        
    # Keçid ehtimallarını hesablayırıq
    # Calculate transition probabilities
    transition = {s: {t: 0.0 for t in states} for s in states}
    for s in states:
        total = state_total_trans[s]
        if total > 0:
            for t in states:
                transition[s][t] = trans_counts[s][t] / total
        else:
            for t in states:
                transition[s][t] = 1.0 / K
                
    # Emissiya ehtimallarını hesablayırıq
    # Calculate emission probabilities
    emission = {s: {a: 0.0 for a in alphabet} for s in states}
    for s in states:
        total = state_total_emit[s]
        if total > 0:
            for a in alphabet:
                emission[s][a] = emit_counts[s][a] / total
        else:
            for a in alphabet:
                emission[s][a] = 1.0 / M
                
    return transition, emission

# Viterbi öyrənmə alqoritmini təyin edirik
# Run Viterbi learning iterations to optimize HMM transition and emission matrices
def run_viterbi_learning(x, alphabet, states, transition, emission, num_iter):
    for it in range(num_iter):
        pi = solve_viterbi(x, alphabet, states, transition, emission)
        transition, emission = estimate_hmm_parameters(x, alphabet, pi, states)
    return transition, emission

# Matrisi formatlamaq üçün köməkçi funksiya
# Helper function to format the matrix output in the required Rosalind format
def format_matrix(states, target_headers, matrix):
    output_lines = []
    output_lines.append("\t" + "\t".join(target_headers))
    for s in states:
        vals = []
        for t in target_headers:
            val = matrix[s][t]
            if val == 0:
                vals.append("0")
            elif val == int(val):
                vals.append(f"{float(val):.1f}")
            else:
                vals.append(str(round(val, 3)))
        output_lines.append(s + "\t" + "\t".join(vals))
    return "\n".join(output_lines)

# Əsas icra funksiyası
# Main execution function
def main():
    # Giriş və çıxış fayllarının yollarını cari qovluğa görə müəyyən edirik
    # Set input and output file paths relative to the current directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba10i.txt")
    output_file = os.path.join(script_dir, "output.txt")
    
    # Giriş faylını oxuyuruq
    # Read the input file
    with open(input_file, "r") as f:
        raw_content = f.read()
        
    parts = [p.strip() for p in raw_content.split("--------") if p.strip()]
    
    num_iter = int(parts[0])
    x = parts[1]
    alphabet = parts[2].split()
    states = parts[3].split()
    
    # Keçid matrisini oxuyuruq
    # Parse transition matrix
    transition_lines = parts[4].splitlines()
    trans_header = transition_lines[0].split()
    transition = {}
    for line in transition_lines[1:]:
        parts_line = line.split()
        if not parts_line:
            continue
        state = parts_line[0]
        transition[state] = {}
        for h, val in zip(trans_header, parts_line[1:]):
            transition[state][h] = float(val)
            
    # Emissiya matrisini oxuyuruq
    # Parse emission matrix
    emission_lines = parts[5].splitlines()
    emit_header = emission_lines[0].split()
    emission = {}
    for line in emission_lines[1:]:
        parts_line = line.split()
        if not parts_line:
            continue
        state = parts_line[0]
        emission[state] = {}
        for h, val in zip(emit_header, parts_line[1:]):
            emission[state][h] = float(val)
            
    # Viterbi öyrənmə alqoritmini işlədirik
    # Execute Viterbi learning iterations
    t, e = run_viterbi_learning(x, alphabet, states, transition, emission, num_iter)
    
    # Nəticə matrislərini formatlayırıq
    # Format resulting matrices
    trans_str = format_matrix(states, states, t)
    emit_str = format_matrix(states, alphabet, e)
    
    # Nəticəni çıxış faylına yazırıq
    # Write the formatted output to output.txt
    with open(output_file, "w") as f:
        f.write(trans_str + "\n")
        f.write("--------\n")
        f.write(emit_str + "\n")
        
    print("Viterbi learning successfully completed and written to output.txt")

if __name__ == "__main__":
    main()
