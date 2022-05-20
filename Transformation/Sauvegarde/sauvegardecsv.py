import sys
import os
sys.path.append(os.getcwd())

from Transformation.Sauvegarde.sauvegarde import Sauvegare
import numpy as np


class SauvegardeCSV(Sauvegare):

    def __init__(self, donnee, nom_fichier):
        
        self.sauvegarde(donnee, nom_fichier)

    def sauvegarde(self, donnee, nom_fichier):
        np.savetxt(nom_fichier, np.row_stack((donnee.variables,donnee.valeurs)), delimiter=",")
