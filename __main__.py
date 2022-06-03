import sys
import os

from Transformation.Sauvegarde.sauvegardecsv import SauvegardeCSV
from Visualisation.graphique import Graphique
from pipepline.pipeline import Pipeline
sys.path.append(os.getcwd())

from Donnee.donnee import Donnee
from Transformation.AgregationSpatiale.agregationregion import AgregationRegion
from Transformation.Fenetrage.convertisseurdate import ConvertisseurDate
from Transformation.Fenetrage.fenetrage import Fenetrage
from Transformation.Jointure.concatenation import Concatenation
from Transformation.Jointure.jointure import Jointure
from Transformation.Jointure.joituregauche import JointureGauche
from Transformation.AgregationSpatiale.agregationnational import AgregationNational
from Transformation.OperationsMathematiques.centrage import Centrage
from Transformation.OperationsMathematiques.moyenneglissante import MoyenneGlissante
from Transformation.OperationsMathematiques.normalisation import Normalisation
from Transformation.Selection.selectioncolonne import SelectionColonne
from Transformation.Selection.selectionligne import selectionLigne
from Transformation.transformation import Transformation
#from Visualisation.graphique import Graphique

from Transformation.Chargement.chargementcsvgz import ChargementCSVGZ
from Transformation.Chargement.chargementjsongz import ChargementJSONGZ
from Transformation.ValeurManquantes.valeurmanquante import ValeurManquante
import numpy as np
from datetime import datetime
from Transformation.transformation import *


#Chargement données météo
dossier = 'données_météo/'
fichiers = 'synop.201301.csv.gz' #[f for f in listdir(dossier) if isfile(join(dossier, f))]
donnee = Donnee()
t0 = ChargementCSVGZ(dossier, fichiers)
t0.appliquer(donnee)
donnee.supprimercolonnes([''])

#chargement données électricité
dossier2 = 'données_électricité/'
fichier2 = '2013-01.json.gz'
donnee2 = Donnee()
t0bis = ChargementJSONGZ(dossier2, fichier2)
t0bis.appliquer(donnee2)

#Import données station
info_station = Donnee()
charg_station = ChargementCSVGZ('Sortie/', 'departements.csv.gz')
charg_station.appliquer(info_station)
typage_station = np.array(['car','car','float','float', 'float', 'car', 'car'])
info_station.ajoutertypage(typage_station)


#Selection des variables et ajout typage

#meteo
t0traitement = SelectionColonne(['numer_sta','pmer','date', 't', 'ff', 'u' ])
t0traitement.appliquer(donnee)
typage_meteo = np.array(['car','car','float','float','float', 'float'])
donnee.ajoutertypage(typage_meteo)

#energie
t0bistraitement = SelectionColonne(['date_heure', 'date', 'heure', 'code_insee_region', 'region', 'consommation_brute_electricite_rte', 'consommation_brute_totale'])
t0bistraitement.appliquer(donnee2)
typage_energie = np.array(['car', 'car', 'car', 'car', 'car', 'float', 'float'])
donnee2.ajoutertypage(typage_energie)

#info statio
t0tristraitement = SelectionColonne(['ID', 'Nom', 'Region', 'departement'])
t0tristraitement.appliquer(info_station)

#pre traitement : ajuster les variables (noms ou valeurs) 
donnee.changernomvariable(['numer_sta'],['ID'])
donnee.changernomvariable(['date'], ['date_heure'])
donnee2.changernomvariable(['region'], ['Region'])


#conversion de la date dans le format iso
conv_date = ConvertisseurDate(['date_heure'])
#Fenêtrage des données
fen = Fenetrage(['date_heure'], '2013-01-01T21:00:00+01:00','2013-01-05T11:00:00+01:00')
#Ajout des informations sur la localisation des stations
jointure_station = JointureGauche(info_station,['ID'])
#aggrégation des information à l'échelle de la région
aggreg_region = AgregationRegion(['date_heure'], ['Region'])
#Jointure des tables électricité et météo
jointure_gen = JointureGauche(donnee2, ['Region','date_heure'])
#ajout d'une moyenne glissante
moyenne_g = MoyenneGlissante(['t'], 3)

conv_date.appliquer(donnee)
print('\n conversion date : \n')
print(donnee)
fen.appliquer(donnee)
print('\n fenetrage : \n')
print(donnee)
fen.appliquer(donnee2)
print(donnee)
jointure_station.appliquer(donnee)
print('\n jointure avec station : \n')
print(donnee)
aggreg_region.appliquer(donnee)
print('\n aggregation region : \n')
print(donnee)
jointure_gen.appliquer(donnee)
print('\n jointure avec les donnees energie : \n')
print(donnee)
moyenne_g.appliquer(donnee)
print('\n moyenne gliassante : \n')
print(donnee)
print('---------')

#pipelinons

#fen.appliquer(donnee2)

#transfo = [conv_date,fen,jointure_station, aggreg_region, jointure_gen, moyenne_g ]
#pipline = Pipeline(donnee, transfo)
#pipline.pipeliner()

#on peut normaliser ou centrer

#norm = Normalisation()
#centrage = Centrage()
#norm.appliquer(donnee)
#centrage.appliquer(donnee)

#possibilite d'enlever les valeurs manquantes
#vm = ValeurManquante()
#vm.appliquer(donnee)


#Sauvegarde
sauvg= SauvegardeCSV('Sortie/test_sauvg.csv')
donnee.trierpardate(['date_heure'])
sauvg.appliquer(donnee)
print('\n Table finale : \n')
print(donnee)

#quelques plots

donneebretagne = selectionLigne(['departement'],['Finistère'])
donneebretagne.appliquer(donnee)
print('\n Selection sur le département Finistère : \n')
print(donnee)

affichage = Graphique(['t'],['consommation_brute_totale'])
affichage.nuage(donnee)

affichage2 = Graphique(['date_heure'],['consommation_brute_totale'])
affichage2.timeserie(donnee)
