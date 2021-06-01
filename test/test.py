# ************************************************************************************************************************* #
#   UTC Header                                                                                                              #
#                                                         ::::::::::::::::::::       :::    ::: :::::::::::  ::::::::       #
#      test.py                                            ::::::::::::::::::::       :+:    :+:     :+:     :+:    :+:      #
#                                                         ::::::::::::::+++#####+++  +:+    +:+     +:+     +:+             #
#      By: branlyst & duranmar <->                        ::+++##############+++     +:+    +:+     +:+     +:+             #
#      https://gitlab.utc.fr/branlyst/ia02-projet     +++##############+++::::       +#+    +:+     +#+     +#+             #
#                                                       +++##+++::::::::::::::       +#+    +:+     +#+     +#+             #
#                                                         ::::::::::::::::::::       +#+    +#+     +#+     +#+             #
#                                                         ::::::::::::::::::::       #+#    #+#     #+#     #+#    #+#      #
#      Update: 2021/06/01 17:29:43 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

import os.path
from typing import List
import time
import random

class couleurs:
    ENTETE = '\033[95m'
    OKBLEU = '\033[94m'
    OKCYAN = '\033[96m'
    OKVERT = '\033[92m'
    ATTENTION = '\033[93m'
    KO = '\033[91m'
    FIN = '\033[0m'
    GRAS = '\033[1m'
    SOUSLIGNE = '\033[4m'

def output():
    return random.randint(0, 1)
    
def extraire_fichiers_map_test() -> List[str]: 
    liste_fichiers: List[str] = [ f for f in os.listdir('./test/test_maps/') if os.path.isfile(os.path.join('./test/test_maps/',f)) ]
    return liste_fichiers

def test():
    print(f"{couleurs.ENTETE}Tests en cours{couleurs.FIN}")
    compteur_ok: int = 0
    liste_fichiers: List[str] = extraire_fichiers_map_test()
    for fichier in liste_fichiers:
        temps_depart: float = time.time()
        print(f"{couleurs.ATTENTION}Test map {fichier}\t...{couleurs.FIN}", end='\r')
        time.sleep(1)
        temps_ecoule: str = format(time.time() - temps_depart, '.3f') + "s"
        if output():
            compteur_ok += 1
            print(f"{couleurs.FIN}Test map {fichier}\t{couleurs.OKVERT}OK {couleurs.FIN}\t{couleurs.GRAS}[{temps_ecoule}]{couleurs.FIN}")
        else:
            print(f"{couleurs.FIN}Test map {fichier}\t{couleurs.KO}KO {couleurs.FIN}\t{couleurs.GRAS}[{temps_ecoule}]{couleurs.FIN}")
        
    print(f"{couleurs.ENTETE}Tests finis{couleurs.FIN}\t\t{couleurs.GRAS}{compteur_ok}/{len(liste_fichiers)} OK{couleurs.FIN}")
    
