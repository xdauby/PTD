import sys
import os
sys.path.append(os.getcwd())

from Transformation.AgregationSpatiale.agregationspatiale import AgregationSpatiale
from Stat.statistiques import Statistiques
from Transformation.Selection.selectionligne import selectionLigne
import numpy as np
from Donnee.donnee import Donnee



class AgregationNational(AgregationSpatiale):
    """
    Agrège des données afin qu'il n'y ait qu'une observation pour chaque Date

    Attributes
    ----------
    var_date : list(str)
        nom de la variable de date
    """

    def __init__(self,var_date):
        """
        Constructeur

        Parameters
        ----------
        var_date : list(str)
            nom de la variable de date

        Examples
        -----
        >>> agreg=AgregationNational(['date'])
        >>> print(agreg.var_date)
        ['date']
        """
        if len(var_date) != 1:
            raise Exception("La variable doit etre dans une liste")
        self.var_date = np.array(var_date)

    def appliquer(self, donnee):
        """
        Applique l'agrégation par région et date sur des données
        Pour les variables quantitatives aggégées, prend la moyenne
        Pour les variables qualitatives aggégées, prend la première valeur

        Parameters
        ----------
        donnee : Donnee
            Les données que l'on cherche à aggréger

        Raises
        ------
        Exception
            vérifie que l'attribut var_date appartient à l'attribut variable de donnee
        Exception
            Vérifie que l'attribut typage de donnee est bien renseigné

        Examples
        -----
        >>> agreg=AgregationNational(['date'])
        >>> donnee = Donnee(np.array(['date','region','valeur']),np.array([[1,'HdF',0],[1,'Brt',10],[2,'Hdf',20],[1,'Brt',200],[2,'Brt',100],[1,'Brt',2]]),np.array(['car','car','float']))
        >>> agreg.appliquer(donnee)
        >>> print(donnee)
        [['date' 'region' 'valeur']
         ['1' 'HdF' '53.0']
         ['2' 'Hdf' '60.0']]

        """

        check = all(item in  donnee.recuperervariable() for item in self.var_date)
        if not check:
            raise Exception('La variable est mal saisie.')

        typage = donnee.recuperertypage()
        if len(typage) != len(donnee.recuperervariable()):
            raise Exception("Le typage doit etre correctement renseigne pour ce type d'operation")

        donnees_final = donnee.recuperervaleurs()
        date_indice =  donnee.indicescolonnes(self.var_date)
        date = np.unique(donnees_final[:,date_indice], axis = 0)

        temp = np.empty((0,len(donnees_final[0,:])))

        for date_courante in date:
            
            lignes = selectionLigne.indiceslignesgardees(donnee, self.var_date , np.array([date_courante[0]]))
            maths = Statistiques(donnees_final[lignes,:], typage)
            temp = np.row_stack((temp, maths.moyenne()))
        
        donnee.supprimerlignes()
        donnee.ajouterlignes(temp)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
