import os

# Simvollara əsaslanan filogenetik ağac qurulması alqoritmi
# Character-based phylogenetic tree construction algorithm


def pick_informative(characters):
    # İnformasiya verən (informative) simvolları seçirik
    # Pick informative characters based on matching values
    for i, ch in enumerate(characters):
        if sum(ch) == 2:
            return i, 1
        if sum(ch) == len(ch) - 2:
            return i, 0


def drop_uninformative(characters):
    # İnformasiya verməyən simvolları siyahıdan çıxarırıq
    # Remove uninformative characters from the list
    return [x for x in characters if 1 < sum(x) < len(x) - 1]


def flatten(x):
    # Nəticəni Newick formatına uyğun olaraq mötərizəli mətnə çeviririk
    # Flatten the tree structure to a Newick-formatted string
    if isinstance(x, (list, tuple)):
        return "(" + ",".join(flatten(e) for e in x) + ")"
    else:
        return str(x)


def chbp(names, characters):
    # Filogenetik ağacı qurmaq üçün simvolları birləşdiririk
    # Iteratively combine characters to build the phylogenetic tree
    while characters:
        i, v = pick_informative(characters)
        ind = [i for i, x in enumerate(characters[i]) if x == v]
        names[ind[0]] = tuple(names[i] for i in ind)
        del names[ind[1]]
        for ch in characters:
            del ch[ind[1]]
        characters = drop_uninformative(characters)
    return tuple(names)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, "rosalind_chbp.txt")
    output_path = os.path.join(base_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    # Giriş məlumatlarını oxuyuruq
    # Read input data from file
    with open(input_path, "r") as f:
        lines = f.read().splitlines()

    names = lines[0].split()
    characters = [[int(x) for x in list(ch)] for ch in lines[1:] if ch.strip()]

    # Ağacı hesablayıb Newick formatında yazdırırıq
    # Compute the tree and write it in Newick format
    res = chbp(names, characters)
    result = flatten(res) + ";"

    with open(output_path, "w") as f:
        f.write(result + "\n")

    print(result)


if __name__ == "__main__":
    main()
