# Həlli üçün lazım olan modulları daxil edirik
# Import the required modules for the solution
import os
import math

# İki vəziyyət arasındakı keçidin HMM qrafında icazəli olub-olmadığını yoxlayırıq
# Determine if the transition from state1 to state2 is allowed (non-forbidden) in the Profile HMM
def is_transition_valid(state1, state2, end_idx):
    def parse_state(state):
        s_type = state.rstrip('0123456789')
        s_idx = state[len(s_type):]
        if s_type == 'S':
            s_idx = 0
        return s_type, int(s_idx) if s_idx != '' else -1

    state1, state2 = [parse_state(s) for s in (state1, state2)]

    # Son vəziyyətə keçidlərin yoxlanması
    # Valid transitions to the end state
    if state2[0] == 'E':
        if state1[0] + str(state1[1]) in [s + str(end_idx) for s in ['M', 'I', 'D']]:
            return True

    # Digər icazəli keçidlərin yoxlanması
    # Other valid transitions
    if state1[0] != 'E':
        if state2[0] + str(state2[1]) in ['D' + str(state1[1] + 1), 'M' + str(state1[1] + 1), 'I' + str(state1[1])]:
            return True

    return False

# Psevdohisablar (pseudocounts) daxil olmaqla Profil HMM quran funksiyanı təyin edirik
# Define a function to construct a Profile HMM with Pseudocounts
def construct_profile_hmm_pseudo(theta, sigma, alphabet, alignment):
    L = len(alignment[0])
    num_seq = len(alignment)
    
    # Hər sütunda boşluq simvolunun (-) nisbətini yoxlayaraq "uyğunluq" sütunlarını təyin edirik
    # Identify "match" columns by checking the fraction of gap symbols (-) in each column
    match_cols = []
    for col in range(L):
        gap_count = sum(1 for seq in alignment if seq[col] == '-')
        gap_fraction = gap_count / num_seq
        if gap_fraction < theta:
            match_cols.append(col)
            
    n = len(match_cols)
    
    # Bütün HMM vəziyyətlərini müəyyən edirik
    # Define the sequence of all HMM states
    states = ['S', 'I0']
    for i in range(1, n + 1):
        states.extend([f'M{i}', f'D{i}', f'I{i}'])
    states.append('E')
    
    # Sütun indekslərini müvafiq HMM vəziyyət indekslərinə uyğunlaşdırırıq
    # Map alignment column indices to the corresponding match state indices
    col_to_match_idx = {}
    match_set = set(match_cols)
    match_counter = 0
    for col in range(L):
        if col in match_set:
            match_counter += 1
            col_to_match_idx[col] = match_counter
        else:
            col_to_match_idx[col] = None
            
    # Hər daxiletmə sütunundan əvvəl olan uyğunluq sütunlarının sayını tapırıq
    # Identify the number of match columns appearing before each insertion column
    num_match_before = {}
    match_counter = 0
    for col in range(L):
        num_match_before[col] = match_counter
        if col in match_set:
            match_counter += 1
            
    # Hər sətir üçün keçid yolunu və emissiyaları tapırıq
    # Trace path and emissions for each alignment string
    paths = []
    emissions = []
    
    for seq in alignment:
        path = ['S']
        seq_emissions = []
        for col in range(L):
            char = seq[col]
            if col in match_set:
                m_idx = col_to_match_idx[col]
                if char != '-':
                    state = f'M{m_idx}'
                    seq_emissions.append((state, char))
                else:
                    state = f'D{m_idx}'
                path.append(state)
            else:
                k = num_match_before[col]
                if char != '-':
                    state = f'I{k}'
                    seq_emissions.append((state, char))
                    path.append(state)
        path.append('E')
        paths.append(path)
        emissions.append(seq_emissions)
        
    # Keçidlərin və emissiyaların sayını hesablamaq üçün strukturlar yaradırıq
    # Create structures to count transitions and emissions
    trans_counts = {s: {t: 0 for t in states} for s in states}
    state_total_trans = {s: 0 for s in states}
    
    emit_counts = {s: {a: 0 for a in alphabet} for s in states}
    state_total_emit = {s: 0 for s in states}
    
    # Keçidləri sayırıq
    # Count transitions from paths
    for path in paths:
        for u, v in zip(path[:-1], path[1:]):
            trans_counts[u][v] += 1
            state_total_trans[u] += 1
            
    # Emissiyaları sayırıq
    # Count emissions
    for seq_emissions in emissions:
        for state, char in seq_emissions:
            emit_counts[state][char] += 1
            state_total_emit[state] += 1
            
    # Xam keçid ehtimallarını hesablayırıq
    # Compute raw transition probabilities
    raw_transition = {s: {t: 0.0 for t in states} for s in states}
    for s in states:
        total = state_total_trans[s]
        if total > 0:
            for t in states:
                raw_transition[s][t] = trans_counts[s][t] / total
                
    # Xam emissiya ehtimallarını hesablayırıq
    # Compute raw emission probabilities
    raw_emission = {s: {a: 0.0 for a in alphabet} for s in states}
    for s in states:
        total = state_total_emit[s]
        if total > 0:
            for a in alphabet:
                raw_emission[s][a] = emit_counts[s][a] / total
                
    # Psevdohisablarla keçid matrisini yenidən normallaşdırırıq
    # Apply pseudocounts and renormalize the transition matrix
    transition = {s: {t: 0.0 for t in states} for s in states}
    for s1 in states:
        norm_factor = 0.0
        for s2 in states:
            if is_transition_valid(s1, s2, n):
                norm_factor += raw_transition[s1][s2] + sigma
                
        for s2 in states:
            if is_transition_valid(s1, s2, n):
                transition[s1][s2] = (raw_transition[s1][s2] + sigma) / norm_factor
            else:
                transition[s1][s2] = raw_transition[s1][s2]
                
    # Psevdohisablarla emissiya matrisini yenidən normallaşdırırıq
    # Apply pseudocounts and renormalize the emission matrix
    emission = {s: {a: 0.0 for a in alphabet} for s in states}
    for s in states:
        if s != 'S' and s != 'E' and not s.startswith('D'):
            norm_factor = 0.0
            for a in alphabet:
                norm_factor += raw_emission[s][a] + sigma
            for a in alphabet:
                emission[s][a] = (raw_emission[s][a] + sigma) / norm_factor
        else:
            for a in alphabet:
                emission[s][a] = raw_emission[s][a]
                
    return states, transition, emission

# Viterbi alqoritmini təyin edirik
# Define the Viterbi algorithm to align text to the Profile HMM
def solve_viterbi_profile_hmm(text, states, transition, emission):
    N = len(text)
    n_match = 0
    for s in states:
        if s.startswith('M'):
            n_match = max(n_match, int(s[1:]))
            
    # Keçid ehtimallarının logaritmini hesablayırıq
    # Compute log transition probabilities
    log_trans = {}
    for s1 in states:
        log_trans[s1] = {}
        for s2 in states:
            p = transition[s1][s2]
            log_trans[s1][s2] = math.log(p) if p > 0 else -float('inf')
            
    # Emissiya ehtimallarının logaritmini hesablayırıq
    # Compute log emission probabilities
    log_emit = {}
    for s in states:
        log_emit[s] = {}
        is_emit = s != 'S' and s != 'E' and not s.startswith('D')
        for a in emission[s]:
            p = emission[s][a] if is_emit else 0.0
            log_emit[s][a] = math.log(p) if p > 0 else -float('inf')
            
    # Dinamik proqramlaşdırma və geriyə izləmə cədvəllərini yaradırıq
    # Create the DP table and backtrack tracking tables
    dp = [ {s: -float('inf') for s in states} for _ in range(N + 1) ]
    backtrack = [ {s: None for s in states} for _ in range(N + 1) ]
    
    # t = 0 üçün ilkin vəziyyəti təyin edirik
    # Initialize DP at time step t = 0
    dp[0]['S'] = 0.0
    
    # t = 0 addımında səssiz silinmə (deletion) vəziyyətləri üçün ehtimalları yayırıq
    # Propagate silent deletion states at step t = 0
    for k in range(1, n_match + 1):
        best_val = -float('inf')
        best_prev = None
        
        # D_{k-1}-dən keçid
        # Transition from D_{k-1}
        prev_D = f'D{k-1}' if k > 1 else None
        if prev_D and dp[0][prev_D] + log_trans[prev_D][f'D{k}'] > best_val:
            best_val = dp[0][prev_D] + log_trans[prev_D][f'D{k}']
            best_prev = prev_D
            
        # M_{k-1}-dən keçid
        # Transition from M_{k-1}
        prev_M = f'M{k-1}' if k > 1 else 'S'
        if dp[0][prev_M] + log_trans[prev_M][f'D{k}'] > best_val:
            best_val = dp[0][prev_M] + log_trans[prev_M][f'D{k}']
            best_prev = prev_M
            
        # I_{k-1}-dən keçid
        # Transition from I_{k-1}
        prev_I = f'I{k-1}'
        if dp[0][prev_I] + log_trans[prev_I][f'D{k}'] > best_val:
            best_val = dp[0][prev_I] + log_trans[prev_I][f'D{k}']
            best_prev = prev_I
            
        if best_val > -float('inf'):
            dp[0][f'D{k}'] = best_val
            backtrack[0][f'D{k}'] = (0, best_prev)
            
    # t = 1-dən N-ə qədər olan addımlar üzrə dinamik proqramlaşdırma işlədirik
    # Run DP iteration for time steps t = 1 to N
    for i in range(1, N + 1):
        char = text[i-1]
        
        # Addım A: Emissiya edən vəziyyətlərin (M_k və I_k) ehtimallarını hesablayırıq
        # Step A: Compute emitting states (M_k and I_k) from i-1
        for s in states:
            if s.startswith('M') or s.startswith('I'):
                best_val = -float('inf')
                best_prev = None
                
                for prev_s in states:
                    if is_transition_valid(prev_s, s, n_match):
                        val = dp[i-1][prev_s] + log_trans[prev_s][s] + log_emit[s][char]
                        if val > best_val:
                            best_val = val
                            best_prev = prev_s
                if best_val > -float('inf'):
                    dp[i][s] = best_val
                    backtrack[i][s] = (i-1, best_prev)
                    
        # Addım B: Səssiz silinmə (deletion) vəziyyətləri üzrə ehtimalları yayırıq
        # Step B: Propagate silent deletion states at current step i
        for k in range(1, n_match + 1):
            best_val = -float('inf')
            best_prev = None
            
            prev_D = f'D{k-1}' if k > 1 else None
            if prev_D and dp[i][prev_D] + log_trans[prev_D][f'D{k}'] > best_val:
                best_val = dp[i][prev_D] + log_trans[prev_D][f'D{k}']
                best_prev = prev_D
                
            prev_M = f'M{k-1}' if k > 1 else 'S'
            if dp[i][prev_M] + log_trans[prev_M][f'D{k}'] > best_val:
                best_val = dp[i][prev_M] + log_trans[prev_M][f'D{k}']
                best_prev = prev_M
                
            prev_I = f'I{k-1}'
            if dp[i][prev_I] + log_trans[prev_I][f'D{k}'] > best_val:
                best_val = dp[i][prev_I] + log_trans[prev_I][f'D{k}']
                best_prev = prev_I
                
            if best_val > -float('inf'):
                dp[i][f'D{k}'] = best_val
                backtrack[i][f'D{k}'] = (i, best_prev)
                
    # Son addım: E vəziyyətinə ən yaxşı keçidi tapırıq
    # Final step: Transition to E at i = N
    best_val = -float('inf')
    best_prev = None
    for prev_s in states:
        if is_transition_valid(prev_s, 'E', n_match):
            val = dp[N][prev_s] + log_trans[prev_s]['E']
            if val > best_val:
                best_val = val
                best_prev = prev_s
                
    # Geriyə izləmə yolu ilə optimal vəziyyət ardıcıllığını tapırıq
    # Backtrack path to retrieve the optimal hidden path of states
    curr_i = N
    curr_s = best_prev
    path = []
    
    while curr_s != 'S':
        path.append(curr_s)
        curr_i, curr_s = backtrack[curr_i][curr_s]
        
    path.reverse()
    return " ".join(path)

# Əsas icra funksiyası
# Main execution function
def main():
    # Giriş və çıxış fayllarının yollarını cari qovluğa görə müəyyən edirik
    # Set input and output file paths relative to the current directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba10g.txt")
    output_file = os.path.join(script_dir, "output.txt")
    
    # Giriş faylını oxuyuruq
    # Read the input file
    with open(input_file, "r") as f:
        raw_content = f.read()
        
    parts = [p.strip() for p in raw_content.split("--------") if p.strip()]
    
    text = parts[0]
    
    first_line_parts = parts[1].split()
    theta = float(first_line_parts[0])
    sigma = float(first_line_parts[1])
    
    alphabet = parts[2].split()
    alignment = [line.strip() for line in parts[3].splitlines() if line.strip()]
    
    # Profil HMM matrislərini qururuq
    # Construct the Profile HMM matrices
    states, transition, emission = construct_profile_hmm_pseudo(theta, sigma, alphabet, alignment)
    
    # Viterbi alqoritmi ilə optimal yolu tapırıq
    # Find the optimal hidden path using Viterbi decoding
    result = solve_viterbi_profile_hmm(text, states, transition, emission)
    
    # Nəticəni çıxış faylına yazırıq
    # Write the result path to the output file
    with open(output_file, "w") as f:
        f.write(result + "\n")
        
    print("Optimal hidden path successfully written to output.txt")

if __name__ == "__main__":
    main()
