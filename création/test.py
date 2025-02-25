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

fasta_filename = "niv1"
all_sequences = parse_fasta(fasta_filename)

genes = []
reads = []

for header, seq in all_sequences.items():
    if header.startswith("Gene"):
        genes.append((header, seq))
    elif header.startswith("Read"):
        reads.append((header, seq))

def split_read(sequence):
    """Coupe une séquence en deux parties à peu près égales."""
    midpoint = len(sequence) // 2
    return sequence[:midpoint], sequence[midpoint:]

def save_split_genes_to_latex(split_genes, output_filename):
    """
    Enregistre les ségments d'ADN dans un fichier LaTeX avec coloration des bases.

    Args:
        split_genes: Liste de tuples (header_part, sequence)
        output_filename: Nom du fichier de sortie .tex
    """
    latex_content = """\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage{xcolor}
\\usepackage{tikz}
\\usepackage[margin=1cm,landscape]{geometry} 

% Définition des couleurs pour chaque base
\\definecolor{Acolor}{rgb}{1,0.8,0.8} % rouge clair
\\definecolor{Tcolor}{rgb}{0.8,1,0.8}  % vert clair
\\definecolor{Ccolor}{rgb}{0.8,0.8,1} % bleu clair
\\definecolor{Gcolor}{rgb}{1,1,0.8}    % jaune clair

% Commande pour la taille de police
\\newcommand{\\dnafont}{\\fontsize{100pt}{70pt}\\selectfont}

% Commande de coloration
\\newcommand{\\highlightDNA}[1]{%
    \\foreach \\base in {#1} {%
        \\ifnum\\pdfstrcmp{\\base}{A}=0 \\colorbox{Acolor}{A}%
        \\else\\ifnum\\pdfstrcmp{\\base}{T}=0 \\colorbox{Tcolor}{T}%
        \\else\\ifnum\\pdfstrcmp{\\base}{C}=0 \\colorbox{Ccolor}{C}%
        \\else\\ifnum\\pdfstrcmp{\\base}{G}=0 \\colorbox{Gcolor}{G}%
        \\else \\textcolor{red}{\\base}%
        \\fi\\fi\\fi\\fi
    }%
}

\\begin{document}

\\begin{center}
    \\dnafont
    \\textbf{NIVEAU4 ASSEMBLAGE:}
"""

    # Ajouter toutes les séquences formatées
    for header, seq in split_genes:
        formatted_seq = ",".join(seq)
        latex_content += f"\n    \\noindent\\highlightDNA{{{formatted_seq}}}"

    # Fermer le document
    latex_content += "\n\\end{center}\n\\end{document}"

    # Écrire dans le fichier
    with open(output_filename, 'w') as f:
        f.write(latex_content)


# Utilisation avec les gènes splittés
split_genes = []
for header, seq in reads:
    part1, part2 = split_read(seq)
    split_genes.append((header + "_part1", part1))
    split_genes.append((header + "_part2", part2))

save_split_genes_to_latex(split_genes, "assemblage4_1.tex")