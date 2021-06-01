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
#      Update: 2021/06/01 16:16:24 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
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
    print(f"{couleurs.ENTETE}Running tests{couleurs.FIN}")
    for fichier in extraire_fichiers_map_test():
        temps_depart: float = time.time()
        print(f"{couleurs.ATTENTION}Test map {fichier}\t...{couleurs.FIN}", end='\r')
        time.sleep(1)
        temps_ecoule: str = format(time.time() - temps_depart, '.3f') + "s"
        if output():
            print(f"{couleurs.FIN}Test map {fichier}\t{couleurs.OKVERT}OK {couleurs.FIN}\t{couleurs.GRAS}[{temps_ecoule}]{couleurs.FIN}")
        else:
            print(f"{couleurs.FIN}Test map {fichier}\t{couleurs.KO}KO {couleurs.FIN}\t{couleurs.GRAS}[{temps_ecoule}]{couleurs.FIN}")
