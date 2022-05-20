import sys
import os
sys.path.append(os.getcwd())

import numpy as np
from Transformation.transformation import Transformation
from Donnee.donnee import Donnee


class Fenetrage(Transformation):
    
    def __init__(self, var_date, date_d, date_f):
        
        if type(date_d) != str or type(date_f) != str:
            raise Exception('Les dates de debut et de fin doivent etre des str.')
        if type(var_date)!= list:
            raise Exception('La variable de date doit etre stockee dans une liste')
        if date_f < date_d:
            raise Exception('Les dates ne sont pas dans le bon ordre.')
       
        self.var_date = np.array(var_date)
        self.date_d = date_d
        self.date_f = date_f

    def appliquer(self,donnees):
        
        check = all(item in donnees.recuperervariable() for item in self.var_date)
        if not check:
            raise Exception("La variable de date est mal saisie.")
        
        indice_date = donnees.indicescolonnes(self.var_date)
        vals = donnees.recuperervaleurs()     
        date_suppr = np.where((vals[:,indice_date] < self.date_d) | (vals[:,indice_date] > self.date_f))[0]

        if len(date_suppr) == len(vals):
            donnees.supprimerlignes()
            return

        if np.size(date_suppr):
            donnees.supprimerlignes(date_suppr)
        
        
