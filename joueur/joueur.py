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
#      Update: 2021/06/24 22:32:03 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

from typing import Callable
from joueur.dimacs import Dimacs
from joueur.solver_template import Solver_template
from joueur.pseudo_boolean import Pseudo_boolean
from types_perso.types_perso import *


def jouer(info_carte_courante: GridInfo, nom_carte: str, chemin_solver:str, type_solver: str, guess:Callable, discover:Callable, chord:Callable) -> Tuple[Status, Msg, float]:   
    surete: float = 1
    solver: Solver_template
    if type_solver == "opb":
        solver = Pseudo_boolean()
    elif type_solver == "cnf":
        solver = Dimacs()
    else:
        raise BaseException("Solver incorrect")
        
    solver.initialiser_fichier_debut(info_carte_courante, nom_carte)
    i_resultat: int
    j_resultat: int
    hyp_resultat: str
    st: str = "OK"
    infos: Infos = []
    cases_a_tester: List[Tuple[int,int]] = [(info_carte_courante['start'][0],info_carte_courante['start'][1])]
    cases_testees_avec_rien: List[Tuple[int,int]] = []
    case_actuelle: Coord
    bordure: List[Coord] = [(info_carte_courante['start'][0],info_carte_courante['start'][1])]
    while st == "OK": # Boucle de jeu sur la partie
        action = None
        liste_actions = []

        # analyse des cases a tester (pour lesquelles on a eu de nouvelles informations)
        solver.initialiser_test_dans_fichier()
        
        while cases_a_tester: # on teste les bordures // cases ou l'on a recu les dernieres informations
            case_actuelle = cases_a_tester.pop(0)
            if not solver.verifier_si_case_exploree(case_actuelle):
                action = solver.hypothese_sur_case(case_actuelle,chemin_solver,"R") # on teste uniquement la non presence d'animaux
                if action: # sauvegarde de la position si bonne action
                    i_resultat = case_actuelle[0]
                    j_resultat = case_actuelle[1]
                    hyp_resultat = "R"
                    liste_actions.append([action,(i_resultat,j_resultat),hyp_resultat])
                    break
            if action: # cassage de boucle si une action est trouvee
                break
            else: # sinon, on indique que la case devra etre testee avec des animaux
                if case_actuelle in cases_testees_avec_rien:
                    cases_testees_avec_rien.remove(case_actuelle)
                cases_testees_avec_rien.insert(0,case_actuelle)

        if not action: # si on n'a pas trouvee d'action disccover, on teste les animaux
            for case_actuelle in cases_testees_avec_rien: # on enregistre les guess pour toutes les cases ou l'on est certain
                for hyp in ['T','S','C']: # pour toutes les hypotheses possibles
                    action = None
                    if not solver.verifier_si_case_exploree(case_actuelle):
                        action = solver.hypothese_sur_case(case_actuelle,chemin_solver,hyp)
                        if action: # sauvegarde de la position si bonne action
                            i_resultat = case_actuelle[0]
                            j_resultat = case_actuelle[1]
                            hyp_resultat = hyp
                            liste_actions.append([action,(i_resultat,j_resultat),hyp_resultat])
                            cases_testees_avec_rien.remove(case_actuelle) # la case selectionnee ne sera plus a tester
                            break

        solver.supprimer_dernier_test_dans_fichier()
        
        if not liste_actions: # si on n'a pas trouve d'action a faire sur la bordure, on fait une action probabiliste
            action, surete_action = solver.choisir_mouvement_aleatoire(bordure)
            liste_actions.append(action)
            surete *= surete_action   
        
        if liste_actions: # pour la liste des actions
            for act in liste_actions:
                action = act[0]
                i_resultat = act[1][0]
                j_resultat = act[1][1]
                hyp_resultat = act[2]
                if not solver.verifier_si_case_exploree((i_resultat,j_resultat)):
                    while (i_resultat,j_resultat) in bordure:
                        bordure.remove((i_resultat,j_resultat))
                    if action == "g":
                        st, msg, infos = guess(i_resultat, j_resultat, hyp_resultat)
                        solver.incrementer_comptage_animal(hyp_resultat) # on indique qu'on a trouve un nouvel animal hyp_resultat
                    elif action == "d":
                        st, msg, infos = discover(i_resultat, j_resultat)
                    solver.conserver_test_dans_fichier(hyp_resultat, (i_resultat,j_resultat)) # on conserve le test fait / on ajoute les informations relatives a ce test
                    solver.indiquer_case_exploree((i_resultat,j_resultat),hyp_resultat) # on indique que la case est maintenant visitee
                    solver.ajouter_informations_dans_fichier(infos) # on ajoute les informations obtenues a l'issu de l'action
                    for info in infos:
                        if not solver.verifier_si_case_exploree(info['pos']):
                            # si case deja a tester, on la remonte en debut de liste
                            while (info['pos'][0],info['pos'][1]) in cases_a_tester:
                                cases_a_tester.remove((info['pos'][0],info['pos'][1]))
                            while (info['pos'][0],info['pos'][1]) in bordure:
                                bordure.remove((info['pos'][0],info['pos'][1]))
                                
                            cases_a_tester.insert(0,(info['pos'][0],info['pos'][1])) # on indique les nouvelles positions a analyser
                            bordure.insert(0,(info['pos'][0],info['pos'][1])) # on indique les nouvelles positions a analyser

                        for v in solver.avoir_voisinage(info['pos']):
                            if not solver.verifier_si_case_exploree(v):
                                while (v[0],v[1]) in cases_a_tester:
                                    cases_a_tester.remove((v[0],v[1]))
                                while (v[0],v[1]) in bordure:
                                    bordure.remove((v[0],v[1]))
                                    
                                cases_a_tester.insert(0,(v[0],v[1])) # on indique les nouvelles positions a analyser
                                bordure.insert(0,(v[0],v[1])) # on indique les nouvelles positions a analyser

        else:
            print(f"{couleurs.KO}/!\ Pas de mouvement trouve{couleurs.FIN}")
            return "KO", msg, surete
        if st == "KO" or st == "GG":
            return st, msg, surete
    return "KO", msg, surete
