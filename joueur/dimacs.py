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
from copy import deepcopy

#pour une case les variables sont: [sea land croco tigre requin découverte]


class dimacs(solver_template): 
    def __init__(self):
        self.nb_clause:int = 0
        super().__init__()
    
    def modifier_nombre_clauses(self, nom_fichier:str, nb_nouvelle_clause:int, nb_var:int)->str:
        f = open(f"./joueur/fichiers_cnf/{nom_fichier}", "r") # ouverture en "read"
        lignes:List[str] = f.readlines() #sauvegarde du contenu du fichier
        f.close()

        self.nb_clause=self.nb_clause+nb_nouvelle_clause
        lignes[1]="p cnf "+str(nb_var)+" "+str(self.nb_clause)+"\n" #modification de la ligne avec le nouveau nombre de clause

        #écriture dans le fichier des lignes déjà présente et de nos nouvelles clauses
        f = open(f"./joueur/fichiers_cnf/{nom_fichier}", "w", newline='\n')
        f.writelines(lignes)
        f.close()
        #print(self.nb_clause, nb_nouvelle_clause)
        #wait=input("modifier nombre clauses")
        return nom_fichier

    # initialisation du fichier .cnf
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
        #texte+=(self.generer_clause_nb_type(infos_grille["tiger_count"],"T",m,n))
        #texte+=(self.generer_clause_nb_type(infos_grille["shark_count"],"S",m,n))
        #texte+=(self.generer_clause_nb_type(infos_grille["croco_count"],"C",m,n))
        #texte+=(self.generer_clause_nb_type(infos_grille["sea_count"],"s",m,n))
        #texte+=(self.generer_clause_nb_type(infos_grille["land_count"],"l",m,n))

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
        self.nb_clause:int = len(tableau_ligne)-1    #nombre de ligne dans le texte-2 (1 commentaire 1 ligne p 1 ligne finale avec juste\n)
        nb_vars:int = n*m*6
        f.write("p cnf "+str(nb_vars)+" "+str(self.nb_clause)+"\n")
        f.write(texte)
        
        f.close()
        wait=input("initialisation")
        return nom_fichier

    # ajout de chaque informatiom dans le fichier
    def ajouter_informations_dans_fichier(self,nom_fichier:str, infos: Infos, m: int, n: int) -> str:
        texte:str = ""
        for info in infos: #génération des clauses
            texte += (self.generer_contraintes_information(info,m,n))

        nb_clause_info:int = len(texte.split('\n'))    #nombre de ligne dans le texte
        f = open(f"./joueur/fichiers_cnf/{nom_fichier}", "a")
        f.write(texte)
        wait=input("ajouter info")
        f.close()
        self.modifier_nombre_clauses(nom_fichier, nb_clause_info, m*n*6)

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

    def au_plus_un(self, vars:List[int]) -> str:
        sortie:str = ""
        for e in combinations(vars, 2):
            sortie+=str(-e[0])+" "+str(-e[1])+" 0\n"
        return sortie

    #[sea land croco tigre requin découverte]
    def generer_variable_avec_position_et_type(self,position: Coord, type_var: str, m: int, n: int) -> int:
        decalage: int = 0
        if type_var == "merre" or type_var=="s":
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
        indice_variable: int = (position[0] + position[1] * m) * 6 + 1 + decalage # positionnement grille * nombre de vars + decalage initiale + decalage selon type var
        return indice_variable

    def generer_variables_avec_position(self,position: Coord, m: int, n: int) -> List[int]:
        sortie: List[int] = []
        for decalage in range(6):
            sortie.append((position[0] + position[1] * m) * 6 + 1 + decalage) # positionnement grille * nombre de vars + decalage initiale + decalage selon type var
        return sortie #[sea land croco tigre requin découverte]

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
    def generer_contraintes_information(self,info: Info, m: int, n: int) -> str:
        contraintes: str = ""
        pos: Coord = info['pos']
        i: int = pos[0]
        j: int = pos[1]

        # information sur le type de terrain
        if 'field' in info.keys() and not self.carte_connue[i][j][1]:
            if info['field'] == "sea":
                contraintes += str(self.generer_variable_avec_position_et_type(pos,'mer',m,n))+" 0\n"
                contraintes += str(-self.generer_variable_avec_position_et_type(pos,'terre',m,n))+" 0\n"
            else:
                contraintes += str(self.generer_variable_avec_position_et_type(pos,'mer',m,n))+" 0\n"
                contraintes += str(-self.generer_variable_avec_position_et_type(pos,'terre',m,n))+" 0\n"
            self.carte_connue[i][j][1] = info['field']

        # information sur le comptage de voisins
        if 'prox_count' in info.keys():
            proximite_comptage: Compte_Proximite = {"C":info['prox_count'][2], "T":info['prox_count'][0], "R":info['prox_count'][1]}
            for animal in ["C", "T", "R"]:

                Voisin:List[int] = [] #Voisin est la liste des variables voisines liée à cet animal
                for cpt1 in [-1, 0, 1]:
                    for cpt2 in [-1, 0, 1]:
                        if (cpt1==0) and (cpt2==0):
                            pass #c'est la case elle même, ce n'est pas un voisin
                        elif self.verifier_position_correcte((i+cpt1, j+cpt2), m, n):
                            #si le voisin est valide alors on ajoute la variable à la liste
                            Voisin.append(self.generer_variable_avec_position_et_type((i+cpt1, j+cpt2), animal, m, n))

                for c in combinations(Voisin, proximite_comptage[animal]+1):
                    clause:str = ""
                    for var in c:
                        clause+=str(-var)+" "
                    if clause:
                        clause+="0\n"
                    contraintes += clause

                if proximite_comptage[animal] > 0:
                    
                    for c in combinations(Voisin, proximite_comptage[animal]-1):
                        liste_var:List[int]=deepcopy(Voisin)
                        clause:str = ""
                        for var in c:
                            liste_var.remove(var)
                        for var in liste_var:
                            clause+=str(var)+" "
                        if clause:
                            clause+="0\n"
                        contraintes += clause


        return contraintes

    # initialisation du fichier pour le prochain test
    #pas nécessaire, il n'y a rien à faire ici
    def initialiser_test_dans_fichier(self,nom_fichier: str) -> str:
        return nom_fichier

    # modification de la derniere ligne pour la remplacer avec le test demande
    def ajouter_test_dans_fichier(self,nom_fichier:str, contrainte:str, position: Coord, m: int, n: int) -> str:
        self.modifier_nombre_clauses(nom_fichier, 1, m*n*6)
        f = open(f"./joueur/fichiers_cnf/{nom_fichier}", "a", newline='\n') # ouverture en "append"
        nouvelle_ligne: str = ""
        if contrainte != "R":
            nouvelle_ligne = str(-self.generer_variable_avec_position_et_type(position, contrainte, m, n))+" 0\n"
        else:
            nouvelle_ligne += str(self.generer_variable_avec_position_et_type(position, "T", m, n))+" "
            nouvelle_ligne += str(self.generer_variable_avec_position_et_type(position, "R", m, n))+" "
            nouvelle_ligne += str(self.generer_variable_avec_position_et_type(position, "C", m, n))+" 0\n"
        f.write(nouvelle_ligne)
        f.close() 
        wait=input("ajouter test dans fichier")
        return nom_fichier

    # sauvegarde de l'hypothese qui a ete testee et validee (on supprime la négation et on ajoute la positive)
    #TODO a tester
    def conserver_test_dans_fichier(self,nom_fichier:str, contrainte:str, position: Coord, m: int, n: int) -> str:
        f = open(f"./joueur/fichiers_cnf/{nom_fichier}", "r") # ouverture en "read"
        lignes:List[str] = f.readlines() #sauvegarde du contenu du fichier
        f.close()

        dernier:int = len(lignes)-1
        nb_clauses_ajoute:int = 0
        #remplacement de la négation par la positive
        if contrainte != "R":
            lignes.append(str(self.generer_variable_avec_position_et_type(position, contrainte, m, n))+" 0\n")
            nb_clauses_ajoute+=1
        else:
            lignes.append (str(-self.generer_variable_avec_position_et_type(position, "T", m, n))+" 0\n")
            lignes.append(str(-self.generer_variable_avec_position_et_type(position, "S", m, n))+" 0\n")
            lignes.append(str(-self.generer_variable_avec_position_et_type(position, "C", m, n))+" 0\n")
            nb_clauses_ajoute+=3

        #ajout des autres contrainte qui en découle (si on valide Requin on peux aussi ajouter les faits -Tigre pour aller plus vite)
        contraintes_non_possibles: List[str] = ["T","S","C","R"]
        contraintes_non_possibles.remove(contrainte)
        for c in contraintes_non_possibles:
            if contrainte != "R":
                lignes.append(str(-self.generer_variable_avec_position_et_type(position, c, m, n))+" 0\n")
                nb_clauses_ajoute+=1
            else:
                #ici c'est pas utile d'ajouter Tigre ou Requin ou Croco si on as déjà ajouté Tigre
                pass

        #écriture dans le fichier des lignes créer
        f = open(f"./joueur/fichiers_cnf/{nom_fichier}", "w", newline='\n')
        f.writelines(lignes)
        f.close()
        self.modifier_nombre_clauses(nom_fichier, nb_clauses_ajoute, m*n*6)
        wait=input("conserver test dans fichier")

        return nom_fichier

    # suppression de la derniere ligne de test
    #TODO a tester
    def supprimer_dernier_test_dans_fichier(self,nom_fichier: str) -> str:
        f = open(f"./joueur/fichiers_cnf/{nom_fichier}", "r") # ouverture en "read"
        lignes:List[str] = f.readlines() #sauvegarde du contenu du fichier
        f.close()

        nb_var:int = int(lignes[1].split(' ')[2])
        dernier:int = len(lignes)-1
        nouveau_fichier:List[str]=[]
        for l in range(dernier):
            nouveau_fichier.append(lignes[l])

        f = open(f"./joueur/fichiers_cnf/{nom_fichier}", "w", newline='\n') # ouverture en "write"
        f.writelines(nouveau_fichier) #sauvegarde du contenu du fichier
        f.close()
        self.modifier_nombre_clauses(nom_fichier, -1, nb_var)
        wait=input("supprimer dernier test dans fichier")
        return nom_fichier