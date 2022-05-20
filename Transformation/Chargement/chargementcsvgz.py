import sys
import os
sys.path.append(os.getcwd())

from Transformation.Chargement.chargementdonnees import ChargementDonnees
import gzip
import csv
import numpy as np


class ChargementCSVGZ(ChargementDonnees):

    def __init__(self,adresse_dossier, fichier):
        
        super().__init__(adresse_dossier, fichier)
    
    def appliquer(self, donnees):
        
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
    

