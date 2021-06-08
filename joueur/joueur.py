# ************************************************************************************************************************* #
#   UTC Header                                                                                                              #
#                                                         ::::::::::::::::::::       :::    ::: :::::::::::  ::::::::       #
#      joueur.py                                          ::::::::::::::::::::       :+:    :+:     :+:     :+:    :+:      #
#                                                         ::::::::::::::+++#####+++  +:+    +:+     +:+     +:+             #
#      By: branlyst & duranmar <->                        ::+++##############+++     +:+    +:+     +:+     +:+             #
#      https://gitlab.utc.fr/branlyst/ia02-projet     +++##############+++::::       +#+    +:+     +#+     +#+             #
#                                                       +++##+++::::::::::::::       +#+    +:+     +#+     +#+             #
#                                                         ::::::::::::::::::::       +#+    +#+     +#+     +#+             #
#                                                         ::::::::::::::::::::       #+#    #+#     #+#     #+#    #+#      #
#      Update: 2021/06/08 19:17:21 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

from joueur.dimacs import dimacs
from joueur.solver_template import solver_template
from joueur.pseudo_boolean import pseudo_boolean
from types_perso.types_perso import *


def jouer(info_carte_courante: GridInfo, nom_carte: str, chemin_solver:str, type_solver: str, guess:object, discover:object, chord:object) -> Status:   
    m: int = info_carte_courante['m']
    n: int = info_carte_courante['n']
    solver: solver_template
    if type_solver == "opb":
        solver = pseudo_boolean()
    else:
        solver = dimacs()
        
    fichier: str = solver.initialiser_fichier_debut(info_carte_courante, nom_carte)
    
    i: int = 0
    i_resultat: int
    j_resultat: int
    hyp_resultat: str
    st: str = "OK"
    infos: Infos = []
    cases_a_tester: List[Tuple[int,int]] = [info_carte_courante['start']]
    case_actuelle: Coord
    while st == "OK":
        action = None
        # analyse des cases a tester (pour lesquelles on a eu de nouvelles informations)
        for case_actuelle in cases_a_tester: 
            if not solver.verifier_si_case_exploree(case_actuelle):
                action, hyp_resultat = solver.hypothese_sur_case(fichier,case_actuelle,m,n,chemin_solver)
                if action: # sauvegarde de la position si bonne action
                    i_resultat = case_actuelle[0]
                    j_resultat = case_actuelle[1]
                    cases_a_tester.remove(case_actuelle) # la case selectionnee ne sera plus a tester
                    break

        # si on n'a pas trouve d'action, on cherche sur toute la map une hypothese sure
        i = 0
        while i < m and not action: 
            j = 0
            while j < n and not action:
                if not solver.verifier_si_case_exploree((i,j)):
                    action, hyp_resultat = solver.hypothese_sur_case(fichier,(i,j),m,n,chemin_solver)
                    if action: # sauvegarde de la position si bonne action
                        i_resultat = i
                        j_resultat = j
                j += 1
            i += 1
            if i == m and not action:
                st == "KO"

        # TODO, faire un random pick (voir avec les probas/proportion des animaux) si aucunes hypothese n'est sure
        
        
        if action:
            if action == "g":
                st, msg, infos = guess(i_resultat, j_resultat, hyp_resultat)
                solver.incrementer_comptage_animal(hyp_resultat) # on indique qu'on a trouve un nouvel animal hyp_resultat
            elif action == "d":
                st, msg, infos = discover(i_resultat, j_resultat)
            solver.conserver_test_dans_fichier(fichier, hyp_resultat, (i_resultat,j_resultat),m,n) # on conserve le test fait / on ajoute les informations relatives a ce test
            solver.indiquer_case_exploree((i_resultat,j_resultat),hyp_resultat) # on indique que la case est maintenant visitee
            solver.ajouter_informations_dans_fichier(fichier, infos, m, n) # on ajoute les informations obtenues a l'issu de l'action
            for info in infos:
                if info['pos'] not in cases_a_tester and not solver.verifier_si_case_exploree(info['pos']):
                    cases_a_tester.insert(0,info['pos']) # on indique les nouvelles positions a analyser

        if st == "KO" or st == "GG":
            return st
    return "KO"    
