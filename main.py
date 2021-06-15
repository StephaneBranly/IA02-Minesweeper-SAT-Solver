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
#      Update: 2021/06/15 13:07:24 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

import sys, getopt, os
from test.generer_cartes import generer_cartes
from test.test import test
from types_perso.types_perso import *

def aide():
    print(f"{couleurs.ENTETE}aide() ; arguments :{couleurs.FIN}")
    print(f" {couleurs.ATTENTION}-h{couleurs.FIN} \t\t: aide()")
    print(f" {couleurs.ATTENTION}-o nomOS{couleurs.FIN} \t: precision OS (windows,linux,macos)")
    print(f" {couleurs.ATTENTION}-s typeSolver{couleurs.FIN} \t: precision Solver (opb,cnf)")
    print(f" {couleurs.ATTENTION}-t typeTest{couleurs.FIN} \t: effectuer les tests (local,serveur)")
    print(f"\n{couleurs.OKVERT}ex: python3 main.py -o macos -s opb -t local")
    print(f"ex: python3 main.py -o windows -s opb -t local{couleurs.FIN}")
    print(f"\n\n{couleurs.OKVERT}Si test sur serveur, lancer le serveur dans un autre terminal\nfichier_serveur localhost:8000 ../../../test/grids{couleurs.FIN}")
    
def main(argv):
    lancer_test: bool = False
    nom_os: str = ""
    chemin_solver: str = ""
    chemin_serveur: str = ""
    type_solver: str = ""
    type_test: str = ""
    try:
        opts, args = getopt.getopt(argv,"ht:o:s:g:",["Type=","OS=","Solver=","NombreCartes="])
    except getopt.GetoptError:
        aide()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            aide()
            sys.exit()
        elif opt == '-t':
            lancer_test=True
            type_test = arg
        elif opt in ("-o","--OS"):
            nom_os = arg
        elif opt in ("-s","--Solver"):
            type_solver = arg
        elif opt in ("-g","--NombreCartes"):
            generer_cartes(int(arg))

    if(nom_os=='linux'):
        chemin_serveur = "/test/serveur/linux64/crocomine-lite-alpha"
        if type_solver=="opb":
            chemin_solver = "/solvers/toysat/linux64/toysat"
        elif type_solver=="cnf":
            chemin_solver = "/solvers/gophersat/linux64/gophersat-1.1.6"
    elif(nom_os=='windows'):
        chemin_serveur = "/test/serveur/win64/crocomine-lite-alpha.exe"
        if type_solver=="opb":
            chemin_solver = "/solvers/toysat/win64/toysat.exe"
        elif type_solver=="cnf":
            chemin_solver = "/solvers/gophersat/win64/gophersat-1.1.6.exe"
    elif(nom_os=='macos'):
        chemin_serveur = "/test/serveur/macos64/crocomine-lite-alpha"
        if type_solver=="opb":
            chemin_solver = "/solvers/toysat/macos64/toysat"
        elif type_solver=="cnf":
            chemin_solver = "/solvers/gophersat/macos64/gophersat-1.1.6"
    if lancer_test:
        test(os.getcwd()+chemin_solver, type_solver, type_test, os.getcwd()+chemin_serveur)
        sys.exit(0)
    aide()
    sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])