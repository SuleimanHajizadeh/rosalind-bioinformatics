# 1. Faylı oxuyuruq
with open("rosalind_rna.txt", "r") as file:
    dna = file.read().strip()  # .strip() boşluqları və yeni sətir simvollarını təmizləyir

# 2. 'T' hərflərini 'U' ilə əvəz edirik
rna = dna.replace("T", "U")

# 3. Nəticəni ekrana yazdırırıq
print(rna)

# 4. İon variantı yeni fayla qeyd edirik (Rosalind-ə yükləmək üçün rahat olsun deyə)
with open("rosalind_rna_output.txt", "w") as output_file:
    output_file.write(rna)