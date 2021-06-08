# ************************************************************************************************************************* #
#   UTC Header                                                                                                              #
#                                                         ::::::::::::::::::::       :::    ::: :::::::::::  ::::::::       #
#      moteur.py                                          ::::::::::::::::::::       :+:    :+:     :+:     :+:    :+:      #
#                                                         ::::::::::::::+++#####+++  +:+    +:+     +:+     +:+             #
#      By: branlyst & duranmar <->                        ::+++##############+++     +:+    +:+     +:+     +:+             #
#      https://gitlab.utc.fr/branlyst/ia02-projet     +++##############+++::::       +#+    +:+     +#+     +#+             #
#                                                       +++##+++::::::::::::::       +#+    +:+     +#+     +#+             #
#                                                         ::::::::::::::::::::       +#+    +#+     +#+     +#+             #
#                                                         ::::::::::::::::::::       #+#    #+#     #+#     #+#    #+#      #
#      Update: 2021/06/06 17:37:00 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

from types_perso.types_perso import *
from typing import Dict, List

carte_courante: Grid = []
info_carte_courante: GridInfo= {}
historique: List[str] = []

def changer_carte_courante_moteur(cc: Grid):
    global carte_courante
    carte_courante = cc

def changer_info_carte_courante_moteur(icc: GridInfo):
    global info_carte_courante
    info_carte_courante = icc
    
def sauvegarder_historique(nom_fichier: str) -> bool:
    global historique
    try:
        compteur: int  = 0
        f = open(nom_fichier, "w")
        for action in historique:
            f.write(f"#{compteur}\t{action}\n")
            compteur += 1
        f.close()
        historique = []
        return True
    except:
        return False

def lecteur_de_map(chemin_fichier: str) -> Tuple[GridInfo,Grid]:
    try:
        with open(chemin_fichier) as fichier:
            info_carte: Dict = dict()
            carte: Grid = list(list(dict()))
            
            numero_ligne: int = -1

            for ligne in fichier:
                ligne_actuelle: List[Case] = list()
                ligne = ligne.replace('\n','')
                ligne_separee: List[str] = ligne.split(',')
                if(numero_ligne == -1):
                    info_carte['start'] = (int(ligne_separee[0]),int(ligne_separee[1]))
                    info_carte['3BV'] = int(ligne_separee[2])
                    info_carte['tiger_count'] = 0
                    info_carte['shark_count'] = 0
                    info_carte['croco_count'] = 0
                    info_carte['sea_count'] = 0
                    info_carte['land_count'] = 0
                    info_carte['cases_jouees'] = 0
                else:
                    numero_colonne: int = 0
                    for colonne in ligne_separee:
                        case_actuelle: Case = dict() 
                        case_actuelle['field'] = colonne[0]
                        case_actuelle['animal'] = None
                        case_actuelle['jouee'] = False
                        if colonne[0] == "s":
                            info_carte['sea_count'] += 1
                        else:
                            info_carte['land_count'] += 1

                        if len(colonne) == 2:
                            case_actuelle['animal'] = colonne[1]

                            if colonne[1] == "C":
                                info_carte['croco_count'] += 1

                            elif colonne[1] == "S":
                                info_carte['shark_count'] += 1
                                
                            elif colonne[1] == "T":
                                info_carte['tiger_count'] += 1
                        ligne_actuelle.append(case_actuelle)
                        numero_colonne += 1
                    carte.append(ligne_actuelle)
                numero_ligne += 1
            info_carte['m'] = numero_ligne
            info_carte['n'] = numero_colonne
            return info_carte, carte
    except ():
        raise

def verifier_position_correcte(position: Coord) -> bool:
    global carte_courante, info_carte_courante
    return not (position[0]<0 or position[0]>= info_carte_courante['m'] 
    or position[1]<0 or position[1]>= info_carte_courante['n'])

# Si la case est un (0,0,0) (c.-à-d. pas de tigre, pas de requin et pas de crocodile),
# toutes les cases vides sont récursivement découverte et leur type donné. 
# Dans tous les cas, le type de terrain de la case découverte est donné.
def discover(i: int, j:int) -> Tuple[Status, Msg, Infos]:
    global carte_courante, info_carte_courante
    historique.append(f"discover({i},{j})")
    if(carte_courante[i][j]['animal']!=None):
        return "KO", "", []
    else:
        infos: Infos = list(dict())
        info_case_actuelle: Dict = generer_information((i,j))
        infos.append(info_case_actuelle)
        vecteur: List[Coord] = [(-1,-1),(-1,0),(-1,1),
                (0,-1),(0,1),
                (1,-1),(1,0),(1,1)]
        for vec in vecteur:
            if(verifier_position_correcte((i+vec[0],j+vec[1]))):
                info_case_voisine: Dict = dict()
                info_case_voisine['pos'] = (i+vec[0],j+vec[1])
                info_case_voisine = ajouter_terrain_dans_info((i+vec[0],j+vec[1]), info_case_voisine)
                infos.append(info_case_voisine)
    return jouer_case((i,j)), "Nice", infos

# animal est à choisir parmi "T", "S", "C" pour respectivement tigre, requin et crocodile.
# Si le guess est faux, la grille est perdue. 
# Sinon, le type de terrain de la case (i,j) est toujours donné.
def guess(i: int, j:int, animal: str) -> Tuple[Status, Msg, Infos]:
    global carte_courante, info_carte_courante, historique
    historique.append(f"guess({i},{j},'{animal}')")
    if(carte_courante[i][j]['animal']!=animal):
        return "KO", "", []

    else:   
        info: Dict = dict()   
        info['pos'] = (i,j) 
        return jouer_case((i,j)), "Nice", [ajouter_terrain_dans_info((i,j), info)]

def jouer_case(position: Coord) -> Status:
    global carte_courante, info_carte_courante
    # Si la case n'a pas encore ete jouee, on la comptabilise
    if carte_courante[position[0]][position[1]]['jouee'] == False:
        carte_courante[position[0]][position[1]]['jouee'] = True
        info_carte_courante['cases_jouees'] += 1

    # Si toutes les cases ont ete jouees, on retourne GG (map finie), sinon on retourne OK
    if info_carte_courante['cases_jouees'] == info_carte_courante['m'] * info_carte_courante['n']:
        return "GG"
    return "OK"

# indique le type de terrain de la position
def ajouter_terrain_dans_info(position: Coord, info):
    global carte_courante, info_carte_courante
    if carte_courante[position[0]][position[1]]['field'] == "l":
        info['field'] = "land"
    else:
        info['field'] = "sea"
    return info
    
def generer_information(position: Coord) -> Info:
    global carte_courante, info_carte_courante
    info: Info = dict()
    info['pos'] = position
    info = ajouter_terrain_dans_info(position, info)
    info['prox_count'] = compter_animaux_proximite(position)
    return info

def verifier_animal_sur_case(position: Coord) -> Compte_Proximite:
    global carte_courante, info_carte_courante
    if(not(verifier_position_correcte(position))):
        return (0,0,0)
    else:
        case: Case = carte_courante[position[0]][position[1]]        
        if case['animal'] == "C":
            return (0,0,1)
        elif case['animal'] == "S":
            return (0,1,0)
        elif case['animal'] == "T":
            return (1,0,0)
    return (0,0,0)
    
def compter_animaux_proximite(position: Coord) -> Compte_Proximite:
    global carte_courante, info_carte_courante
    vecteur: List[Coord] = [(-1,-1),(-1,0),(-1,1),
                (0,-1),(0,1),
                (1,-1),(1,0),(1,1)]

    compteur: Compte_Proximite = (0,0,0)
    for vec in vecteur:
        animaux_case_voisine: Compte_Proximite = verifier_animal_sur_case((position[0]+vec[0], position[1]+vec[1]))
        compteur = (compteur[0]+animaux_case_voisine[0],
                    compteur[1]+animaux_case_voisine[1],
                    compteur[2]+animaux_case_voisine[2],
                    )
       
    return compteur
    