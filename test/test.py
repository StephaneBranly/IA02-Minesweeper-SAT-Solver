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
#      Update: 2021/06/10 22:47:09 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

from moteur.crocomine_client import CrocomineClient
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

def test(chemin_solver: str, type_solver:str, type_test:str, chemin_serveur:str):
    global carte_courante, info_carte_courante
    
    print(f"{couleurs.ENTETE}Tests en cours{couleurs.FIN}")
    compteur_ok: int = 0
    liste_fichiers: List[str] = extraire_fichiers_map_test()

    if type_test == "local":
        for fichier in liste_fichiers:
            info_carte_courante, carte_courante = lecteur_de_map('./test/test_maps/'+fichier)
            changer_carte_courante_moteur(carte_courante)
            changer_info_carte_courante_moteur(info_carte_courante)
            temps_depart: float = time.time()
            print(f"{couleurs.ATTENTION}Test sur {fichier}\t...{couleurs.FIN}", end='\r')
            status: Status = jouer(info_carte_courante, fichier.split(".")[0], chemin_solver,type_solver,guess,discover,None) 
            temps_ecoule: str = format(time.time() - temps_depart, '.3f') + "s"
            sauvegarder_historique('./test/historique_maps/'+fichier.split(".")[0]+'.txt')
            if status == "GG":
                compteur_ok += 1
                print(f"{couleurs.FIN}Test sur {fichier}\t{couleurs.OKVERT}OK {couleurs.FIN}\t{couleurs.GRAS}[{temps_ecoule}]{couleurs.FIN}")
            else:
                print(f"{couleurs.FIN}Test sur {fichier}\t{couleurs.KO}KO {couleurs.FIN}\t{couleurs.GRAS}[{temps_ecoule}]{couleurs.FIN}")
            
        print(f"{couleurs.ENTETE}Tests finis{couleurs.FIN}\t\t{couleurs.GRAS}{compteur_ok}/{len(liste_fichiers)} OK{couleurs.FIN}")
    
    else:
        # os.system(f"{chemin_serveur} localhost:8000 ./test/grids/")
        server = "http://localhost:8000"
        group = "Groupe 12"
        members = "Ici."
        croco = CrocomineClient(server, group, members)
        status, Msg, info_carte_courante = croco.new_grid()
        compteur: int = 0
        while status == "OK":
            compteur += 1
            temps_depart: float = time.time()
            status: Status = jouer(info_carte_courante, None, chemin_solver,type_solver,croco.guess,croco.discover,None) 
            temps_ecoule: str = format(time.time() - temps_depart, '.3f') + "s"
            if status == "GG":
                compteur_ok += 1
                print(f"{couleurs.FIN}Test sur {Msg}\t{couleurs.OKVERT}OK {couleurs.FIN}\t{couleurs.GRAS}[{temps_ecoule}]{couleurs.FIN}")
            else:
                print(f"{couleurs.FIN}Test sur {Msg}\t{couleurs.KO}KO {couleurs.FIN}\t{couleurs.GRAS}[{temps_ecoule}]{couleurs.FIN}")
            status, Msg, info_carte_courante = croco.new_grid()
        print(f"{couleurs.ENTETE}Tests finis{couleurs.FIN}\t\t{couleurs.GRAS}{compteur_ok}/{compteur} OK{couleurs.FIN}")
        # os.system(f"{chemin_serveur} localhost:8000 ./test/grids/")
