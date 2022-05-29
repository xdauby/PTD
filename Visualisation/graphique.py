import sys
import os
sys.path.append(os.getcwd())
from Donnee.donnee import Donnee
import numpy as np


import matplotlib.pyplot as plt

class Graphique:
    """
    Permet de produire des graphiques à partir de deux variables

    Attributes
    -----
    varx : str
        Variable en abscisse
    vary : _type_
        Variable en ordonnée    


    """

    def __init__(self, varx, vary):
        """
        Constructeur

        Parameters
        ----------
        varx : str
            Variable en abscisse
        vary : _type_
            Variable en ordonnée
        """

        self.varx = varx
        self.vary = vary

    def timeserie(self, donnee):
        """
        Crée une série temporelle selon les variables mis en attribut (varx la variable date)
        Rmq:  Le temps n'est pas représenté à l'échelle

        Parameters
        ----------
        donnee : Donnee
            Table de données contenant les variables que l'on veut visualiser

        Examples
        -----
        >>> data=Donnee(np.array(['date','age']),np.array([['2013-02-01T21:00:00+01:00',1],['2014-01-01T21:00:00+01:00',2],['2013-04-01T21:00:00+01:00',3]]))
        >>> graph = Graphique('date','age')
        >>> graph.timeserie(data)
        """
        
        datatemp=donnee
        datatemp.trierpardate([self.varx])
        vals = datatemp.recuperervaleurs()
        indxy = datatemp.indicescolonnes([self.varx, self.vary])
        
        
        plt.plot(vals[:,indxy[0]], vals[:,indxy[1]].astype(float))
        plt.show()

    def nuage(self, donnee):
        """
        Crée un nuage de point des deux variables mis en attribut


        Parameters
        ----------
        donnee : Donnee
            Table de données contenant les variables que l'on veut visualiser

        Examples
        -----
        >>> donnee = Donnee(np.array(['tps','lieu','valeur']),np.array([['01','x',0],['02','y',10],['01','y',10],['03.5','y',10],['03','y',9],['04','y',18]]))
        >>> graph1 = Graphique('tps','valeur')
        >>> graph1.nuage(donnee)
        """

        vals = donnee.recuperervaleurs()
        indxy = donnee.indicescolonnes([self.varx, self.vary])

        plt.scatter( vals[:,indxy[0]].astype(float), vals[:,indxy[1]].astype(float))
        plt.show()


if __name__ == '__main__':
    import doctest
    doctest.testmod()        
