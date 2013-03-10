# -*- coding: utf-8 -*-

"""
créé par Réchèr. Licence CC-BY ou Art Libre.
https://github.com/darkrecher/Anti-Idle-Math-Solver
je prends les bitcoins : 12wF4PWLeVAoaU1ozD1cnQprSiKr6dYW1G

Mon super module pour créer des type enums (comme en C++).

:Example:
CARROT_STATE = enum(
    "CARROT_STATE",      # il faut répéter le nom du type enum.
    "GRAIN",             # nom de l'état 1
    "GROWING",           # nom de l'état 2
    "OK",                # etc...
    "ROTTEN",
)   
cst = CARROT_STATE
current_state = cst.GROWING

Pour plus de détail, voir mon article : 
http://sametmax.com/faire-des-enums-en-python/


"""

def enum(enumName, *listValueNames):
    # Une suite d'entiers, on en crée autant
    # qu'il y a de valeurs dans l'enum.
    listValueNumbers = range(len(listValueNames))
    # création du dictionaire des attributs.
    # Remplissage initial avec les correspondances : valeur d'enum -> entier
    dictAttrib = dict( zip(listValueNames, listValueNumbers) )
    # création du dictionnaire inverse. entier -> valeur d'enum
    dictReverse = dict( zip(listValueNumbers, listValueNames) )
    # ajout du dictionnaire inverse dans les attributs
    dictAttrib["dictReverse"] = dictReverse
    # création et renvoyage du type
    mainType = type(enumName, (), dictAttrib)
    return mainType
   