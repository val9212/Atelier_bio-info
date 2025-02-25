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
├───creation
│       diapo.pptx                      #Fichier Powerpoint du diaporama.
│       fasta_latex.py                  #Script permettant de convertir des reads au format Fasta en LaTeX.
│       generate_and_verify_fasta.py    #Script python capable de generer un jeu de données. 
│       niv1                            #Reads et gènes de l'exercice1 uniquement.    
│       niv2                            #Reads et gènes de l'exercice2 uniquement. 
│       niv3                            #Consensus et gènes de l'exercice3. 
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
        Alignement_n1.sb3
        Alignement_n2.sb3
        readme.md                       #Enoncé des exercices Scratch.
        Sequences.sb3

```

fasta_latex exemple de commande py .\creation\fasta_latex.py --input .\creation\niv1.txt --output .\creation\test.tex