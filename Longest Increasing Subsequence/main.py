import bisect

def get_lis(seq):
    n = len(seq)
    tails = []
    tails_indices = []
    prev = [-1] * n
    for i, x in enumerate(seq):
        idx = bisect.bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
            tails_indices.append(i)
        else:
            tails[idx] = x
            tails_indices[idx] = i
        if idx > 0:
            prev[i] = tails_indices[idx - 1]
    
    # Ardıcıllığı bərpa edirik
    curr = tails_indices[-1]
    res = []
    while curr != -1:
        res.append(seq[curr])
        curr = prev[curr]
    return res[::-1]

# Faylı düzgün oxumaq üçün mütləq faylın tam yolunu istifadə et
file_path = "/Users/macbookairm2/Documents/GitHub/rosalind-bioinformatics/Longest Increasing Subsequence/rosalind_lgis.txt"

with open(file_path, "r") as f:
    lines = f.readlines()
    pi = []
    for line in lines[1:]:
        pi.extend(map(int, line.split()))

# LIS və LDS hesablayırıq
lis = get_lis(pi)
lds = get_lis([-x for x in pi]) # LDS üçün mənfi işarə ilə LIS
lds = [-x for x in lds]

# Nəticəni fayla yazaq (formatı yoxlamaq üçün)
with open("output.txt", "w") as out:
    out.write(" ".join(map(str, lis)) + "\n")
    out.write(" ".join(map(str, lds)) + "\n")

print("İşləndi! 'output.txt' faylına bax.")