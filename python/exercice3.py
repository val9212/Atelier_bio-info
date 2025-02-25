def parse_fasta(filename):
    """Parse un fichier FASTA et retourne un dictionnaire {header: sequence}."""
    sequences = {}
    with open(filename, 'r') as f:
        header = None
        seq_lines = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    sequences[header] = "".join(seq_lines)
                header = line[1:]
                seq_lines = []
            else:
                seq_lines.append(line)
        if header is not None:
            sequences[header] = "".join(seq_lines)
    return sequences

fasta_filename = "./reads.fasta"
all_sequences = parse_fasta(fasta_filename)

consensus = []
genes = []

for header, seq in all_sequences.items():
    if header.startswith("Consensus"):
        consensus.append((header, seq))
    if header.startswith("Gene"):
        genes.append((header, seq))

gene_1 = genes[-2][1]
gene_2 = genes[-1][1]

consensus_1 = consensus[0][1]

# =====================================
# CHARGEMENT ET REGROUPEMENT DES GÈNES ET DES LECTURES
# =====================================

def compare(seq1, seq2):
    """
    Compare deux séquences de même longueur et compte le nombre de différences (mismatches).

    Paramètres :
    ------------
    seq1 : str
        Première séquence à comparer.
    seq2 : str
        Seconde séquence à comparer.

    Retourne :
    ----------
    int
        Le nombre de positions où les deux séquences diffèrent.
"""







