import sys
import os
sys.path.append(os.getcwd())

import numpy as np
from Transformation.Selection.selection import Selection
from Donnee.donnee import Donnee


class selectionLigne(Selection):
    """
    Sélectionne des lignes d'une table de données pour des valeurs de certaines colones, supprime les autres lignes
    Rmq: Pour chaque variable, ne conserve les observations que pour une seule valeur

    Attributes
    -----
    vars_selec : list(str)
        variables sur lesquelles se fait la sélection
    vals_selec : list(str)
        valeurs pour lesquelles ont garde une observation

    """

    def __init__(self, vars_selec, vals_selec):
        """
        Constructeur

        Parameters
        ----------
        vars_selec : list(str)
            variables sur lesquelles se fait la sélection
        vals_selec : list(str)
            valeurs pour lesquelles ont garde une observation
        """

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
        """
        Applique la sélection

        Parameters
        ----------
        donnees : Donnee
            Table de données que l'on veut modifier

        
        Examples
        -----
        >>> select=SelectionLigne(['region','date'], ['Brt','1'])
        >>> donnee = Donnee(np.array(['date','region','valeur']),np.array([[1,'Brt',0],[1,'Brt',10],[1,'Hdf',20],[1,'Hdf',200],[2,'Brt',100],[1,'Hdf',2]]),np.array(['car','car','float']))
        >>> select.appliquer(donnee)
        >>> print(donnee)
        [['date' 'region' 'valeur']
         ['1' 'Brt' '0']
         ['1' 'Brt' '10']]
        """

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
            

if __name__ == '__main__':
    import doctest
    doctest.testmod()
