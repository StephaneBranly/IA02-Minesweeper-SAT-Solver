# ************************************************************************************************************************* #
#   UTC Header                                                                                                              #
#                                                         ::::::::::::::::::::       :::    ::: :::::::::::  ::::::::       #
#      generer_cartes.py                                  ::::::::::::::::::::       :+:    :+:     :+:     :+:    :+:      #
#                                                         ::::::::::::::+++#####+++  +:+    +:+     +:+     +:+             #
#      By: branlyst & duranmar <->                        ::+++##############+++     +:+    +:+     +:+     +:+             #
#      https://gitlab.utc.fr/branlyst/ia02-projet     +++##############+++::::       +#+    +:+     +#+     +#+             #
#                                                       +++##+++::::::::::::::       +#+    +:+     +#+     +#+             #
#                                                         ::::::::::::::::::::       +#+    +#+     +#+     +#+             #
#                                                         ::::::::::::::::::::       #+#    #+#     #+#     #+#    #+#      #
#      Update: 2021/06/24 23:00:47 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

import random
from typing import List
from datetime import datetime



def generer_cartes(nombre_cartes: int) -> List[str]:
    noms_cartes: List[str] = []
    for n in range(nombre_cartes):
        nom_carte = f"{n}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.croco"
        noms_cartes.append(generer_carte(nom_carte))
    return noms_cartes

def generer_carte(nom_carte: str) -> str:
    # DEBUT PARAMETRES
    n = random.randint(5,15)
    m = random.randint(5,15)
    pourcentage_animaux: int = random.randint(0,30)
    pourcentage_eau: int = random.randint(0,50)
    # FIN PARAMETRES


    carte: List[List[str]] = []

    for i in range(m):
        ligne: List[str] = []
        for j in range(n):
            if random.randint(0,100) < pourcentage_eau:
                type_terrain = "~"
            else:
                type_terrain = "-"
            ligne.append(type_terrain)
        carte.append(ligne)

   
    
    x_depart: int = random.randint(0,m-1)
    y_depart: int = random.randint(0,n-1)
    
    nombre_animaux:int = int(n*m*pourcentage_animaux/100) - 9
    if nombre_animaux < 1: 
        nombre_animaux = 0
    for a in range(nombre_animaux):
        x_pos_animal: int = x_depart
        y_pos_animal: int = y_depart
        while x_pos_animal >= x_depart-1 and x_pos_animal <= x_depart+1 and y_pos_animal >= y_depart-1 and y_pos_animal <= y_depart+1 or not (carte[x_pos_animal][y_pos_animal] == "~" or carte[x_pos_animal][y_pos_animal] == "-"):
            x_pos_animal = random.randint(0,m-1)
            y_pos_animal = random.randint(0,n-1)
        if not random.randint(0,2):
            if carte[x_pos_animal][y_pos_animal] == "~":
                carte[x_pos_animal][y_pos_animal] = "W"
            else:
                carte[x_pos_animal][y_pos_animal] = "C"
        else:
            if carte[x_pos_animal][y_pos_animal] == "~":
                carte[x_pos_animal][y_pos_animal] = "S"
            else:
                carte[x_pos_animal][y_pos_animal] = "T"
    pourcentage_animaux = int(nombre_animaux/(n*m)*100)
    f = open(f"./grilles/croco/gen/t_{n*m}_p_{pourcentage_animaux}_r_{nom_carte}", "w", newline='\n')
    f.write(f"{nom_carte}| %animaux ~= {pourcentage_animaux}, | %eau ~= {pourcentage_eau}\n")
    f.write(f"{m} {n}\n")
    f.write(f"{x_depart} {y_depart}\n")
    for l in carte:
        ligne_fichier = ""
        for case in l:
            ligne_fichier += f"{case} "
        f.write(f"{ligne_fichier}\n")
    f.close()
    return nom_carte
