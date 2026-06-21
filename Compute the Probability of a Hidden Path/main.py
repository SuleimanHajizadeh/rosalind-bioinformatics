# Həlli üçün lazım olan modulu daxil edirik
# Import the required module for the solution
import os

def main():
    # Cari skriptin qovluğunu tapırıq və giriş/çıxış fayllarının yollarını müəyyən edirik
    # Get the directory of the current script and define paths for input/output files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba10a.txt")
    output_file = os.path.join(script_dir, "output.txt")
    
    # Giriş faylını oxumaq üçün açırıq
    # Open the input file for reading
    with open(input_file, "r") as f:
        # Birinci sətirdən gizli yolu oxuyuruq
        # Read the hidden path from the first line
        path = f.readline().strip()
        
        # Sonrakı sətirləri oxuyuruq və təmizləyirik
        # Read the subsequent lines and strip them
        lines = [line.strip() for line in f if line.strip()]
        
    # Seperatoru və vəziyyətləri tapırıq
    # Locate the separator and states
    # Biz bilirik ki, faylda "--------" ayırıcı sətirləri var
    # We know that the file contains "--------" separator lines
    idx = 0
    while idx < len(lines) and lines[idx] == "--------":
        idx += 1
        
    # Vəziyyətləri oxuyuruq
    # Read the states
    states = lines[idx].split()
    idx += 1
    
    # Növbəti ayırıcını keçirik
    # Skip the next separator
    while idx < len(lines) and lines[idx] == "--------":
        idx += 1
        
    # Matris başlığını oxuyuruq
    # Read the matrix header
    target_states = lines[idx].split()
    idx += 1
    
    # Keçid ehtimalları matrisini qururuq
    # Construct the transition probability matrix
    transition = {s: {} for s in states}
    while idx < len(lines):
        parts = lines[idx].split()
        if len(parts) >= 1 + len(target_states):
            source = parts[0]
            for j, target in enumerate(target_states):
                transition[source][target] = float(parts[j + 1])
        idx += 1
        
    # Gizli yolun ehtimalını hesablayırıq
    # Compute the probability of the hidden path
    # Başlanğıc ehtimalların bərabər olduğunu fərz edirik (1 / vəziyyətlərin sayı)
    # Assume that initial probabilities are equal (1 / number of states)
    prob = 1.0 / len(states)
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        prob *= transition[u][v]
        
    # Hesablanmış ehtimalı çıxış faylına yazırıq
    # Write the calculated probability to the output file
    with open(output_file, "w") as f:
        f.write(str(prob) + "\n")

# Proqramın əsas giriş nöqtəsini yoxlayırıq
# Check for the main entry point of the program
if __name__ == "__main__":
    main()
