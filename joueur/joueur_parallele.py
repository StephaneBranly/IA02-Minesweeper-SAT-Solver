# ************************************************************************************************************************* #
#   UTC Header                                                                                                              #
#                                                         ::::::::::::::::::::       :::    ::: :::::::::::  ::::::::       #
#      joueur_parallele.py                                ::::::::::::::::::::       :+:    :+:     :+:     :+:    :+:      #
#                                                         ::::::::::::::+++#####+++  +:+    +:+     +:+     +:+             #
#      By: branlyst & duranmar <->                        ::+++##############+++     +:+    +:+     +:+     +:+             #
#      https://gitlab.utc.fr/branlyst/ia02-projet     +++##############+++::::       +#+    +:+     +#+     +#+             #
#                                                       +++##+++::::::::::::::       +#+    +:+     +#+     +#+             #
#                                                         ::::::::::::::::::::       +#+    +#+     +#+     +#+             #
#                                                         ::::::::::::::::::::       #+#    #+#     #+#     #+#    #+#      #
#      Update: 2021/06/24 22:47:52 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

import threading
from typing import Callable
from joueur.dimacs import Dimacs
from joueur.solver_template import Solver_template
from types_perso.types_perso import *
from threading import Thread

status: str = "OK"

def mettre_a_jour_status(nouveau_status: str):
    global status
    status = nouveau_status
    
def avoir_status() -> str:
    global status
    return status
    
def jouer_para(info_carte_courante: GridInfo, nom_carte: str, chemin_solver:str, guess:Callable, discover:Callable, chord:Callable) -> Tuple[Status, Msg, float]:   
    m: int = info_carte_courante['m']
    n: int = info_carte_courante['n']
    surete: float = 1
    solver: Solver_template
    solver = Dimacs(True)
    
    solver.initialiser_fichier_debut(info_carte_courante, nom_carte)
    st: str = "OK"
    cases_a_tester: List[Tuple[int,int]] = [(info_carte_courante['start'][0],info_carte_courante['start'][1])]
    case_actuelle: Coord
    actions: List = []
    bordure: List[Coord] = [(info_carte_courante['start'][0],info_carte_courante['start'][1])]
    infos: Infos = []

    while st == "OK": # Boucle de jeu sur la partie
        while cases_a_tester: # pour toute la bordure, on effectue les tests, lancés en //
            case_actuelle = cases_a_tester.pop(0)
            if not solver.verifier_si_case_exploree(case_actuelle):
                nouveau_thread = Hypothese_thread(case_actuelle,"R",solver,chemin_solver,actions)
                nouveau_thread.start()
        

        if threading.active_count() == 1 and not actions: # si on n'a plus de thread en cours et que toutes les actions ont ete jouees, on fait une action avec la proba            
            action, surete_action = solver.choisir_mouvement_aleatoire(bordure)
            actions.append(action)
            surete *= surete_action
            
        while actions and st == "OK": # tant que l'on peut effectuer des actions, on les execute
            act = actions.pop()
            action = act[0]
            i_resultat = act[1][0]
            j_resultat = act[1][1]
            hyp_resultat = act[2]
            if not solver.verifier_si_case_exploree((i_resultat,j_resultat)):
                solver.indiquer_case_exploree((i_resultat,j_resultat),hyp_resultat) # on indique que la case est maintenant visitee
                while (i_resultat,j_resultat) in bordure:
                    bordure.remove((i_resultat,j_resultat))
                if action == "g":
                    st, msg, infos = guess(i_resultat, j_resultat, hyp_resultat)
                    solver.incrementer_comptage_animal(hyp_resultat) # on indique qu'on a trouve un nouvel animal hyp_resultat
                elif action == "d":
                    st, msg, infos = discover(i_resultat, j_resultat)
                solver.conserver_test_dans_fichier(hyp_resultat, (i_resultat,j_resultat)) # on conserve le test fait / on ajoute les informations relatives a ce test
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
                            # si case deja a tester, on la remonte en debut de liste
                            while (v[0],v[1]) in cases_a_tester:
                                cases_a_tester.remove((v[0],v[1]))
                            while (v[0],v[1]) in bordure:
                                bordure.remove((v[0],v[1]))
                                
                            cases_a_tester.insert(0,(v[0],v[1])) # on indique les nouvelles positions a analyser
                            bordure.insert(0,(v[0],v[1])) # on indique les nouvelles positions a analyser


        if st == "KO" or st == "GG":
            return st, msg, surete
    return "KO", msg, surete

class Hypothese_thread(Thread):
    def __init__(self, position: Coord, hypothese: str, solver: Solver_template, chemin_solver: str, actions):
        super().__init__()
        self.position: Coord = position
        self.hypothese: str = hypothese
        self.solver: Solver_template = solver
        self.chemin_solver: str = chemin_solver
        self.actions: List = actions

    def run(self):
        action = None
        clause_sup = self.solver.avoir_ligne_test(self.hypothese, self.position)
        action = self.solver.hypothese_sur_case(self.position,self.chemin_solver,self.hypothese, clause_sup)
        if action:  # si on a trouve une action, on l'ajoute
            self.actions.append([action,self.position,self.hypothese])
        else: # sinon, on lance le prochain test sur la meme case
            if self.hypothese == "R":
                nouveau_thread = Hypothese_thread(self.position,"C",self.solver,self.chemin_solver,self.actions)
            elif self.hypothese == "C":
                nouveau_thread = Hypothese_thread(self.position,"S",self.solver,self.chemin_solver,self.actions)
            elif self.hypothese == "S":
                nouveau_thread = Hypothese_thread(self.position,"T",self.solver,self.chemin_solver,self.actions)
            else:
                return None
            nouveau_thread.start()
            
        return None