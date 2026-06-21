# Həlli üçün lazım olan modulları daxil edirik
# Import the required modules for the solution
import os

# Baum-Welch alqoritmini təyin edirik
# Define the Baum-Welch algorithm
def run_baum_welch_scaled(x, alphabet, states, transition, emission, num_iter):
    N = len(x)
    K = len(states)
    
    # Başlanğıc vəziyyət ehtimalını 1/K olaraq təyin edirik
    # Initialize state start probabilities to 1/K
    init_prob = {s: 1.0 / K for s in states}
    
    for it in range(num_iter):
        # 1. Forward pass with scaling (İrəli keçid miqyaslaşdırma ilə)
        forward = [ {s: 0.0 for s in states} for _ in range(N) ]
        scale = [ 1.0 for _ in range(N) ]
        
        # t = 0 üçün irəli ehtimalları və miqyas əmsalını hesablayırıq
        # Calculate forward probabilities and scaling factor for t = 0
        s_val = 0.0
        for s in states:
            forward[0][s] = init_prob[s] * emission[s][x[0]]
            s_val += forward[0][s]
        if s_val > 0:
            scale[0] = s_val
            for s in states:
                forward[0][s] /= s_val
                
        # t = 1-dən N-1-ə qədər irəli ehtimalları və miqyas əmsallarını hesablayırıq
        # Calculate forward probabilities and scaling factors for t = 1 to N-1
        for i in range(1, N):
            char = x[i]
            s_val = 0.0
            for curr_s in states:
                val = 0.0
                for prev_s in states:
                    val += forward[i-1][prev_s] * transition[prev_s][curr_s]
                forward[i][curr_s] = val * emission[curr_s][char]
                s_val += forward[i][curr_s]
            if s_val > 0:
                scale[i] = s_val
                for curr_s in states:
                    forward[i][curr_s] /= s_val
                    
        # 2. Backward pass with scaling (Geri keçid miqyaslaşdırma ilə)
        backward = [ {s: 0.0 for s in states} for _ in range(N) ]
        for s in states:
            backward[-1][s] = 1.0
            
        for i in range(N - 2, -1, -1):
            next_char = x[i+1]
            for curr_s in states:
                val = 0.0
                for next_s in states:
                    val += backward[i+1][next_s] * transition[curr_s][next_s] * emission[next_s][next_char]
                backward[i][curr_s] = val / scale[i+1]
                
        # 3. Node and Edge responsibilities (Təpə və til məsuliyyət dərəcələri)
        node_resp = [ {s: 0.0 for s in states} for _ in range(N) ]
        for i in range(N):
            denom = sum(forward[i][s] * backward[i][s] for s in states)
            for s in states:
                node_resp[i][s] = (forward[i][s] * backward[i][s]) / denom if denom > 0 else 1.0 / K
                
        edge_resp = [ {s1: {s2: 0.0 for s2 in states} for s1 in states} for _ in range(N - 1) ]
        for i in range(N - 1):
            next_char = x[i+1]
            denom = 0.0
            for s1 in states:
                for s2 in states:
                    val = forward[i][s1] * transition[s1][s2] * emission[s2][next_char] * backward[i+1][s2]
                    edge_resp[i][s1][s2] = val
                    denom += val
            for s1 in states:
                for s2 in states:
                    edge_resp[i][s1][s2] = edge_resp[i][s1][s2] / denom if denom > 0 else 0.0
                    
        # 4. M-step: Keçid və emissiya matrislərinin yenilənməsi
        # 4. M-step: Update transition and emission matrices
        new_transition = {s1: {s2: 0.0 for s2 in states} for s1 in states}
        for s1 in states:
            denom = sum(sum(edge_resp[i][s1][s2] for i in range(N - 1)) for s2 in states)
            for s2 in states:
                num = sum(edge_resp[i][s1][s2] for i in range(N - 1))
                new_transition[s1][s2] = num / denom if denom > 0 else 1.0 / K
                
        new_emission = {s: {a: 0.0 for a in alphabet} for s in states}
        for s in states:
            denom = sum(node_resp[i][s] for i in range(N))
            for a in alphabet:
                num = sum(node_resp[i][s] if x[i] == a else 0.0 for i in range(N))
                new_emission[s][a] = num / denom if denom > 0 else 1.0 / len(alphabet)
                
        transition = new_transition
        emission = new_emission
        
    return transition, emission

# Əsas icra funksiyası
# Main execution function
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba10k.txt")
    output_file = os.path.join(script_dir, "output.txt")
    
    # Giriş faylı yoxdursa, işi dayandırırıq
    # If input file doesn't exist, stop execution
    if not os.path.exists(input_file):
        print(f"Input file not found at {input_file}")
        return
        
    # Giriş faylını oxuyuruq
    # Read the input file
    with open(input_file, "r") as f:
        raw_content = f.read()
        
    parts = [p.strip() for p in raw_content.split("--------") if p.strip()]
    
    # İterasiya sayını və x simvol ardıcıllığını oxuyuruq
    # Parse iteration count and sequence x
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
            
    # Baum-Welch öyrənmə alqoritmini işə salırıq
    # Run the Baum-Welch learning algorithm
    t, e = run_baum_welch_scaled(x, alphabet, states, transition, emission, num_iter)
    
    # Keçid və emissiya matrislərini formatlayırıq
    # Format the transition and emission matrices
    trans_str = format_matrix(states, states, t)
    emit_str = format_matrix(states, alphabet, e)
    
    # Nəticəni çıxış faylına yazırıq
    # Write the formatted output to output.txt
    with open(output_file, "w") as f:
        f.write(trans_str + "\n")
        f.write("--------\n")
        f.write(emit_str + "\n")
        
    print("Baum-Welch learning completed successfully. Results written to output.txt")

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

if __name__ == "__main__":
    main()
