import sys
import os
sys.path.append(os.getcwd())

from Stat.statistiques import Statistiques
from Transformation.OperationsMathematiques.operationsmathematiques import OperationMathematiques

import numpy as np

class MoyenneGlissante(OperationMathematiques):

    def __init__(self, var, periode):
        
        if periode % 2 == 0:
            raise Exception('La periode doit etre impair')

        self.var = np.array(var)
        self.periode = periode
        
    def appliquer(self, donnee):
        

        indice_var = donnee.indicescolonnes(self.var)
        vals = donnee.recuperervaleurs()
        vals = vals[:,indice_var]
        
        typage = donnee.recuperertypage()[indice_var]

        if not np.all(typage == 'float'):
            raise Exception('Toutes les variables doivent etre de type float')

        for i in range(len(indice_var)):
           
            moyenne_glissante = np.full((1,len(vals[:,0])), 'nan', dtype='<U80')[0]
            for rows in range(self.periode//2, len(vals) - self.periode//2):
                stat = Statistiques(np.array([vals[rows -self.periode//2: rows +self.periode//2 +1,i]]).T, np.array([typage[i]]))
                moyenne_glissante[rows] = stat.moyenne()[0]

            nom_var_moyenne = self.var[i] + '_moyenne_glissante' 
            donnee.ajoutercolonnes(np.array([np.append(nom_var_moyenne, moyenne_glissante)]).T, typage[i])

