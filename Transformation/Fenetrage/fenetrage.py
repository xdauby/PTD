import sys
import os
sys.path.append(os.getcwd())

import numpy as np
from Transformation.transformation import Transformation
from Donnee.donnee import Donnee


class Fenetrage(Transformation):
    """
    Sélectionne des observations (lignes de l'attribut valeurs d'un objet donnees)
    qui sont entre deux dates

    Attributes
    -----
    var_date: list(str),
        nom de la variable date
    date_d: str,
        date de début du fenêtrage au format 'YYYY'-'MM'-'DD'T'HH':'MN':'SS'+01:00
    date_f: str,
        date de fin du fenêtrage

    
    """
    def __init__(self, var_date, date_d, date_f):
        """
        Constructeur

        Parameters
        -----
        var_date: list(str),
            nom de la variable date
        date_d: str,
            date de début du fenêtrage au format 'YYYY'-'MM'-'DD'T'HH':'MN':'SS'+01:00
        date_f: str,
            date de fin du fenêtrage

        Examples
        -----
        >>> fenetre= Fenetrage(['date'],'2013-01-01T21:00:00+01:00','2014-01-01T21:00:00+01:00')
        >>> print(fenetre.var_date)
        ['date']
        
        """
        
        if type(date_d) != str or type(date_f) != str:
            raise Exception('Les dates de debut et de fin doivent etre des str.')
        if type(var_date)!= list:
            raise Exception('La variable de date doit etre stockee dans une liste')
        if date_f < date_d:
            raise Exception('Les dates ne sont pas dans le bon ordre.')
       
        self.var_date = np.array(var_date)
        self.date_d = date_d
        self.date_f = date_f

    def appliquer(self,donnees):
        """
        Sur un paramètre donnees, applique un fenetrage selon les attributs date_d et date_f

        Parameters
        ----------
        donnees : Donnee
            Les donnees que l'on veut fenêtrer

        Raises
        ------
        Exception
            Si dans donnees, il n'y a pas de variable avec le nom de var_date:
            "La variable de date est mal saisie."

        Examples
        -----
        >>> data=Donnee(np.array(['date','age']),np.array([['2013-02-01T21:00:00+01:00',1],['2014-01-01T21:00:00+01:00',2],['2015-01-01T21:00:00+01:00',3]]))
        >>> fenetre= Fenetrage(['date'],'2013-01-01T21:00:00+01:00','2014-05-01T21:00:00+01:00')
        >>> fenetre.appliquer(data)
        >>> print(data.recuperervaleurs())
        [['2013-02-01T21:00:00+01:00' '1']
         ['2014-01-01T21:00:00+01:00' '2']]
        """
        
        check = all(item in donnees.recuperervariable() for item in self.var_date)
        if not check:
            raise Exception("La variable de date est mal saisie.")
        
        indice_date = donnees.indicescolonnes(self.var_date)
        vals = donnees.recuperervaleurs()     
        date_suppr = np.where((vals[:,indice_date] < self.date_d) | (vals[:,indice_date] > self.date_f))[0]

        if len(date_suppr) == len(vals):
            donnees.supprimerlignes()
            return

        if np.size(date_suppr):
            donnees.supprimerlignes(date_suppr)
        
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()
