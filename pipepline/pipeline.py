import sys
import os
sys.path.append(os.getcwd())

class Pipeline:

    def __init__(self, donnees, transformation):

        self.donnees = donnees
        self.transformation = transformation 
        

    def pipeliner(self):
        
        for trans in self.transformation:
            trans.appliquer(self.donnees)