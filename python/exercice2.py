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

fasta_filename = "reads.fasta"
all_sequences = parse_fasta(fasta_filename)

genes = []
reads = []

for header, seq in all_sequences.items():
    if header.startswith("Gene"):
        genes.append((header, seq))
    elif header.startswith("Read"):
        reads.append((header, seq))

# =====================================
# CHARGEMENT ET REGROUPEMENT DES GÈNES ET DES LECTURES
# =====================================

# print(genes)/print(reads) -> [(header, seq), (header,seq)...]

def align(gene_seq, read_seq):
    """
    Recherche l'alignement exact d'une séquence de lecture (read_seq) dans une séquence de référence (gene_seq).

    Paramètres :
    ------------
    gene_seq : str
        Séquence de référence (gène) dans laquelle on cherche l'alignement.
    read_seq : str
        read à rechercher dans la séquence de référence.

    Retourne :
    ----------
    int
        L'indice de départ de la première occurrence de `read_seq` dans `gene_seq`, ou -1 si aucun alignement n'est trouvé.
    """

def align_half(gene_seq, read_seq):
    """
    Recherche si la première ou la seconde moitié d'une séquence de lecture (read_seq)
    s'aligne dans une séquence de référence (gene_seq).

    Paramètres :
    ------------
    gene_seq : str
        Séquence de référence (gène) dans laquelle on cherche l'alignement.
    read_seq : str
        Séquence à diviser en deux et à rechercher dans la séquence de référence.

    Retourne :
    ----------
    tuple (bool, int)
        - Un booléen indiquant si c'est la première moitié (True) ou la seconde moitié (False) qui est alignée.
        - L'indice de départ de l'alignement dans `gene_seq`, ou -1 si aucun alignement n'est trouvé.
    """




