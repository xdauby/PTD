import sys
import os
sys.path.append(os.getcwd())

from Transformation.Selection.selection import Selection
import numpy as np
from Donnee.donnee import Donnee

class SelectionColonne(Selection):
    """
    Sélectionne des colones d'une table de données et supprime les autres

    Attributes
    ----------
    vars_selec : list(str)
        nom des variables (colones) que l'on veut conserver
    """

    def __init__(self, vars_selec):
        """
        Constructeur

        Parameters
        ----------
        vars_selec : list(str)
            nom des variables (colones) que l'on veut conserver

        Examples
        -----
        >>> selec = SelectionColonne(['taille'])
        >>> print(selec.vars_selec)
        ['taille']
        """
        
        if type(vars_selec) != list:
            raise Exception(f"{vars_selec} n'est pas une liste.")
        else:
            self.vars_selec = np.array(vars_selec)  
        
    def appliquer(self, donnees):
        """
        Applique la sélection sur une table de données

        Parameters
        ----------
        donnees : Donnee
            table que l'on veut modifier

        Examples
        -----
        >>> selec = SelectionColonne(['taille'])
        >>> data = Donnee(np.array(['taille','poids']), np.array([[1,10],[12,20],[15,10],[11,12]]))
        >>> selec.appliquer(data)
        >>> print(data)
        [['taille']
         ['1']
         ['12']
         ['15']
         ['11']]
        """

        if not np.size(self.vars_selec):
            raise Exception('La liste des variables selectionnees est vide.')
        
        check = all(item in donnees.recuperervariable() for item in self.vars_selec)
        if not check:
            raise Exception('Au moins une des variables est mal saisie.')

        vars_suppr = np.delete(donnees.recuperervariable() , donnees.indicescolonnes(self.vars_selec) , 0)
        donnees.supprimercolonnes(vars_suppr)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
