# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba4h.txt")
    if not os.path.exists(input_file):
        return []
    with open(input_file, "r") as f:
        return list(map(int, f.read().split()))

# Spektr konvolusiyasını (convolution) hesablayırıq
# Generate the convolution of a spectrum
def spectral_convolution(spectrum):
    spectrum.sort()
    convolution = []
    n = len(spectrum)
    for i in range(n):
        for j in range(i):
            diff = spectrum[i] - spectrum[j]
            if diff > 0:
                convolution.append(diff)
    return convolution

def main():
    spectrum = read_input()
    if not spectrum:
        return
    conv = spectral_convolution(spectrum)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(map(str, conv)) + "\n")

if __name__ == "__main__":
    main()
