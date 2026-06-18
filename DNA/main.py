dnk = input().strip()

def dnk_sum(dnk):
    c = 0
    b = 0
    d = 0
    y = 0

    for key in dnk:
        match key:
            case "A":
                c += 1
            case "C":
                b += 1
            case "G":
                d += 1
            case "T":
                y += 1
            case _:
                pass

    print(c)
    print(b)
    print(d)
    print(y)

dnk_sum(dnk)