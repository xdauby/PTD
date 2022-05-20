import sys
import os
sys.path.append(os.getcwd())


import matplotlib.pyplot as plt

class Graphique:

    def __init__(self, varx, vary):

        self.varx = varx
        self.vary = vary

    def timeserie(self, donnee):
        
        vals = donnee.recuperervaleurs()
        indxy = donnee.indicescolonnes([self.varx, self.vary])
        
        
        plt.plot(vals[:,indxy[0]], vals[:,indxy[1]].astype(float))
        plt.show()

    def nuage(self, donnee):

        vals = donnee.recuperervaleurs()
        indxy = donnee.indicescolonnes([self.varx, self.vary])

        plt.scatter( vals[:,indxy[0]].astype(float), vals[:,indxy[1]].astype(float))
        plt.show()