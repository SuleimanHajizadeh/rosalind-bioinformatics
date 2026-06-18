# rosalind_mprt.py
import requests
import re

def get_fasta_sequence(uniprot_id):
    """UniProt ID-ə uyğun FASTA ardıcıllığını internetdən yükləyən funksiya"""
    # Əgər ID P01044_AMIL_HUMAN kimidirsə, yalnız 'P01044' hissəsini götürürük
    clean_id = uniprot_id.split('_')[0]
    url = f"https://www.uniprot.org/uniprot/{clean_id}.fasta"
    
    response = requests.get(url)
    if response.status_code == 200:
        lines = response.text.strip().split('\n')
        # İlk sətir (Header) atlanır, qalan sətirlər birləşdirilir
        sequence = "".join(lines[1:])
        return sequence
    else:
        print(f"Xəta: {uniprot_id} yüklənə bilmədi.")
        return None

def find_motif_positions(sequence):
    """N{P}[ST]{P} motivinin bütün 1-əsaslı mövqelərini tapan funksiya"""
    # (?=...) üst-üstə düşən (overlapping) motivləri qaçırmamaq üçün istifadə olunur
    pattern = re.compile(r'(?=(N[^P][ST][^P]))')
    positions = []
    
    for match in pattern.finditer(sequence):
        # match.start() 0-dan başladığı üçün üzərinə 1 gəlirik (Rosalind formatı)
        positions.append(match.start() + 1)
        
    return positions

# 1. Giriş faylını oxuyuruq
with open("rosalind_mprt.txt", "r") as file:
    uniprot_ids = file.read().splitlines()

# 2. Hər bir ID üçün prosesi icra edirik
for uniprot_id in uniprot_ids:
    if not uniprot_id.strip():
        continue
        
    sequence = get_fasta_sequence(uniprot_id)
    if sequence:
        positions = find_motif_positions(sequence)
        
        # Əgər zülalda motiv tapılarsa, ID-ni və mövqeləri yazdırırıq
        if positions:
            print(uniprot_id)
            print(" ".join(map(str, positions)))