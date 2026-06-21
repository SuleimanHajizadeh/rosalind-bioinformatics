# Həlli üçün lazım olan modulu daxil edirik
# Import the required module for the solution
import os

# Verilmiş emissiya ardıcıllığı və gizli yola əsasən HMM parametrlərini qiymətləndiririk
# Estimate the HMM parameters (transition and emission matrices) from the emission sequence and state path
def estimate_hmm_parameters(x, alphabet, pi, states):
    K = len(states)
    M = len(alphabet)
    N = len(pi)
    
    # Keçidlərin və emissiyaların sayını hesablamaq üçün strukturlar qururuq
    # Create structures to count transition and emission events
    trans_counts = {s: {t: 0 for t in states} for s in states}
    state_total_trans = {s: 0 for s in states}
    
    emit_counts = {s: {a: 0 for a in alphabet} for s in states}
    state_total_emit = {s: 0 for s in states}
    
    # Keçidləri sayırıq
    # Count state transitions along the path pi
    for i in range(N - 1):
        u = pi[i]
        v = pi[i+1]
        trans_counts[u][v] += 1
        state_total_trans[u] += 1
        
    # Emissiyaları sayırıq
    # Count symbol emissions along x and pi
    for i in range(N):
        s = pi[i]
        char = x[i]
        emit_counts[s][char] += 1
        state_total_emit[s] += 1
        
    # Keçid ehtimalları matrisini hesablayırıq
    # Calculate the transition probability matrix
    transition = {s: {t: 0.0 for t in states} for s in states}
    for s in states:
        total = state_total_trans[s]
        if total > 0:
            for t in states:
                transition[s][t] = trans_counts[s][t] / total
        else:
            # Əgər keçid yoxdursa, bərabər ehtimallar təyin edirik
            # If no outgoing transitions, assign uniform probabilities
            for t in states:
                transition[s][t] = 1.0 / K
                
    # Emissiya ehtimalları matrisini hesablayırıq
    # Calculate the emission probability matrix
    emission = {s: {a: 0.0 for a in alphabet} for s in states}
    for s in states:
        total = state_total_emit[s]
        if total > 0:
            for a in alphabet:
                emission[s][a] = emit_counts[s][a] / total
        else:
            # Əgər vəziyyət heç ziyarət olunmayıbsa, bərabər ehtimallar təyin edirik
            # If a state is never visited, assign uniform probabilities
            for a in alphabet:
                emission[s][a] = 1.0 / M
                
    return transition, emission

# Matrisi Rosalind formatında təqdim etmək üçün köməkçi funksiya
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
    input_file = os.path.join(script_dir, "rosalind_ba10h.txt")
    output_file = os.path.join(script_dir, "output.txt")
    
    # Giriş faylını oxuyuruq
    # Read the input file
    with open(input_file, "r") as f:
        raw_content = f.read()
        
    parts = [p.strip() for p in raw_content.split("--------") if p.strip()]
    
    x = parts[0]
    alphabet = parts[1].split()
    pi = parts[2]
    states = parts[3].split()
    
    # HMM parametrlərini qiymətləndiririk
    # Estimate the HMM parameters
    transition, emission = estimate_hmm_parameters(x, alphabet, pi, states)
    
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
        
    print("HMM parameters successfully estimated and written to output.txt")

if __name__ == "__main__":
    main()
