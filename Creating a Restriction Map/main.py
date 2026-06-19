import os
from collections import Counter

# Multiset fərqlərindən istifadə edərək restriksiya xəritəsi (restriction map) bərpa edirik
# Reconstruct restriction map coordinates from the multiset of pairwise distances


def solve(L_list):
    counter = Counter(L_list)
    unique_sorted = sorted(counter.keys())

    # Maksimal məsafə xəritənin son nöqtəsidir (L)
    # The max distance in the multiset represents the total length L
    L = max(L_list)
    X = {0, L}

    # Bütün yarımçıq məsafələri yoxlayaraq nöqtələri bərpa edirik
    # Iteratively select coordinates that generate matching pairwise distances in multiset
    remaining_dists = counter.copy()
    remaining_dists[L] -= 1

    possible_coords = set()
    for d in unique_sorted:
        if d != 0 and d != L:
            possible_coords.add(d)
            possible_coords.add(L - d)

    sorted_poss = sorted(list(possible_coords))

    # Nöqtələrin koordinatlarını X çoxluğuna yığırıq
    # Assemble final coordinates set
    for coord in sorted_poss:
        # Hər bir namizəd koordinat üçün cari X-dəki nöqtələrlə məsafələri yoxlayırıq
        # Check pairwise distances between candidate coordinate and current X points
        valid = True
        temp_dists = Counter()
        for x in X:
            dist = abs(coord - x)
            temp_dists[dist] += 1

        for dist, count in temp_dists.items():
            if remaining_dists[dist] < count:
                valid = False
                break

        if valid:
            X.add(coord)
            for dist, count in temp_dists.items():
                remaining_dists[dist] -= 1

    return sorted(list(X))


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_pd.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        content = f.read().strip()

    L_list = list(map(int, content.split()))
    coords = solve(L_list)

    result_str = " ".join(map(str, coords))
    print(result_str)

    with open(output_path, "w") as f:
        f.write(result_str + "\n")


if __name__ == "__main__":
    main()
