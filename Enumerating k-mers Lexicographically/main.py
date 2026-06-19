import itertools

# Verilmiş əlifba üzrə n uzunluqlu k-merləri leksikoqrafik ardıcıllıqla qururuq
# Generate k-mers of length n lexicographically from the given alphabet

# Giriş faylından əlifbanı və k-mer uzunluğunu oxuyuruq
# Read alphabet symbols and length n from the file
with open("rosalind_lexf.txt", "r") as file:
    lines = file.readlines()
    alphabet = lines[0].split()
    n = int(lines[1].strip())

# Əlifba simvollarını sıralayırıq
# Ensure the alphabet is sorted
alphabet.sort()
kmers = itertools.product(alphabet, repeat=n)

# Nəticələri output.txt-yə yazırıq
# Write the results to output.txt
with open("output.txt", "w") as output_file:
    for kmer in kmers:
        output_file.write("".join(kmer) + "\n")

print("Lexicographical k-mers generated.")
