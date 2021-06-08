# ************************************************************************************************************************* #
#   UTC Header                                                                                                              #
#                                                         ::::::::::::::::::::       :::    ::: :::::::::::  ::::::::       #
#      main.py                                            ::::::::::::::::::::       :+:    :+:     :+:     :+:    :+:      #
#                                                         ::::::::::::::+++#####+++  +:+    +:+     +:+     +:+             #
#      By: branlyst & duranmar <->                        ::+++##############+++     +:+    +:+     +:+     +:+             #
#      https://gitlab.utc.fr/branlyst/ia02-projet     +++##############+++::::       +#+    +:+     +#+     +#+             #
#                                                       +++##+++::::::::::::::       +#+    +:+     +#+     +#+             #
#                                                         ::::::::::::::::::::       +#+    +#+     +#+     +#+             #
#                                                         ::::::::::::::::::::       #+#    #+#     #+#     #+#    #+#      #
#      Update: 2021/06/07 18:14:12 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

import sys, getopt
from test.test import test
from types_perso.types_perso import *

def aide():
    print(f"{couleurs.ENTETE}help() ; arguments :{couleurs.FIN}")
    print(f" {couleurs.ATTENTION}-h{couleurs.FIN} : aide()")
    print(f" {couleurs.ATTENTION}-o nomOS{couleurs.FIN} : precision OS (windows,linux,macos)")
    print(f" {couleurs.ATTENTION}-s typeSolver{couleurs.FIN} : precision Solver (opb,cnf)")
    print(f" {couleurs.ATTENTION}-t{couleurs.FIN} : effectuer les tests")
    print(f"\n{couleurs.OKVERT}ex: python3 main.py -o macos -s opb -t")
    print(f"ex: python3 main.py -o windows -s opb -t{couleurs.FIN}")
    
def main(argv):
    lancer_test: bool = False
    nom_os: str = ""
    chemin_solver: str = ""
    type_solver: str = ""
    try:
        opts, args = getopt.getopt(argv,"hto:s:",["OS=","Solver="])
    except getopt.GetoptError:
        aide()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            aide()
            sys.exit()
        elif opt == '-t':
            lancer_test=True
        elif opt in ("-o","--OS"):
            nom_os = arg
        elif opt in ("-s","--Solver"):
            type_solver = arg

    if(nom_os=='linux'):
        if type_solver=="opb":
            chemin_solver = "./solvers/toysat/linux64/toysat"
        elif type_solver=="cnf":
            chemin_solver = "./solvers/gophersat/linux64/gophersat-1.1.6"
    elif(nom_os=='windows'):
        if type_solver=="opb":
            #chemin_solver = ".\solvers\toysat\win64\toysat.exe"
            chemin_solver = "toysat.exe"
        elif type_solver=="cnf":
            chemin_solver = "./solvers/gophersat/win64/gophersat-1.1.6.exe"
    elif(nom_os=='macos'):
        if type_solver=="opb":
            chemin_solver = "./solvers/toysat/macos64/toysat"
        elif type_solver=="cnf":
            chemin_solver = "./solvers/gophersat/macos64/gophersat-1.1.6"
    if lancer_test:
        test(chemin_solver)
        sys.exit(0)

    aide()
    sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])