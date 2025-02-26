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

fasta_filename = "../reads.fasta"
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

def align(gene_seq, read_seq):
    for i in range((len(gene_seq)-len(read_seq))+1):
        if gene_seq[i:i+len(read_seq)] == read_seq:
            return i
        else:continue
    return -1

final = []
for gene, seq_gen in genes:
    gene_l = []
    for read, seq_read in reads:
        aligned = -1
        aligned = align(seq_gen, seq_read)
        if aligned != -1:
            gene_l.append((aligned, aligned+len(seq_read)))
            print(f"gène: {gene}, read: {read}, pos: ({aligned}, {aligned + len(seq_read)})")
    final.append(gene_l)

print(final)




