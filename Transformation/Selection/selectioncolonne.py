import sys
import os
sys.path.append(os.getcwd())

from Transformation.Selection.selection import Selection
import numpy as np

class SelectionColonne(Selection):

    def __init__(self, vars_selec):
        
        if type(vars_selec) != list:
            raise Exception(f"{vars_selec} n'est pas une liste.")
        else:
            self.vars_selec = np.array(vars_selec)  
        
    def appliquer(self, donnees):

        if not np.size(self.vars_selec):
            raise Exception('La liste des variables selectionnees est vide.')
        
        check = all(item in donnees.recuperervariable() for item in self.vars_selec)
        if not check:
            raise Exception('Au moins une des variables est mal saisie.')

        vars_suppr = np.delete(donnees.recuperervariable() , donnees.indicescolonnes(self.vars_selec) , 0)
        donnees.supprimercolonnes(vars_suppr)


    