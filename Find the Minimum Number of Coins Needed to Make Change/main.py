# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba5a.txt")
    if not os.path.exists(input_file):
        return 0, []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    money = int(lines[0])
    coins = list(map(int, lines[1].split(",")))
    return money, coins

# Minimum sayda qəpik tapırıq (Change problem)
# Find the minimum number of coins needed to make change
def min_coins_change(money, coins):
    dp = [float('inf')] * (money + 1)
    dp[0] = 0
    for i in range(1, money + 1):
        for coin in coins:
            if i - coin >= 0:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[money]

def main():
    money, coins = read_input()
    if money == 0:
        return
    result = min_coins_change(money, coins)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(result) + "\n")

if __name__ == "__main__":
    main()
