import sys
import os
sys.path.append(os.getcwd())
from Donnee.donnee import Donnee
from Transformation.Fenetrage.fenetrage import Fenetrage
from Transformation.ValeurManquantes.valeurmanquante import ValeurManquante
import numpy as np

class Pipeline:
    """
    Pipeline. Regroupe un ensemble de transformations dans un ordre précis qui peuvent
    être appliquer en une fois à une table de données

    Attribut
    -----
    donnees : Donnee
        Table de données que l'on veut modifier
    transformation : list(Transformation)
        L'ensemble des transformations que l'on veut appliquer

    """

    def __init__(self, donnees, transformation):
        """
        Constructeur

        Parameters
        ----------
        donnees : Donnee
            Table de données que l'on veut modifier
        transformation : list(Transformation)
            L'ensemble des transformations que l'on veut appliquer
        """

        self.donnees = donnees
        self.transformation = transformation 
        

    def pipeliner(self):
        """
        Applique le pipeline

        Examples
        -----
        >>> data = Donnee(np.array(['date','age']),np.array([['nan',1],['2014-01-01T21:00:00+01:00',2],['2015-01-01T21:00:00+01:00',3]]))
        >>> pipl = Pipeline(data, [ValeurManquante(), Fenetrage(['date'],'2013-01-01T21:00:00+01:00','2014-05-01T21:00:00+01:00')])
        >>> pipl.pipeliner()
        >>> print(data)
        [['date' 'age']
         ['2014-01-01T21:00:00+01:00' '2']]
        """
        
        for trans in self.transformation:
            trans.appliquer(self.donnees)


if __name__ == '__main__':
    import doctest
    doctest.testmod()  
