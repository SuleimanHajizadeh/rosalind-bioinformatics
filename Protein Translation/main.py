import os
import glob
import warnings
from Bio.Seq import translate
from Bio.Seq import BiopythonWarning

# Biopython xəbərdarlıqlarını gizlədirik (bir kodon həm STOP həm aminturşu üçün ola bilər)
# Suppress Biopython warnings about codons coding for both STOP and amino acids
warnings.simplefilter('ignore', BiopythonWarning)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Dataset faylını tapırıq
    # Find the dataset file
    dataset_files = glob.glob(os.path.join(script_dir, 'rosalind_*.txt'))
    if not dataset_files:
        print("Xəta: fayl tapılmadı.")
        return

    with open(dataset_files[0], 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Birinci sətir DNT ardıcıllığı, ikinci sətir gözlənilən zülaldır
    # First line: DNA sequence, second line: expected protein
    dna = lines[0]
    expected_protein = lines[1]

    # NCBI-nin 1-dən 33-ə qədər bütün kodon cədvəllərini yoxlayırıq
    # Test all NCBI codon tables from 1 to 33
    matched_table = None
    for table_id in range(1, 34):
        try:
            # DNT-ni hər cədvəl ilə zülala çeviririk
            # Translate DNA using this table (to_stop=False to see all codons)
            translated = str(translate(dna, table=table_id, to_stop=False))

            # 1-ci üsul: bütün stop kodonlarını silib müqayisə edirik
            # Strategy 1: remove all stop codons and compare
            if translated.replace("*", "") == expected_protein:
                matched_table = table_id
                break

            # 2-ci üsul: yalnız sondakı stop kodonunu silib müqayisə edirik
            # Strategy 2: remove only trailing stop codons
            if translated.rstrip("*") == expected_protein:
                matched_table = table_id
                break

            # 3-cü üsul: ilk N simvolu müqayisə edirik (N = zülalın uzunluğu)
            # Strategy 3: compare only the first N characters
            if translated[:len(expected_protein)] == expected_protein:
                matched_table = table_id
                break

        except Exception:
            pass

    if matched_table is None:
        print("Xəta: uyğun kodon cədvəli tapılmadı.")
        return

    # Nəticəni output.txt-ə yazırıq
    # Write the matched table ID to output.txt
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out:
        out.write(f"{matched_table}\n")


if __name__ == '__main__':
    main()
