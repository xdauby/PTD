import sys
import os
sys.path.append(os.getcwd())

from Stat.statistiques import Statistiques
import numpy as np
from Transformation.OperationsMathematiques.operationsmathematiques import OperationMathematiques
from Transformation.OperationsMathematiques.centrage import Centrage


class Normalisation(OperationMathematiques):

    def appliquer(self, donnee):

        t = Centrage()
        t.appliquer(donnee)

        vals = donnee.recuperervaleurs()
        typage = donnee.recuperertypage()
        float_indices = np.where(typage == 'float')[0]


        stat = Statistiques(vals, typage)
        sigma = stat.ecarttype()

        for cols in float_indices:
                if float(sigma[cols]) != 0.0:
                    vals[:,cols] = vals[:,cols].astype(float)/sigma[cols].astype(float) 
                else:
                    vals[:,cols] = 0

        donnee.supprimerlignes()
        donnee.ajouterlignes(vals)

        
