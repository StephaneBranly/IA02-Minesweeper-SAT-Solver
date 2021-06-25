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
#      Update: 2021/06/24 12:13:02 by branlyst & duranma  ::::::::::::::::::::        ########      ###      ######## .fr   #
#                                                                                                                           #
# ************************************************************************************************************************* #

import sys, getopt, os, subprocess
from test.generer_cartes import generer_cartes
from test.test import test
from types_perso.types_perso import *

def aide():
    print(f"{couleurs.ENTETE}aide() ; arguments :{couleurs.FIN}")
    print(f" {couleurs.ATTENTION}-h{couleurs.FIN} \t\t: aide()")
    print(f" {couleurs.ATTENTION}-o nomOS{couleurs.FIN} \t: precision OS (windows,linux,macos)")
    print(f" {couleurs.ATTENTION}-s typeSolver{couleurs.FIN} \t: precision Solver (opb,cnf)")
    print(f" {couleurs.ATTENTION}-p{couleurs.FIN} \t\t: résolution en utilisant le joueur parallèle")
    print(f" {couleurs.ATTENTION}-t typeTest{couleurs.FIN} \t: effectuer les tests (local,serveur)")
    print(f" {couleurs.ATTENTION}-g nombreCartes{couleurs.FIN} \t: generer des cartes")
    print(f"\n{couleurs.OKVERT}ex: python3 main.py -o macos -s cnf -t serveur")
    print(f"ex: python3 main.py -o windows -s cnf -t serveur{couleurs.FIN}")
    print(f"\n\n{couleurs.OKVERT}Si test sur serveur, lancer le serveur dans un autre terminal\nfichier_serveur localhost:8000 ../../../grilles/croco/performances/{couleurs.FIN}")
    
def main(argv):
    lancer_test: bool = False
    nom_os: str = ""
    chemin_solver: str = ""
    chemin_serveur: str = ""
    type_solver: str = ""
    type_test: str = ""
    parallele: bool = False
    try:
        opts, args = getopt.getopt(argv,"hpt:o:s:g:",["Type=","OS=","Solver=","NombreCartes="])
    except getopt.GetoptError:
        aide()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            aide()
            sys.exit()
        elif opt == "-p":
            parallele = True
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
        chemin_serveur = "/moteur/serveur/linux64/crocomine-lite-beta4"
        if type_solver=="opb":
            chemin_solver = "/solvers/toysat/linux64/toysat"
        elif type_solver=="cnf":
            chemin_solver = "/solvers/gophersat/linux64/gophersat-1.1.6"
    elif(nom_os=='windows'):
        chemin_serveur = "/moteur/serveur/win64/crocomine-lite-beta4.exe"
        if type_solver=="opb":
            chemin_solver = "/solvers/toysat/win64/toysat.exe"
        elif type_solver=="cnf":
            chemin_solver = "/solvers/gophersat/win64/gophersat-1.1.6.exe"
    elif(nom_os=='macos'):
        chemin_serveur = "moteur/serveur/darwin64/crocomine-lite-beta4"
        if type_solver=="opb":
            chemin_solver = "/solvers/toysat/macos64/toysat"
        elif type_solver=="cnf":
            if parallele:
                chemin_solver = "/solvers/glucose/macos64/glucose"
            else:
                chemin_solver = "/solvers/glucose/macos64/glucose_static"

            # chemin_solver = "/solvers/gophersat/macos64/gophersat-1.1.6"
    if parallele and type_solver == "opb":
        print(f"{couleurs.ATTENTION}Le mode parallèle a été desactivé, il ne peut être appliqué que pour cnf avec le solveur Glucose personnalisé.\nVoir le ReadMe pour compiler le Glucose personalisé{couleurs.FIN}\n")
        parallele = False
        
    if lancer_test:
        test(os.getcwd()+chemin_solver, type_solver, type_test, os.getcwd()+chemin_serveur, parallele)
        sys.exit(0)
    aide()
    sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])