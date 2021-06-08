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
#      Update: 2021/06/07 20:31:19 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

import os.path
from joueur.joueur import jouer
from typing import List
import time
import random
from moteur.moteur import *
from types_perso.types_perso import *


def output():
    return random.randint(0, 1)
    
def extraire_fichiers_map_test() -> List[str]: 
    liste_fichiers: List[str] = [ f for f in os.listdir('./test/test_maps/') if os.path.isfile(os.path.join('./test/test_maps/',f)) ]
    liste_fichiers = sorted(liste_fichiers)
    return liste_fichiers

def test(chemin_solver: str, type_solver:str="opb"):
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
        status: Status = jouer(info_carte_courante, fichier.split(".")[0], chemin_solver) 
        temps_ecoule: str = format(time.time() - temps_depart, '.3f') + "s"
        sauvegarder_historique('./test/historique_maps/'+fichier.split(".")[0]+'.txt')
        if status == "GG":
            compteur_ok += 1
            print(f"{couleurs.FIN}Test sur {fichier}\t{couleurs.OKVERT}OK {couleurs.FIN}\t{couleurs.GRAS}[{temps_ecoule}]{couleurs.FIN}")
        else:
            print(f"{couleurs.FIN}Test sur {fichier}\t{couleurs.KO}KO {couleurs.FIN}\t{couleurs.GRAS}[{temps_ecoule}]{couleurs.FIN}")
        
    print(f"{couleurs.ENTETE}Tests finis{couleurs.FIN}\t\t{couleurs.GRAS}{compteur_ok}/{len(liste_fichiers)} OK{couleurs.FIN}")
    
