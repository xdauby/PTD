import sys
import os
sys.path.append(os.getcwd())

from Transformation.Chargement.chargementdonnees import ChargementDonnees
import gzip
import csv
import numpy as np


class ChargementCSVGZ(ChargementDonnees):
    """
    Charge dans un objet Donnee "vide" des données issues d'un fichier CSVGZ

    Attributes
    ----------
    adresse_dossier : str
        chemin du dossier où se trouve le fichier
    fichier : str
        nom du fichier csvgz à importer
    """

    def __init__(self,adresse_dossier, fichier):
        """
        Constructeur

        Parameters
        ----------
        adresse_dossier : str
            chemin du dossier où se trouve le fichier
        fichier : str
            nom du fichier csvgz à importer
        """
        
        super().__init__(adresse_dossier, fichier)
    
    def appliquer(self, donnees):
        """
        Applique le chargement sur les données

        Parameters
        ----------
        donnees : Donnee
            un objet Donnnee vide dans lequel on chargera le fichier csvgz
        """
        
        folder = self.adresse_dossier
        filename = self.fichier
        data = []
        
        with gzip.open(folder + filename, mode='rt') as gzfile :
            synopreader = csv.reader(gzfile, delimiter=';')
            for row in synopreader :
                data.append(row)
        
        self.donnees_brutes = np.array(data, dtype='<U100')
        self.donnees_brutes[self.donnees_brutes == 'mq'] = 'nan'
        donnees.ajoutercolonnes(np.row_stack((self.donnees_brutes[0,:],self.donnees_brutes[1:,:])))
