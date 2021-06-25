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
#      Update: 2021/06/25 18:20:02 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

from joueur.joueur_parallele import jouer_para
from moteur.crocomine_client import CrocomineClient
import os.path
from datetime import datetime
from joueur.joueur import jouer
from typing import List
import time
import random
from moteur.moteur import *
from types_perso.types_perso import *


def output():
    return random.randint(0, 1)
    
def extraire_fichiers_map_test() -> List[str]: 
    liste_fichiers: List[str] = [ f for f in os.listdir('./grilles/map/') if os.path.isfile(os.path.join('./grilles/map/',f)) ]
    liste_fichiers = sorted(liste_fichiers)
    return liste_fichiers

def test(chemin_solver: str, type_solver:str, type_test:str, chemin_serveur:str, parallele: bool):
    global carte_courante, info_carte_courante
    
    print(f"{couleurs.ENTETE}Tests en cours{couleurs.FIN}")
    compteur_ok: int = 0
    liste_fichiers: List[str] = extraire_fichiers_map_test()

    temps_depart: float
    temps_depart_total: float = time.time()
    status: Status
    surete: float
    message_final: str
    temps_ecoule: str
    compteur: int = 0

    if type_test == "local":
        for fichier in liste_fichiers:
            compteur += 1
            info_carte_courante, carte_courante = lecteur_de_map('./grilles/map/'+fichier)
            changer_carte_courante_moteur(carte_courante)
            changer_info_carte_courante_moteur(info_carte_courante)
            temps_depart = time.time()
            print(f"{couleurs.ATTENTION}\t...\t\t\t\tTest sur {fichier}{couleurs.FIN}", end='\r')
            if parallele:
                status, message_final, surete = jouer_para(info_carte_courante, fichier.split(".")[0], chemin_solver,guess,discover,discover) 
            else:
                status, message_final, surete = jouer(info_carte_courante, fichier.split(".")[0], chemin_solver,type_solver,guess,discover,discover) 
            temps_ecoule = format(time.time() - temps_depart, '.3f') + "s"
            sauvegarder_historique('./test/historique_maps/'+fichier.split(".")[0]+'.txt')
            if status == "GG":
                compteur_ok += 1
                print(f"{couleurs.OKVERT}\tOK {couleurs.FIN}\t{couleurs.GRAS}[{temps_ecoule}]{couleurs.FIN}\ts={format(surete,'.2f')}\tTest sur {fichier}")
            else:
                print(f"{couleurs.KO}\tKO {couleurs.FIN}\t{couleurs.GRAS}[{temps_ecoule}]{couleurs.FIN}\ts={format(surete,'.2f')}\tTest sur {fichier}")
    else:
        historique_temps: List[Dict] = []
        server = "http://croco.lagrue.ninja:80"
        group = "Groupe 33"
        members = "BRANLY Stephane & DURAND Marion"
        passwd = "mondeParalleleCommeNotreAlgo"
        croco = CrocomineClient(server, group, members, passwd)
        status, Msg, info_carte_courante = croco.new_grid()
       
        while status == "OK":
            compteur += 1
            temps_depart = time.time()
            print(f"{couleurs.ATTENTION}\t...\t\t\t\tTest sur {Msg}{couleurs.FIN}", end='\r')
            if parallele:
                status, message_final, surete = jouer_para(info_carte_courante, "f", chemin_solver,croco.guess,croco.discover,croco.chord) 
            else:
                status, message_final, surete = jouer(info_carte_courante, "f", chemin_solver,type_solver,croco.guess,croco.discover,croco.chord) 
            temps_ecoule = format(time.time() - temps_depart, '.3f') + "s"
            new_data = dict()
            new_data['n'] = info_carte_courante['n']
            new_data['tmps'] = temps_ecoule
            historique_temps.append(new_data)
            if status == "GG":
                compteur_ok += 1
                print(f"{couleurs.OKVERT}\tOK {couleurs.FIN}\t{couleurs.GRAS}[{temps_ecoule}]{couleurs.FIN}\ts={format(surete,'.2f')}\tTest sur {Msg}\t")
            else:
                print(f"{couleurs.KO}\tKO {couleurs.FIN}\t{couleurs.GRAS}[{temps_ecoule}]{couleurs.FIN}\ts={format(surete,'.2f')}Test sur {Msg}")
            print(f"\t\t--> {message_final}")
            status, Msg, info_carte_courante = croco.new_grid()
        historique_temps = sorted(historique_temps, key=lambda k: k['n']) 
        print("\n")
        texte = f"{type_solver}-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        for entree in historique_temps:
            temps = entree['tmps'][:-1].replace('.',',')
            texte += f";{temps}"
        print(f"{texte}\n")
        

    print(f"{couleurs.ENTETE}Tests finis{couleurs.FIN}\t\t{couleurs.ATTENTION}{compteur_ok}/{compteur} OK{couleurs.FIN}")
    temps_ecoule_total: str = format(time.time() - temps_depart_total, '.3f') + "s"
    print(f"{couleurs.ENTETE}Temps total{couleurs.FIN}\t\t{couleurs.ATTENTION}[{temps_ecoule_total}]{couleurs.FIN}")


