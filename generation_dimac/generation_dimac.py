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
#from types_perso.types_perso import *
import os.path
import time
import random
from itertools import combinations

#temporaire : c'est pour le test du fichier seul
Case = Dict
# type_case: "terre" | "mer"
# animal: None | "C" | "R" | "T"
# visite: boolean
# voisins: (nb_croco: int, nb_requins: int, nb_tigres: int)

Compte_Proximite = Tuple[int, int, int]
Coord = Tuple[int,int]
Info = Dict
# {
#     "pos": Coord, # (i, j) i < M, j < N 
#     "field": str, # "sea"|"land"
#     "prox_count": Compte_Proximite # (tiger_count, shark_count, croco_count), optional
# }

Infos = List[Info]

GridInfo = Dict
# {
#     "m": int,
#     "n": int,
#     "start": (int, int),
#     "tiger_count": int,
#     "shark_count": int,
#     "croco_count": int,
#     "sea_count": int,
#     "land_count": int,
#     "3BV": int,
#     "infos": Infos # Optional  
# }

Status = str # "OK"|"KO"|"Err"|"GG"
Msg = str

Grid = List[List[Case]]
#fin du temporaire

#alisas de type
Map = List[List[Case]]
Clause = List[int]
Clause_Base = List[Clause]
MapComplete = (GridInfo,Map)


def au_plus_un(vars: List[int]) -> Clause_Base: #entrée = [1, 2, 3]
    sortie: Clause_Base = [] 
    for e in combinations(vars, 2): 
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

#génère les contrainte pour les infos initiales
#les autres information seront ajouter après
def contrainte_info_connu(carte_connu:GridInfo) -> Clause_Base:
    bc:Clause_Base=[]
    m:int = carte_connu['m']
    n:int = carte_connu['n']
    for case_ij in carte_connu['infos']:
        i:int = case_ij['pos'][0]
        j:int = case_ij['pos'][1]
        vars:List[int] = cell_to_variables(i, j, m, n)
        if case_ij["field"]=="terre":
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

def contrainte_voisin(carte_connu:GridInfo) -> Clause_Base:
    bc:Clause_Base = []
    m:int = carte_connu['m']
    n:int = carte_connu['n']
    #to do
    return bc

def generate_problem(carte_connu:GridInfo) -> Clause_Base:
    m:int = carte_connu['m']
    n:int = carte_connu['n']
    base: Clause_Base = []
    base = (
        base
        + contrainte_animal_case(m, n)
        + contrainte_animal_terrin(m, n)
        + contrainte_info_connu(carte_connu)
        + contrainte_voisin(carte_connu)
    )
    return base

#met la base de clause sous forme de texte et l'écrit dans le dimac
def write_dimac(clauses: Clause_Base, nb_vars: int) -> str:
    with open('./generation_dimac/dimac.cnf', 'w', newline='\n') as f:
        texte:str= "c\nc IA02 projet demineur ameliorer\nc\n"
        texte+='p cnf '+str(nb_vars)+' '+str(len(clauses))+'\n'
        for c in clauses:
            for var in c:
                texte += str(var) + " "
            texte += "0\n"
        f.write(texte)


def ajout_clause(clauses: Clause_Base) -> str:
    #to do
    return " "



#cette fonction permet de tester. elle n'a pas pour vocation à rester
#temporaire
def test():
    #définition des info de la carte
    m:int = 3
    n:int = 3
    start:Tuple(int) = (0, 0)
    tc:int = 0
    sc:int = 0
    cc:int = 0
    seaC:int = 7
    landC:int = 2

    #generation de la carte vide de la bonne taille
    #represente le début
    carte: GridInfo=dict()
    carte['m']=m
    carte['n']=n
    carte['start']=start
    carte['3BV']=0
    carte['tiger_count']=tc
    carte['shark_count']=sc
    carte['croco_count']=cc
    carte['sea_count']=seaC
    carte['land_count']=landC
    carte['infos']=[]
    #ajout des infos de la case initiale
    case_initiale:Infos ={
        "pos":start, 
        "field":"sea", 
        "prox_count":(0, 0, 1),
        "animal":None
    }
    carte["infos"].append(case_initiale)

    #génération initale du problème
    nb_vars=n*m*6
    base: Clause_Base = generate_problem(carte)
    write_dimac(base, nb_vars)

    #ajout d'info (suite à un guess ou un discover)

def cell_to_variables1(i:int, j:int, m:int, n:int)->List[int]:
    depart:int=i*6* n + j*6 + 1
    result:List[int]=[]
    for i in range(6):
        result.append(depart)
        depart+=1
    return result

def cell_to_variables(i:int, j:int, m:int, n:int)->List[int]:
    depart:int=1+(i+j*m)*6
    result:List[int]=[]
    for i in range(6):
        result.append(depart)
        depart+=1
    return result

#temporaire
#test()

#print(cell_to_variables(4, 0, 8, 2))
#print(cell_to_variables(3, 8, 8, 2))

for i in range(8):
    for j in range(3):
        print("i="+str(i)+" j="+str(j))
        print(cell_to_variables(i,j, 8, 3))
