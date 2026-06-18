# Take input of kmer length, motif, and genome/sequence to determine if the motif is found in it with equal or less than mismatches of the kmer
# example ouptut from rosalind gives 3 outputs, since the motif can be found in the genome 3 times while <= kmer
# sample output doesn't include motif mathes less than a legnth of 4, motif length -k, I made the assumption that I don't want matches lower than the max k value since the sample output did as well



def edit_distance(s1, s2):
    #Calculate the edit distance (Levenshtein distance) between the motif and genome since they are different lengths.
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n]

def find_substrings_within_edit_distance(k, motif, genome):
    #Find all substrings of the genome where the edit distance to the motif is <= k
    results = []
    motif_length = len(motif)
    genome_length = len(genome)

    for start in range(genome_length):
        # Restrict substring lengths to be within [motif_length - k, motif_length + k]
        for end in range(start + max(1, motif_length - k), min(start + motif_length + 1, genome_length + 1)):
            substring = genome[start:end]
            distance = edit_distance(motif, substring)
            if distance <= k:
                # Adding one to the count since Python indexes starting at 0
                results.append((start + 1, len(substring)))  

    return results

def main():
      # User input and double check that it is valid
    while True:
        try:
            k = int(input("Enter the k value (whole integer): "))
            if k < 0 or k > 50:
                raise ValueError("k must be a non-negative integer.")
            break
        except ValueError:
            print("Invalid input. Please enter a whole number for k.")
    
    while True:
        motif = input("Enter the motif (genomic sequence, max 5 kbp): ").strip().upper()
        if len(motif) > 5000:
            print("Motif sequence is too long. Please enter a sequence with at most 5 kbp.")
        else:
            break
    
    while True:
        genome = input("Enter the genome (genomic sequence, max 50 kbp): ").strip().upper()
        if len(genome) > 50000:
            print("Genome sequence is too long. Please enter a sequence with at most 50 kbp.")
        else:
            break

    # Call function to solve
    substrings = find_substrings_within_edit_distance(k, motif, genome)

    # Output
    for start, length in substrings:
        print(start, length)

if __name__ == "__main__":
    main()