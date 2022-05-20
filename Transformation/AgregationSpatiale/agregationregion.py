import sys
import os
sys.path.append(os.getcwd())

from Transformation.AgregationSpatiale.agregationspatiale import AgregationSpatiale
from Stat.statistiques import Statistiques
from Transformation.Selection.selectionligne import selectionLigne
import numpy as np



class AgregationRegion(AgregationSpatiale):

    def __init__(self, var_date, var_reg):

        if len(var_date) != 1 or len(var_reg) != 1:
            raise Exception("Les variables doivent etre dans deux liste separees")

        self.var_date = np.array(var_date)
        self.var_reg = np.array(var_reg)

    def appliquer(self, donnee):
        
        check1 = all(item in  donnee.recuperervariable() for item in self.var_date)
        check2 = all(item in  donnee.recuperervariable() for item in self.var_reg)
        if not (check1 and check2):
            raise Exception('Au moins une des variables est mal saisie.')
        
        typage = donnee.recuperertypage()
        if len(typage) != len(donnee.recuperervariable()):
            raise Exception("Le typage doit etre correctement renseigne pour ce type d'operation")


        donnees_final = donnee.recuperervaleurs()
        date_indice =  donnee.indicescolonnes(self.var_date)
        region_indice = donnee.indicescolonnes(self.var_reg)
        
        regions = np.unique(donnees_final[:,region_indice], axis = 0)
        date = np.unique(donnees_final[:,date_indice], axis = 0)
        temp = np.empty((0,len(donnees_final[0,:])))
      
        for date_courante in date:
            for region_courante in regions:
                
                lignes = selectionLigne.indiceslignesgardees(donnee, np.array([self.var_date,self.var_reg]) , np.array([date_courante[0],region_courante[0]]))
                maths = Statistiques(donnees_final[lignes,:], typage)
                temp = np.row_stack((temp, maths.moyenne()))

        donnee.supprimerlignes()
        donnee.ajouterlignes(temp)




            
                






        

