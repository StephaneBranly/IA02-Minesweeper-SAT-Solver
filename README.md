# IA02-Projet

Projet dans le cadre de l'UV IA02 "Logique et Résolution de problèmes par la recherche" de l'Université de Technologie de Compiègne.
Résolution d'un problème style démineur.
![image_map](https://i.imgur.com/sm6zzQb.png)

## Copier le projet

- `git clone https://gitlab.utc.fr/branlyst/ia02-projet.git`

## Pour lancer le projet 
```python3 main.py -o macos -s cnf -t serveur -p```
=> ```macos | windows | linux```
=> Si utilisation du mode parallele, il faut utiliser le ```glucose``` personnalisé.
-> dans le ```main.py```, peuvent être changés les chemins des solveurs

```python3 main.py -h``` pour voir les differentes instructions possibles.

## Projet 
### Spécifités :
- Changement du sat solver et personnalisation
- Execution en parallele possible
- Execution avec du pseudo boolean non parallele possible
- Selection specifique des futurs noeuds a visiter
- Prise en compte des probabilites pour les coups aleatoires

### Pistes d'améliorations
- Prendre en compte l'utilisation de chords
- Utiliser une librairie Python pour avoir un solveur
- Prendre en compte le comptage total

## Quelques infos dans le tas :

- [Sujet du projet](https://hackmd.io/@ia02/By_zb5GFd)
- Pour coder, 
    - essayer au maximum de typer (ex: `from Typing import Dict`, `def test(a: str) -> Dict: ...` ), utiliser `mypy` pour vérifier : 
    ``` mypy **.py ./joueur/*.py ./moteur/*.py ./test/*.py ./types_perso/*.py```
    - utiliser le snake_case avec des noms concis pour les variables, et des verbes pour les fonctions (ex: `ma_variable`, `verifier_carte()`)
    - utiliser `black` pour avoir un code propre visuellement (indentation, ...)
    - utiliser si possible sur VS Code l'extension UTC-Header [github extension](https://github.com/StephaneBranly/vscode-utc-header)

## TO DO 
- [x] voir le fonctionnement de l'API
- [x] faire en sorte que l'on peut effectuer des tests facilement sur une multitude de maps créées en local
- [x] etudier la parallelisation / creation de `thread` -> pas efficace
- [x] tester en cnf pour comparer les performances -> on conserve `cnf`
- [x] effectuer un test en priorite sur le type d'animal le plus present sur le reste de la map `(T,S,C,R)` => R pour rien
- [x] avant test final, retirer les commentaires dans le fichier
- [ ] retirer clauses en double
- [x] retirer variable inutilisee

## Structuration du projet
```
projet/ 
|-- main.py
|-- joueur/ 
|       |-- joueur.py
|       |-- joueur_parallele.py
|       |-- solver_template.py
|       |-- dimacs.py
|       |-- pseudo_boolean.py
|       |-- fichiers_cnf/
|       |-- fichiers_opb/
|
|-- moteur/ 
|       |-- moteur.py
|       |-- crocomine_client.py
|       |-- serveur/
|
|-- test/ 
|       |-- test.py
|       |-- generer_cartes.py
|       |-- test_maps/
|       |-- historique_maps/
|
|-- grilles/ 
|       |-- croco/
|       |-- map/
|
|-- types_perso/ 
|       |-- types_perso.py
|
|-- solvers/                    
```

## Exécution des tests
Dans le dossier `./test/` se trouvent les outils utilisés pour effectuer les tests. 
- On retrouve un générateur de cartes dont on pourra modifier certains paramètres comme `n`, `m`, la `proportion d'eau` et la `proportion d'animaux`. La case de départ est toujours libre d'animaux ainsi que son voisinage.
- Nous avons aussi une fonction de test exécutant toutes les cartes du `serveur local` ou du `moteur local` (moteur implémenté avant l'apparition de la première version du serveur) et indiquant des statistiques relatives aux parties comme le résultat de la carte (`OK`|`KO`), le temps pour la résoudre, la donnée `s` correspondant à la sureté des coups joués (`s=1.00` signifie que tous les coups étaient certains, pour `s < 1` on a des coups qui ont été selectionnés par des probabilités). 
- Une comparaison des temps d'exécution a été réalisé afin d'évaluer la qualité des optimisations. Cette comparaison est faite sur une carte de `51x51` avec le point de départ au centre. Un `zoom` est effectué sur cette carte pour comparer les performances en fonction de la taille.


## Optimisations
- Gestion du fichier
    - Lecture limitée au strict minimum
    - Edition en `append` quand possible (pour éviter de devoir tout réécrire) 
    - Sauvegarde de la position du curseur pour tester et modifier les hypothèses (non parallèle)
- Sélection des cases à tester
    - Les cases ayant recues les dernieres informations sont testées en priorité (non parallèle)
- Test des hypothèses sur une case
    - Test uniquement si le terrain est cohérent avec l'animal de l'hypothèse
    - Test uniquement s'il reste encore sur la carte l'animal de l'hypothèse
    - Tests effectués en parallèle
- Modélisation du problème
    - Utilisation de seulement 3 variables par cellule `(Croco, Tigre, Requin)`
- Solveur SAT
    - Utilisation de `Glucose` au lieu de `Gophersat` (indiqué comme 2 à 5 fois plus rapide)
        - Glucose personnalisé dispo ici : [glucose-syrup-4.1](https://github.com/StephaneBranly/glucose-syrup-4.1)
    - Recompilation du solveur en changeant le contenu de `stdout` (`0`|`1`|`2` au lieu de `s UNSATISFIABLE`|`s SATISFIABLE` + informations superflux)
    - Recompilation du solveur pour changer les arguments : `solver fichier.cnf nb_clauses "clause a tester"` (parallèle)



## Comparaison des performances
![Performances](Documents_divers/perfs.png)
Informations sur les courbes:
| Version             | Commentaire                                                 |                      |       |       |       |       |        |        |         |         |         |         |         |         |         |         |         |         |         |         |         |         |         |         |          |          |          |  |
|---------------------|-------------------------------------------------------------|----------------------|-------|-------|-------|-------|--------|--------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|----------|----------|----------|--|
|                     |                                                             | n =                  | 3     | 5     | 7     | 9     | 11     | 13     | 15      | 17      | 19      | 21      | 23      | 25      | 27      | 29      | 31      | 33      | 35      | 37      | 39      | 41      | 43      | 45      | 47       | 49       | 51       |  |
|                     |                                                             | nombre de cellules = | 9     | 25    | 49    | 81    | 121    | 169    | 225     | 289     | 361     | 441     | 529     | 625     | 729     | 841     | 961     | 1089    | 1225    | 1369    | 1521    | 1681    | 1849    | 2025    | 2209     | 2401     | 2601     |  |
| cnf-20210618_024118 | version initiale aux tests de performance                   |                      | 0,179 | 0,776 | 1,979 | 5,388 | 22,289 | 31,237 | 46,001  | 70,427  | 127,031 | 167,153 | 257,536 | 312,087 | 194,378 | 397,87  | 458,249 | 360,232 | 377,365 | 562,049 | 853,418 | 709,19  | 935,57  | 865,112 | 1184,168 | 1189,111 | 1830,975 |  |
| opb-20210618_181516 | nombre de variable passe a 3 / pour opb                     |                      | 0,193 | 0,924 | 2,289 | 6,744 | 44,737 | 58,23  | 111,227 | 148,499 | 448,322 | 398,847 | 672,467 | 815,384 | 572,757 | 1024,76 |         |         |         |         |         |         |         |         |          |          |          |  |
| cnf-20210618_192155 | changement ordre priorite des tests                         |                      | 0,187 | 0,743 | 1,825 | 5,044 | 20,628 | 28,743 | 41,77   | 64,279  | 114,884 | 149,303 | 221,869 | 267,183 | 168,145 | 334,116 |         |         |         |         |         |         |         |         |          |          |          |  |
| cnf-20210618_195739 | guess effectues a la toute fin                              |                      | 0,188 | 0,771 | 1,966 | 6,187 | 16,34  | 22,774 | 30,934  | 54,037  | 84,821  | 112,97  | 145,108 | 194,264 | 279,275 | 347,516 |         |         |         |         |         |         |         |         |          |          |          |  |
| cnf-20210619_005743 | utilisation de glucose-simp recompile en changeant l'output |                      | 0,179 | 0,738 | 1,867 | 5,655 | 15,245 | 20,921 | 27,776  | 46,013  | 67,859  | 86,773  | 108,944 | 140,756 | 188,181 | 235,606 |         |         |         |         |         |         |         |         |          |          |          |  |
| cnf-20210622_204835 | meilleure gestion de la liste des cases a tester            |                      | 0,187 | 0,737 | 1,839 | 5,047 | 13,821 | 18,731 | 24,496  | 33,731  | 46,431  | 58,888  | 72,087  | 80,757  | 99,075  | 117,644 | 124,019 | 142,136 | 168,416 | 196,906 | 241,655 | 277,712 | 312,403 | 352,218 | 407,35   | 440,81   | 498,05   |  |
| cnf-20210623_194342 | nombre de variable passe a 3 / pour cnf                     |                      | 0,181 | 0,725 | 1,877 | 4,987 | 13,213 | 19,771 | 25,016  | 33,898  | 46,221  | 58,657  | 69,941  | 82,373  | 98,25   | 107,074 | 121,446 | 138,09  | 163,569 | 192,688 | 233,8   | 275,711 | 308,917 | 343,563 | 392,52   | 434,472  | 490,24   |  |
| cnf-20210623_223619 | recompilation de glucose pour utiliser des arguments        |                      | 0,176 | 0,717 | 1,833 | 4,934 | 13,016 | 19,486 | 24,636  | 33,285  | 45,053  | 57,187  | 68,813  | 79,955  | 94,645  | 104,178 | 116,455 | 132,454 | 158,346 | 186,839 | 222,949 | 261,666 | 292,978 | 329,29  | 374,296  | 407,764  | 455,445  |  |
| cnf-20210624_024010 | parallelisation                                             |                      | 0,187 | 0,7   | 1,759 | 4,851 | 11,794 | 18,092 | 22,212  | 32,609  | 40,843  | 51,251  | 59,172  | 69,721  | 80,446  | 91,317  | 100,046 | 112,998 | 133,019 | 152,538 | 178,836 | 201,442 | 225,524 | 249,69  | 279,264  | 300,886  | 336,056  |  |