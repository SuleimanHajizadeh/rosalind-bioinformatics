import os

# Ən uzun artan (LIS) və azalan (LDS) alt-ardıcıllıqları tapırıq
# Compute the Longest Increasing Subsequence (LIS) and Longest Decreasing Subsequence (LDS)


def get_lis(arr):
    # LIS tapmaq üçün dinamik proqramlaşdırma və ikilik axtarış (binary search)
    # LIS algorithm using DP and binary search
    n = len(arr)
    tails = []
    parent = [-1] * n
    tails_indices = []

    for i, x in enumerate(arr):
        # tails massivində x-in yerləşə biləcəyi mövqeyi tapırıq
        # Binary search for position of x in tails
        low, high = 0, len(tails) - 1
        pos = len(tails)
        while low <= high:
            mid = (low + high) // 2
            if tails[mid] >= x:
                pos = mid
                high = mid - 1
            else:
                low = mid + 1

        if pos == len(tails):
            tails.append(x)
            tails_indices.append(i)
        else:
            tails[pos] = x
            tails_indices[pos] = i

        if pos > 0:
            parent[i] = tails_indices[pos - 1]

    # Geri izləmə ilə ardıcıllığı qururuq
    # Reconstruct LIS sequence via backtracking
    curr = tails_indices[-1]
    subseq = []
    while curr != -1:
        subseq.append(arr[curr])
        curr = parent[curr]
    subseq.reverse()
    return subseq


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_lgis.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        lines = f.read().splitlines()

    n = int(lines[0].strip())
    arr = list(map(int, lines[1].split()))

    # LIS hesablayırıq
    # Compute LIS
    lis = get_lis(arr)

    # LDS tapmaq üçün elementləri mənfiləşdirib LIS tətbiq edirik
    # Compute LDS by negating elements and running LIS algorithm
    neg_arr = [-x for x in arr]
    lds_neg = get_lis(neg_arr)
    lds = [-x for x in lds_neg]

    lis_str = " ".join(map(str, lis))
    lds_str = " ".join(map(str, lds))

    print(lis_str)
    print(lds_str)

    with open(output_path, "w") as f:
        f.write(lis_str + "\n")
        f.write(lds_str + "\n")


if __name__ == "__main__":
    main()
