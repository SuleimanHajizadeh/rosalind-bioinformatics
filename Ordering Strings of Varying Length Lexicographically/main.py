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

def generate_lexv(alphabet, n):
    results = []
    
    def dfs(current_str):
        if len(current_str) > 0:
            results.append(current_str)
        if len(current_str) < n:
            for char in alphabet:
                dfs(current_str + char)
                
    dfs("")
    return results

def main():
    try:
        lines = read_input()
    except FileNotFoundError as e:
        print(e)
        return
        
    alphabet = lines[0].split()
    n = int(lines[1])
    
    print(f"Əlifba: {alphabet}, Maksimal uzunluq n = {n}")
    
    results = generate_lexv(alphabet, n)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "output.txt")
    
    with open(output_path, "w") as out_file:
        for item in results:
            out_file.write(item + "\n")
            
    print(f"Uğurla tamamlandı! Ümumi sətir sayı: {len(results)}")
    print("İlk 10 nəticə:")
    for item in results[:10]:
        print(item)

if __name__ == "__main__":
    main()
