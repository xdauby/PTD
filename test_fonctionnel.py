import sys
import os
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
dossier = 'C:/Users/33628/Downloads/'
fichiers = 'synop.201301.csv.gz' #[f for f in listdir(dossier) if isfile(join(dossier, f))]

donnee = Donnee()
t0 = ChargementCSVGZ(dossier, fichiers)
t0.appliquer(donnee)
donnee.supprimercolonnes([''])


#chargement données électricité
dossier2 = 'C:/Users/33628/Downloads/'
fichier2 = '2013-01.json.gz'
donnee2 = Donnee()
t0bis = ChargementJSONGZ(dossier2, fichier2)
t0bis.appliquer(donnee2)

#Selection des variables
t1 = SelectionColonne(['numer_sta','pmer','date', 't', 'ff' ])
t1.appliquer(donnee)
#print(donnee)

t0bistraitement = SelectionColonne(['date_heure', 'date', 'heure', 'code_insee_region', 'region', 'consommation_brute_electricite_rte', 'consommation_brute_totale'])
t0bistraitement.appliquer(donnee2)

#print("---\n",donnee.recuperervariable(),"\n---\n",donnee2.recuperervariable())

#Ajout typage
typage_meteo = np.array(['car', 'float', 'car', 'float', 'float'])
donnee.ajoutertypage(typage_meteo)
typage_energie = np.array(['car', 'car', 'car', 'car', 'car', 'float', 'float'])
donnee2.ajoutertypage(typage_energie)


#Fenêtrage avec conversion date
conv_date = ConvertisseurDate(['date'])
conv_date.appliquer(donnee)
fen_date1 = Fenetrage(['date'], '2013-01-01T21:00:00+01:00','2013-02-01T07:00:00+01:00')
fen_date1.appliquer(donnee)
fen_date2 = Fenetrage(['date_heure'], '2013-01-01T21:00:00+01:00','2013-02-01T07:00:00+01:00')
fen_date2.appliquer(donnee2)
#print(len(donnee.recuperervaleurs()))


#Import données station
info_station = Donnee()
charg_station = ChargementCSVGZ('C:/Users/33628/Downloads/', 'postesSynopAvecRegions.csv.gz')
charg_station.appliquer(info_station)
typage_station = np.array(['car','car','float','float', 'float', 'car'])
info_station.ajoutertypage(typage_station)
selection_variables_station = SelectionColonne(['ID', 'Nom', 'Region'])
selection_variables_station.appliquer(info_station)

#Complétion et modification de la table météo pour préparer la jointure

#Ajout des informations sur la localisation des stations
donnee.changernomvariable(['numer_sta'],['ID'])
jointure_station = JointureGauche(info_station,['ID'])
jointure_station.appliquer(donnee)
print(donnee.recuperervariable())

#aggrégation des information à l'échelle de la région
aggrg_region = AgregationRegion(['date'], ['Region'])
aggrg_region.appliquer(donnee)

#Jointure des tables électricité et météo
donnee2.changernomvariable(['region'], ['Region'])
donnee.changernomvariable(['date'], ['date_heure'])
jointure_gen = JointureGauche(donnee2, ['Region','date_heure'])
jointure_gen.appliquer(donnee)
print(donnee.recuperervariable())
print(donnee.recuperervaleurs())

#
t7 = MoyenneGlissante(['t'], 3)
t7.appliquer(donnee)