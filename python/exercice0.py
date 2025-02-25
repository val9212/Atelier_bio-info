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

fasta_filename = "./niv0.fasta"
all_sequences = parse_fasta(fasta_filename)

genes = []
for header, seq in all_sequences.items():
    if header.startswith("Gene"):
        genes.append((header, seq))

# =====================================
# CHARGEMENT ET REGROUPEMENT DES GÈNES ET DES LECTURES
# =====================================

# print(genes) -> [(header, seq), (header,seq)...]

gene_niv3 = ""

