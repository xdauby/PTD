import sys
import os
sys.path.append(os.getcwd())

from Transformation.transformation import Transformation
import numpy as np

class ValeurManquante(Transformation):

    def appliquer(self, donnee):

        lignes_suppr = []
        vals = donnee.recuperervaleurs()

        for rows in vals:
            lignes_suppr.append(np.any(rows == 'nan'))
        donnee.supprimerlignes(np.array(lignes_suppr))



        