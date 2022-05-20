from abc import abstractmethod
import sys
import os
sys.path.append(os.getcwd())

from Transformation.transformation import Transformation

class ChargementDonnees(Transformation):
    
    def __init__(self,adresse_dossier, fichier):
        
        self.adresse_dossier = adresse_dossier
        self.fichier = fichier

    @abstractmethod
    def appliquer(donnee):
        pass
