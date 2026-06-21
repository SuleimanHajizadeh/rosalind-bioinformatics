# Həlli üçün lazım olan modulu daxil edirik
# Import the required module for the solution
import os

def main():
    # Cari skriptin qovluğunu tapırıq və giriş/çıxış fayllarının yollarını müəyyən edirik
    # Get the directory of the current script and define paths for input/output files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba10b.txt")
    output_file = os.path.join(script_dir, "output.txt")
    
    # Giriş faylını oxumaq üçün açırıq
    # Open the input file for reading
    with open(input_file, "r") as f:
        # Birinci sətirdən emisiya olunmuş sətri (x) oxuyuruq
        # Read the emitted string (x) from the first line
        x = f.readline().strip()
        
        # Sonrakı sətirləri oxuyuruq və təmizləyirik
        # Read the subsequent lines and strip them
        lines = [line.strip() for line in f if line.strip()]
        
    # Seperatorları və digər məlumatları tapmaq üçün indeks təyin edirik
    # Define an index to locate separators and other data
    idx = 0
    while idx < len(lines) and lines[idx] == "--------":
        idx += 1
        
    # Əlifbanı oxuyuruq
    # Read the alphabet
    alphabet = lines[idx].split()
    idx += 1
    
    # Ayırıcını keçirik
    # Skip the separator
    while idx < len(lines) and lines[idx] == "--------":
        idx += 1
        
    # Gizli yolu (pi) oxuyuruq
    # Read the hidden path (pi)
    path = lines[idx]
    idx += 1
    
    # Ayırıcını keçirik
    # Skip the separator
    while idx < len(lines) and lines[idx] == "--------":
        idx += 1
        
    # Vəziyyətləri oxuyuruq
    # Read the states
    states = lines[idx].split()
    idx += 1
    
    # Ayırıcını keçirik
    # Skip the separator
    while idx < len(lines) and lines[idx] == "--------":
        idx += 1
        
    # Matris başlığını (emisiya simvollarını) oxuyuruq
    # Read the matrix header (emission characters)
    emitted_chars = lines[idx].split()
    idx += 1
    
    # Emisiya ehtimalları matrisini qururuq
    # Construct the emission probability matrix
    emission = {s: {} for s in states}
    while idx < len(lines):
        parts = lines[idx].split()
        if len(parts) >= 1 + len(emitted_chars):
            source = parts[0]
            for j, char in enumerate(emitted_chars):
                emission[source][char] = float(parts[j + 1])
        idx += 1
        
    # Gizli yola görə sətrin emisiya olunma ehtimalını hesablayırıq
    # Compute the probability of the outcome given the hidden path
    prob = 1.0
    for i in range(len(x)):
        state = path[i]
        char = x[i]
        prob *= emission[state][char]
        
    # Hesablanmış ehtimalı çıxış faylına yazırıq
    # Write the calculated probability to the output file
    with open(output_file, "w") as f:
        f.write(str(prob) + "\n")

# Proqramın əsas giriş nöqtəsini yoxlayırıq
# Check for the main entry point of the program
if __name__ == "__main__":
    main()
