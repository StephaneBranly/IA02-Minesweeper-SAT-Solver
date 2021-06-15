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
#      Update: 2021/06/15 17:30:59 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

from joueur.solver_template import solver_template
import os
from types_perso.types_perso import *
from typing import List
from itertools import combinations
from shutil import copy, copyfile

#pour une case les variables sont: [sea land croco tigre requin découverte]


class dimacs(solver_template): 
    def __init__(self):
        self.nb_clause:int = 0
        self.nb_var:int = 0
        super().__init__()
    
    def mettre_a_jour_nombre_clauses(self)->str:
        f = open(f"./joueur/fichiers_cnf/{self.nom_fichier}", "r") # ouverture en "read"
        lignes:List[str] = f.readlines() #sauvegarde du contenu du fichier
        f.close()

        lignes[0]=f"p cnf {self.nb_var} {self.nb_clause}\n" #modification de la ligne avec le nouveau nombre de clause

        #écriture dans le fichier des lignes déjà présente et de nos nouvelles clauses
        f = open(f"./joueur/fichiers_cnf/{self.nom_fichier}", "w", newline='\n')
        f.writelines(lignes)
        f.close()
        return self.nom_fichier

    # initialisation du fichier .cnf
    def initialiser_fichier_debut(self,infos_grille: GridInfo, nom_carte: str = "") -> str:
        if nom_carte:
            self.nom_fichier: str = f"{nom_carte}.cnf"
        else:
            self.nom_fichier: str = f"f.cnf"
        self.n: int = infos_grille["n"]
        self.m: int = infos_grille["m"]  
        self.nb_var=self.m*self.n*6  

        flatList = []
        #initialisation de la carte a vide
        self.carte_connue = []
        for i in range(self.m):
            rang = []
            for j in range(self.n):
                rang.append([0,0])
                flatList.append([i,j])
            self.carte_connue.append(rang)


        # ajout des clauses de comptage
        # texte+=(self.generer_clause_nb_type(infos_grille["tiger_count"],"T",flatList))
        # texte+=(self.generer_clause_nb_type(infos_grille["shark_count"],"S",flatList))
        # texte+=(self.generer_clause_nb_type(infos_grille["croco_count"],"C",flatList))
        # texte+=(self.generer_clause_nb_type(infos_grille["sea_count"],"s",flatList))
        # texte+=(self.generer_clause_nb_type(infos_grille["land_count"],"l",flatList))

        # initilisation des comptages
        self.comptage_animaux_carte_total = [infos_grille["tiger_count"],infos_grille["shark_count"],infos_grille["croco_count"]]
        self.comptage_animaux_carte_actuel = [0,0,0]

        if not os.path.isfile(f"./joueur/templates_cnf/carte_{self.n}x{self.m}.cnf"):
            self.generer_template_carte(self.n, self.m)
        copyfile(f"./joueur/templates_cnf/carte_{self.n}x{self.m}.cnf", f"./joueur/fichiers_cnf/{self.nom_fichier}")
        self.nb_clause = self.n * self.m *(3+2+4)
        f = open(f"./joueur/fichiers_cnf/{self.nom_fichier}", "a", newline='\n') # ouverture en "append", ajout en fin de fichier
        # ajout de l'information sur la case de debut
        f.write(self.generer_information_depart(infos_grille['start']))
        
        
        # TODO, voir pour ajouter informations obtenues au debut de la map
               
        f.close()
        return self.nom_fichier

    def generer_template_carte(self, n: int, m: int) -> str:
        nom_template: str = f"carte_{n}x{m}.cnf"
        f = open(f"./joueur/templates_cnf/{nom_template}", "w", newline='\n') # ouverture en "write", ecrase l'ancien si existant
        texte: str = ''
        # ajout des clauses pour chaque case (animal, terrain, animal -> terrain)
        for i in range(m):
            for j in range(n):
                texte+=(self.generer_contrainte_unicite_animal((i,j)))
                texte+=(self.generer_contrainte_unicite_terrain((i,j)))
                texte+=(self.generer_implication_animal_terrain((i,j)))
        f.write(f"p cnf {self.nb_var} {self.nb_clause}\n")
        f.write(texte)

        f.close()
        return nom_template


    # ajout de chaque informatiom dans le fichier
    def ajouter_informations_dans_fichier(self, infos: Infos) -> str:
        texte:str = ""
        for info in infos: #génération des clauses
            texte += (self.generer_contraintes_information(info))

        f = open(f"./joueur/fichiers_cnf/{self.nom_fichier}", "a")
        f.write(texte)
        f.close()
        self.mettre_a_jour_nombre_clauses()

        return self.nom_fichier

    # generateur clause de comptage
    #TODO    
    def generer_clause_nb_type(self,nb_animal: int, type_var: str, flatList) -> str:
        contraintes = ""
        for c in combinations(flatList, self.m*self.n-nb_animal+1):
            clause:str = ""
            for var in c:
                clause+= f"{self.generer_variable_avec_position_et_type(var,type_var)} "
            if clause:
                clause+= "0\n"
                self.nb_clause += 1

            contraintes += clause
        
        for c in combinations(flatList, nb_animal+1):
            clause:str = ""
            for var in c:
                clause+= f"-{self.generer_variable_avec_position_et_type(var,type_var)} "
            if clause:
                clause+= "0\n"
                self.nb_clause += 1

            contraintes += clause        
        return contraintes

    def au_plus_un(self, vars:List[int]) -> str:
        sortie:str = ""
        for e in combinations(vars, 2):
            sortie+= f"-{e[0]} -{e[1]} 0\n"
            self.nb_clause += 1

        return sortie

    #[sea land croco tigre requin découverte]
    def generer_variable_avec_position_et_type(self,position: Coord, type_var: str) -> int:
        decalage: int = 0
        if type_var == "mer" or type_var=="s":
            decalage = 0
        elif type_var == "terre" or type_var=="l":
            decalage = 1
        elif type_var == "C":
            decalage = 2
        elif type_var == "T":
            decalage = 3
        elif type_var == "R" or type_var=="S":
            decalage = 4
        elif type_var == "D":
            decalage = 5
        indice_variable: int = (position[0] + position[1] * self.m) * 6 + 1 + decalage # positionnement grille * nombre de vars + decalage initiale + decalage selon type var
        return indice_variable

    def generer_variables_avec_position(self,position: Coord) -> List[int]:
        sortie: List[int] = []
        for decalage in range(6):
            sortie.append((position[0] + position[1] * self.m) * 6 + 1 + decalage) # positionnement grille * nombre de vars + decalage initiale + decalage selon type var
        return sortie #[sea land croco tigre requin découverte]

    # les differents generateurs de clauses essentielles
    def generer_contrainte_unicite_animal(self,position: Coord) -> str:
        var_ij:List[int] = self.generer_variables_avec_position(position) #recupere toute les variables liées à la case position
        var:list[int] = [var_ij[2], var_ij[3], var_ij[4]] #recupère juste les variables liées aux animaux présents sur position
        bc:str = str(self.au_plus_un(var))
        return bc

    def generer_contrainte_unicite_terrain(self,position: Coord) -> str:
        var_ij:List[int] = self.generer_variables_avec_position(position) #recupere toute les variables liées à la case (i,j)
        var:list[int] = [var_ij[0], var_ij[1]] #recupère juste les variables liées aux terrin présents sur (i,j)
        bc:str = f"-{var[0]} -{var[1]} 0\n{var[0]} {var[1]} 0\n"
        self.nb_clause += 2
        return bc

    def generer_implication_animal_terrain(self,position: Coord) -> str:
        bc:str = ""
        vars:List[int] = self.generer_variables_avec_position(position) #recupere toute les variables liées à la case (i,j)                
        clause:str= f"-{vars[1]} -{vars[4]} 0\n-{vars[0]} -{vars[3]} 0\n-{vars[4]} {vars[0]} 0\n-{vars[3]} {vars[1]} 0\n"
        self.nb_clause += 4
        bc+=clause
        return bc

    #génère l'info comme quoi la case de départ est vide de tout animal
    def generer_information_depart(self,position: Coord) -> str:
        clause:str = ""
        for i in range(3):
            clause+= f"-{self.generer_variables_avec_position(position)[i+2]} 0\n"
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
                contraintes += f"{self.generer_variable_avec_position_et_type(pos,'s')} 0\n"
                contraintes += f"-{self.generer_variable_avec_position_et_type(pos,'l')} 0\n"
            else:
                contraintes += f"-{self.generer_variable_avec_position_et_type(pos,'s')} 0\n"
                contraintes += f"{self.generer_variable_avec_position_et_type(pos,'l')} 0\n"
            self.carte_connue[i][j][1] = info['field']
            self.nb_clause += 2


        # information sur le comptage de voisins
        if 'prox_count' in info.keys():
            self.indiquer_case_exploree((i,j),"R")
            proximite_comptage: Compte_Proximite = {"C":info['prox_count'][2], "T":info['prox_count'][0], "R":info['prox_count'][1]}
            for animal in ["C", "T", "R"]:
                Voisin:List[int] = [] #Voisin est la liste des variables voisines liée à cet animal
                for cpt1 in [-1, 0, 1]:
                    for cpt2 in [-1, 0, 1]:
                        if (cpt1==0) and (cpt2==0):
                            pass #c'est la case elle même, ce n'est pas un voisin
                        elif self.verifier_position_correcte((i+cpt1, j+cpt2)):
                            #si le voisin est valide alors on ajoute la variable à la liste
                            Voisin.append(self.generer_variable_avec_position_et_type((i+cpt1, j+cpt2), animal))

                for c in combinations(Voisin, len(Voisin)-proximite_comptage[animal]+1):
                    clause:str = ""
                    for var in c:
                        clause+= f"{var} "
                    if clause:
                        clause+= "0\n"
                        self.nb_clause += 1

                    contraintes += clause
             
                for c in combinations(Voisin, proximite_comptage[animal]+1):
                    clause:str = ""
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
        self.mettre_a_jour_nombre_clauses()

        self.taille_derniere_ligne = len("c test ici")
        return self.nom_fichier

    # modification de la derniere ligne pour la remplacer avec le test demande
    def ajouter_test_dans_fichier(self, contrainte:str, position: Coord) -> str:  
        f = open(f"./joueur/fichiers_cnf/{self.nom_fichier}", "rb+") # ouverture en "read and write (bytes)"
        f.seek(-self.taille_derniere_ligne, os.SEEK_END) # positionnement curseur a la ligne "* test ici"
        
        nouvelle_ligne: str = ""
        if contrainte != "R":
            nouvelle_ligne = f"-{self.generer_variable_avec_position_et_type(position, contrainte)} 0\n"
        else:
            nouvelle_ligne += f"{self.generer_variable_avec_position_et_type(position, 'T')} "
            nouvelle_ligne += f"{self.generer_variable_avec_position_et_type(position, 'S')} "
            nouvelle_ligne += f"{self.generer_variable_avec_position_et_type(position, 'C')} 0\n"
        
        self.taille_derniere_ligne = len(nouvelle_ligne) # sauvegarde position debut de la nouvelle ligne
        f.write(str.encode(nouvelle_ligne))
        f.truncate()
        f.close() 
        return self.nom_fichier

    # sauvegarde de l'hypothese qui a ete testee et validee (on supprime la négation et on ajoute la positive)
    def conserver_test_dans_fichier(self, contrainte:str, position: Coord) -> str:
        f = open(f"./joueur/fichiers_cnf/{self.nom_fichier}", "a") # ouverture en "read"
        #remplacement de la négation par la positive
        if contrainte != "R":
            f.write(f"{self.generer_variable_avec_position_et_type(position, contrainte)} 0\n")
            self.nb_clause += 1
        else:
            f.write(f"-{self.generer_variable_avec_position_et_type(position, 'T')} 0\n")
            f.write(f"-{self.generer_variable_avec_position_et_type(position, 'S')} 0\n")
            f.write(f"-{self.generer_variable_avec_position_et_type(position, 'C')} 0\n")
            self.nb_clause += 3

        #ajout des autres contrainte qui en découle (si on valide Requin on peux aussi ajouter les faits -Tigre pour aller plus vite)
        contraintes_non_possibles: List[str] = ["T","S","C","R"]
        contraintes_non_possibles.remove(contrainte)
        for c in contraintes_non_possibles:
            if c != "R":
                f.write(str(-self.generer_variable_avec_position_et_type(position, c))+" 0\n")
                self.nb_clause += 1
            else:
                #ici c'est pas utile d'ajouter Tigre ou Requin ou Croco si on as déjà ajouté Tigre
                pass
            
        f.close()
        self.mettre_a_jour_nombre_clauses()

        return self.nom_fichier

    # suppression de la derniere ligne de test
    def supprimer_dernier_test_dans_fichier(self) -> str:
        f = open(f"./joueur/fichiers_cnf/{self.nom_fichier}", "rb+") # ouverture en "read and write (bytes)"
        f.seek(-self.taille_derniere_ligne, os.SEEK_END) 
        f.truncate()
        f.close() 

        self.nb_clause -= 1
        self.mettre_a_jour_nombre_clauses()
        return self.nom_fichier

    # verification si le probleme est satisfiable
    def verifier_sat_fichier(self, chemin_solver: str) -> bool:
        output = os.popen(f"{chemin_solver} ./joueur/fichiers_cnf/{self.nom_fichier}").read()
        return "s SATISFIABLE" in output 
