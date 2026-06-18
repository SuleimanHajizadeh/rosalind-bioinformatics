# rosalind_fibd.py

# 1. Fayldan n və m qiymətlərini oxuyuruq
with open("rosalind_fibd.txt", "r") as file:
    n, m = map(int, file.read().split())

def mortal_rabits(n, m):
    # m ölçülü siyahı yaradırıq. İndeks 'i' dovşanın cari yaşını (ayını) göstərir.
    # 1-ci ayda: yalnız 1 cütlük yeni doğulmuş (0 yaşlı) dovşan var.
    ages = [0] * m
    ages[0] = 1
    
    # 2-ci aydan n-ci aya qədər hesablama aparılır
    for month in range(2, n + 1):
        # Yaşı >= 1 olan bütün yetkin dovşanlar yeni nəsil (bala) dünyaya gətirir
        newborns = sum(ages[1:])
        
        # Dovşanları 1 ay qocaldırıq (yaşları sürüşdürürük)
        next_ages = [0] * m
        next_ages[0] = newborns # yeni doğulanlar 0-cı indeksə keçir
        
        for i in range(1, m):
            next_ages[i] = ages[i - 1]
            
        # m-ci aya çatan (ages[m-1]) dovşanlar next_ages-ə keçmədiyi üçün avtomatik ölürlər
        ages = next_ages
        
    # n-ci ayın sonunda bütün yaş qruplarındakı dovşanları toplayırıq
    return sum(ages)

# 2. Funksiyanı çağırırıq və nəticəni çap edirik
result = mortal_rabits(n, m)
print(result)

# 3. Cavabı yeni çıxış faylına yazırıq
with open("rosalind_fibd_output.txt", "w") as output_file:
    output_file.write(str(result))