import sys
import os
sys.path.append(os.getcwd())

from datetime import datetime
from Transformation.Selection.selectioncolonne import SelectionColonne
from Transformation.transformation import Transformation
import numpy as np


class ConvertisseurDate(Transformation):

    def __init__(self, var_date):
        
        self.var_date = np.array(var_date)

    @staticmethod
    def conversion_date_iso(date, strdate="%Y%m%d%H%M%S"):
        datetime_format = datetime.strptime(date, strdate)
        return datetime_format.isoformat() + "+01:00"

    def appliquer(self, donnees):

        check = all(item in donnees.recuperervariable() for item in self.var_date)
        if not check:
            raise Exception('La variable de date est mal saisie.')

        indice_date = donnees.indicescolonnes(self.var_date)
        vfunc = np.vectorize(self.conversion_date_iso)
        
        vals = donnees.recuperervaleurs()
        vals[:,indice_date] = vfunc(vals[:,indice_date])
        donnees.supprimercolonnes(self.var_date)

        donnees.ajoutercolonnes(np.array([np.append(self.var_date, vals[:, indice_date])]).T, np.array(['car']))

    








            


