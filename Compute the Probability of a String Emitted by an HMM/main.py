# Həlli üçün lazım olan modulları daxil edirik
# Import the required modules for the solution
import os

# Verilmiş sətrin HMM tərəfindən emissiya edilmə ehtimalını hesablamaq üçün Forward alqoritmini təyin edirik
# Define the Forward algorithm to compute the probability of a string emitted by an HMM
def solve_forward(x, alphabet, states, transition, emission):
    N = len(x)
    K = len(states)
    
    # Başlanğıc ehtimallarının bərabər olduğunu fərz edirik (1 / vəziyyətlərin sayı)
    # Assume that initial probabilities are equal (1 / number of states)
    init_prob = {state: 1.0 / K for state in states}
    
    # Dinamik proqramlaşdırma cədvəlini yaradırıq (hər addım üçün ehtimalları saxlamaq üçün)
    # Create the dynamic programming table (to store probabilities at each step)
    dp = []
    
    # t = 0 üçün ilkin vəziyyətlərin ehtimallarını hesablayırıq
    # Initialize DP at t = 0
    dp_t = {}
    for state in states:
        dp_t[state] = init_prob[state] * emission[state][x[0]]
    dp.append(dp_t)
    
    # t = 1-dən N-1-ə qədər olan addımlar üçün irəli ehtimalları hesablayırıq
    # Compute forward probabilities for time steps t = 1 to N-1
    for i in range(1, N):
        dp_t = {}
        for curr_state in states:
            val = 0.0
            p_emit = emission[curr_state][x[i]]
            # Əvvəlki vəziyyətlərdən keçid ehtimallarının cəmini hesablayırıq
            # Sum up transition probabilities from all previous states
            for prev_state in states:
                p_trans = transition[prev_state][curr_state]
                val += dp[i-1][prev_state] * p_trans
            dp_t[curr_state] = val * p_emit
        dp.append(dp_t)
        
    # Son addımdakı bütün vəziyyətlərin ehtimallarını toplayırıq
    # Sum up the probabilities of all states at the final step
    return sum(dp[-1][s] for s in states)

# Əsas icra funksiyası
# Main execution function
def main():
    # Giriş və çıxış fayllarının yollarını cari qovluğa görə müəyyən edirik
    # Set input and output file paths relative to the current directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba10d.txt")
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
            
    # Forward alqoritmini çağırıb ümumi ehtimalı tapırıq
    # Solve the forward probability and retrieve result
    result = solve_forward(x, alphabet, states, transition, emission)
    
    # Nəticəni çıxış faylına yazırıq
    # Write the result probability to the output file
    with open(output_file, "w") as f:
        f.write(str(result) + "\n")
    print("Outcome likelihood probability successfully written to output.txt")

if __name__ == "__main__":
    main()
