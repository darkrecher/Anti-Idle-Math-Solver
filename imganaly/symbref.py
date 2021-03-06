﻿# -*- coding: utf-8 -*-

""" 
créé par Réchèr. Licence CC-BY ou Art Libre.
https://github.com/darkrecher/Anti-Idle-Math-Solver
je prends les bitcoins : 12wF4PWLeVAoaU1ozD1cnQprSiKr6dYW1G

Module définissant la classe SymbolReferences. Cette classe charge la 
bibliothèque des symboles connus, et fait la correspondance entre un symbole 
dans une énigme, et um symbole de la bibliothèque.

Mode d'emploi
=============
Instancier une classe SymbolReferences. La bibliothèque de symbole connus,
sitée dans le module symbdata.py se charge automatiquement.

Exécuter la fonction find_signifiance pour connaître la signification d'un
symbole inconnu.
Exécuter la fonction add_reference pour ajouter un symbole dans la 
bibliothèque.
À la fin du script, exécuter la fonction msg_newly_added_symbols, pour
balancer sur la sortie standard tous les symboles nouvellement ajoutés via la
fonction add_reference. C'est à l'utilisateur de copier-coller ces symboles 
dans symbdata.py.

Fonctionnement interne
======================
Ouais c'est pas bien compliqué. Voir les docstring de chaque fonction.
"""

from log import log, msg
from symbdata import LIST_SYMB_ALARRACHE
from imganaly.symbol import Symbol

class SymbolReferences():

    def __init__(self):
        """
        Fonction init.
        Initialise la variable membre list_references. Il s'agit d'une liste
        de Symbol. Ils sont créés à partir des symboles connus, trouvés dans 
        le module symbdata.py
        """
        self.list_references = [ 
            Symbol(saved_data=saved_data) 
            for saved_data in LIST_SYMB_ALARRACHE ]
        
    def find_signifiance(self, symbol):
        """
        :param symbol: objet Symbol. Sa signifiance est, à priori, non définie
        (si elle l'est, ça sert à rien d'appeler cette fonction !)
        
        Cherche dans la bibliothèque de symboles connus si on n'en retrouve 
        pas un qui aurait le même dessin que celui passé en paramètre. Si oui,
        la fonction renvoie la signifiance du symbole de la bibliothèque.
        
        Si non, la fonction renvoie le caractère "!", qui représente, par
        convention, une signifiance inconnue.
        
        Lors de la recherche dans les symboles connus, on ne retient que celui
        dont le dessin sera exactement pareil que le symbole passé en param.
        Il faut que les dimensions largeur et hauteurs soient les mêmes, et
        que le tableau des valeurs d'encres soient exactement les mêmes aussi.
        """
        for symb_ref in self.list_references:
            if self._is_same_symbol(symb_ref, symbol):
                return symb_ref.signifiance
        return "!"
        
    def add_reference(self, new_symb_ref):
        """
        :param symbol: objet Symbol. Sa signifiance doit être définie. Sinon
        on pourrit la bibliothèque avec des conneries inutiles.
        
        Ajoute un symbole dans la bibliothèque des symboles connus.
        
        On a le droit d'ajouter plusieurs symboles ayant la même signifiance,
        mais des dessins différents. (Et heureusement, parce que ce cas 
        arrive très souvent dans le jeu).
        
        On n'a pas le droit d'ajouter plusieurs symboles ayant le même dessin.
        Si on essaye d'ajouter plusieurs fois de suite un symbole ayant le
        même dessin et la même signifiance, ce n'est pas un cas d'erreur.
        Mais c'est refusé quand même, et une ligne de log est émise.
        
        Si on essaye d'ajouter plusieurs fois un symbole ayant le même dessin, 
        mais des signifiance différentes, c'est un cas d'erreur. C'est refusé,
        et une ligne de log est également émise.
        
        Ouais du coup, les cas d'erreur et les cas de pas-erreur ne sont pas
        vraiment distingués. On s'en fout, l'utilisateur se démerde avec le
        contenu du log. De toutes façons c'est de sa faute s'il essaie 
        d'ajouter des symboles de mêmes dessins et de pas-mêmes signifiance.
        """
        existing_signifiance = self.find_signifiance(new_symb_ref)
        if existing_signifiance == "!":
            self.list_references.append(new_symb_ref)
            return
        else:
            if existing_signifiance == new_symb_ref.signifiance:
                log(
                    "Demande d'ajout d'un symbole existant :", 
                    existing_signifiance)
            else:
                log(
                    "Demande d'ajout d'un symbole existant mais pas pareil",
                    existing_signifiance,
                    "!=",
                    new_symb_ref.signifiance)
                      
    def msg_newly_added_symbols(self):
        """
        Écrit, sur la sortie standard, la définition de tous les symboles
        qui ont été ajoutés, durant l'exécution courante du script, par la
        fonction add_reference.
        
        Le format des chaînes de caratères écrites en sortie correspond à
        celui décrit dans le module symbdata.py.
        """
        for symb in self.list_references:
            if symb.comes_from_raw_symbol:
                msg(str(symb))
                msg("#" * 10)
    
    def _is_same_symbol(self, symb_1, symb_2):
        """
        Compare les dessins de deux symboles (mais pas les signifiance). 
        Ils viennent de n'importe où, de la bibliothèque ou d'ailleurs, osef,
        on les compare.
        
        Renvoie True si les dessins sont exactement pareils, sinon, renvoie
        False. 
        TRIP: Voili voilà, voyez. Captain Obvious, tout ça...
        """
        if symb_1.width != symb_2.width or symb_1.height != symb_2.height:
            return False
        if symb_1.flat_list_ink != symb_2.flat_list_ink:
            return False
        return True
    
        