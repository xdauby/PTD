import sys
import os
sys.path.append(os.getcwd())


from Transformation.OperationsMathematiques.operationsmathematiques import OperationMathematiques
from Stat.statistiques import Statistiques
import numpy as np

class Centrage(OperationMathematiques):

    def appliquer(self, donnee):
        
        vals = donnee.recuperervaleurs()
        typage = donnee.recuperertypage()

        stat = Statistiques(vals, typage)
        moyenne = stat.moyenne()
        float_indices = np.where(typage == 'float')[0]

        for cols in float_indices:
            for rows in range(len(vals[:,0])): 
                if not vals[rows, cols] == 'nan':
                    vals[rows, cols] = str(float(vals[rows, cols]) - float(moyenne[cols]))

        donnee.supprimerlignes()
        donnee.ajouterlignes(vals)

    
        


