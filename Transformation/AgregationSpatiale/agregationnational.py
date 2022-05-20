import sys
import os
sys.path.append(os.getcwd())

from Transformation.AgregationSpatiale.agregationspatiale import AgregationSpatiale
from Stat.statistiques import Statistiques
from Transformation.Selection.selectionligne import selectionLigne
import numpy as np



class AgregationNational(AgregationSpatiale):

    def __init__(self,var_date):
        
        if len(var_date) != 1:
            raise Exception("La variable doit etre dans une liste")
        self.var_date = np.array(var_date)

    def appliquer(self, donnee):

        check = all(item in  self.donnee_droite.recuperervariable() for item in self.var_date)
        if not check:
            raise Exception('La variable est mal saisie.')

        typage = donnee.recuperertypage()
        if len(typage) != len(donnee.recuperervariable()):
            raise Exception("Le typage doit etre correctement renseigne pour ce type d'operation")

        donnees_final = donnee.recuperervaleurs()
        date_indice =  donnee.indicescolonnes(self.var_date)
        date = np.unique(donnees_final[:,date_indice], axis = 0)

        temp = np.empty((0,len(donnees_final[0,:])))

        for date_courante in date:
            
            lignes = selectionLigne.indiceslignesgardees(donnee, self.var_date , np.array([date_courante[0]]))
            maths = Statistiques(donnees_final[lignes,:], typage)
            temp = np.row_stack((temp, maths.moyenne()))
        
        donnee.supprimerlignes()
        donnee.ajouterlignes(temp)


