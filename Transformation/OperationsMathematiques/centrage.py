import sys
import os
sys.path.append(os.getcwd())


from Transformation.OperationsMathematiques.operationsmathematiques import OperationMathematiques
from Stat.statistiques import Statistiques
import numpy as np
from Donnee.donnee import Donnee

class Centrage(OperationMathematiques):
    """
    Centre les variables numériques d'une table de données
    N'a pas de paramètres
    """

    def appliquer(self, donnee):
        """
        Applique le centrage

        Parameters
        ----------
        donnee : Donnee
            Table de données que l'on veut centrer. Est modifiée par la méthode
            Les typages doivent être spécifiés

        Examples
        -----
        >>> centr = Centrage()
        >>> data = Donnee(np.array(['id','valeur']),np.array([['01',0],['25',10]]),np.array(['car','float']))
        >>> centr.appliquer(data)
        >>> print(data)
        [['id' 'valeur']
         ['01' '-5.0']
         ['25' '5.0']]
        """
        
        vals = donnee.recuperervaleurs()
        typage = donnee.recuperertypage()

        stat = Statistiques(vals, typage)
        moyenne = stat.moyenne()
        float_indices = np.where(typage == 'float')[0]

        for cols in float_indices:
            for rows in range(len(vals[:,0])): 
                if not vals[rows, cols] == 'nan':
                    vals[rows, cols] = str(float(vals[rows, cols]) - float(moyenne[cols]))

        donnee.supprimerlignes()
        donnee.ajouterlignes(vals)

    
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()

    
        


