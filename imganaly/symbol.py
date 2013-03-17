# -*- coding: utf-8 -*-

"""
créé par Réchèr. Licence CC-BY ou Art Libre.
https://github.com/darkrecher/Anti-Idle-Math-Solver
je prends les bitcoins : 12wF4PWLeVAoaU1ozD1cnQprSiKr6dYW1G

Module définissant la classe symbole. Un symbole contient :
 - width, height : hauteur et largeur du dessin du symbole à l'écran.
 - flat_list_ink : le tableau des valeur d'encres, définissant le dessin.
 - signifiance : le caractère dans le texte d'énigme correspondant au 
   symbole. (Il peut être None)
 - comes_from_raw_symbol : booléen. True : le symbole a été défini par un
   tableau "raw" de valeurs d'encre. Ça veut dire que c'est un nouveau 
   symbole qu'on vient de découvrir.
   
Chargement d'un symbole connu
-----------------------------
Instancier la classe en lui passant le paramètre saved_data. Laisser les 
valeurs par défaut des autres paramètres.

saved_data est une string, formatée comme décrit dans le fichier symbdata.py.

Les symboles chargés de cette manière ont une signifiance définie. (Elle est
récupérée depuis le paramètre saved_data.

Chargement d'un nouveau symbole
-------------------------------
Instantier la classe en lui passant le paramètre raw_symbol. Laisser les 
valeurs par défaut des autres paramètres.

raw_symbol est une liste de liste de nombres. Chaque nombre est une valeur
d'encre d'un pixel. Chaque liste de nombre est une ligne du symbole. Puisque
c'est du "raw", on peut avoir des lignes au début et à la fin, ne comportant 
que des 0. Ces lignes sont supprimées au moment de créer le symbole, c'est 
cette opération qui permet de passer du raw symbol au symbol affiné.

Les symboles chargés de cette manière ont une signifiance indéfinie. Il faut
la définir plus tard, en appelant la fonction assign_signifiance.

Chargement d'un symbole bidon
-------------------------------
Instantier la classe en ne lui passant aucun paramètre.

Un symbole bidon a une hauteur et une largeur de 0, pas de tableau de valeur
d'encres, et pas de signifiance. Il ne sert pas à grand chose, mais un peu
quand même. Voir module eniocr.py.

Utilisation des symboles
------------------------
Un symbole tout seul ne sert pas à grand-chose. Voir module symbref.py pour
avoir des idées d'utilisation cools.

Sinon, le truc qu'on peut faire, c'est logger les infos du symbole, avec la
fonction __str__. Le texte loggé peut directement être copié-collé comme 
nouvel élément de symbdata.LIST_SYMB_ALARRACHE. Et ça fera un symbole connu
de plus. 
"""

from log import log
from enum import enum

class Symbol():
    """ 
    """
    
    def __init__(self, raw_symbol=None, saved_data=None):
        if raw_symbol is not None:
            self._init_with_raw_symbol(raw_symbol)
        elif saved_data is not None:
            self._init_with_saved_data(saved_data)
        else:
            self._init_with_none()
    
    def assign_signifiance(self, signifiance):
        """ signifiance n'est peut être pas un mot qui existe. osef."""
        self.signifiance = signifiance    
    
    def _init_with_raw_symbol(self, raw_symbol):
        self.array_inks = [
            ink_line for ink_line in raw_symbol
            if any( (ink > 0 for ink in ink_line) ) ]
        self.width = len(self.array_inks[0])
        self.height = len(self.array_inks)
        self.signifiance = None
        self.flat_list_ink = []
        for ink_line in self.array_inks:
            self.flat_list_ink.extend(ink_line)    
        self.flat_list_ink = tuple(self.flat_list_ink)
        self.comes_from_raw_symbol = True
    
    def _init_with_saved_data(self, saved_data):
        list_saved_data = saved_data.split(" ")
        self.signifiance = list_saved_data.pop(0)
        self.width = int(list_saved_data.pop(0))
        self.height = int(list_saved_data.pop(0))
        self.flat_list_ink = [ int(ink) for ink in list_saved_data ]
        self.flat_list_ink = tuple(self.flat_list_ink)
        assert len(self.flat_list_ink) == self.width * self.height
        self.comes_from_raw_symbol = False
    
    def _init_with_none(self):
        self.width = 0
        self.height = 0
        self.signifiance = None
        self.flat_list_ink = []        
        self.comes_from_raw_symbol = False
            
    def __str__(self):
        if self.signifiance is None:
            str_sig = "!"
        else:
            str_sig = self.signifiance
        list_data = [ str_sig, self.width, self.height ]
        list_data.extend(self.flat_list_ink)
        list_data_str = [ str(elem) for elem in list_data ]
        return " ".join(list_data_str)
        