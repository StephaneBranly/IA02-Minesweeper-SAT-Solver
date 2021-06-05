# ************************************************************************************************************************* #
#   UTC Header                                                                                                              #
#                                                         ::::::::::::::::::::       :::    ::: :::::::::::  ::::::::       #
#      generation_dimac.py                                ::::::::::::::::::::       :+:    :+:     :+:     :+:    :+:      #
#                                                         ::::::::::::::+++#####+++  +:+    +:+     +:+     +:+             #
#      By: branlyst & duranmar <->                        ::+++##############+++     +:+    +:+     +:+     +:+             #
#      https://gitlab.utc.fr/branlyst/ia02-projet     +++##############+++::::       +#+    +:+     +#+     +#+             #
#                                                       +++##+++::::::::::::::       +#+    +:+     +#+     +#+             #
#                                                         ::::::::::::::::::::       +#+    +#+     +#+     +#+             #
#                                                         ::::::::::::::::::::       #+#    #+#     #+#     #+#    #+#      #
#      Update: 2021/06/02 16:00:26 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

from typing import Dict, List, Tuple
import os.path
import time
import random
from itertools import combinations


Case = Dict
# type_case: "terre" | "mer"
# animal: None | "C" | "R" | "T"
# visite: boolean
# voisins: (nb_croco: int, nb_requins: int, nb_tigres: int)

GridInfo = Dict
Map = List[List[Case]]
Clause = List[int]
Clause_Base = List[Clause]

MapComplete = (GridInfo,Map)

def cell_to_variables(i:int, j:int, m:int, n:int)->List[int]:
    depart:int=1+(i)*6*m+(j)*6
    result:List[int]=[]
    for i in range(6):
        result.append(depart)
        depart+=1
    return result

def au_plus_un(vars: List[int]) -> Clause_Base: #entrée = [1, 2, 3]
    sortie: Clause_Base = [] 
    for e in combinations(vars, 2): #e prend à chaque itération une valeur parmi {(1, 2) (2, 3), (1, 3)}
        sortie.append([-e[0], -e[1]])
    return sortie #[[-1, -2], [-2, -3], [-1, -3]]


#genere les contrainte d'unicite de l'animal sur une case
#génère les contraintes sur les voisins de la case (x,y) pour un type d'animal
def contrainte_animal_case(m:int, n:int) -> Clause_Base:
    bc: Clause_Base=[]
    for i in range(m):
        for j in range(n):
            var_ij:List[int] = cell_to_variables(i, j, m, n) #recupere toute les variables liées à la case (i,j)
            var:list[int] = [var_ij[2], var_ij[3], var_ij[4]] #recupère juste les variables liées aux animaux présents sur (i,j)
            bc=bc+au_plus_un(var)
    return bc

#creation des contrainte liant le type de terrin et les animaux
def contrainte_animal_terrin(m:int, n:int) -> Clause_Base:
    bc: Clause_Base=[]
    for i in range(m):
        for j in range(n):
            vars:List[int] = cell_to_variables(i, j, m, n) #recupere toute les variables liées à la case (i,j)
            clause:Clause_Base=[[-vars[2], -vars[5]], [-vars[1], -vars[4]], [-vars[5], vars[1]], [-vars[4], vars[2]]]
            bc=bc+clause
    return bc

def contrainte_info_connu(carte_connu:MapComplete) -> Clause_Base:
    bc:Clause_Base=[]
    m:int = carte_connu[0]['m']
    n:int = carte_connu[0]['n']
    for i in range(m):
        for j in range(n):
            vars:List[int] = cell_to_variables(i, j, m, n)
            case_ij:Case=carte_connu[1][i][j]
            if case_ij != None:
                if case_ij["type_case"]=="terre":
                    bc+=[[vars[1]]]
                else:
                    bc+=[[vars[2]]]
                if case_ij["animal"]=="C":
                    bc+=[[vars[3]]]
                elif case_ij["animal"]=="T":
                    bc+=[[vars[4]]]
                elif case_ij["animal"]=="R":
                    bc+=[[vars[5]]]
                else:
                    bc+=[[vars[-3]], [vars[-4]], [vars[-5]]]

    return bc

def contrainte_voisin(carte_connu:MapComplete) -> Clause_Base:
    bc:Clause_Base = []
    m:int = carte_connu[0]['m']
    n:int = carte_connu[0]['n']
    #to do
    return bc

def generate_problem(carte_connu:MapComplete) -> Clause_Base:
    m:int =carte_connu[0]['m']
    n:int =carte_connu[0]['n']
    base: Clause_Base = []
    base = (
        base
        + contrainte_animal_case(m, n)
        + contrainte_animal_terrin(m, n)
        + contrainte_info_connu(carte_connu)
        + contrainte_voisin(carte_connu)
    )
    return base

def write_dimac(clauses: Clause_Base, nb_vars: int) -> str:
    with open('./generation_dimac/dimac.cnf', 'w', newline='\n') as f:
        texte:str= "c\nc IA02 projet demineur ameliorer\nc\n"
        texte+='p cnf '+str(nb_vars)+' '+str(len(clauses))+'\n'
        for c in clauses:
            for var in c:
                texte += str(var) + " "
            texte += "0\n"
        f.write(texte)

   





#cette fonction permet de tester. elle n'a pas pour vocation à rester
#temporaire
def test():
    m=3
    n=3
    #generation de la carte vide de la bonne taille
    #represente le début : on n'a pas d'info du tout
    carte=list(list(dict()))
    for i in range(m):
        ligne: List[Case]=list()
        for j in range(n):
            case: Case=None
            ligne.append(case)
        carte.append(ligne)
    print(carte)
    info: Dict=dict()
    info['m']=m
    info['n']=n
    info['start']=(0, 0)
    info['3BV']=0
    info['tiger_count']=0
    info['shark_count']=0
    info['croco_count']=1
    info['sea_count']=7
    info['land_count']=2
    #ajout des infos de la case initiale
    case_initiale:Case = {"animal":None, "type_case":"merre", "visite":True, "voisins":(1, 0, 0)}
    carte[0][0]=case_initiale
    print(carte)

    carte_info:MapComplete = (info, carte)

    nb_vars=n*m*6
    base: Clause_Base = generate_problem(carte_info)
    write_dimac(base, nb_vars)

#temporaire
test()
