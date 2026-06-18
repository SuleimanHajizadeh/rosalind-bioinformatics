import os
import glob

def read_input():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    txt_files = glob.glob(os.path.join(script_dir, "*.txt"))
    # Filter out output.txt
    txt_files = [f for f in txt_files if os.path.basename(f) != "output.txt"]
    if not txt_files:
        raise FileNotFoundError("Giriş faylı (*.txt) tapılmadı. Zəhmət olmasa Rosalind-dən yüklədiyiniz faylı bu qovluğa yerləşdirin.")
    input_path = txt_files[0]
    print(f"Giriş faylı oxunur: {os.path.basename(input_path)}")
    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

def main():
    try:
        lines = read_input()
    except FileNotFoundError as e:
        print(e)
        return
        
    n = int(lines[0])
    s = lines[1]
    A = list(map(float, lines[2].split()))
    
    L = len(s)
    gc_count = s.count('G') + s.count('C')
    at_count = s.count('A') + s.count('T')
    
    # Expected values
    expected_values = []
    for x in A:
        p = ((x / 2.0) ** gc_count) * (((1.0 - x) / 2.0) ** at_count)
        # Expected number of times s appears in t of length n
        ev = (n - L + 1) * p
        expected_values.append(f"{ev:.3f}")
        
    result_str = " ".join(expected_values)
    print(f"n = {n}, s = {s}")
    print(f"GC-kontentləri A = {A}")
    print(f"Gözlənilən saylar = {result_str}")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        out_file.write(result_str + "\n")

if __name__ == "__main__":
    main()
