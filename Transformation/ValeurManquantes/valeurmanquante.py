import sys
import os
sys.path.append(os.getcwd())

from Transformation.transformation import Transformation
import numpy as np
from Donnee.donnee import Donnee

class ValeurManquante(Transformation):
    """
    Supprime les observations contenant des valeurs manquantes
    Pas d'attibuts
    """

    def appliquer(self, donnee):
        """
        Applique la suppression des valeurs manquantes

        Parameters
        ----------
        donnee : Donnee
            Table de données que l'on veut modifier

        Examples
        -----
        >>> manq = ValeurManquante()
        >>> data = Donnee(np.array(['taille','poids']), np.array([[1,10],[12,'nan'],[15,10],['nan','nan']]))  
        >>> manq.appliquer(data)
        >>> print(data)    
        [['taille' 'poids']
         ['1' '10']
         ['15' '10']]
        """

        lignes_suppr = []
        vals = donnee.recuperervaleurs()

        for rows in vals:
            lignes_suppr.append(np.any(rows == 'nan'))
        donnee.supprimerlignes(np.array(lignes_suppr))



if __name__ == '__main__':
    import doctest
    doctest.testmod()



        
