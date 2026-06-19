import os
import glob

# Cari qovluqdakı "rosalind_" ilə başlayan giriş faylını tapırıq.
# Locate the input file starting with "rosalind_" in the current directory.
input_files = glob.glob(os.path.join(os.path.dirname(__file__), 'rosalind_*.txt'))
if not input_files:
    raise FileNotFoundError("Giriş faylı tapılmadı / Input file not found")

# Giriş faylından məlumatları oxuyuruq.
# Read data from the input file.
with open(input_files[0], 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

# k və n parametrlərini təyin edirik.
# Parse parameters k and n.
k, n = map(int, lines[0].split())

# 3SUM problemini həll edən optimallaşdırılmış funksiya.
# Optimized function to solve the 3SUM problem.
def solve_3sum(arr):
    size = len(arr)
    # Massivi elementlərin orijinal indeksləri ilə sıralayırıq.
    # Sort the array elements along with their original 1-based indices.
    sorted_arr = sorted((val, idx + 1) for idx, val in enumerate(arr))
    
    # Müqayisələrin sürətli olması üçün elementlərin dəyərlərini və indekslərini ayrıca massivlərə yığırıq.
    # Collect values and indices into flat lists to make inner-loop operations faster.
    vals = [item[0] for item in sorted_arr]
    idxs = [item[1] for item in sorted_arr]
    
    last_val = vals[-1]
    second_last_val = vals[-2]
    
    for i in range(size - 2):
        pivot = vals[i]
        
        # Əgər pivot-un ən kiçik mümkün cəmi sıfırdan böyükdürsə, axtarışı dayandırırıq.
        # If the minimum possible sum with the pivot is positive, we break early.
        if pivot + vals[i+1] + vals[i+2] > 0:
            break
            
        # Əgər pivot-un ən böyük mümkün cəmi sıfırdan kiçikdirsə, bu pivot-u ötürürük.
        # If the maximum possible sum with the pivot is negative, we skip this pivot.
        if pivot + last_val + second_last_val < 0:
            continue
            
        left = i + 1
        right = size - 1
        
        # İki göstərici (two-pointer) yanaşması.
        # Two-pointer search approach.
        while left < right:
            current_sum = pivot + vals[left] + vals[right]
            if current_sum == 0:
                # Tapılan orijinal indeksləri artan sıra ilə qaytarırıq.
                # Return the sorted original indices.
                return sorted([idxs[i], idxs[left], idxs[right]])
            elif current_sum < 0:
                left += 1
            else:
                right -= 1
    return -1

# Hər bir massiv üçün 3SUM problemini həll edib nəticələri toplayırıq.
# Solve 3SUM for each array and collect results.
results = []
for i in range(1, k + 1):
    A = list(map(int, lines[i].split()))
    ans = solve_3sum(A)
    if ans == -1:
        results.append("-1")
    else:
        results.append(' '.join(map(str, ans)))

# Nəticələri sətirlər şəklində birləşdiririk.
# Join the results with newlines.
output_data = '\n'.join(results)

# Nəticələri konsolda göstəririk.
# Print the results to the console.
print(output_data[:200] + "\n...")

# Nəticəni "output.txt" faylına yazırıq.
# Write the results to the "output.txt" file.
output_path = os.path.join(os.path.dirname(__file__), 'output.txt')
with open(output_path, 'w') as f:
    f.write(output_data + '\n')
