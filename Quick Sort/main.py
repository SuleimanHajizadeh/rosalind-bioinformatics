# Həlli üçün lazım olan modulları daxil edirik
# Import the required modules for the solution
import random
import sys

# Rekursiya limitini artırırıq ki, dərin rekursiya zamanı xəta baş verməsin
# Increase the recursion limit to avoid stack overflow during deep recursion
sys.setrecursionlimit(200000)

def quick_sort(arr):
    # Əgər massivin uzunluğu 1 və ya daha azdırsa, o artıq sıralanmışdır
    # If the array has 1 or fewer elements, it is already sorted
    if len(arr) <= 1:
        return arr
        
    # Təsadüfi bir pivot elementi seçirik
    # Choose a random pivot element
    pivot = random.choice(arr)
    
    # Pivot-dan kiçik olan elementləri ayırırıq
    # Separate elements smaller than the pivot
    left = [x for x in arr if x < pivot]
    # Pivot-a bərabər olan elementləri ayırırıq
    # Separate elements equal to the pivot
    middle = [x for x in arr if x == pivot]
    # Pivot-dan böyük olan elementləri ayırırıq
    # Separate elements greater than the pivot
    right = [x for x in arr if x > pivot]
    
    # Sol və sağ hissələri rekursiv olaraq sıralayıb birləşdiririk
    # Recursively sort the left and right parts, then combine them
    return quick_sort(left) + middle + quick_sort(right)

def main():
    # Giriş faylının adını təyin edirik
    # Define the input file name
    input_file = "rosalind_qs.txt"
    # Çıxış faylının adını təyin edirik
    # Define the output file name
    output_file = "output.txt"
    
    # Giriş faylını oxumaq üçün açırıq
    # Open the input file for reading
    with open(input_file, "r") as f:
        # Birinci sətirdən massivin ölçüsünü oxuyuruq
        # Read the size of the array from the first line
        n = int(f.readline().strip())
        # İkinci sətirdən massivin elementlərini tam ədəd siyahısı kimi oxuyuruq
        # Read the elements of the array as a list of integers from the second line
        A = list(map(int, f.readline().strip().split()))
        
    # Quick Sort alqoritmi ilə massivi sıralayırıq
    # Sort the array using the Quick Sort algorithm
    sorted_A = quick_sort(A)
    
    # Sıralanmış massivi boşluqla ayrılmış şəkildə çıxış faylına yazırıq
    # Write the sorted array to the output file separated by spaces
    with open(output_file, "w") as f:
        f.write(" ".join(map(str, sorted_A)) + "\n")

# Proqramın əsas giriş nöqtəsini yoxlayırıq
# Check for the main entry point of the program
if __name__ == "__main__":
    main()
