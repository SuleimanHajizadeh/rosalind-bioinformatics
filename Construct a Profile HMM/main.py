# Həlli üçün lazım olan modulu daxil edirik
# Import the required module for the solution
import os

# Profil HMM qurmaq və ehtimalları hesablamaq üçün funksiyanı təyin edirik
# Define a function to construct a Profile HMM and compute probabilities
def construct_profile_hmm(theta, alphabet, alignment):
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
            
    # Keçid ehtimalları matrisini hesablayırıq
    # Calculate transition probabilities
    transition = {s: {t: 0.0 for t in states} for s in states}
    for s in states:
        total = state_total_trans[s]
        if total > 0:
            for t in states:
                transition[s][t] = trans_counts[s][t] / total
                
    # Emissiya ehtimalları matrisini hesablayırıq
    # Calculate emission probabilities
    emission = {s: {a: 0.0 for a in alphabet} for s in states}
    for s in states:
        total = state_total_emit[s]
        if total > 0:
            for a in alphabet:
                emission[s][a] = emit_counts[s][a] / total
                
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
    input_file = os.path.join(script_dir, "rosalind_ba10e.txt")
    output_file = os.path.join(script_dir, "output.txt")
    
    # Giriş faylını oxuyuruq
    # Read the input file
    with open(input_file, "r") as f:
        raw_content = f.read()
        
    parts = [p.strip() for p in raw_content.split("--------") if p.strip()]
    theta = float(parts[0])
    alphabet = parts[1].split()
    alignment = [line.strip() for line in parts[2].splitlines() if line.strip()]
    
    # Profil HMM-i qururuq
    # Construct the Profile HMM
    states, transition, emission = construct_profile_hmm(theta, alphabet, alignment)
    
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
        
    print("Profile HMM successfully written to output.txt")

if __name__ == "__main__":
    main()
