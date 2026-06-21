# Həlli üçün lazım olan modulları daxil edirik
# Import the required modules for the solution
import os

# HMM soft decoding (Forward-Backward) alqoritmini təyin edirik
# Define the HMM soft decoding (Forward-Backward) algorithm
def solve_soft_decoding(x, alphabet, states, transition, emission):
    N = len(x)
    K = len(states)
    
    # Başlanğıc ehtimallarının bərabər olduğunu fərz edirik (1 / vəziyyətlərin sayı)
    # Assume that initial probabilities are equal (1 / number of states)
    init_prob = {state: 1.0 / K for state in states}
    
    # 1. İrəli (Forward) ehtimalları hesablayırıq
    # 1. Compute Forward probabilities: forward[i][s] = F(i, s)
    forward = [ {s: 0.0 for s in states} for _ in range(N) ]
    for s in states:
        forward[0][s] = init_prob[s] * emission[s][x[0]]
        
    for i in range(1, N):
        char = x[i]
        for curr_s in states:
            val = 0.0
            p_emit = emission[curr_s][char]
            for prev_s in states:
                val += forward[i-1][prev_s] * transition[prev_s][curr_s]
            forward[i][curr_s] = val * p_emit
            
    # Ümumi ehtimalı P(x) hesablayırıq
    # Compute total probability P(x)
    p_x = sum(forward[-1][s] for s in states)
    
    # 2. Geri (Backward) ehtimalları hesablayırıq
    # 2. Compute Backward probabilities: backward[i][s] = B(i, s)
    backward = [ {s: 0.0 for s in states} for _ in range(N) ]
    for s in states:
        backward[-1][s] = 1.0
        
    for i in range(N - 2, -1, -1):
        next_char = x[i+1]
        for curr_s in states:
            val = 0.0
            for next_s in states:
                val += backward[i+1][next_s] * transition[curr_s][next_s] * emission[next_s][next_char]
            backward[i][curr_s] = val
            
    # 3. Hər bir addımda soft decoding ehtimallarını hesablayırıq
    # 3. Compute posterior soft decoding probabilities: posterior = F(i, s) * B(i, s) / P(x)
    soft = []
    for i in range(N):
        row = {}
        for s in states:
            row[s] = (forward[i][s] * backward[i][s]) / p_x
        soft.append(row)
        
    return soft

# Əsas icra funksiyası
# Main execution function
def main():
    # Giriş və çıxış fayllarının yollarını cari qovluğa görə müəyyən edirik
    # Set input and output file paths relative to the current directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba10j.txt")
    output_file = os.path.join(script_dir, "output.txt")
    
    # Giriş faylını oxuyuruq
    # Read the input file
    with open(input_file, "r") as f:
        raw_content = f.read()
        
    parts = [p.strip() for p in raw_content.split("--------") if p.strip()]
    
    x = parts[0]
    alphabet = parts[1].split()
    states = parts[2].split()
    
    # Keçid matrisini oxuyuruq
    # Parse transition matrix
    transition_lines = parts[3].splitlines()
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
    emission_lines = parts[4].splitlines()
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
            
    # Soft decoding ehtimallarını hesablayırıq
    # Compute soft decoding probabilities
    soft = solve_soft_decoding(x, alphabet, states, transition, emission)
    
    # Nəticəni çıxış faylına formatlaşdırılmış şəkildə yazırıq
    # Write the formatted soft decoding output to output.txt
    output_lines = []
    output_lines.append("\t".join(states))
    for row in soft:
        output_lines.append("\t".join(str(round(row[s], 4)) for s in states))
        
    with open(output_file, "w") as f:
        f.write("\n".join(output_lines) + "\n")
        
    print("Soft decoding probabilities successfully calculated and written to output.txt")

if __name__ == "__main__":
    main()
