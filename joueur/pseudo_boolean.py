# ************************************************************************************************************************* #
#   UTC Header                                                                                                              #
#                                                         ::::::::::::::::::::       :::    ::: :::::::::::  ::::::::       #
#      pseudo_boolean.py                                  ::::::::::::::::::::       :+:    :+:     :+:     :+:    :+:      #
#                                                         ::::::::::::::+++#####+++  +:+    +:+     +:+     +:+             #
#      By: branlyst & duranmar <->                        ::+++##############+++     +:+    +:+     +:+     +:+             #
#      https://gitlab.utc.fr/branlyst/ia02-projet     +++##############+++::::       +#+    +:+     +#+     +#+             #
#                                                       +++##+++::::::::::::::       +#+    +:+     +#+     +#+             #
#                                                         ::::::::::::::::::::       +#+    +#+     +#+     +#+             #
#                                                         ::::::::::::::::::::       #+#    #+#     #+#     #+#    #+#      #
#      Update: 2021/06/08 19:04:49 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

from joueur.solver_template import solver_template
import os
from types_perso.types_perso import *
from typing import List

class pseudo_boolean(solver_template): 
    def __init__(self):
       super().__init__()

    # initialisation du fichier .opb
    def initialiser_fichier_debut(self,infos_grille: GridInfo, nom_carte: str = "") -> str:

        if nom_carte:
            nom_fichier: str = f"{nom_carte}.opb"
        else:
            nom_fichier: str = f"f.opb"
        f = open(f"./joueur/fichiers_opb/{nom_fichier}", "w") # ouverture en "write", ecrase l'ancien si existant
        n: int = infos_grille["n"]
        m: int = infos_grille["m"]    

        #initialisation de la carte a vide
        self.carte_connue = []
        for i in range(m):
            rang = []
            for j in range(n):
                rang.append([0,0])
            self.carte_connue.append(rang)
        f.write(f"* carte {nom_carte}.map\n")

        # ajout des clauses de comptage
        f.write(self.generer_clause_nb_type(infos_grille["tiger_count"],"T",m,n))
        f.write(self.generer_clause_nb_type(infos_grille["shark_count"],"S",m,n))
        f.write(self.generer_clause_nb_type(infos_grille["croco_count"],"C",m,n))
        f.write(self.generer_clause_nb_type(infos_grille["sea_count"],"s",m,n))
        f.write(self.generer_clause_nb_type(infos_grille["land_count"],"l",m,n))

        # initilisation des comptages
        self.comptage_animaux_carte_total = [infos_grille["tiger_count"],infos_grille["shark_count"],infos_grille["croco_count"]]
        self.comptage_animaux_carte_actuel = [0,0,0]

        # ajout des clauses pour chaque case (animal, terrain, animal -> terrain)
        for i in range(infos_grille["m"]):
            for j in range(infos_grille['n']):
                f.write(self.generer_contrainte_unicite_animal((i,j),m,n))
                f.write(self.generer_contrainte_unicite_terrain((i,j),m,n))
                f.write(self.generer_implication_animal_terrain((i,j),m,n))

        # ajout de l'information sur la case de debut
        f.write(self.generer_information_depart(infos_grille['start'],m,n))

        # TODO, voir pour ajouter informations obtenues au debut de la map
        f.close()
        return nom_fichier

    # ajout de chaque informatiom dans le fichier
    def ajouter_informations_dans_fichier(self,nom_fichier:str, infos: Infos, m: int, n: int) -> str:
        f = open(f"./joueur/fichiers_opb/{nom_fichier}", "a") # ouverture en "append"
        for info in infos:
            f.write(self.generer_contraintes_information(info,m,n))
        f.close()
        return nom_fichier

    # generateur clause de comptage    
    def generer_clause_nb_type(self,nb_animal: int, type_var: str, m: int, n:int) -> str:
        clause: str = ""
        for i in range(m):
            for j in range(n):
                clause += f"+1 {self.generer_variable_avec_position_et_type((i,j), type_var, m, n)} " # somme de chaque variable
        clause += f"= {nb_animal}; * comptage total de {type_var}\n" # = comptage total pour ce type
        return clause

    # generateur de variable pour position(i,j) et type variable
    def generer_variable_avec_position_et_type(self,position: Coord, type_var: str, m: int, n: int) -> str:
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
        nom_variable: str = f"x{indice_variable}"
        return nom_variable

    # les differents generateurs de clauses essentielles
    def generer_contrainte_unicite_animal(self,position: Coord, m: int, n: int) -> str:
        return f"+1 {self.generer_variable_avec_position_et_type(position,'T',m,n)} +1 {self.generer_variable_avec_position_et_type(position,'S',m,n)} +1 {self.generer_variable_avec_position_et_type(position,'C',m,n)} +1 {self.generer_variable_avec_position_et_type(position,'R',m,n)} = 1; * unicite animal case ({position[0]},{position[1]})\n"

    def generer_contrainte_unicite_terrain(self,position: Coord, m: int, n: int) -> str:
        return f"+1 {self.generer_variable_avec_position_et_type(position,'s',m,n)} +1 {self.generer_variable_avec_position_et_type(position,'l',m,n)} = 1; * unicite type terrain case ({position[0]},{position[1]})\n"

    def generer_implication_animal_terrain(self,position: Coord, m: int, n: int) -> str:
        return f"+1 ~{self.generer_variable_avec_position_et_type(position,'S',m,n)} +1 {self.generer_variable_avec_position_et_type(position,'s',m,n)} >= 1; * non requin ou eau ({position[0]},{position[1]})\n+1 ~{self.generer_variable_avec_position_et_type(position,'T',m,n)} +1 {self.generer_variable_avec_position_et_type(position,'l',m,n)} >= 1; * non tigre ou terre ({position[0]},{position[1]})\n"

    def generer_information_depart(self,position: Coord, m: int, n:int) -> str:
        return f"+1 {self.generer_variable_avec_position_et_type(position,'R',m,n)} = 1; * case de depart ({position[0]},{position[1]})\n"

    # generateur de contraintes en fonction des informations obtenues
    def generer_contraintes_information(self,info: Info, m: int, n: int) -> str:
        contraintes: str = ""
        pos: Coord = info['pos']
        i: int = pos[0]
        j: int = pos[1]

        # information sur le type de terrain
        if 'field' in info.keys() and not self.carte_connue[i][j][1]:
            if info['field'] == "sea":
                contraintes += f"+1 {self.generer_variable_avec_position_et_type(pos,'s',m,n)} = 1; * case sea  ({i},{j})\n"
                contraintes += f"+1 {self.generer_variable_avec_position_et_type(pos,'l',m,n)} = 0; * case non land  ({i},{j})\n"
            else:
                contraintes += f"+1 {self.generer_variable_avec_position_et_type(pos,'l',m,n)} = 1; * case land ({i},{j})\n"
                contraintes += f"+1 {self.generer_variable_avec_position_et_type(pos,'s',m,n)} = 0; * case non sea  ({i},{j})\n"
            self.carte_connue[i][j][1] = info['field']

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
    def initialiser_test_dans_fichier(self,nom_fichier: str) -> str:
        f = open(f"./joueur/fichiers_opb/{nom_fichier}", "a") # ouverture en "append"
        f.write("* test ici")
        f.close()
        self.taille_derniere_ligne = len("* test ici")

        return nom_fichier

    # modification de la derniere ligne pour la remplacer avec le test demande
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
    def supprimer_dernier_test_dans_fichier(self,nom_fichier: str) -> str:
        f = open(f"./joueur/fichiers_opb/{nom_fichier}", "rb+") # ouverture en "read and write (bytes)"
        f.seek(-self.taille_derniere_ligne, os.SEEK_END) 
        f.truncate()
        f.close() 
        
        return nom_fichier