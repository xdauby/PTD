import sys
import os
sys.path.append(os.getcwd())

import numpy as np
from Transformation.Selection.selection import Selection


class selectionLigne(Selection):

    def __init__(self, vars_selec, vals_selec):

        if type(vars_selec) != list or type(vals_selec) != list:
            raise Exception(f"{vars_selec} ou {vals_selec} n'est pas une liste.")

        if len(vars_selec) != len(vals_selec):
            raise Exception("Les deux listes d'entree doivent etre de la meme taille")

        self.vars_selec = np.array(vars_selec)
        self.vals_selec = np.array(vals_selec)

    @staticmethod
    def indiceslignesgardees(donnees, variables_selection, valeurs_selection):

        check = all(item in donnees.recuperervariable() for item in variables_selection)
        if not check:
            raise Exception("Une des variables n'est pas dans la liste")

        vals = donnees.recuperervaleurs()
        indices_colonnes = donnees.indicescolonnes(variables_selection)
        lignes_gardees = np.where(np.all(vals[:,indices_colonnes] == valeurs_selection, axis = 1))[0]
        
        return lignes_gardees
    
    def appliquer(self, donnees):

        check = all(item in donnees.recuperervariable() for item in self.vars_selec)
        if not check:
            raise Exception("Une des variables n'est pas dans la liste")
            
        vals = donnees.recuperervaleurs()
        indices_colonnes = donnees.indicescolonnes(self.vars_selec)
        lignes_suppr = np.where(vals[:,indices_colonnes] != self.vals_selec)[0]
        
        if not np.size(lignes_suppr):
            return
        elif len(vals) == len(lignes_suppr):
            donnees.supprimerlignes()
        else:
            donnees.supprimerlignes(lignes_suppr)
            