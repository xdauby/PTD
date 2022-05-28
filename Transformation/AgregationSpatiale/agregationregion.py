import sys
import os
sys.path.append(os.getcwd())

from Transformation.AgregationSpatiale.agregationspatiale import AgregationSpatiale
from Stat.statistiques import Statistiques
from Transformation.Selection.selectionligne import selectionLigne
from Donnee.donnee import Donnee
import numpy as np



class AgregationRegion(AgregationSpatiale):
    """
    Agrège des données afin qu'il n'y ait qu'une observation pour chaque Région à chaque Date (peut s'appliquer pour 
    d'autres couples de variables)
    Attributes
    ----------
    var_date : list(str)
        nom de la variable de date
    var_reg : list(str)
        nom de la variable de région
    """

    def __init__(self, var_date, var_reg):
        """
        Constructeur
        Parameters
        ----------
        var_date : list(str)
            nom de la variable de date
        var_reg : list(str)
            nom de la variable de région
        Examples
        -----
        >>> agreg=AgregationRegion(['date'], ['Region'])
        >>> print(agreg.var_date)
        ['date']
        """

        if len(var_date) != 1 or len(var_reg) != 1:
            raise Exception("Les variables doivent etre dans deux liste separees")

        self.var_date = np.array(var_date)
        self.var_reg = np.array(var_reg)

    def appliquer(self, donnee):
        """
        Applique l'agrégation par région et date sur des données
        Pour les variables quantitatives agrégées, prend la moyenne
        Pour les variables qualitatives agrégées, prend la première valeur
        Parameters
        ----------
        donnee : Donnee
            Les données que l'on cherche à aggréger
        Raises
        ------
        Exception
            vérifie que les attributs var_date et var_region appartiennent à l'attribut variable de donnee
        Exception
            Vérifie que l'attribut typage de donnee est bien renseigné
        Examples
        -----
        >>> agreg=AgregationRegion(['date'], ['region'])
        >>> donnee = Donnee(np.array(['date','region','valeur']),np.array([[1,'Brt',0],[1,'Brt',10],[1,'Hdf',20],[1,'Hdf',200],[2,'Brt',100],[1,'Hdf',2]]),np.array(['car','car','float']))
        >>> agreg.appliquer(donnee)
        >>> print(donnee)
        [['date' 'region' 'valeur']
         ['1' 'Brt' '5.0']
         ['2' 'Brt' '100.0']
         ['1' 'Hdf' '74.0']]
        """
        
        check1 = all(item in  donnee.recuperervariable() for item in self.var_date)
        check2 = all(item in  donnee.recuperervariable() for item in self.var_reg)
        if not (check1 and check2):
            raise Exception('Au moins une des variables est mal saisie.')
        
        typage = donnee.recuperertypage()
        if len(typage) != len(donnee.recuperervariable()):
            raise Exception("Le typage doit etre correctement renseigne pour ce type d'operation")


        donnees_final = donnee.recuperervaleurs()
        date_indice =  donnee.indicescolonnes(self.var_date)
        region_indice = donnee.indicescolonnes(self.var_reg)
        
        regdate = np.unique(donnees_final[:,[region_indice[0], date_indice[0]]], axis = 0)
        temp = np.empty((0,len(donnees_final[0,:])))


        for elmt in regdate:
            lignes = selectionLigne.indiceslignesgardees(donnee, np.array([self.var_date,self.var_reg]) , np.array([elmt[1],elmt[0]]))
            maths = Statistiques(donnees_final[lignes,:], typage)
            temp = np.row_stack((temp, maths.moyenne()))
        
        donnee.supprimerlignes()
        donnee.ajouterlignes(temp)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
