import random
import math
import argparse

def generate_random_gene(length):
    """Génère une séquence d'ADN aléatoire de la longueur spécifiée."""
    return "".join(random.choice("ACGT") for _ in range(length))

def introduce_errors(seq, error_rate, region=None):
    """
    Introduit aléatoirement des erreurs (substitutions) dans la séquence avec un taux donné.
    :param seq: La séquence d'entrée.
    :param error_rate: Probabilité de substitution par nt.
    :param region: Tuple (start, end) indiquant la région (indices relatifs) où introduire les erreurs.
                   Si None, toute la séquence est modifiée.
    :return: La séquence modifiée.
    """
    bases = "ACGT"
    seq_list = list(seq)
    if region is None:
        start, end = 0, len(seq)
    else:
        start, end = region
    for i in range(start, end):
        if random.random() < error_rate:
            original = seq_list[i]
            alternatives = [b for b in bases if b != original]
            seq_list[i] = random.choice(alternatives)
    return "".join(seq_list)


def generate_reads_systematic(gene, min_read_length, max_read_length, desired_coverage, error_rate=0.0,
                              error_region=None):
    """
    Génère des reads à partir d'un gène donné de manière systématique pour garantir une couverture,
    avec une taille de read variable dans l'intervalle [min_read_length, max_read_length].

    Retourne une liste de tuples (header, read, start_pos).
    """
    gene_length = len(gene)
    sys_reads = []
    pos = 0

    while pos < gene_length:
        read_length = random.randint(min_read_length, max_read_length)
        if pos + read_length > gene_length:
            break
        read = gene[pos:pos + read_length]
        if error_rate > 0.0:
            read = introduce_errors(read, error_rate, error_region)
        sys_reads.append((None, read, pos))
        pos += read_length // 2


    total_nt_reads = int(math.ceil(desired_coverage * gene_length))
    n_total = max(len(sys_reads), math.ceil(total_nt_reads / ((min_read_length + max_read_length) / 2)))

    extra_reads = []
    while len(sys_reads) + len(extra_reads) < n_total:
        read_length = random.randint(min_read_length, max_read_length)
        pos = random.randint(0, gene_length - read_length)
        read = gene[pos:pos + read_length]
        if error_rate > 0.0:
            read = introduce_errors(read, error_rate, error_region)
        extra_reads.append((None, read, pos))

    all_reads = sys_reads + extra_reads
    reads_with_header = []
    for i, (h, read, pos) in enumerate(all_reads):
        y = random.randint(100, 10000)
        reads_with_header.append((f"Read_{y}", read, pos))

    return reads_with_header

def write_fasta(filename, sequences):
    """Écrit les séquences dans un fichier FASTA.
    :param filename: Nom du fichier de sortie.
    :param sequences: Liste de tuples (header, sequence).
    """
    with open(filename, "w") as f:
        for header, seq in sequences:
            f.write(f">{header}\n")
            for i in range(0, len(seq), 80):
                f.write(seq[i:i+80] + "\n")

def verify_coverage(gene, reads, max_allowed_mismatches=1):
    """
    Vérifie que le gène est couvert par les reads en marquant les positions recouvertes.
    Retourne True si la couverture est complète, sinon False.
    """
    gene_length = len(gene)
    coverage = [False] * gene_length

    def hamming_distance(s1, s2):
        return sum(c1 != c2 for c1, c2 in zip(s1, s2))

    for header, read, _ in reads:
        rlen = len(read)
        best = None
        best_pos = None
        for i in range(gene_length - rlen + 1):
            window = gene[i:i+rlen]
            d = hamming_distance(window, read)
            if best is None or d < best:
                best = d
                best_pos = i
                if best == 0:
                    break
        if best is not None and best <= max_allowed_mismatches:
            for j in range(best_pos, best_pos + rlen):
                coverage[j] = True

    if all(coverage):
        return True
    else:
        missing = [i for i, cov in enumerate(coverage) if not cov]
        print(f"Positions non couvertes : {missing[:10]}{' ...' if len(missing)>10 else ''}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Génère un fichier FASTA simulé avec 2 niveaux de complexité."
    )
    parser.add_argument("--gene_length", type=int, default=300, help="Longueur des gènes (nt)")
    parser.add_argument("--min_read_length", type=int, help="Longueur des reads (nt)")
    parser.add_argument("--max_read_length", type=int, help="Longueur des reads (nt)")
    parser.add_argument("--coverage", type=float, help="Couverture désirée pour niveaux 1 et 2")
    parser.add_argument("--error_rate_level2", type=float, help="Taux d'erreur pour le niveau 2")
    parser.add_argument("--output", type=str, help="Nom du fichier FASTA de sortie")
    args = parser.parse_args()

    fasta_sequences = []

    # --- Niveau 1 : Reads parfaits (sans erreur) ---
    gene1 = generate_random_gene(args.gene_length)
    fasta_sequences.append(("Gene1_N1", gene1))
    reads_n1 = generate_reads_systematic(gene1, args.min_read_length, args.max_read_length, args.coverage, error_rate=0.0)
    for header, read, pos in reads_n1:
        fasta_sequences.append((f"{header}", read))
    print("Niveau 1 généré.")
    if verify_coverage(gene1, reads_n1, max_allowed_mismatches=0):
        print("Couverture complète pour Gene1_N1 (Niveau 1).")
    else:
        print("Couverture incomplète pour Gene1_N1 (Niveau 1).")

    # --- Niveau 2 : Reads avec erreur isolée dans une moitiée ---
    gene2 = generate_random_gene(args.gene_length)
    fasta_sequences.append(("Gene2_N2", gene2))
    error_region = (0, 15 // 2)
    reads_n2 = generate_reads_systematic(gene2, args.min_read_length, args.max_read_length, args.coverage, error_rate=args.error_rate_level2, error_region=error_region)
    for header, read, pos in reads_n2:
        fasta_sequences.append((f"{header}", read))
    print("Niveau 2 généré.")
    if verify_coverage(gene2, reads_n2, max_allowed_mismatches=1):
        print("Couverture complète pour Gene2_N2 (Niveau 2).")
    else:
        print("Couverture incomplète pour Gene2_N2 (Niveau 2).")

    write_fasta(args.output, fasta_sequences)
    print(f"Fichier FASTA généré : {args.output}")

if __name__ == "__main__":
    main()
