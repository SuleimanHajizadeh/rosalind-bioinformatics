# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba4d.txt")
    if not os.path.exists(input_file):
        return 0
    with open(input_file, "r") as f:
        return int(f.read().strip())

# Amin turşularının unikal kütlələri
# Unique amino acid masses
MASSES = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]

# Verilən kütləyə malik peptidlərin sayını dinamik proqramlaşdırma ilə tapırıq
# Compute the number of peptides of given total mass
def count_peptides_of_mass(total_mass):
    dp = [0] * (total_mass + 1)
    dp[0] = 1
    for i in range(1, total_mass + 1):
        for m in MASSES:
            if i - m >= 0:
                dp[i] += dp[i-m]
    return dp[total_mass]

def main():
    total_mass = read_input()
    if total_mass == 0:
        return
    result = count_peptides_of_mass(total_mass)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(result) + "\n")

if __name__ == "__main__":
    main()
