import sys
import os
sys.path.append(os.getcwd())

from datetime import datetime
from Transformation.Selection.selectioncolonne import SelectionColonne
from Transformation.transformation import Transformation
import numpy as np

from Donnee.donnee import Donnee


class ConvertisseurDate(Transformation):
    """
    Les objets de cette classe ont une méthode pour transformer les objets de classe Donnee.
    Ils transforment le valeurs que prennent une  variable date du format 'YYYY''MM''DD''HH''MN''SS' (ex: 20130101210000) 
    au format  'YYYY'-'MM'-'DD'T'HH':'MN':'SS'+01:00 (ex: 2013-01-01T21:00:00+01:00)
    Où YYYY l'année, MM le mois, DD le jour, HH l'heure, MN la minute, SS la seconde

    Attributes
    ----------
    var_date: numpy.ndarray([str]),
        Le nom de la variable prenant comme valeur les dates

    Examples
    -----
    >>> data=Donnee(np.array(['date']),np.array([[20130101210000],[20130101210010],[20130102051733]]))
    >>> convert = ConvertisseurDate(['date'])
    >>> convert.appliquer(data)
    >>> print(data.recuperervaleurs())
    [['2013-01-01T21:00:00+01:00']
     ['2013-01-01T21:00:10+01:00']
     ['2013-01-02T05:17:33+01:00']]
    """

    def __init__(self, var_date):
        """
        Constructeur d'objets modifiant les valeurs de la variable date.

        Parameters
        ----------
        var_date: list[str] ou numpy.ndarray([str]),
            Le nom de la variable prenant comme valeur les dates
        
        Examples
        -----
        >>> convert = ConvertisseurDate(['date'])
        >>> convert.var_date
        array(['date'], dtype='<U4')
        """        
        self.var_date = np.array(var_date)

    @staticmethod
    def conversion_date_iso(date, strdate="%Y%m%d%H%M%S"):
        """
        Convertit une date du format 'YYYY''MM''DD''HH''MN''SS'
        au format 'YYYY'-'MM'-'DD'T'HH':'MN':'SS'+01:00

        Parameters
        ----------
        date : str
            Date au format 'YYYY''MM''DD''HH''MN''SS'
        strdate : str, optional
            correspond au format auquel la date que l'on veut changer est fournie, selon la convention
            utilisée dans le module datetime, by default "%Y%m%d%H%M%S"

        Returns
        -------
        datetime.datetime
            un objet de classe datetime, exprimant la même date, mais qui sera plus simple pour nous à manipuler

        Examples
        -----
        >>> print(datetime.strptime('20130101210000', "%Y%m%d%H%M%S"))
        2013-01-01 21:00:00
        """
        datetime_format = datetime.strptime(date, strdate)
        return datetime_format.isoformat() + "+01:00"

    def appliquer(self, donnees):
        """
        Convertit les valeurs d'une variable de date du format 'YYYY''MM''DD''HH''MN''SS' (ex: 20130101210000) 
        au format  'YYYY'-'MM'-'DD'T'HH':'MN':'SS'+01:00 (ex: 2013-01-01T21:00:00+01:00)
        La variable convertit est un attribut de la classe

        Parameters
        ----------
        donnees : Donnee
            la table de données ayant une variable date dont on veut modifier le format

        Raises
        ------
        Exception
            Si le nom de l'attribut de classe var_date ne correspond à aucune variable de l'objet donnees mis en paramètre, retourne une exception

        Examples
        -----
        >>> data=Donnee(np.array(['date']),np.array([[20130101210000],[20130101210010],[20130102051733]]))
        >>> convert = ConvertisseurDate(['date'])
        >>> convert.appliquer(data)
        >>> print(data.recuperervaleurs())
        [['2013-01-01T21:00:00+01:00']
         ['2013-01-01T21:00:10+01:00']
         ['2013-01-02T05:17:33+01:00']]
        """

        check = all(item in donnees.recuperervariable() for item in self.var_date)
        if not check:
            raise Exception('La variable de date est mal saisie.')

        indice_date = donnees.indicescolonnes(self.var_date)
        vfunc = np.vectorize(self.conversion_date_iso)
        
        vals = donnees.recuperervaleurs()
        vals[:,indice_date] = vfunc(vals[:,indice_date])
        donnees.supprimercolonnes(self.var_date)

        donnees.ajoutercolonnes(np.array([np.append(self.var_date, vals[:, indice_date])]).T, np.array(['car']))

    

if __name__ == '__main__':
    import doctest
    doctest.testmod()






            


