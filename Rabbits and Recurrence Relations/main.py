# 1. Fayldan n və k qiymətlərini oxuyuruq
with open("rosalind_fib.txt", "r") as file:
    n, k = map(int, file.read().split())

# 2. Dinamik proqramlaşdırma metodu ilə dovşanların sayını hesablayan funksiya
def rabbit_pairs(n, k):
    if n == 1 or n == 2:
        return 1
    
    # n+1 ölçülü siyahı yaradırıq (indexlər 1-dən başlasın deyə)
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 1
    
    # 3-cü aydan başlayaraq düsturu tətbiq edirik: F_n = F_{n-1} + k * F_{n-2}
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + k * dp[i-2]
        
    return dp[n]

# 3. Nəticəni tapırıq və yazdırırıq
result = rabbit_pairs(n, k)
print(result)

# 4. Cavabı yeni fayla qeyd edirik
with open("rosalind_fib_output.txt", "w") as output_file:
    output_file.write(str(result))