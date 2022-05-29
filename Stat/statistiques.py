import sys
import os
sys.path.append(os.getcwd())

from math import sqrt
import numpy as np
from Donnee.donnee import Donnee


class Statistiques:
    """
    Fournit des méthodes de calcul que l'on peut appliquer sur des attributs d'un objet Donnee

    Attributes
    -----
    vals : numpy.array()
        Matrice contenant les valeurs d'une table de données. Chaque ligne correspond à une observation
    typage : np.array
        Contient les type ('car' ou 'float') des variables de la table de données
    """

    def __init__(self, valeurs_variable, typage):
        """
        Constructeur

        Parameters
        ----------
        valeurs_variable : numpy.array()
            Matrice contenant les valeurs d'une table de données. Chaque ligne correspond à une observation
        typage : np.array
            Contient les type ('car' ou 'float') des variables de la table de données

        Examples
        -----
        >>> donnee = Donnee(np.array(['date','region','valeur']),np.array([[1,'Brt',0],[1,'Brt',10],[1,'Hdf',20]]),np.array(['car','car','float']))
        >>> stat = Statistiques(donnee.recuperervaleurs(), donnee.recuperertypage())
        >>> print(stat.vals)
        [['1' 'Brt' '0']
         ['1' 'Brt' '10']
         ['1' 'Hdf' '20']]
        """
        
        self.vals = valeurs_variable
        self.typage = typage

    def moyenne(self):
        """
        Calcule la moyenne des colones de la matrice en attribut (self.vals)

        Returns
        -------
        numpy.array
            Contient une liste, chaque élément correspond à la moyenne de la colone correspondante. Si la colone n'est pas numérique, retourne la première valeur de la colone

        Examples
        -----
        >>> donnee = Donnee(np.array(['date','region','valeur']),np.array([[1,'Brt',-10],[1,'Brt',10],[1,'Hdf',20],[1,'Hdf',30],[2,'Brt',-50],[1,'Hdf',0]]),np.array(['car','car','float']))
        >>> stat = Statistiques(donnee.recuperervaleurs(), donnee.recuperertypage())
        >>> print(stat.moyenne())
        ['1' 'Brt' '0.0']
        """

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
        """
        Calcule l'écart-type (non corrigé) des colones de la matrice en attribut (self.vals)
        Les valeurs des colones doivent être centrées

        Returns
        -------
        numpy.array
            Contient une liste, chaque élément correspond à l'écart-type de la colone correspondante. Si la colone n'est pas numérique, retourne la première valeur de la colone

        Examples
        ------
        >>> donnee = Donnee(np.array(['date','region','valeur']),np.array([[1,'Brt',-10],[1,'Brt',10],[1,'Hdf',20],[1,'Hdf',30],[2,'Brt',-50],[1,'Hdf',0]]),np.array(['car','car','float']))
        >>> stat = Statistiques(donnee.recuperervaleurs(), donnee.recuperertypage())
        >>> print(stat.ecarttype())
        ['1' 'Brt' '25.81988897471611']
        """

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

        
        

if __name__ == '__main__':
    import doctest
    doctest.testmod()        

        
        
        

