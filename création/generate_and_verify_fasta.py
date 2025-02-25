import random, math, argparse

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

def assemble_consensus(gene_length, reads):
    """
    Assemble un consensus à partir d'une liste de reads (avec leur position de départ).
    Pour chaque position du gène, on regroupe toutes les bases couvertes par des reads et on prend
    la base majoritaire. Si aucune lecture ne couvre la position, on met 'N'.
    """
    consensus = []
    for i in range(gene_length):
        bases = []
        for header, read, start in reads:
            if start <= i < start + len(read):
                bases.append(read[i - start])
        if bases:
            base = max(set(bases), key=bases.count)
        else:
            base = 'N'
        consensus.append(base)
    return "".join(consensus)

def count_errors(true_seq, consensus_seq):
    """Compte le nombre de positions où les deux séquences diffèrent."""
    return sum(1 for a, b in zip(true_seq, consensus_seq) if a != b)

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
        description="Génère un fichier FASTA simulé avec 3 niveaux de complexité. "
                    "Pour le niveau 3, on simule une couverture partielle (pas suffisante pour couvrir le gène uniquement avec des moitiés de reads), "
                    "on assemble les reads disponibles pour obtenir un consensus et on compare le nombre d'erreurs entre deux gènes."
    )
    parser.add_argument("--gene_length", type=int, default=300, help="Longueur des gènes (nt)")
    parser.add_argument("--min_read_length", type=int, help="Longueur des reads (nt)")
    parser.add_argument("--max_read_length", type=int, help="Longueur des reads (nt)")
    parser.add_argument("--coverage", type=float, default=5.0, help="Couverture désirée pour niveaux 1 et 2")
    parser.add_argument("--coverage_level3", type=float, default=1.5, help="Couverture désirée pour le niveau 3 (insuffisante pour couvrir entièrement le gène)")
    parser.add_argument("--error_rate_level2", type=float, default=0.02, help="Taux d'erreur pour le niveau 2 (appliqué dans la première moitié)")
    parser.add_argument("--error_rate_level3", type=float, default=0.04, help="Taux d'erreur pour le niveau 3")
    parser.add_argument("--output", type=str, default="simulated.fasta", help="Nom du fichier FASTA de sortie")
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
    
    # --- Niveau 3 : Couverture partielle + Assemblage et comparaison ---
    gene3 = generate_random_gene(args.gene_length)
    gene4 = generate_random_gene(args.gene_length)
    fasta_sequences.append(("Gene3_N3", gene3))
    fasta_sequences.append(("Gene4_N3", gene4))
    reads_n3_gene3 = generate_reads_systematic(gene3, args.min_read_length, args.max_read_length, args.coverage_level3, error_rate=args.error_rate_level3)
    reads_n3_gene4 = generate_reads_systematic(gene4, args.min_read_length, args.max_read_length, args.coverage_level3, error_rate=args.error_rate_level3)
    for header, read, pos in reads_n3_gene3:
        fasta_sequences.append((f"{header}_N3", read))
    for header, read, pos in reads_n3_gene4:
        fasta_sequences.append((f"{header}_N3", read))
    print("Niveau 3 généré (reads partiels pour Gene3_N3 et Gene4_N3).")
    
    consensus_gene3 = assemble_consensus(args.gene_length, reads_n3_gene3)
    consensus_gene4 = assemble_consensus(args.gene_length, reads_n3_gene4)
    fasta_sequences.append(("Consensus_Gene3_N3", consensus_gene3))
    fasta_sequences.append(("Consensus_Gene4_N3", consensus_gene4))
    
    errors_gene3 = count_errors(gene3, consensus_gene3)
    errors_gene4 = count_errors(gene4, consensus_gene4)
    print(f"Erreurs dans l'assemblage de Gene3_N3 : {errors_gene3} / {args.gene_length}")
    print(f"Erreurs dans l'assemblage de Gene4_N3 : {errors_gene4} / {args.gene_length}")
    
    if errors_gene3 < errors_gene4:
        print("Gene3_N3 est le moins erroné.")
    elif errors_gene4 < errors_gene3:
        print("Gene4_N3 est le moins erroné.")
    else:
        print("Les deux gènes ont le même nombre d'erreurs.")

    write_fasta(args.output, fasta_sequences)
    print(f"Fichier FASTA généré : {args.output}")

if __name__ == "__main__":
    main()
