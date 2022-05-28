import sys
import os
sys.path.append(os.getcwd())

from Stat.statistiques import Statistiques
from Transformation.OperationsMathematiques.operationsmathematiques import OperationMathematiques

import numpy as np
from Donnee.donnee import Donnee

class MoyenneGlissante(OperationMathematiques):
    """
    Sur des valeurs ordonnées d'une table de données, calcule une moyenne glissante

    Attributes
    -----
    var : list(str)
        nom des variables sur lesquelles s'appliquera la moyenne
    periode : int
        taille de l'intervalle d'observation sur lequel on applique la moyenne glissante

    """

    def __init__(self, var, periode):
        """
        Constructeur

        Parameters
        ----------
        var : list(str)
            nom des variables sur lesquelles s'appliquera la moyenne
        periode : int
            taille de l'intervalle d'observation sur lequel on applique la moyenne glissante

        Examples
        -----
        >>> mg = MoyenneGlissante('valeur',3)
        >>> print(mg.var)
        valeur
        """
        
        if periode % 2 == 0:
            raise Exception('La periode doit etre impair')

        self.var = np.array(var)
        self.periode = periode
        
    def appliquer(self, donnee):
        """
        Applique la moyenne glissante

        Parameters
        ----------
        donnee : Donnee
            Table de données sur laquelle s'applique la moyenne glissante
            Le typage doit être spécifié
            La méthode modifie ce paramètre

        Examples
        -----
        >>> data = Donnee(np.array(['date','valeur']),np.array([[2001,0],[2002,10],[2005,100],[2003,10],[1997,10]]),np.array(['date','float']))
        >>> data.trierpardate(['date'])
        >>> mg = MoyenneGlissante(['valeur'],3)
        >>> mg.appliquer(data)
        >>> print(data)
        [['date' 'valeur' 'valeur_moyenne_glissante']
         ['1997' '10' 'nan']
         ['2001' '0' '6.666666666666667']
         ['2002' '10' '6.666666666666667']
         ['2003' '10' '40.0']
         ['2005' '100' 'nan']]
        """
        

        indice_var = donnee.indicescolonnes(self.var)
        vals = donnee.recuperervaleurs()
        vals = vals[:,indice_var]
        
        typage = donnee.recuperertypage()[indice_var]

        if not np.all(typage == 'float'):
            raise Exception('Toutes les variables doivent etre de type float')

        for i in range(len(indice_var)):
           
            moyenne_glissante = np.full((1,len(vals[:,0])), 'nan', dtype='<U80')[0]
            for rows in range(self.periode//2, len(vals) - self.periode//2):
                stat = Statistiques(np.array([vals[rows -self.periode//2: rows +self.periode//2 +1,i]]).T, np.array([typage[i]]))
                moyenne_glissante[rows] = stat.moyenne()[0]

            nom_var_moyenne = self.var[i] + '_moyenne_glissante' 
            donnee.ajoutercolonnes(np.array([np.append(nom_var_moyenne, moyenne_glissante)]).T, typage[i])

if __name__ == '__main__':
    import doctest
    doctest.testmod()
