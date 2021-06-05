# ************************************************************************************************************************* #
#   UTC Header                                                                                                              #
#                                                         ::::::::::::::::::::       :::    ::: :::::::::::  ::::::::       #
#      types_perso.py                                     ::::::::::::::::::::       :+:    :+:     :+:     :+:    :+:      #
#                                                         ::::::::::::::+++#####+++  +:+    +:+     +:+     +:+             #
#      By: branlyst & duranmar <->                        ::+++##############+++     +:+    +:+     +:+     +:+             #
#      https://gitlab.utc.fr/branlyst/ia02-projet     +++##############+++::::       +#+    +:+     +#+     +#+             #
#                                                       +++##+++::::::::::::::       +#+    +:+     +#+     +#+             #
#                                                         ::::::::::::::::::::       +#+    +#+     +#+     +#+             #
#                                                         ::::::::::::::::::::       #+#    #+#     #+#     #+#    #+#      #
#      Update: 2021/06/05 17:16:40 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

from typing import Dict, List, Tuple

Case = Dict
# type_case: "terre" | "mer"
# animal: None | "C" | "R" | "T"
# visite: boolean
# voisins: (nb_croco: int, nb_requins: int, nb_tigres: int)

Compte_Proximite = Tuple[int, int, int]
Coord = Tuple[int,int]
Info = Dict
# {
#     "pos": Coord, # (i, j) i < M, j < N 
#     "field": str, # "sea"|"land"
#     "prox_count": Compte_Proximite # (tiger_count, shark_count, croco_count), optional
# }

Infos = List[Info]

GridInfo = Dict
# {
#     "m": int,
#     "n": int,
#     "start": (int, int),
#     "tiger_count": int,
#     "shark_count": int,
#     "croco_count": int,
#     "sea_count": int,
#     "land_count": int,
#     "3BV": int,
#     "infos": Infos # Optional  
# }

Status = str # "OK"|"KO"|"Err"|"GG"
Msg = str

Grid = List[List[Case]]