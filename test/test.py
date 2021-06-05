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
#      Update: 2021/06/05 22:01:49 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

import os.path
from player.player import play
from typing import List
import time
import random
from moteur.moteur import *

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
    global carte_courante, info_carte_courante
    
    print(f"{couleurs.ENTETE}Tests en cours{couleurs.FIN}")
    compteur_ok: int = 0
    liste_fichiers: List[str] = extraire_fichiers_map_test()
    for fichier in liste_fichiers:
        info_carte_courante, carte_courante = lecteur_de_map('./test/test_maps/'+fichier)
        changer_carte_courante_moteur(carte_courante)
        changer_info_carte_courante_moteur(info_carte_courante)
        temps_depart: float = time.time()
        print(f"{couleurs.ATTENTION}Test sur {fichier}\t...{couleurs.FIN}", end='\r')
        status: Status = play() 
        temps_ecoule: str = format(time.time() - temps_depart, '.3f') + "s"
        sauvegarder_historique('./test/historique_maps/'+fichier)
        if status == "GG":
            compteur_ok += 1
            print(f"{couleurs.FIN}Test sur {fichier}\t{couleurs.OKVERT}OK {couleurs.FIN}\t{couleurs.GRAS}[{temps_ecoule}]{couleurs.FIN}")
        else:
            print(f"{couleurs.FIN}Test sur {fichier}\t{couleurs.KO}KO {couleurs.FIN}\t{couleurs.GRAS}[{temps_ecoule}]{couleurs.FIN}")
        
    print(f"{couleurs.ENTETE}Tests finis{couleurs.FIN}\t\t{couleurs.GRAS}{compteur_ok}/{len(liste_fichiers)} OK{couleurs.FIN}")
    
