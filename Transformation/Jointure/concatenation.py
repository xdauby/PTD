import sys
import os
sys.path.append(os.getcwd())

import numpy as np
from Transformation.Jointure.jointure import Jointure
from Donnee.donnee import Donnee

class Concatenation:
    """
    Concatène deux tables de données avec les mêmes variables mais des observations différentes

    Attributes
    -----
    donnee_haut : Donnee
        La première table de données de la concaténation


    """

    def __init__(self, donnee_haut):
        """
        Constructeur

        Parameters
        ----------
        donnee_haut : Donnee
            La première table de données de la concaténation
        
        Examples
        -----
        >>> data1 = Donnee(np.array(['date','region','valeur']),np.array([[1,'Brt',0],[1,'Brt',10],[1,'Hdf',20],[1,'Hdf',200],[2,'Brt',100],[1,'Hdf',2]]))
        >>> concat = Concatenation(data1)
        >>> print(concat.donnee_haut)
        [['date' 'region' 'valeur']
         ['1' 'Brt' '0']
         ['1' 'Brt' '10']
         ['1' 'Hdf' '20']
         ['1' 'Hdf' '200']
         ['2' 'Brt' '100']
         ['1' 'Hdf' '2']]
        """
        self.donnee_haut = donnee_haut
        

    def appliquer(self, donnee):
        """
        Applique la concaténation (une table à partir de 2 ayant les mêmes variables)
        Modifie la table entrée en paramètre

        Parameters
        ----------
        donnee : Donnee
            La deuxième table de données de la concaténation
        
        Examples
        -----
        >>> data1 = Donnee(np.array(['date','region','valeur']),np.array([[1,'Brt',0],[1,'Brt',10]]))
        >>> data2 = Donnee(np.array(['date','region','valeur']),np.array([[3,'Brt',50],[3,'Hdf',10]]))
        >>> concat = Concatenation(data1)
        >>> concat.appliquer(data2)
        >>> print(data2)
        [['date' 'region' 'valeur']
         ['3' 'Brt' '50']
         ['3' 'Hdf' '10']
         ['1' 'Brt' '0']
         ['1' 'Brt' '10']]

        >>> data1 = Donnee(np.array(['date','region','valeur']),np.array([[1,'Brt',0]]))
        >>> data2 = Donnee(np.array(['region','valeur','date']),np.array([['Brt',50,3]]))
        >>> concat = Concatenation(data1)
        >>> concat.appliquer(data2)
        >>> print(data2)
        [['region' 'valeur' 'date']
         ['Brt' '50' '3']
         ['Brt' '0' '1']]
        """

        if not((donnee.recuperervariable() == self.donnee_haut.recuperervariable()).all()):
            raise Exception('Les deux tables doivent avoir les memes variables')
        donnee.ajouterlignes(self.donnee_haut.recuperervaleurs())

            


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
