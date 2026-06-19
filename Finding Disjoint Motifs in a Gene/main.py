import os

# Giriş sətirlərini fayldan oxuyuruq
# Read template string s and patterns from input file


def read_input(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    if not lines:
        raise ValueError("Giriş faylı boşdur.")
    s = lines[0]
    patterns = lines[1:]
    return s, patterns


def can_interweave(s, t, u):
    # Dinamik proqramlaşdırma ilə t və u motiflərinin s-də kəsişmədən paylaşılan ardıcıllıq olub-olmadığını yoxlayırıq
    # DP to verify if prefixes of t and u can interweave to form a substring of s
    len_s = len(s)
    len_t = len(t)
    len_u = len(u)

    # dp_prev[i][j] əvvəlki addım üçün uyğunluğu saxlayır
    # dp_prev[i][j] stores match status of prefixes t[:i] and u[:j]
    dp_prev = [[False] * (len_u + 1) for _ in range(len_t + 1)]
    dp_prev[0][0] = True

    for p in range(1, len_s + 1):
        dp_curr = [[False] * (len_u + 1) for _ in range(len_t + 1)]
        dp_curr[0][0] = True

        char = s[p - 1]
        for i in range(len_t + 1):
            for j in range(len_u + 1):
                if i == 0 and j == 0:
                    continue
                match_t = False
                if i > 0 and char == t[i - 1]:
                    match_t = dp_prev[i - 1][j]
                match_u = False
                if j > 0 and char == u[j - 1]:
                    match_u = dp_prev[i][j - 1]
                dp_curr[i][j] = match_t or match_u

        if dp_curr[len_t][len_u]:
            return True
        dp_prev = dp_curr

    return False


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_itwv.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    s, patterns = read_input(input_path)
    n = len(patterns)
    M = [[0] * n for _ in range(n)]

    # Simmetriyanı nəzərə alaraq matrisi doldururuq
    # Fill the interweaving matrix, leveraging symmetry M[i][j] == M[j][i]
    for i in range(n):
        for j in range(i, n):
            res = 1 if can_interweave(s, patterns[i], patterns[j]) else 0
            M[i][j] = res
            M[j][i] = res

    with open(output_path, "w") as out_file:
        for row in M:
            out_file.write(" ".join(map(str, row)) + "\n")

    print(f"Computed matrix of size {n}x{n}.")


if __name__ == "__main__":
    main()
