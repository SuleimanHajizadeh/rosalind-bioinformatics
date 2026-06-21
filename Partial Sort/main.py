# Həlli üçün lazım olan modulu daxil edirik
# Import the required module for the solution
import heapq

def main():
    # Giriş faylının adını təyin edirik
    # Define the input file name
    input_file = "rosalind_ps.txt"
    # Çıxış faylının adını təyin edirik
    # Define the output file name
    output_file = "output.txt"
    
    # Giriş faylını oxumaq üçün açırıq
    # Open the input file for reading
    with open(input_file, "r") as f:
        # Birinci sətirdən massivin ölçüsünü oxuyuruq və tam ədədə çeviririk
        # Read the size of the array from the first line and convert to integer
        n = int(f.readline().strip())
        # İkinci sətirdən boşluqla ayrılmış elementləri oxuyub siyahı halına salırıq
        # Read space-separated elements from the second line into a list of integers
        A = list(map(int, f.readline().strip().split()))
        # Üçüncü sətirdən k dəyərini oxuyuruq və tam ədədə çeviririk
        # Read the value of k from the third line and convert to integer
        k = int(f.readline().strip())
        
    # Massivdəki ən kiçik k elementi tapıb onları artan ardıcıllıqla sıralayırıq
    # Find the k smallest elements in the array and sort them in ascending order
    # heapq.nsmallest funksiyası k sayda ən kiçik elementi sıralanmış şəkildə qaytarır
    # The heapq.nsmallest function returns the k smallest elements in sorted order
    result = heapq.nsmallest(k, A)
    
    # Nəticəni boşluqla ayrılmış şəkildə çıxış faylına yazırıq
    # Write the result to the output file as space-separated values
    with open(output_file, "w") as f:
        f.write(" ".join(map(str, result)))

# Proqramın əsas giriş nöqtəsini yoxlayırıq
# Check for the main entry point of the program
if __name__ == "__main__":
    main()
