import sys
import os
sys.path.append(os.getcwd())

from Stat.statistiques import Statistiques
import numpy as np
from Transformation.OperationsMathematiques.operationsmathematiques import OperationMathematiques
from Transformation.OperationsMathematiques.centrage import Centrage
from Donnee.donnee import Donnee


class Normalisation(OperationMathematiques):
    """
    Centre et réduit les variables quantitatives d'une table de données
    Pas d'attributs
    """

    def appliquer(self, donnee):
        """
        Applique la normalisation

        Parameters
        ----------
        donnee : Donnee
            Table de données que l'on veut modifier

        Examples
        -----
        >>> norm = Normalisation()
        >>> data = Donnee(np.array(['id','valeur']),np.array([['01',0],['25',3],['08',9],['08',12]]),np.array(['car','float']))
        >>> norm.appliquer(data)
        >>> print(data)
        [['id' 'valeur']
         ['01' '-1.2649110640673518']
         ['25' '-0.6324555320336759']
         ['08' '0.6324555320336759']
         ['08' '1.2649110640673518']]
        """

        t = Centrage()
        t.appliquer(donnee)

        vals = donnee.recuperervaleurs()
        typage = donnee.recuperertypage()
        float_indices = np.where(typage == 'float')[0]


        stat = Statistiques(vals, typage)
        sigma = stat.ecarttype()

        for cols in float_indices:
                if float(sigma[cols]) != 0.0:
                    vals[:,cols] = vals[:,cols].astype(float)/sigma[cols].astype(float) 
                else:
                    vals[:,cols] = 0

        donnee.supprimerlignes()
        donnee.ajouterlignes(vals)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
