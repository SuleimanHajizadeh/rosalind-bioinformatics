# Həlli üçün lazım olan modulu daxil edirik
# Import the required module for the solution
import os

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
    
    # 1. Hər sütunda boşluq simvolunun (-) nisbətini yoxlayaraq "uyğunluq" sütunlarını təyin edirik
    # 1. Identify "match" columns by checking the fraction of gap symbols (-) in each column
    match_cols = []
    for col in range(L):
        gap_count = sum(1 for seq in alignment if seq[col] == '-')
        gap_fraction = gap_count / num_seq
        if gap_fraction < theta:
            match_cols.append(col)
            
    n = len(match_cols)
    
    # Bütün mümkün HMM vəziyyətlərinin ardıcıllığını müəyyən edirik
    # Define the sequence of all possible HMM states
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
            
    # Hər bir daxiletmə sütunundan əvvəl neçə uyğunluq sütunu olduğunu təyin edirik
    # Identify the number of match columns appearing before each insertion column
    num_match_before = {}
    match_counter = 0
    for col in range(L):
        num_match_before[col] = match_counter
        if col in match_set:
            match_counter += 1
            
    # 2. Hər bir hizalanmış sətir üçün keçid yolunu və emissiyaları müəyyən edirik
    # 2. Trace path and emissions for each alignment string
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
            
    # İlk olaraq normallaşdırılmamış (xam) keçid ehtimallarını hesablayırıq
    # Compute raw transition probabilities
    raw_transition = {s: {t: 0.0 for t in states} for s in states}
    for s in states:
        total = state_total_trans[s]
        if total > 0:
            for t in states:
                raw_transition[s][t] = trans_counts[s][t] / total
                
    # İlk olaraq normallaşdırılmamış (xam) emissiya ehtimallarını hesablayırıq
    # Compute raw emission probabilities
    raw_emission = {s: {a: 0.0 for a in alphabet} for s in states}
    for s in states:
        total = state_total_emit[s]
        if total > 0:
            for a in alphabet:
                raw_emission[s][a] = emit_counts[s][a] / total
                
    # Psevdohisablar (pseudocounts) əlavə edib keçid matrisini yenidən normallaşdırırıq
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
                
    # Psevdohisablar əlavə edib emissiya matrisini yenidən normallaşdırırıq
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

# Nəticəni tələb olunan formatda string olaraq hazırlayan köməkçi funksiya
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
    input_file = os.path.join(script_dir, "rosalind_ba10f.txt")
    output_file = os.path.join(script_dir, "output.txt")
    
    # Giriş faylını oxuyuruq
    # Read the input file
    with open(input_file, "r") as f:
        raw_content = f.read()
        
    parts = [p.strip() for p in raw_content.split("--------") if p.strip()]
    
    first_line_parts = parts[0].split()
    theta = float(first_line_parts[0])
    sigma = float(first_line_parts[1])
    
    alphabet = parts[1].split()
    alignment = [line.strip() for line in parts[2].splitlines() if line.strip()]
    
    # Psevdohisablarla Profil HMM-i qururuq
    # Construct the Profile HMM with Pseudocounts
    states, transition, emission = construct_profile_hmm_pseudo(theta, sigma, alphabet, alignment)
    
    # Keçid və emissiya matrislərini formatlayırıq
    # Format the transition and emission matrices
    trans_str = format_matrix(states, states, transition)
    emit_str = format_matrix(states, alphabet, emission)
    
    # Nəticəni çıxış faylına yazırıq
    # Write the formatted output to output.txt
    with open(output_file, "w") as f:
        f.write(trans_str + "\n")
        f.write("--------\n")
        f.write(emit_str + "\n")
        
    print("Profile HMM with Pseudocounts successfully written to output.txt")

if __name__ == "__main__":
    main()
