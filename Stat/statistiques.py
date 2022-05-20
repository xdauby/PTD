import sys
import os
sys.path.append(os.getcwd())

from math import sqrt
import numpy as np


class Statistiques:

    def __init__(self, valeurs_variable, typage):
        
        self.vals = valeurs_variable
        self.typage = typage

    def moyenne(self):

        moy = []
        cpt = 0

        for cols in self.vals.T:
            if  self.typage[cpt] == 'float':
                try:     
                    vals_float = cols.astype(float)
                except:
                    print("Vous n'avez pas rentre les bon types.")
                if len(vals_float) > 0 and np.sum(~np.isnan(vals_float)) > 0:
                    moy.append(np.nansum(vals_float)/np.sum(~np.isnan(vals_float)))
                else:
                    moy.append('nan')
            else:
                if np.size(cols[np.where( cols !=  "nan")]):
                    cols_no_mq = cols[np.where( cols !=  "nan")]
                    moy.append(cols_no_mq[0])
                else:
                    moy.append('nan')
            cpt +=1
        
        return np.array(moy)

        

    def ecarttype(self): #les valeurs_variable doivent etre centre avant

        sigma = []
        cpt = 0

        for cols in self.vals.T:
            if  self.typage[cpt] == 'float':
                vals_nan = np.delete(cols, np.where(cols == 'nan'))     
                vals_float = vals_nan.astype(float) 
                
                if len(vals_float) > 0:
                    sigcol = 0
                    for i in range(len(vals_float)):
                        sigcol += (vals_float[i])**2
                    sigma.append(sqrt(sigcol/len(vals_float)))
                else:
                    sigma.append('nan')
            else:
                if np.size(cols[np.where( cols !=  "nan")]):
                    cols_no_mq = cols[np.where( cols !=  "nan")]
                    sigma.append(cols_no_mq[0])
                else:
                    sigma.append('nan')
                
            cpt +=1
        
        return np.array(sigma)

        
        
        

