import sys
import os
sys.path.append(os.getcwd())

from Transformation.Selection.selectionligne import selectionLigne
from Transformation.Jointure.jointure import Jointure
import numpy as np
from Donnee.donnee import Donnee


class JointureGauche(Jointure):
    """
    Joint deux tables correspondant aux même observations mais ayant différentes variables
    Les observations s'identifient selon une ou plusieurs variables

    Attributes
    ----------
    donnee_droite : Donnee
        La première table de données de la jointure
    vars_joiture : list(str)
        Là ou les variables de la jointure
    """


    def __init__(self,donnee_droite ,vars_joitures): #liste
        """
        Constructeur

        Parameters
        ----------
        donnee_droite : Donnee
            La première table de données de la jointure
        vars_joiture : list(str)
            Là ou les variables de la jointure

        Examples
        -----
        >>> data1 = Donnee(np.array(['id','valeur']),np.array([['01',0],['25',10]]))
        >>> joint = JointureGauche(data1, 'id')
        >>> print(joint.vars_joitures)
        id

        """
        
        self.vars_joitures = np.array(vars_joitures)
        self.donnee_droite = donnee_droite

    def appliquer(self, donnee_gauche):
        """
        Applique la jointure
        Modifie la table entrée en paramètre

        Parameters
        ----------
        donnee_gauche : Donnee
            La deuxième table de données de la jointure

        Examples
        -----
        >>> data1 = Donnee(np.array(['id','valeur']),np.array([['01',0],['25',10]]),np.array(['car','float']))
        >>> data2 = Donnee(np.array(['id','valeur2']),np.array([['01','a'],['25','b']]))
        >>> joint = JointureGauche(data1, ['id'])
        >>> joint.appliquer(data2)
        >>> print(data2)
        [['id' 'valeur2' 'valeur']
         ['01' 'a' '0']
         ['25' 'b' '10']]

        >>> data1 = Donnee(np.array(['tps','lieu','valeur']),np.array([['01','x',0],['01','y',10]]),np.array(['car','float']))
        >>> data2 = Donnee(np.array(['tps','lieu','valeur2']),np.array([['01','x','a'],['01','y','b']]))
        >>> joint = JointureGauche(data1, ['tps','lieu'])
        >>> joint.appliquer(data2)
        >>> print(data2)        
        [['tps' 'lieu' 'valeur2' 'valeur']
         ['01' 'x' 'a' '0']
         ['01' 'y' 'b' '10']]
        """
        
        check = all(item in  self.donnee_droite.recuperervariable() for item in self.vars_joitures)
        if not check:
            raise Exception('Au moins une des variables est mal saisie.')
        if not len(donnee_gauche.recuperervaleurs()[:,0]):
            raise Exception('Fusion impossible, la table de droite est vide.')

        vals = self.donnee_droite.recuperervaleurs()
        indices_vars = self.donnee_droite.indicescolonnes(self.vars_joitures)
        vals_droite = np.full((len(donnee_gauche.recuperervaleurs()[:,0]), len(self.donnee_droite.recuperervariable())), 'nan', dtype='<U100')  
       

        if not len(np.unique(vals[:,indices_vars], axis = 0)) == len(vals[:,indices_vars]):
            raise Exception("La cle dans la table de droite n'est pas unique")

        for key in vals[:,indices_vars]:


            selectionG = selectionLigne.indiceslignesgardees(donnee_gauche, self.vars_joitures, np.array(key))
    
            selectionD = selectionLigne.indiceslignesgardees(self.donnee_droite, self.vars_joitures, np.array(key))
            vals_droite[selectionG,:] = vals[selectionD,:]

        vals_droite = np.delete(vals_droite,indices_vars,1)
        vars_droite = np.delete(self.donnee_droite.recuperervariable(), indices_vars)
        typage = np.delete(self.donnee_droite.recuperertypage(), indices_vars)
        table =  np.row_stack((vars_droite, vals_droite))
        donnee_gauche.ajoutercolonnes(table, typage)

        
if __name__ == '__main__':
    import doctest
    doctest.testmod()  
