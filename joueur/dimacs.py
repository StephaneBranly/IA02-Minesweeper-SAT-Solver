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
#      Update: 2021/06/25 14:21:39 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

from joueur.solver_template import Solver_template
import os
from types_perso.types_perso import *
from typing import List
from itertools import combinations

#pour une case les variables sont: [croco tigre requin]

class Dimacs(Solver_template): 
    def __init__(self,parallele=False):
        self.nb_clause:int = 0
        self.nb_var:int = 0
        self.parallele = parallele
        super().__init__()
    
    # initialisation du fichier .cnf
    def initialiser_fichier_debut(self,infos_grille: GridInfo, nom_carte: str = "") -> str:
        if nom_carte:
            self.nom_fichier = f"{nom_carte}.cnf"
        else:
            self.nom_fichier = f"f.cnf"
        f = open(f"./joueur/fichiers_cnf/{self.nom_fichier}", "w", newline='\n') # ouverture en "write", ecrase l'ancien si existant
        self.n: int = infos_grille["n"]
        self.m: int = infos_grille["m"]  
        self.nb_var=self.m*self.n*3
        self.nombre_cases_restantes = self.n * self.m
        
        flatList = []
        #initialisation de la carte a vide
        self.carte_connue = []
        for i in range(self.m):
            rang = []
            for j in range(self.n):
                rang.append([0,0,None])
                flatList.append([i,j])
            self.carte_connue.append(rang)
        f.write(f"c {nom_carte}.map\n")

        texte:str = ""
        
        # initilisation des comptages
        self.comptage_animaux_carte_total = [infos_grille["tiger_count"],infos_grille["shark_count"],infos_grille["croco_count"]]
        self.comptage_animaux_carte_actuel = [0,0,0]
        self.comptage_type_case_total = [infos_grille["sea_count"],infos_grille["land_count"]]
        self.comptage_type_case_actuel = [0,0]

        # ajout des clauses pour chaque case (animal, terrain, animal -> terrain)
        for i in range(infos_grille["m"]):
            for j in range(infos_grille['n']):
                texte+=(self.generer_contrainte_unicite_animal((i,j)))

        # ajout de l'information sur la case de debut
        texte+=(self.generer_information_depart(infos_grille['start']))

        # ajout des informations optionnelles de la carte
        if 'infos' in infos_grille.keys():
            infos: Infos = infos_grille['infos']
            for info in infos: #génération des clauses
                texte += (self.generer_contraintes_information(info))
            

        f.write(f"p cnf {self.nb_var} {self.nb_clause}\n")
        f.write(texte)
        
        f.close()
        return self.nom_fichier

    def mettre_a_jour_entete(self) -> str:
        f = open(f"./joueur/fichiers_cnf/{self.nom_fichier}", "r") # ouverture en "read"
        lignes:List[str] = f.readlines() #sauvegarde du contenu du fichier
        f.close()

        lignes[1]=f"p cnf {self.nb_var} {self.nb_clause}\n" #modification de la ligne avec le nouveau nombre de clauses

        #écriture dans le fichier des lignes déjà présente et de nos nouvelles clauses
        f = open(f"./joueur/fichiers_cnf/{self.nom_fichier}", "w", newline='\n')
        f.writelines(lignes)
        f.close()
        return self.nom_fichier

    # ajout de chaque informatiom dans le fichier
    def ajouter_informations_dans_fichier(self, infos: Infos) -> str:
        texte:str = ""
        for info in infos: #génération des clauses
            texte += (self.generer_contraintes_information(info))

        f = open(f"./joueur/fichiers_cnf/{self.nom_fichier}", "a")
        f.write(texte)
        f.close()
        
        if not self.parallele:
            self.mettre_a_jour_entete()

        return self.nom_fichier

    # clause de comptage, au plus 1 variable
    def au_plus_un(self, vars:List[int]) -> str:
        sortie:str = ""
        for e in combinations(vars, 2):
            sortie+= f"-{e[0]} -{e[1]} 0\n"
            self.nb_clause += 1

        return sortie

    #[sea land croco tigre requin découverte]
    def generer_variable_avec_position_et_type(self,position: Coord, type_var: str) -> str:
        decalage: int = 0
        if type_var == "C":
            decalage = 0
        elif type_var == "T":
            decalage = 1
        elif type_var == "R" or type_var == "S":
            decalage = 2
        indice_variable: str = f"{(position[0] + position[1] * self.m) * 3 + 1 + decalage}" # positionnement grille * nombre de vars + decalage initiale + decalage selon type var
        return indice_variable

    def generer_variables_avec_position(self,position: Coord) -> List[int]:
        sortie: List[int] = []
        for decalage in range(3):
            sortie.append((position[0] + position[1] * self.m) * 3 + 1 + decalage) # positionnement grille * nombre de vars + decalage initiale + decalage selon type var
        return sortie #[sea croco tigre requin]

    # les differents generateurs de clauses essentielles
    def generer_contrainte_unicite_animal(self,position: Coord) -> str:
        var_ij:List[int] = self.generer_variables_avec_position(position) #recupere toute les variables liées à la case position
        var:list[int] = [var_ij[0], var_ij[1], var_ij[2]] #recupère juste les variables liées aux animaux présents sur position
        bc:str = str(self.au_plus_un(var))
        return bc

    #génère l'info comme quoi la case de départ est vide de tout animal
    def generer_information_depart(self,position: Coord) -> str:
        clause:str = ""
        for i in range(3):
            clause+= f"-{self.generer_variables_avec_position(position)[i]} 0\n"
        self.nb_clause += 3
        
        return clause

    # generateur de contraintes en fonction des informations obtenues
    def generer_contraintes_information(self,info: Info) -> str:
        contraintes: str = ""
        pos: Coord = info['pos']
        i: int = pos[0]
        j: int = pos[1]
            
        # information sur le type de terrain
        if 'field' in info.keys() and not self.carte_connue[i][j][1]:
            if info['field'] == "sea":
                contraintes += f"-{self.generer_variable_avec_position_et_type(pos,'T')} 0\n" # si c'est la mer, on dit qu'il ne peut pas y avoir de tigre
                self.comptage_type_case_actuel[0] += 1
            else:
                contraintes += f"-{self.generer_variable_avec_position_et_type(pos,'S')} 0\n" # si c'est la terre, il ne peut pas y avoir de requin
                self.comptage_type_case_actuel[1] += 1

            self.carte_connue[i][j][1] = info['field']

            verification_type_case: int = self.verification_type_cases_decouvert_totalement()

            if verification_type_case != 0: # si on a decouvert toutes les cases d'un certain type
                terrain_restant: str = "sea"
                animal_non_present: str = "T"
                if verification_type_case == 1: # check du type de case restante
                    animal_non_present = "S" # - pour indiquer non mer
                    terrain_restant = "land"

                # pour toutes les cases restantes, on indique le type restant
                for i_f in range(self.m):
                    for j_f in range(self.n):
                        if not self.carte_connue[i_f][j_f][1]: # si le type n'etait pas encore connu
                            contraintes += f"-{self.generer_variable_avec_position_et_type((i_f,j_f),animal_non_present)} 0\n" # on ajoute le type d'animal qui ne pourra pas etre present
                            self.carte_connue[i_f][j_f][1] = terrain_restant
                            self.nb_clause += 1

            self.nb_clause += 1


        # information sur le comptage de voisins
        if 'prox_count' in info.keys():
            clause:str
            self.indiquer_case_exploree((i,j),"R")
            proximite_comptage: Dict[str,int] = {"C":info['prox_count'][2], "T":info['prox_count'][0], "S":info['prox_count'][1]}
            self.carte_connue[i][j][2] = info['prox_count'] 
            for animal in ["C", "T", "S"]:
                voisinnage = self.avoir_voisinage((i,j))
                variables_voisinnage:List[str] = [] #Voisin est la liste des variables voisines liée à cet animal
                for v in voisinnage:
                    variables_voisinnage.append(self.generer_variable_avec_position_et_type(v, animal))
              
                # partie positive
                for c in combinations(variables_voisinnage, len(variables_voisinnage)-proximite_comptage[animal]+1):
                    clause = ""
                    for var in c:
                        clause+= f"{var} "
                    if clause:
                        clause+= "0\n"
                        self.nb_clause += 1

                    contraintes += clause
             
                # partie negative
                for c in combinations(variables_voisinnage, proximite_comptage[animal]+1):
                    clause = ""
                    for var in c:
                        clause+= f"-{var} "
                    if clause:
                        clause+= "0\n"
                        self.nb_clause += 1

                    contraintes += clause           
                             
        return contraintes

    # initialisation du fichier pour le prochain test
    def initialiser_test_dans_fichier(self) -> str:
        f = open(f"./joueur/fichiers_cnf/{self.nom_fichier}", "a", newline='\n')
        f.write('c test ici')
        self.nb_clause += 1
        f.close()

        if not self.parallele:
            self.mettre_a_jour_entete()

        self.taille_derniere_ligne = len("c test ici")
        return self.nom_fichier

    # modification de la derniere ligne pour la remplacer avec le test demande
    def ajouter_test_dans_fichier(self, contrainte:str, position: Coord) -> str:  
        f = open(f"./joueur/fichiers_cnf/{self.nom_fichier}", "rb+") # ouverture en "read and write (bytes)"
        f.seek(-self.taille_derniere_ligne, os.SEEK_END) # positionnement curseur a la ligne "* test ici"
        
        nouvelle_ligne = f"{self.avoir_ligne_test(contrainte, position)}0\n"
        
        self.taille_derniere_ligne = len(nouvelle_ligne) # sauvegarde position debut de la nouvelle ligne
        f.write(str.encode(nouvelle_ligne))
        f.truncate()
        f.close() 
        return self.nom_fichier

    # sauvegarde de l'hypothese qui a ete testee et validee (on supprime la négation et on ajoute la positive)
    def conserver_test_dans_fichier(self, contrainte:str, position: Coord) -> str:
        f = open(f"./joueur/fichiers_cnf/{self.nom_fichier}", "a") # ouverture en "read"
                
        #remplacement de la négation par la positive et ajout des clauses pour indiquer l'animal 
        if contrainte != "R":
            f.write(f"{self.generer_variable_avec_position_et_type(position, contrainte)} 0\n")
            self.nb_clause += 1
        else:
            f.write(f"-{self.generer_variable_avec_position_et_type(position, 'T')} 0\n")
            f.write(f"-{self.generer_variable_avec_position_et_type(position, 'S')} 0\n")
            f.write(f"-{self.generer_variable_avec_position_et_type(position, 'C')} 0\n")
            self.nb_clause += 3

        # ajout des autres contraintes qui en découlent (si on valide Requin on peut aussi ajouter les faits -Tigre, -Croco pour aller plus vite)
        contraintes_non_possibles: List[str] = ["T","S","C","R"]
        contraintes_non_possibles.remove(contrainte)
        for c in contraintes_non_possibles:
            if c != "R":
                f.write(f"-{self.generer_variable_avec_position_et_type(position, c)} 0\n")
                self.nb_clause += 1
            else:
                #ici c'est pas utile d'ajouter Tigre ou Requin ou Croco si on a déjà ajouté Tigre
                pass
            
        f.close()

        if not self.parallele:
            self.mettre_a_jour_entete()

        return self.nom_fichier

    # suppression de la derniere ligne de test
    def supprimer_dernier_test_dans_fichier(self) -> str:
        f = open(f"./joueur/fichiers_cnf/{self.nom_fichier}", "rb+") # ouverture en "read and write (bytes)"
        f.seek(-self.taille_derniere_ligne, os.SEEK_END) 
        f.truncate()
        f.close() 

        self.nb_clause -= 1

        self.mettre_a_jour_entete()
        return self.nom_fichier

    # retourne la clause correspondant au test que l'on veut effectuer
    def avoir_ligne_test(self, contrainte: str, position: Coord ) -> str:
        nouvelle_ligne: str = ""
        if contrainte != "R":
            nouvelle_ligne = f"-{self.generer_variable_avec_position_et_type(position, contrainte)} 0"
        else:
            nouvelle_ligne += f"{self.generer_variable_avec_position_et_type(position, 'T')} "
            nouvelle_ligne += f"{self.generer_variable_avec_position_et_type(position, 'S')} "
            nouvelle_ligne += f"{self.generer_variable_avec_position_et_type(position, 'C')} 0"
        return nouvelle_ligne

    # verification si le probleme est satisfiable
    def verifier_sat_fichier(self, chemin_solver: str, clause_sup = "") -> bool:
        # /!\ WINDOWS, REMETTRE LIGNE EN DESSOUS
        # output = os.popen(f"{chemin_solver} ./joueur/fichiers_cnf/{self.nom_fichier} | grep \"s [A-Z]\"").read()
        # return output[2] == "S" #pour verifier si output == "s SATISFIABLE"
        
        if clause_sup != "":
            output = os.popen(f"{chemin_solver} ./joueur/fichiers_cnf/{self.nom_fichier} {self.nb_clause} \"{clause_sup}\"").read()
        else:
            output = os.popen(f"{chemin_solver} ./joueur/fichiers_cnf/{self.nom_fichier}").read()

        return output == "1" #pour verifier si output == "s SATISFIABLE"