import sys
sys.path.append("/home/anonymous/Documents/ENSAI/1A/projet_info_bis")
import numpy as np



class Donnee:
    """
    Les données météo et de consommation d'énergie ou autres sont instanciées dans cette classe.
    Un tableau de classe Donnee avec des informations est crée généralement en utilisant 
    un tableau vide de classe Donnee est en l'utilisant comme parametre d'une instance 
    de la classe ChargementCSVGZ ou ChargementJSONGZ.
    A simple titre d'exemple, les tableaux seront crées "manuellement" dans les tests de la classe Donnee.
    Attributes
    -----
    __variables : numpy.ndarray([str]), optionel
        Le nom des variables, par défaut np.array([])
    __valeurs : numpy.ndarray([str]) ou numpy.ndarray([float]), optionel
        Le np.array contient une liste de liste, chacune correspondant à une observation.
        Chacune contient les valeurs que prennent les variables pour une observation donnée, par défaut np.array([])
    __typage : numpy.ndarray([str]), optionel
        Le type ('str' ou 'float') de chaque variable. Il peut rester vide mais cela limite l'utilisation de 
        la classe OperationsMathematiques, par défaut np.array([])
    Examples
    -----
    >>> data1=Donnee()
    >>> print(data1)
    []
    >>> data=Donnee(np.array(["a","b","c"]),np.array([[1,2,6],[3,4,5]]),np.array(['float','float','float']))
    >>> print(data)
    [['a' 'b' 'c']
     ['1' '2' '6']
     ['3' '4' '5']]
    """
    
    def __init__(self, variables=np.array([],  dtype='<U100'), valeurs=np.array([], dtype='<U100'), typage = np.array([])):
        """
        Création d'une table à partir du noms de variables, des valeurs qu'elles prennent pour chaque observation,
        et le type de la variable.
        Parameters
        ----------
        variables : numpy.ndarray([str]), optionel
            Le nom des variables, par défaut np.array([])
        valeurs : numpy.ndarray([str]) ou numpy.ndarray([float]), optionel
            Le np.array contient une liste de liste, chacune correspondant à une observation.
            Chacune contient les valeurs que prennent les variables pour une observation donnée, par défaut np.array([])
        typage : numpy.ndarray([str]), optionel
            Le type ('str' ou 'float') de chaque variable. Il peut rester vide mais cela limite l'utilisation de 
            la classe OperationsMathematiques, par défaut np.array([])
        Examples
        -----
        >>> data1=Donnee()
        >>> print(data1)
        []
        >>> data=Donnee(np.array(["a","b","c"]),np.array([[1,2,6],[3,4,5]]),np.array(['float','float','float']))
        >>> print(data)
        [['a' 'b' 'c']
         ['1' '2' '6']
         ['3' '4' '5']]
        """
        
        self.__variables = np.array(variables, dtype='<U100')
        self.__valeurs = np.array(valeurs, dtype='<U100')
        self.__typage = np.array(typage, dtype='<U100')

    def __str__(self):
        """
        Conversion en chaîne de charactère
        Examples
        -----
        >>> data1=Donnee()
        >>> print(data1)
        []
        >>> data=Donnee(np.array(["a","b","c"]),np.array([[1,2,6],[3,4,5]]),np.array(['char','char','char']))
        >>> print(data)
        [['a' 'b' 'c']
         ['1' '2' '6']
         ['3' '4' '5']]
        """
        return np.row_stack((self.__variables,self.__valeurs)).__str__()

    def ajoutercolonnes(self, colonnes, typage = np.array([])):
        """
        Ajoute une ou plusieurs variables (colones) dans la table
        Parameters
        ----------
        colonnes : numpy.ndarray([])
            le np.array contient une liste, ou une liste de liste, chacune liste ayant le nom de la variable
            comme premier élément, et les valeurs qu'elle prend ensuite
        typage : numpy.ndarray([]), optional
            le np.array contient une liste des types ('float' ou 'str') des variables ajoutés, par défaut np.array([])
        Examples
        -----
        >>> data=Donnee()
        >>> data.ajoutercolonnes(np.array([["d",10,15]]).T)
        >>> print(data)
        [['d']
         ['10']
         ['15']]
        
        >>> data2=Donnee()
        >>> data2.ajoutercolonnes(np.array([["a","grand","petit"]]).T,np.array(['str']))
        >>> data2.ajoutercolonnes(np.array([["d",10,15],["e","blanc","noir"]]).T,np.array(['float','str']))
        >>> print(data2)
        [['a' 'd' 'e']
         ['grand' '10' 'blanc']
         ['petit' '15' 'noir']]
        >>> print(data2.recuperertypage())
        ['str' 'float' 'str']
        >>> data3=Donnee()
        >>> data3.ajoutercolonnes(np.array([["d",10,15],["e","blanc","noir"]]).T,np.array(['float','str']))
        >>> print(data3.recuperertypage())
        ['float' 'str']
        """    
        if  type(self.__variables) != np.ndarray:
            self.__variables = np.array(self.__variables)

        if  not np.size(self.__variables):
            self.__variables = colonnes[0,:]
            self.__valeurs = colonnes[1:,:]
        else:
            self.__variables = np.concatenate((self.__variables, colonnes[0,:]))
            self.__valeurs = np.concatenate((self.__valeurs, colonnes[1:,:]), axis = 1)
        
        if np.size(typage):
            self.__typage = np.append(self.__typage, typage)

    def supprimercolonnes(self, variables_a_supprimer):
        """
        Supprime une ou plusieurs variables (colones) dans la table.
        Parameters
        ----------
        variables_a_supprimer : str ou list(str)
            le nom d'une variable, ou une liste contenant des noms de variables
        Examples
        -----
        >>> data2=Donnee()
        >>> data2.ajoutercolonnes(np.array([["a","grand","petit"],["d",10,15],["e","blanc","noir"]]).T,np.array(['str','float','str']))
        >>> data2.supprimercolonnes("e")
        >>> print(data2)
        [['a' 'd']
         ['grand' '10']
         ['petit' '15']]
        >>> data2.supprimercolonnes(["a",'d'])
        >>> print(data2)
        []
        """        
        indice_colonnes = self.indicescolonnes(variables_a_supprimer)
        variable_suppr = np.delete(np.arange(len(self.__variables)) , np.array(indice_colonnes))

        self.__valeurs = self.__valeurs[:,variable_suppr]
        self.__variables = self.__variables[variable_suppr]

        if np.size(self.__typage):
            self.__typage = self.__typage[variable_suppr]


    def ajouterlignes(self, lignes):
        """
        Ajoute une ou plusieurs observations (lignes) dans la table
        Parameters
        ----------
        lignes : numpy.ndarray([str]) ou numpy.ndarray([float])
            Le np.array contient une liste de liste, chacune correspondant à une observation.
            Chacune contient les valeurs que prennent les variables pour une observation donnée
        Examples
        -----
        >>> data=Donnee(np.array(["a","b","c"]),np.array([[1,2,'bleu'],[3,4,'blanc']]),np.array(['float','float','str']))
        >>> data.ajouterlignes(np.array([[10,11,'vert']]))
        >>> print(data)
        [['a' 'b' 'c']
         ['1' '2' 'bleu']
         ['3' '4' 'blanc']
         ['10' '11' 'vert']]
        >>> data.ajouterlignes(np.array([[20,21,'jaune'],[30,31,'rouge']]))
        >>> print(data)
        [['a' 'b' 'c']
         ['1' '2' 'bleu']
         ['3' '4' 'blanc']
         ['10' '11' 'vert']
         ['20' '21' 'jaune']
         ['30' '31' 'rouge']]
        """        
        self.__valeurs = np.concatenate((self.__valeurs, lignes), axis=0)
        if np.all(self.__valeurs[0] == 'nan'):
            self.__valeurs = self.__valeurs[1:,:]

    def supprimerlignes(self, indices_lignes = np.array([-1])):
        """
        Enlève une ou plusieurs observations (lignes), à partir de leur position dans la table (indice)
        Parameters
        ----------
        indices_lignes : int ou list(int), optional
            Indice des lignes à supprimer. Par défaut,supprime toute les lignes et np.array([-1])
        Examples
        -----
        >>> data=Donnee(np.array(["a","b","c"]),np.array([[1,2,'bleu'],[3,4,'blanc'],[5,6,'gris'],[30,31,'rouge']]),np.array(['float','float','str']))
        >>> data.supprimerlignes(0)
        >>> print(data)
        [['a' 'b' 'c']
         ['3' '4' 'blanc']
         ['5' '6' 'gris']
         ['30' '31' 'rouge']]
        >>> data.supprimerlignes([0,1])
        >>> print(data)
        [['a' 'b' 'c']
         ['30' '31' 'rouge']]
        >>> data.supprimerlignes()
        >>> print(data)
        [['a' 'b' 'c']
         ['nan' 'nan' 'nan']]
        """        
        if (indices_lignes == np.array([-1])).all():
            self.__valeurs = np.full((1,len(self.__variables)) , 'nan')
        else:
            self.__valeurs = np.delete(self.__valeurs ,indices_lignes, 0) 
    
    def indicescolonnes(self, variables_selection):
        """
        Permet de retrouver l'indice d'une ou plusieurs variables (colones) à partir de leurs noms
        Parameters
        ----------
        variables_selection : str ou list[str]
            nom des variables dont on cherche l'indice
        Returns
        -------
        list[int]
            indices des variables examinées
        Raises
        ------
        Exception
            Lorsque le nom de la variable n'est pas reconnu
        Examples
        -----
        >>> data=Donnee(np.array(["a","b","c"]),np.array([[1,2,'bleu'],[3,4,'blanc'],[5,6,'gris'],[30,31,'rouge']]),np.array(['float','float','str']))
        >>> print(data.indicescolonnes('a'))
        [0]
        >>> print(data.indicescolonnes(['b',"c"]))
        [1, 2]
        """
        indice_colonnes = []
        for elmt in variables_selection:
            indice_colonnes.append(np.where(self.__variables ==  elmt)[0][0])
        
        if indice_colonnes == []:
            raise Exception("Une de vos variables n'a pas ete reconnue.")

        return indice_colonnes
     

    def changernomvariable(self, ancien_nom, nouveau_nom):
        """
        Change le nom d'une variable
        Parameters
        ----------
        ancien_nom : str
            nom de la variable que l'on veut changer
        nouveau_nom : str
            nouveau nom de la variable
        Examples
        -----
        >>> data=Donnee(np.array(["a","b","c"]),np.array([[1,2,'bleu'],[3,4,'blanc'],[5,6,'gris'],[30,31,'rouge']]),np.array(['float','float','str']))
        >>> data.changernomvariable(["a"],["talent"])
        >>> print(data.recuperervariable())
        ['talent' 'b' 'c']
        >>> data.changernomvariable(["b"],["ancienneté"])
        >>> print(data.recuperervariable())
        ['talent' 'ancienneté' 'c']
        """        
        indice_colonne = self.indicescolonnes(ancien_nom)
        self.__variables[indice_colonne] = nouveau_nom

    def trierpardate(self, var):
        """
        Ordonne les observations (lignes) selon une date (variable de type str)
        N'ordonne pas par nombre croissant
        Parameters
        ----------
        var : str
            Nom de la variable selon laquelle on veut trier les observations
        Examples
        -----
        >>> data=Donnee(np.array(["date","b","c"]),np.array([['2000-02-05T06:11:15:10',2,'bleu'],['2001-01-05T06:15:09:23',4,'blanc'],['2000-02-05T06:01:25:05',6,'gris'],['2000-02-05T06:01:25:15','100bouteilles','rouge']]))
        >>> data.trierpardate(['date'])
        >>> print(data)
        [['date' 'b' 'c']
         ['2000-02-05T06:01:25:05' '6' 'gris']
         ['2000-02-05T06:01:25:15' '100bouteilles' 'rouge']
         ['2000-02-05T06:11:15:10' '2' 'bleu']
         ['2001-01-05T06:15:09:23' '4' 'blanc']]
        >>> data.trierpardate('b')
        >>> print(data)
        [['date' 'b' 'c']
         ['2000-02-05T06:01:25:15' '100bouteilles' 'rouge']
         ['2000-02-05T06:11:15:10' '2' 'bleu']
         ['2001-01-05T06:15:09:23' '4' 'blanc']
         ['2000-02-05T06:01:25:05' '6' 'gris']]
        """
        indice_cols = self.indicescolonnes(var)[0]
        self.__valeurs = self.__valeurs[self.__valeurs[:,indice_cols].argsort()]

    def ajoutertypage(self, typage):
        """
        Modifie l'attribut typage, pour ajouter le type ('float' ou 'str') des variables (colones)
        Parameters
        ----------
        typage : numpy.ndarray([str])
            Le np.array contient une liste contenant le type de chaque variable
        Raises
        ------
        Exception
            Il n'y a pas autant de types spécifiés que de variables
        Examples
        -----
        >>> data=Donnee(np.array(["a","c"]),np.array([[1,'bleu'],[5,'gris'],[30,'rouge']]))
        >>> data.ajoutertypage(['float','str'])
        >>> print(data.recuperertypage())
        ['float', 'str']
        >>> data=Donnee(np.array(["a","b","c"]),np.array([[1,2,'bleu'],[3,4,'blanc'],[5,6,'gris'],[30,'100bouteilles','rouge']]),np.array(['float','float','str']))
        >>> data.ajoutertypage(np.array(['float','str','str']))
        >>> print(data.recuperertypage())
        ['float' 'str' 'str']
        """        
        if not(len(typage) == len(self.__variables)):
            raise Exception('Il doit y avoir autant de types que de variables.')
        
        self.__typage = typage
    
    
    def recuperertypage(self):
        """
        Retourne les types de variables
        Returns
        -------
        numpy.ndarray([str])
            les types de chaque variable
        Examples
        -----
        >>> data=Donnee(np.array(["a","b","c"]),np.array([[1,2,'bleu'],[3,4,'blanc'],[5,6,'gris'],[30,'100bouteilles','rouge']]),np.array(['float','str','str']))
        >>> print(data.recuperertypage())
        ['float' 'str' 'str']
        """
        return self.__typage

    def recuperervariable(self):
        """
        Retourne les noms des variables
        Returns
        -------
        numpy.ndarray([str])
            Contient les noms des variables
        
        Examples
        -----
        >>> data=Donnee(np.array(["a","b","c"]),np.array([[1,2,'bleu'],[3,4,'blanc'],[5,6,'gris'],[30,'100bouteilles','rouge']]),np.array(['float','str','str']))
        >>> print(data.recuperervariable())
        ['a' 'b' 'c']
        """
        return self.__variables

    def recuperervaleurs(self):
        """
        Retourne une matrice contenant les valeurs de la table
        Returns
        -------
        numpy.ndarray([str])
            Contient les variables de la table
        Examples
        -----
        >>> data=Donnee(np.array(["a","b","c"]),np.array([[1,2,'bleu'],[3,4,'blanc'],[5,6,'gris'],[30,'100bouteilles','rouge']]),np.array(['float','str','str']))
        >>> print(data.recuperervaleurs())
        [['1' '2' 'bleu']
         ['3' '4' 'blanc']
         ['5' '6' 'gris']
         ['30' '100bouteilles' 'rouge']]
        """
        return self.__valeurs

        

 
if __name__ == '__main__':
    import doctest
    doctest.testmod()