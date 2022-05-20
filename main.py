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
from Visualisation.graphique import Graphique

from Transformation.Chargement.chargementcsvgz import ChargementCSVGZ
from Transformation.Chargement.chargementjsongz import ChargementJSONGZ
from Transformation.ValeurManquantes.valeurmanquante import ValeurManquante
import numpy as np
from datetime import datetime
from Transformation.transformation import *


#chargement jeu 1
dossier = '/home/anonymous/Documents/ENSAI/1A/projet_info_bis/données_météo/'
fichiers = 'synop.201302.csv.gz' #[f for f in listdir(dossier) if isfile(join(dossier, f))]

#pour tout importer, mais c'est long est deconseille
#cpt = 0
#for fichier in fichiers[1:2]:
    #if cpt == 0:
        #donnee = Donnee([],[])
        #ChargementCSVGZ(donnee, dossier, fichier)
        #ChargementCSVGZ(donnee, dossier, fichier)
        #cpt +=1
    #else:
        #donnee2 = Donnee([],[])
        #ChargementCSVGZ(donnee2, dossier, fichier)
        #Concatenation(donnee, donnee2)

donnee = Donnee()
t0 = ChargementCSVGZ(dossier, fichiers)
t0.appliquer(donnee)
donnee.supprimercolonnes([''])

#chargement jeu 2


dossier2 = '/home/anonymous/Documents/ENSAI/1A/projet_info/données_électricité/'
fichier2 = '2013-02.json.gz'
donnee2 = Donnee()
t0bis = ChargementJSONGZ(dossier2, fichier2)
t0bistraitement = SelectionColonne(['date_heure', 'date', 'heure', 'code_insee_region', 'region', 'consommation_brute_gaz_grtgaz', 'statut_grtgaz', 'consommation_brute_gaz_terega', 'statut_terega', 'consommation_brute_gaz_totale', 'consommation_brute_electricite_rte', 'statut_rte', 'consommation_brute_totale'])
t0bis.appliquer(donnee2)
t0bistraitement.appliquer(donnee2)

#chargement info station

info_station = Donnee()
t0tris = ChargementCSVGZ('/home/anonymous/Documents/ENSAI/1A/projet_info_bis/données_régions/', 'postesSynopAvecRegions.csv.gz')
t0tris.appliquer(info_station)





#ajout des typages

typage_meteo = np.array(['car', 'car', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float','float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float'])
donnee.ajoutertypage(typage_meteo)
typage_energie = np.array(['float', 'float', 'car', 'car', 'float', 'car', 'car', 'car', 'float', 'car', 'car', 'car','float'])
donnee2.ajoutertypage(typage_energie)
typage_station = np.array(['car','car','float','float', 'float', 'car'])
info_station.ajoutertypage(typage_station)



t1 = SelectionColonne(['numer_sta','pmer','date', 'ctype4', 't', 'hnuage4' ])
t2 = ConvertisseurDate(['date'])
t3 = Fenetrage(['date'], '2013-02-24T21:00:00+01:00','2013-02-25T07:00:00+01:00')
t3bis = Fenetrage(['date_heure'], '2013-02-24T21:00:00+01:00','2013-02-25T07:00:00+01:00')
t4 = JointureGauche(info_station,['ID'])
t5 = AgregationRegion(['date'], ['Region'])
t6 = JointureGauche(donnee2, ['Region','date_heure'])
t7 = MoyenneGlissante(['pmer'], 3)
t8 = Normalisation()


t1.appliquer(donnee)
t2.appliquer(donnee)
t3.appliquer(donnee)
t3bis.appliquer(donnee2)
donnee.changernomvariable(['numer_sta'], ['ID'])
t4.appliquer(donnee)
t5.appliquer(donnee)
donnee2.changernomvariable(['region'], ['Region'])
donnee.changernomvariable(['date'], ['date_heure'])
t6.appliquer(donnee)

print(donnee)

np.set_printoptions(threshold=sys.maxsize)


t7.appliquer(donnee)
t8.appliquer(donnee)


print(donnee)

