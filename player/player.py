# ************************************************************************************************************************* #
#   UTC Header                                                                                                              #
#                                                         ::::::::::::::::::::       :::    ::: :::::::::::  ::::::::       #
#      player.py                                          ::::::::::::::::::::       :+:    :+:     :+:     :+:    :+:      #
#                                                         ::::::::::::::+++#####+++  +:+    +:+     +:+     +:+             #
#      By: branlyst & duranmar <->                        ::+++##############+++     +:+    +:+     +:+     +:+             #
#      https://gitlab.utc.fr/branlyst/ia02-projet     +++##############+++::::       +#+    +:+     +#+     +#+             #
#                                                       +++##+++::::::::::::::       +#+    +:+     +#+     +#+             #
#                                                         ::::::::::::::::::::       +#+    +#+     +#+     +#+             #
#                                                         ::::::::::::::::::::       #+#    #+#     #+#     #+#    #+#      #
#      Update: 2021/06/05 22:01:39 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

from types_perso.types_perso import *
from moteur.moteur import *


def play() -> Status:
    status: List[Status] = list()
    actions = []
    # actions.append([guess, (0,0,"S")])
    # actions.append([guess, (0,1,"C")])
    # actions.append([discover, (0,2)])
    # actions.append([discover, (0,3)])
    # actions.append([discover, (1,0)])
    # actions.append([discover, (1,1)])
    # actions.append([guess, (1,2,"T")])
    # actions.append([discover, (1,3)])
    # actions.append([guess, (2,0,"S")])
    # actions.append([discover, (2,1)])
    # actions.append([discover, (2,2)])
    # actions.append([discover, (2,3)])
    # actions.append([guess, (3,0,"C")])
    # actions.append([discover, (3,1)])
    # actions.append([discover, (3,2)])
    # actions.append([discover, (3,3)])

    for a in actions:
        if a[0] == guess:
            st, msg, infos = a[0](a[1][0],a[1][1],a[1][2])
        else:
            st, msg, infos = a[0](a[1][0],a[1][1])
        if st == "KO" or st == "GG":
            return st
    return "KO"
