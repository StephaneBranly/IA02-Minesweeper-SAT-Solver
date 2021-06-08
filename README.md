# IA02-Projet

Projet dans le cadre de l'UV IA02 "Logique et Résolution de problèmes par la recherche" de l'Université de Technologie de Compiègne.
Résolution d'un problème style démineur.
![image_map](https://i.imgur.com/sm6zzQb.png)

## Copier le projet

- `git clone https://gitlab.utc.fr/branlyst/ia02-projet.git`

## Ajouter une feature / branche

### Creer sa branche
- `git checkout main`
- `git pull`
- `git checkout -b nomBranche`

### Sequencer l'ajout de contenu en commit
- `git add .`
- `git commit -m "Description du commit"`
- `git push`

### Review du code
- Créer une Pull Request (PR) via l'interface Gitlab
- Tester en local en allant sur la branche
    - `git fetch origin`
    - `git checkout nomBranche`
    - tests à effectuer
- Commenter sur la PR les eventuelles modifications à faire ou valider la PR

## Quelques infos dans le tas :

- [Sujet du projet](https://hackmd.io/@ia02/By_zb5GFd)
- Pour coder, 
    - essayer au maximum de typer (ex: `from Typing import Dict`, `def test(a: str) -> Dict: ...` ), utiliser `mypy` pour vérifier
    - utiliser le snake_case avec des noms concis pour les variables, et des verbes pour les fonctions (ex: `ma_variable`, `verifie_map()`)
    - utiliser `black` pour avoir un code propre visuellement (indentation, ...)
    - utiliser si possible sur VS Code l'extension UTC-Header [github extension](https://github.com/StephaneBranly/vscode-utc-header)

## TO DO 
- [ ] voir le fonctionnement de l'API
- [x] faire en sorte que l'on peut effectuer des tests facilement sur une multitude de maps créées en local
- [ ] etudier la parallelisation / creation de `thread`
- [ ] tester en cnf pour comparer les performances
- [ ] effectuer un test en priorite sur le type d'animal le plus present sur le reste de la map `(T,S,C,R)` => R pour rien
- [ ] avant test final, retirer les commentaires dans le fichier

## Optimisations actuelles
- Gestion du fichier
    - Lecture limitée au strict minimum
    - Edition en `append` quand possible (pour éviter de devoir tout réécrire) 
    - Sauvegarde de la position du curseur pour tester et modifier les hypothèses
- Sélection des cases à tester
    - Les cases ayant recues les dernieres informations sont testées en priorité
- Test des hypothèses sur une case
    - Test uniquement si le terrain est cohérent avec l'animal de l'hypothèse
    - Test uniquement s'il reste encore sur la carte l'animal de l'hypothèse
