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
#      Update: 2021/06/15 13:14:33 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

import random
import os
from typing import List
from datetime import datetime



def generer_cartes(nombre_cartes: int) -> List[str]:
    noms_cartes: List[str] = []
    for n in range(nombre_cartes):
        nom_carte = f"{n}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.croco"
        noms_cartes.append(generer_carte(nom_carte))
    return noms_cartes

    
def generer_carte(nom_carte: str) -> str:
    f = open(f"./test/grids/{nom_carte}", "w", newline='\n')
    n = random.randint(5,50)
    m = random.randint(5,50)
    carte: List[List[str]] = []
    for i in range(m):
        ligne: List[str] = []
        for j in range(n):
            if random.randint(0,1):
                type_terrain = "~"
            else:
                type_terrain = "-"
            ligne.append(type_terrain)
        carte.append(ligne)

   
    
    x_depart: int = random.randint(0,m-1)
    y_depart: int = random.randint(0,n-1)
    
    max:int = n*m-9 - int(n*m*0.75)
    if max < 1: 
        max = 0
    nombre_animaux: int = random.randint(0,max)
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
    f.write(f"{nom_carte}\n")
    f.write(f"{m} {n}\n")
    f.write(f"{x_depart} {y_depart}\n")
    for l in carte:
        ligne_fichier = ""
        for case in l:
            ligne_fichier += f"{case} "
        f.write(f"{ligne_fichier}\n")
    f.close()
    return nom_carte
