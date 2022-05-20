import sys
import os
sys.path.append(os.getcwd())

import numpy as np
from Transformation.Jointure.jointure import Jointure

class Concatenation:

    def __init__(self, donnee_haut):
        self.donnee_haut = donnee_haut

    def appliquer(self, donnee):

        if not((donnee.recuperervariable() == self.donnee_haut.recuperervariable()).all()):
            raise Exception('Les deux tables doivent avoir les memes variables')
        donnee.ajouterlignes(self.donnee_haut.recuperervaleurs())

            


    



    