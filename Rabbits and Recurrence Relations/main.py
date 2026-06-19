# 1. Fayldan n və k qiymətlərini oxuyuruq
# Read n (months) and k (offspring pairs count) from the input dataset
with open("rosalind_fib.txt", "r") as file:
    n, k = map(int, file.read().split())

# 2. Dinamik proqramlaşdırma metodu ilə dovşanların sayını hesablayan funksiya
# Calculate total rabbit pairs using dynamic programming
def rabbit_pairs(n, k):
    if n == 1 or n == 2:
        return 1
    
    # n+1 ölçülü siyahı yaradırıq
    # Initialize DP array of size n+1
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 1
    
    # 3-cü aydan başlayaraq recurrence formulasını tətbiq edirik: F_n = F_{n-1} + k * F_{n-2}
    # Compute population for each month iteratively
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + k * dp[i-2]
        
    return dp[n]

result = rabbit_pairs(n, k)
print(result)

# 3. Cavabı output.txt faylına yazırıq
# Write result to output.txt
with open("output.txt", "w") as output_file:
    output_file.write(str(result) + "\n")
