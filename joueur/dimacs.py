# ************************************************************************************************************************* #
#   UTC Header                                                                                                              #
#                                                         ::::::::::::::::::::       :::    ::: :::::::::::  ::::::::       #
#      dimacs.py                                          ::::::::::::::::::::       :+:    :+:     :+:     :+:    :+:      #
#                                                         ::::::::::::::+++#####+++  +:+    +:+     +:+     +:+             #
#      By: branlyst & duranmar <->                        ::+++##############+++     +:+    +:+     +:+     +:+             #
#      https://gitlab.utc.fr/branlyst/ia02-projet     +++##############+++::::       +#+    +:+     +#+     +#+             #
#                                                       +++##+++::::::::::::::       +#+    +:+     +#+     +#+             #
#                                                         ::::::::::::::::::::       +#+    +#+     +#+     +#+             #
#                                                         ::::::::::::::::::::       #+#    #+#     #+#     #+#    #+#      #
#      Update: 2021/06/08 19:07:05 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

from joueur.solver_template import solver_template
import os
from types_perso.types_perso import *
from typing import List
from itertools import combinations

class dimacs(solver_template): 
    def __init__(self):
       super().__init__()

    # initialisation du fichier .cnf
    #TODO
    def initialiser_fichier_debut(self,infos_grille: GridInfo, nom_carte: str = "") -> str:

        if nom_carte:
            nom_fichier: str = f"{nom_carte}.cnf"
        else:
            nom_fichier: str = f"f.cnf"
        f = open(f"./joueur/fichiers_cnf/{nom_fichier}", "w", newline='\n') # ouverture en "write", ecrase l'ancien si existant
        n: int = infos_grille["n"]
        m: int = infos_grille["m"]    

        #initialisation de la carte a vide
        self.carte_connue = []
        for i in range(m):
            rang = []
            for j in range(n):
                rang.append([0,0])
            self.carte_connue.append(rang)
        f.write(f"c {nom_carte}.map\n")

        texte:str = ""

        # ajout des clauses de comptage
        texte+=(self.generer_clause_nb_type(infos_grille["tiger_count"],"T",m,n))
        texte+=(self.generer_clause_nb_type(infos_grille["shark_count"],"S",m,n))
        texte+=(self.generer_clause_nb_type(infos_grille["croco_count"],"C",m,n))
        texte+=(self.generer_clause_nb_type(infos_grille["sea_count"],"s",m,n))
        texte+=(self.generer_clause_nb_type(infos_grille["land_count"],"l",m,n))

        # initilisation des comptages
        self.comptage_animaux_carte_total = [infos_grille["tiger_count"],infos_grille["shark_count"],infos_grille["croco_count"]]
        self.comptage_animaux_carte_actuel = [0,0,0]

        # ajout des clauses pour chaque case (animal, terrain, animal -> terrain)
        for i in range(infos_grille["m"]):
            for j in range(infos_grille['n']):
                texte+=(self.generer_contrainte_unicite_animal((i,j),m,n))
                texte+=(self.generer_contrainte_unicite_terrain((i,j),m,n))
                texte+=(self.generer_implication_animal_terrain((i,j),m,n))

        # ajout de l'information sur la case de debut
        texte+=(self.generer_information_depart(infos_grille['start'],m,n))

        # TODO, voir pour ajouter informations obtenues au debut de la map

        #écriture dans le fichier
        tableau_ligne=texte.split('\n')
        nb_clause:int = len(tableau_ligne)-2    #nombre de ligne dans le texte-2 (1 commentaire 1 ligne p 1 ligne finale avec juste\n)
        nb_vars:int = n*m*6
        f.write("p cnf "+str(nb_vars)+" "+str(nb_clause)+"\n")
        f.write(texte)

        f.close()
        return nom_fichier

    # ajout de chaque informatiom dans le fichier
    def ajouter_informations_dans_fichier(self,nom_fichier:str, infos: Infos, m: int, n: int) -> str:
        f = open(f"./joueur/fichiers_cnf/{nom_fichier}", "r") # ouverture en "read"
        lignes:List[str] = f.readlines() #sauvegarde du contenu du fichier
        f.close()

        texte:str = ""
        for info in infos: #génération des clauses
            texte += (self.generer_contraintes_information(info,m,n))

        nb_clause:int = len(texte.split('\n'))    #nombre de ligne dans le texte
        nb_vars:int = n*m*6
        lignes[1]="p cnf "+str(nb_vars)+" "+str(nb_clause)+"\n" #modification de la ligne avec le nouveau nombre de clause

        #écriture dans le fichier des lignes déjà présente et de nos nouvelles clauses
        f = open(f"./joueur/fichiers_cnf/{nom_fichier}", "w", newline='\n')
        f.writelines(lignes)
        f.write(texte)
        f.close()

        return nom_fichier

    # generateur clause de comptage
    #TODO    
    def generer_clause_nb_type(self,nb_animal: int, type_var: str, m: int, n:int) -> str:
        clause: str = ""
        for i in range(m):
            for j in range(n):
                clause += f"+1 {self.generer_variable_avec_position_et_type((i,j), type_var, m, n)} " # somme de chaque variable
        clause += f"= {nb_animal}; * comptage total de {type_var}\n" # = comptage total pour ce type
        return clause

    def au_plus_un(vars:List[int]) -> str:
        sortie:str = ""
        for e in combinations(vars, 2):
            sortie+=str(-e[0])+" "+str(-e[1])+" 0\n"
        return sortie

    def generer_variable_avec_position_et_type(self,position: Coord, type_var: str, m: int, n: int) -> int:
        decalage: int = 0
        if type_var == "S":
            decalage = 1
        elif type_var == "C":
            decalage = 2
        elif type_var == "R":
            decalage = 3
        elif type_var == "s":
            decalage = 4
        elif type_var == "l":
            decalage = 5
        indice_variable: int = (position[0] + position[1] * m) * 6 + 1 + decalage # positionnement grille * nombre de vars + decalage initiale + decalage selon type var
        return indice_variable

    def generer_variables_avec_position(self,position: Coord, m: int, n: int) -> List[int]:
        sortie: List[int] = []
        for decalage in range(6):
            sortie.append((position[0] + position[1] * m) * 6 + 1 + decalage) # positionnement grille * nombre de vars + decalage initiale + decalage selon type var
        return sortie

    # les differents generateurs de clauses essentielles
    def generer_contrainte_unicite_animal(self,position: Coord, m: int, n: int) -> str:
        var_ij:List[int] = self.generer_variables_avec_position(position, m, n) #recupere toute les variables liées à la case position
        var:list[int] = [var_ij[2], var_ij[3], var_ij[4]] #recupère juste les variables liées aux animaux présents sur position
        bc:str = str(self.au_plus_un(var))
        return bc

    def generer_contrainte_unicite_terrain(self,position: Coord, m: int, n: int) -> str:
        var_ij:List[int] = self.generer_variables_avec_position(position, m, n) #recupere toute les variables liées à la case (i,j)
        var:list[int] = [var_ij[0], var_ij[1]] #recupère juste les variables liées aux terrin présents sur (i,j)
        bc:str = str(self.au_plus_un(var))
        return bc

    def generer_implication_animal_terrain(self,position: Coord, m: int, n: int) -> str:
        bc:str = ""
        vars:List[int] = self.generer_variables_avec_position(position, m, n) #recupere toute les variables liées à la case (i,j)                
        clause:str=str(-vars[1])+" "+str(-vars[4])+" 0\n"+str(-vars[0])+" "+str(-vars[3])+" 0\n"+str(-vars[4])+" "+str(vars[0])+" 0\n"+str(-vars[3])+" "+str(vars[1])+" 0\n"
        bc+=clause
        return bc

    #génère l'info comme quoi la case de départ est vide de tout animal
    def generer_information_depart(self,position: Coord, m: int, n:int) -> str:
        clause:str = ""
        for i in range(3):
            clause+=str(-self.generer_variables_avec_position(position,m,n)[i+2])+" 0\n"
        return clause

    # generateur de contraintes en fonction des informations obtenues
    #TODO
    def generer_contraintes_information(self,info: Info, m: int, n: int) -> str:
        contraintes: str = ""
        pos: Coord = info['pos']
        i: int = pos[0]
        j: int = pos[1]

        # information sur le type de terrain
        if 'field' in info.keys() and not self.carte_connue[i][j][1]:
            if info['field'] == "sea":
                contraintes += str(self.generer_variables_avec_position(pos,m,n)[0])+" 0\n"
                contraintes += str(-self.generer_variables_avec_position(pos,m,n)[1])+" 0\n"
            else:
                contraintes += str(self.generer_variables_avec_position(pos,m,n)[1])+" 0\n"
                contraintes += str(-self.generer_variables_avec_position(pos,m,n)[0])+" 0\n"
            self.carte_connue[i][j][1] = info['field']

        #TODO
        # information sur le comptage de voisins
        if 'prox_count' in info.keys():
            vecteur: List[Coord] = [(-1,-1),(-1,0),(-1,1),
                    (0,-1),(0,1),
                    (1,-1),(1,0),(1,1)]
            animaux: List[Tuple[int,str]] = [("T",0), ("S",1), ("C",2)]
            proximite_comptage: Compte_Proximite = info['prox_count']
            for animal in animaux:
                contrainte_actuelle = ""
                for vec in vecteur:
                    if self.verifier_position_correcte((i+vec[0],j+vec[1]), m, n):
                        contrainte_actuelle += f"+1 {self.generer_variable_avec_position_et_type((i+vec[0],j+vec[1]), animal[0], m, n)} "
                if contrainte_actuelle:
                    contrainte_actuelle += f"= {proximite_comptage[animal[1]]}; * voisinage animal {animal[0]} de la case ({i},{j})\n"
                    contraintes += contrainte_actuelle
        return contraintes

    # initialisation du fichier pour le prochain test
    #TODO
    def initialiser_test_dans_fichier(self,nom_fichier: str) -> str:
        f = open(f"./joueur/fichiers_cnf/{nom_fichier}", "a") # ouverture en "append"
        f.write("* test ici")
        f.close()
        self.taille_derniere_ligne = len("* test ici")

        return nom_fichier

    # modification de la derniere ligne pour la remplacer avec le test demande
    #TODO
    def ajouter_test_dans_fichier(self,nom_fichier:str, contrainte:str, position: Coord, m: int, n: int) -> str:
        f = open(f"./joueur/fichiers_opb/{nom_fichier}", "rb+") # ouverture en "read and write (bytes)"
        f.seek(-self.taille_derniere_ligne, os.SEEK_END) # positionnement curseur a la ligne "* test ici"
        nouvelle_ligne: str = f"+1 {self.generer_variable_avec_position_et_type(position, contrainte, m, n)} = 0; * hypothese\n"
        self.taille_derniere_ligne = len(nouvelle_ligne) # sauvegarde position debut de la nouvelle ligne
        f.write(str.encode(nouvelle_ligne))
        f.truncate()
        f.close() 
        
        return nom_fichier

    # sauvegarde de l'hypothese qui a ete testee et validee
    #TODO
    def conserver_test_dans_fichier(self,nom_fichier:str, contrainte:str, position: Coord, m: int, n: int) -> str:
        f = open(f"./joueur/fichiers_opb/{nom_fichier}", "a") # ouverture en "append"

        # presence de la contrainte
        f.write(f"+1 {self.generer_variable_avec_position_et_type(position, contrainte, m, n)} = 1; * {contrainte} sur la case {position[0]},{position[1]}\n")
    
        # non presence des autres contraintes sur cette case
        contraintes_non_possibles: List[str] = ["T","S","C","R"]
        contraintes_non_possibles.remove(contrainte)
        non_presence_animaux: str = ""
        for animal in contraintes_non_possibles:
            non_presence_animaux += f"+1 {self.generer_variable_avec_position_et_type(position, animal, m, n)} "
        non_presence_animaux += f" = 0; * les autres animaux ne sont pas sur la case {position[0]},{position[1]}\n"
        f.write(non_presence_animaux)
        
        f.close()

        return nom_fichier

    # suppression de la derniere ligne de test
    #TODO
    def supprimer_dernier_test_dans_fichier(self,nom_fichier: str) -> str:
        f = open(f"./joueur/fichiers_opb/{nom_fichier}", "rb+") # ouverture en "read and write (bytes)"
        f.seek(-self.taille_derniere_ligne, os.SEEK_END) 
        f.truncate()
        f.close() 
        
        return nom_fichier