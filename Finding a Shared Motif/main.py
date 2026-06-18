# rosalind_lcsm.py

def read_fasta(filename):
    """FASTA formatlı faylı oxuyub sətirlər siyahısı qaytaran funksiya"""
    sequences = []
    current_seq = ""
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                if current_seq:
                    sequences.append(current_seq)
                    current_seq = ""
            else:
                current_seq += line
        if current_seq:
            sequences.append(current_seq)
    return sequences

def longest_common_substring(filename):
    sequences = read_fasta(filename)
    if not sequences:
        return ""
        
    # Ən qısa sətiri tapırıq, çünki ortaq alt-ardıcıllıq ondan uzun ola bilməz
    sequences.sort(key=len)
    shortest = sequences[0]
    other_seqs = sequences[1:]
    
    # Alt-ardıcıllığın uzunluğu üzərində İkili Axtarış (Binary Search)
    low = 1
    high = len(shortest)
    best_lcs = ""
    
    while low <= high:
        mid = (low + high) // 2
        found = False
        
        # 'mid' uzunluğundakı bütün alt-ardıcıllıqları yoxlayırıq
        for i in range(len(shortest) - mid + 1):
            sub = shortest[i:i+mid]
            
            # Əgər bu alt-ardıcıllıq digər bütün sətirlərdə varsa
            if all(sub in s for s in other_seqs):
                best_lcs = sub
                found = True
                break # Bu uzunluqda tapıldı, daha uzununu axtarmağa keçirik
                
        if found:
            low = mid + 1 # Sağ tərəfi axtar (daha uzun)
        else:
            high = mid - 1 # Sol tərəfi axtar (daha qısa)
            
    return best_lcs

# Funksiyanı icra edirik
result = longest_common_substring("rosalind_lcsm.txt")
print(result)

# Cavabı yeni fayla qeyd edirik
with open("rosalind_lcsm_output.txt", "w") as output_file:
    output_file.write(result)