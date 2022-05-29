import sys
import os
sys.path.append(os.getcwd())

from Transformation.Sauvegarde.sauvegarde import Sauvegare
import numpy as np
from Donnee.donnee import Donnee


class SauvegardeCSV(Sauvegare):
    """
    Sauvegarde une table de données comme fichier CSV. La table est sauvegardée dans le dossier PTD-master

    Attributes
    ----------
    nom_fichier : str
        nom du fichier dans lequel les données sont sauvegardées
    """

    def __init__(self, nom_fichier):
        """
        Constructeur

        Parameters
        ----------
        nom_fichier : str
            nom du fichier dans lequel les données sont sauvegardées

        Examples
        -----
        >>> data = Donnee(np.array(['date','region','valeur']),np.array([[1,'Brt',0],[1,'Brt',10],[1,'Hdf',20],[1,'Hdf',200],[2,'Brt',100],[1,'Hdf',2]]),np.array(['car','car','float']))
        >>> sauvg = SauvegardeCSV('nom')
        >>> print(sauvg.nom_fichier)
        nom
        """
        
        self.nom_fichier=nom_fichier

    def appliquer(self, donnee):
        """
        Applique la sauvegarde à une table

        Parameters
        ----------
        donnee : Donnee
            Table de données que l'on veut sauvegarder
        """
        np.savetxt(self.nom_fichier, np.row_stack((donnee.recuperervariable(),donnee.recuperervaleurs())), delimiter=",",fmt='%s')

if __name__ == '__main__':
    import doctest
    doctest.testmod()
