# ************************************************************************************************************************* #
#   UTC Header                                                                                                              #
#                                                         ::::::::::::::::::::       :::    ::: :::::::::::  ::::::::       #
#      solver_template.py                                 ::::::::::::::::::::       :+:    :+:     :+:     :+:    :+:      #
#                                                         ::::::::::::::+++#####+++  +:+    +:+     +:+     +:+             #
#      By: branlyst & duranmar <->                        ::+++##############+++     +:+    +:+     +:+     +:+             #
#      https://gitlab.utc.fr/branlyst/ia02-projet     +++##############+++::::       +#+    +:+     +#+     +#+             #
#                                                       +++##+++::::::::::::::       +#+    +:+     +#+     +#+             #
#                                                         ::::::::::::::::::::       +#+    +#+     +#+     +#+             #
#                                                         ::::::::::::::::::::       #+#    #+#     #+#     #+#    #+#      #
#      Update: 2021/06/15 17:07:51 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

from types_perso.types_perso import *
from typing import List
import os

class solver_template():
    def __init__(self):
        self.taille_derniere_ligne: int
        # variables globales pour enregistrer la partie en cours
        self.carte_connue: List[List[List[str]]]
        self.comptage_animaux_carte_total: List[int]
        self.comptage_animaux_carte_actuel: List[int]
        self.n: int = 0
        self.m: int = 0
        self.nom_fichier: str = ""

     # initialisation du fichier .opb
    def initialiser_fichier_debut(self, infos_grille: GridInfo, nom_carte: str = "") -> str:
        pass
    
    # ajout de chaque informatiom dans le fichier
    def ajouter_informations_dans_fichier(self, infos: Infos) -> str:
        pass

    # generateur clause de comptage    
    def generer_clause_nb_type(self, nb_animal: int, type_var: str) -> str:
        pass

    # generateur de variable pour position(i,j) et type variable
    def generer_variable_avec_position_et_type(self,position: Coord, type_var: str) -> str:
        pass

    # les differents generateurs de clauses essentielles
    def generer_contrainte_unicite_animal(self,position: Coord) -> str:
        pass

    def generer_contrainte_unicite_terrain(self,position: Coord) -> str:
        pass

    def generer_implication_animal_terrain(self,position: Coord) -> str:
        pass

    def generer_information_depart(self,position: Coord) -> str:
        pass

    # generateur de contraintes en fonction des informations obtenues
    def generer_contraintes_information(self,info: Info) -> str:
        pass

    # initialisation du fichier pour le prochain test
    def initialiser_test_dans_fichier(self) -> str:
        pass

    # modification de la derniere ligne pour la remplacer avec le test demande
    def ajouter_test_dans_fichier(self, contrainte:str, position: Coord) -> str:
        pass
        
    # sauvegarde de l'hypothese qui a ete testee et validee
    def conserver_test_dans_fichier(self, contrainte:str, position: Coord) -> str:
        pass

    # suppression de la derniere ligne de test
    def supprimer_dernier_test_dans_fichier(self) -> str:
        pass

    # verification de position valide
    def verifier_position_correcte(self,position: Coord) -> bool:
        return not (position[0]<0 or position[0]>= self.m 
        or position[1]<0 or position[1]>= self.n)

    # verification si le probleme est satisfiable
    def verifier_sat_fichier(self, chemin_solver: str) -> bool:
        pass

    
    def verifier_si_case_exploree(self,position: Coord) -> bool:
        return self.carte_connue[position[0]][position[1]][0] != 0

    def indiquer_case_exploree(self,position: Coord, type_animal: str):
        self.carte_connue[position[0]][position[1]][0] = type_animal

    def incrementer_comptage_animal(self,type_animal: str) -> int:
        id: int = 0 
        if type_animal == 'S':
            id = 1
        elif type_animal == 'C':
            id = 2
        self.comptage_animaux_carte_actuel[id] += 1
        return self.comptage_animaux_carte_actuel[id]
        
    def avoir_comptage_animaux_actuel(self) -> Tuple[int,int,int]:
        return (self.comptage_animaux_carte_actuel[0],self.comptage_animaux_carte_actuel[1],self.comptage_animaux_carte_actuel[2])

    # optimisation de coup, ne test pas si tous les animaux de l'hypothese ont deja ete trouves, ou si le terrain ne convient pas a l'animal de l'hypothese
    def vaut_le_coup_de_tester(self,hypothese: str, position: Coord) -> bool:
        if hypothese == "T":
            if self.carte_connue[position[0]][position[1]][1] == "sea":
                return False
            if self.comptage_animaux_carte_actuel[0] == self.comptage_animaux_carte_total[0]:
                return False
        elif hypothese == "S":
            if self.carte_connue[position[0]][position[1]][1] == "land":
                return False
            if self.comptage_animaux_carte_actuel[1] == self.comptage_animaux_carte_total[1]:
                return False
        elif hypothese == "C":
            if self.comptage_animaux_carte_actuel[2] == self.comptage_animaux_carte_total[2]:
                return False
        return True

    # generateur d'hypothese sur la case
    def hypothese_sur_case(self, position: Coord, chemin_solver:str):
        action = None
        resultat: bool
        hyp_resultat: str = None
        self.initialiser_test_dans_fichier()
        for hyp in ['T','S','C','R']: # pour toutes les hypotheses possibles
            if self.vaut_le_coup_de_tester(hyp,position):
                self.ajouter_test_dans_fichier(hyp,position)
                resultat = self.verifier_sat_fichier(chemin_solver)
                if not resultat:
                    hyp_resultat = hyp
                    if hyp == "R":
                        action = "d"
                    else:
                        action = "g"
        self.supprimer_dernier_test_dans_fichier()
        return action, hyp_resultat

    def generer_template_carte(self, n: int, m: int) -> str:
        pass