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
#      Update: 2021/06/24 22:47:09 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

import random
from types_perso.types_perso import *
from typing import List

class Solver_template():
    def __init__(self):
        # variables globales pour enregistrer la partie en cours
        self.taille_derniere_ligne: int = 0
        self.carte_connue: List[List[List[str,int]]] = []
        self.nombre_cases_restantes: int = 0
        self.comptage_animaux_carte_total: List[int] = []
        self.comptage_animaux_carte_actuel: List[int] = []
        self.comptage_type_case_total: List[int] =[]
        self.comptage_type_case_actuel: List[int] = []
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
    def verifier_sat_fichier(self, chemin_solver: str, clause_sup:str = "") -> bool:
        pass

    # verification si case deja exploree
    def verifier_si_case_exploree(self,position: Coord) -> bool:
        valeur:str = self.carte_connue[position[0]][position[1]][0]
        return valeur == "R" or valeur == "S" or valeur == "C" or valeur == "T"

    # indication type case exploree
    def indiquer_case_exploree(self,position: Coord, type_animal: str):
        if not self.verifier_si_case_exploree(position):
            self.nombre_cases_restantes -= 1
        self.carte_connue[position[0]][position[1]][0] = type_animal


    # verification si toutes les cases d'un type de case a ete decouvert, retourne l'indice i+1 du type de case
    def verification_type_cases_decouvert_totalement(self) -> int:
        if self.comptage_type_case_total[0] == self.comptage_type_case_actuel[0]:
            self.comptage_type_case_actuel[0] = -1
            return 1
        elif self.comptage_type_case_total[1] == self.comptage_type_case_actuel[1]:
            self.comptage_type_case_actuel[1] = -1
            return 2
        return 0

    # incrementation du compteur d'animaux quand decouvert
    def incrementer_comptage_animal(self,type_animal: str) -> int:
        id: int = 0 
        if type_animal == 'S':
            id = 1
        elif type_animal == 'C':
            id = 2
        self.comptage_animaux_carte_actuel[id] += 1
        return self.comptage_animaux_carte_actuel[id]

    # indique le nombre actuel d'animaux decouverts  
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
    def hypothese_sur_case(self, position: Coord, chemin_solver:str, hyp:str, clause_sup: str = ""):
        action = None
        resultat: bool
        if self.vaut_le_coup_de_tester(hyp,position):
            if not clause_sup:
                self.ajouter_test_dans_fichier(hyp,position)
            resultat = self.verifier_sat_fichier(chemin_solver, clause_sup)
            if not resultat: # si unsat, on a donc [clauses],hypothese => None // [clauses] => hypothese 
                if hyp == "R":
                    action = "d"
                else:
                    action = "g"
        return action

    # renvoie le voisinage d'une case
    def avoir_voisinage(self, position: Coord) -> List[Coord]:
        voisins: List[Coord] = []
        vecteur: List[Coord] = [(-1,-1),(-1,0),(-1,1),
                    (0,-1),(0,1),
                    (1,-1),(1,0),(1,1)]
        for vec in vecteur:
            if self.verifier_position_correcte((position[0]+vec[0],position[1]+vec[1])):
                voisins.append((position[0]+vec[0],position[1]+vec[1]))
        return voisins


    def avoir_nombre_cases_restantes(self) -> int:
        return self.nombre_cases_restantes

    def avoir_nombre_animaux_restants(self) -> int:
        restant: int = 0
        for i in range(3):
            restant += self.comptage_animaux_carte_total[i] - self.comptage_animaux_carte_actuel[i]
        return restant

    # permet d'indiquer quel est le meilleur coup a faire en se basant sur des probabiles
    def choisir_mouvement_aleatoire(self, bordure: List[Coord]) -> Tuple[List, float]:
        act = None
        surete: float
        coups_conseilles: List[Dict] = []

        # analyse du meilleur coup pour chaque case de la bordure
        for case in bordure:
            if not self.verifier_si_case_exploree(case):
                conseil = self.calculer_meilleur_coup_case(case)
                if conseil != None:
                    coups_conseilles.append(conseil)
        
        # si on a des coups conseilles, on prend le meilleur coup parmis toutes les cases
        if coups_conseilles:
            coups_conseilles = sorted(coups_conseilles, key=lambda k: k['probabilite'], reverse=True) 
            coup = coups_conseilles[0]
            if coup['animal'] == "R":
                act = ["d",coup['pos'],coup['animal']]
            else:
                act = ["g",coup['pos'],coup['animal']]
            surete = coup['probabilite']

        # si on a pas trouve d'action, on prend une case au hasard et l'on effcecxtue un discover
        if not act:
            x_ramdom = random.randint(0,self.m-1)
            y_ramdom = random.randint(0,self.n-1)
            while not self.verifier_position_correcte((x_ramdom,y_ramdom)) or self.verifier_si_case_exploree((x_ramdom,y_ramdom)):
                x_ramdom = random.randint(0,self.m-1)
                y_ramdom = random.randint(0,self.n-1)
            i_resultat = x_ramdom
            j_resultat = y_ramdom
            hyp_resultat = "R"
            action = "d"
            act = [action,(i_resultat,j_resultat),hyp_resultat]
            surete = (self.avoir_nombre_cases_restantes() - self.avoir_nombre_animaux_restants()) / self.avoir_nombre_cases_restantes()
        
        return act, surete

    # retourne le meilleur coup pour une case
    def calculer_meilleur_coup_case(self, position:Coord):
        coups_conseilles: List[Dict] = []
        for v in self.avoir_voisinage(position): # analyse de tous les voisins de cette case pour voir ce qu'ils pensent que position contient
            conseil = self.calculer_coup_conseille_voisin(v, position)
            if conseil != None:
                coups_conseilles.append(conseil)
        if len(coups_conseilles): # selection du contenu le plus probable
            coups_conseilles = sorted(coups_conseilles, key=lambda k: k['probabilite'], reverse=True) 
            coups_conseilles[0]['pos'] = position
            return coups_conseilles[0]
        return None

    # retourne un conseil sur la case conseille en se basant sur la vue de position et son entourage
    def calculer_coup_conseille_voisin(self, position: Coord, conseille: Coord):
        if self.verifier_si_case_exploree(position):
            if self.carte_connue[position[0]][position[1]][0] == "R":
                compteur_terre_restante:  int = 0
                compteur_mer_restante:  int = 0
                compteur_case_restante: int = 0
                comptage_animaux_restants: List[int] = self.carte_connue[position[0]][position[1]][2].copy()
                # analyse et comptage du voisinage
                for v in self.avoir_voisinage(position):
                    if self.verifier_si_case_exploree(v):
                        if self.carte_connue[v[0]][v[1]][0] != "R":
                            if self.carte_connue[v[0]][v[1]][0] == "T":
                                comptage_animaux_restants[0] -= 1 
                            elif self.carte_connue[v[0]][v[1]][0] == "S":
                                comptage_animaux_restants[1] -= 1 
                            elif self.carte_connue[v[0]][v[1]][0] == "C":
                                comptage_animaux_restants[2] -= 1 

                    else:
                        compteur_case_restante += 1
                        if self.carte_connue[v[0]][v[1]][1] == "land":
                            compteur_terre_restante += 1
                        else:
                            compteur_mer_restante += 1

                proba_croco: float = (comptage_animaux_restants[2] / compteur_case_restante) # proba que ce soit un crocodile
                proba_adapte: float = 0
                coup_conseille: Dict = dict()

                # probabilite d'avoir l'autre type d'animal qui vit sur le terrain
                if self.carte_connue[conseille[0]][conseille[1]][1] == "land":
                    coup_conseille['animal'] = "T"
                    proba_adapte = (comptage_animaux_restants[0] / compteur_terre_restante)
                else:
                    coup_conseille['animal'] = "S"
                    proba_adapte = (comptage_animaux_restants[1] / compteur_mer_restante)
                proba_rien: float = 1 - proba_croco - proba_adapte # proba qu'il n'y ait rien

                # selection de la meilleure probabilite
                coup_conseille['probabilite'] = proba_adapte
                if proba_croco > proba_adapte:
                    coup_conseille['animal'] = "C"
                    coup_conseille['probabilite'] = proba_croco
                if proba_rien > coup_conseille["probabilite"]:
                    coup_conseille['animal'] = "R"
                    coup_conseille['probabilite'] = proba_rien

                return coup_conseille
                        
        return None