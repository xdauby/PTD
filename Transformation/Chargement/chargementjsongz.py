import sys
import os
sys.path.append(os.getcwd())


from Transformation.Chargement.chargementdonnees import ChargementDonnees
import gzip
import json
import numpy as np

class ChargementJSONGZ(ChargementDonnees):
    """
    Charge dans un objet Donnee "vide" des données issues d'un fichier JSONGZ

    Attributes
    ----------
    adresse_dossier : str
        chemin du dossier où se trouve le fichier
    fichier : str
        nom du fichier jsongz à importer
    """

    def __init__(self, adresse_dossier, fichier):
        """
        Constructeur

        Parameters
        ----------
        adresse_dossier : str
            chemin du dossier où se trouve le fichier
        fichier : str
            nom du fichier jsongz à importer
        """

        super().__init__(adresse_dossier, fichier)


    def appliquer(self, donnees):
        """
        Applique le chargement sur les données

        Parameters
        ----------
        donnees : Donnee
            un objet Donnnee vide dans lequel on chargera le fichier jsongz
        """

        folder = self.adresse_dossier
        filename = self.fichier 
        with gzip.open(folder + filename, mode='rt') as gzfile :
            data = json.load(gzfile)
        self.donnees_brutes = data    

        initial = np.array(list(self.donnees_brutes[0].items())).T
        
        ind_suppr = []
        for cols in range(len(initial[0])):
            if type(initial[1,cols])== dict:
                unzip = np.array(list(initial[1,cols].items())).T
                ind_suppr.append(cols)          
        initial = np.delete(initial , ind_suppr, 1)
        initial = np.concatenate((initial, unzip), axis = 1)

        temp = np.full((len(self.donnees_brutes) + 1, len(initial[0]) ), 'nan', dtype='<U100')
        temp[0] = initial[0]
        temp[1] = initial[1]

        for rows in range(1,len(self.donnees_brutes)):
            
            currentline = self.donnees_brutes[rows]
            currentline = np.array(list(currentline.items())).T

            for cols in range(len(self.donnees_brutes[rows])):
                
                if type(currentline[1,cols]) == dict:
                    
                    unzip = np.array(list(currentline[1,cols].items())).T
                    
                    for cols2 in range(len(unzip[0])):
                       
                        xj = np.where(unzip[0,cols2] == temp[0])[0]
                        
                        if np.size(xj):
                            temp[rows+1,xj] = unzip[1,cols2]
                        else:
                            temp2 = np.full((1, len(temp)), 'nan', dtype='<U100')[0]
                            temp2[0] = unzip[0,cols2]
                            temp2[rows+1] = unzip[1,cols2]
                            temp2 = np.array([temp2]).T
                            temp = np.concatenate((temp, temp2), axis = 1)
                                
                else:
                    xi = np.where(currentline[0,cols] == temp[0])[0]
                    if np.size(xi):
                        temp[rows+1,xi] = currentline[1,cols]
                    else:
                        temp2 = np.full((1, len(temp)), 'nan', dtype='<U100')[0]
                        temp2[0] = currentline[0,cols]
                        temp2[rows+1] = currentline[1,cols]
                        temp2 = np.array([temp2]).T
                        temp = np.concatenate((temp, temp2), axis = 1)
                        

        donnees.ajoutercolonnes(temp)

        #partie a specialiser
        #for i in range(len(self.donnees_brutes)):
        #    for j in range(len(list(self.donnees_brutes[i]['fields'].keys()))):
        #        xj = np.where(list(self.donnees_brutes[i]['fields'].keys())[j] == vars)
        #        vals[i,xj] = list(self.donnees_brutes[i]['fields'].values())[j]
        #self.expi2 = vals
        
