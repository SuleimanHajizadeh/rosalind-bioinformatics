# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9i.txt")
    if not os.path.exists(input_file):
        return ""
    with open(input_file, "r") as f:
        return f.read().strip()

# Burrows-Wheeler Transformasiyasını (BWT) hesablayırıq
# Construct the Burrows-Wheeler Transform of a String
def burrows_wheeler_transform(text):
    # Sətrin bütün dövri sürüşmələrini (matrix rotations) tapıb əlifba sırası ilə düzürük
    # Form and sort all cyclic rotations
    n = len(text)
    rotations = [text[i:] + text[:i] for i in range(n)]
    rotations.sort()
    
    # Hər birinin sonuncu sütununu birləşdirib BWT alırıq
    # Take the last character of each rotation
    return "".join(rot[n-1] for rot in rotations)

def main():
    text = read_input()
    if not text:
        return
    result = burrows_wheeler_transform(text)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    main()
