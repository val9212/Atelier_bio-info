# Documents Atelier Bio-informatique

```
│   carnet.pdf
│   diapo.pdf
│   readme.md
│
├───Assemblages
│       Assemblage1.tex                 #Assemblage niveau1.
│       Assemblage2.tex                 #Assemblage niveau2.
│       Assemblage3.tex                 #Assemblage niveau3.
│       assemblage4_1.tex               #Assemblage niveau4 partie1.
│       assemblage4_2.tex               #Assemblage niveau4 partie1.
│
├───automates
│   │   légende.png                    #Légende des automates.
│   │   niveau1.png                    #Automate niveau 1.
│   │   niveau2.png                    #Automate niveau 2.
│   │   niveau3.png                    #Automate niveau 3.
│   │   niveau4.png                    #Automate niveau 4.
│   │
│   └───correction                     #Correction des automates
│           niveau1-corrigé.png
│           niveau2-corrigé.png
│           niveau3-corrigé.png
│           niveau4-corrigé.png
│
├───create
│       carnet_pfe                       #Fichier word du carnet. 
│       fasta_latex.py                   #Script permettant de convertir des reads au format Fasta en LaTeX.
│       generate_and_verify_fasta.py     #Script python capable de generer un jeu de données. 
│       Mystere_du_medicament_perdu.pptx #Fichier Powerpoint du diaporama.
│       niv1                             #Reads et gènes de l'exercice1 uniquement.    
│       niv2                             #Reads et gènes de l'exercice2 uniquement. 
│       niv3                             #Consensus et gènes de l'exercice3. 
│       reads.fasta                      #Test de jeu de données.
│
├───python
│   │   exercice0.py                    #Script exercice0.
│   │   exercice1.py                    #Script exercice1.
│   │   exercice2.py                    #Script exercice2.
│   │   exercice3.py                    #Script exercice3.
│   │   niv0.fasta                      #Jeu de donnée pour l'exercice 0.
│   │   readme.md                       #Enoncé des exercices Pyhton.
│   │   reads.fasta                     #Jeu de données pour les exercices 1, 2 et 3.
│   │
│   └───correction                      #Script corrigé des exercices python.
│           exercice0.py
│           exercice1.py
│           exercice2.py
│           exercice3.py
│
└───scratch
        exercice0.sb3
        exercice1.sb3
        exercice2.sb3
        jd_scratch.fasta
        readme.md                       #Enoncé des exercices Scratch.

```

## Liens

- Carnet
> `https://docs.google.com/document/d/1HITE3KPE_eUss2RUHZ9Ar2EJ5bEXz_Apae5CAiFWETE/edit?usp=sharing`

- Diaporama
> `https://docs.google.com/presentation/d/17Axj2qatgtzGglY-XbqR1_Z82SHLJNwp2kpv3NbDUvY/edit?usp=sharing`

## Utilisation des script create

### fasta_latex.py

Script capable de transformer les "Read" d'un fichier fasta en sequence LaTeX

- Argument
    
    - --input : Fichier FASTA en entrée
    - --output : Fichier LaTeX en sortie


- Exemple d'utilisation
> `py .\creation\fasta_latex.py --input .\creation\niv1.txt --output .\creation\test.tex`

### generate_and_verify_fasta.py

Script capable à partir de différents paramètres de créer des gènes et des reads associées. Le programme vérifie ensuite que les reads couvrent bien la totalité des gènes.

- Argument 
  - --gene_length : Longueur des gènes (nt)
  - --min_read_length : Longueur des reads (nt)
  - --max_read_length : Longueur des reads (nt)
  - --coverage : Couverture désirée pour niveaux 1 et 2
  - --error_rate_level2 : Taux d'erreur pour le niveau 2 
  - --output : Nom du fichier FASTA de sortie


- Exemple d'utilisation
>`py .\creation\generate_and_verify_fasta.py --gene_length 150 --min_read_length 10 --max_read_length 20 --coverage 5.0 --error_rate_level2 0.02 --output .\creation\test.fasta`