import os
import sys
sys.path.append(os.getcwd())

import requests as req
import time
from Donnee.donnee import Donnee
from Transformation.Chargement.chargementcsvgz import ChargementCSVGZ
from Transformation.Sauvegarde.sauvegardecsv import SauvegardeCSV
import numpy as np 

info_station = Donnee()
t0tris = ChargementCSVGZ(os.getcwd() + '/données_régions/', 'postesSynopAvecRegions.csv.gz')
t0tris.appliquer(info_station)

def get_departements(donnee, vars_longlat, var_reg):

    #  vars_longlat = ['Longitude', Lattitude] \
    lon_lat_reg = vars_longlat
    lon_lat_reg.append(var_reg)
    
    indice_vars = donnee.indicescolonnes(lon_lat_reg)
    list_longlat = donnee.recuperervaleurs()[:,indice_vars]
    list_departements = ['departement']
    
    for longlat in list_longlat:
        time.sleep(5)
        try:
            rep = req.get(f'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={longlat[1]}6&lon={longlat[0]}')
            departement = rep.json()['address']['county']
            list_departements.append(departement)
        except KeyError:
            list_departements.append(longlat[2])
    
    donnee.ajoutercolonnes(np.array([list_departements]).T)
    sauv =SauvegardeCSV('Sortie/departements.csv')
    sauv.appliquer(donnee)

get_departements(info_station, ['Longitude', 'Latitude'], 'Region')
