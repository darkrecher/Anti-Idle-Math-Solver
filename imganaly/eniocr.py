﻿# -*- coding: utf-8 -*-

""" 
créé par Réchèr. Licence CC-BY ou Art Libre.
https://github.com/darkrecher/Anti-Idle-Math-Solver
je prends les bitcoins : 12wF4PWLeVAoaU1ozD1cnQprSiKr6dYW1G

Module contenant la classe EnigmaOcr, qui tente de reconnaître les symboles et
le gros opérateur trouvés dans une zone d'énigme, afin d'en déduire le texte 
de l'énigme.

Mode d'emploi
=============
Instancier une classe EnigmaOcr.

Première reconnaissance des symboles
------------------------------------

Exécuter la fonction ocr_ify_enigma, en indiquant les paramètres requis 
 - listes des symboles situés avant le gros opérateur.
 - RGB de la couleur de fond du gros opérateur. (None si pas de gros op.)
 - listes des symboles situés après le gros opérateur. (liste vide si pas de
   gros op.)

Les listes de symboles sont créées à partir des listes de "raw_symbol",
qui sont renvoyées par la classe SymbolExtractor. (voir module symbextr.py).

Après exécution de ocr_ify_enigma, la variable membre "enigma_text" contient
le texte de l'énigme déduit.

Si ocr_ify_enigma a renvoyé True, enigma_text ne comporte aucun point 
d'exclamation, l'énigme est solvable immédiatement. 

Si ocr_ify_enigma a renvoyé False, il faudra trouver une aide extérieure pour 
remplacer les points d'exclamation par les vrais symboles de l'énigme, 
qui n'ont pas pu être reconnu. En général, l'aide extérieur, c'est le joueur,
mais si c'est autre chose (TRIP: un bœuf musqué, une salade, ...) 
c'est bien aussi.

Prise en compte de l'aide extérieure
------------------------------------

Si on a un texte d'énigme avec des points d'exclamation, et qu'on a trouvé
une aide extérieure, on peut appeler la fonction record_enigma_text_complete.

Le paramètre à passer à cette fonction peut être de deux formes différentes :

1) une chaîne de caractère, de longueur égale au texte de l'énigme, point
d'exclamation compris. 
Exemple : texte d'énigme : (8+!)*!=?
          texte d'aide   : (8+5)*3=?
La fonction fait la correspondance : 5 <=> 1er point d'exclamation, et 
3 <=> 2ème. Elle ajoute ces nouveaux symboles dans sa bibliothèque.
Les autres caractères du texte d'aide ne sont pas utilisés. Si ils ne sont pas
égaux au texte d'énigme, ça ne fait rien. Aucun contrôle n'est fait dessus.

2) une chaîne de caractère, avec autant de caractère qu'il y a de points 
d'exclamation dans le texte d'énigme.
Exemple : texte d'énigme : (8+!)*!=?
          texte d'aide   : 53

Si on n'est dans aucun de ces 2 cas, la fonction ne fait rien.

La fonction ne renvoie aucune valeur. Elle se contente d'ajouter (ou pas) des
symboles dans sa bibliothèque. Pour vérifier si ça a marché, il faut
re-exécuter ocr_ify_enigma, avec les mêmes paramètre que la 1ère
fois. Les ajouts dans la bibliothèque devraient permettre, cette fois-ci, de 
trouver la "signifiance" de tous les symboles.

Si le texte d'aide passé en paramètre à record_enigma_text_complete ne 
contient pas les bons symboles à la place des points d'exclamation, on ne peut
pas s'en apercevoir. On se retrouve avec des symboles erronés dans la 
bibliothèque, et la suite du fonctionnement du script n'est pas garantie.

Fonctionnement interne
======================

Lors de l'instanciation, on crée une bibliothèque de symboles, et on la
remplit avec les définitions de symboles connnues (dans symbdata.py).

ocr_ify_enigma
--------------
C'est pas très compliqué. Pour chaque symbole des deux listes passées en 
paramètre, on essaie de trouver la signifiance correspondante, à l'aide
de la bibliothèque de symboles. (voir symbref.py).

On déduit la signifiance du gros opérateur à partir de la couleur de fond
passée en paramètre.

Avec tout ça, on définit 2 variables membres : list_symbol et 
list_signifiance. Ces deux listes ont le même nombre d'éléments. 
Dans list_symbol, on a tous les symboles de l'énigme : 
les symboles avant le gros opérateur + un symbole bidon pour prendre la place
du gros op + les symboles après le gros op.
Dans list_signifiance, on a toutes les signifiances correspondants à chaque
symbole, et au gros opérateur, le tout dans le même ordre. Il peut y avoir
des points d'exclamation dans ces signifiances.

Le texte de l'énigme est constitué de tous les caractères de list_signifiance,
mis bout à bout.

record_enigma_text_complete
---------------------------
Voir commentaire dans le code, parce que l'algo est un peu compliqué.

cas de "plusieurs fois le même symbole inconnu dans une énigme"
---------------------------------------------------------------
Exemple. L'énigme en cours est : 3+3=?
Les "3" sont dessinés exactement pareils. Ils correspondent donc au même 
symbole. Mais ce symbole est encore inconnu dans la bibliothèque.
Après première analyse, le texte de l'énigme est donc : !+!=?
On envoie ce texte au joueur. Il répond : "33". Ce qui est bien.

On fait correspondre les deux "3" avec les deux points d'exclamation.
Dans la bibliothèque des symboles, on ajoute une première fois le symbole "3",
avec sa signifiance. On tente de l'ajouter une deuxième fois, mais c'est 
refusé par la bibliothèque de symbole. Car elle le connait déjà. La fonction
symbref.SymbolReferences.add_reference va logger le texte : 
"Demande d'ajout d'un symbole existant"

Si le joueur répond une connerie, par exemple : "34". Le deuxième ajout de 
symbole sera refusé par la bibliothèque, à plus forte raison que c'est pas la
même signifiance, pour un même dessin. La fonction 
symbref.SymbolReferences.add_reference va logger le texte : 
"Demande d'ajout d'un symbole existant mais pas pareil"

Et si le joueur répond une méga-connerie, par exemple : "44", alors ça va 
pourrir la bibliothèque de symbole. Mais là on peut rien pour lui. S'il sait
pas lire...
"""

from log import log, msg
from symbol import Symbol
from symbref import SymbolReferences

class EnigmaOcr():
    """Ouais bon, c'est pas du tout de l'OCR, mais fallait bien que je trouve
    un nom. non de non."""
    
    DICT_OPERATOR_FROM_EXACT_RGB = {
        (76, 140, 76) : "+",
        (140, 76, 76) : "-",
        (140, 140, 76) : "*",
        (76, 76, 140) : "/",
    }
    
    def __init__(self):
        self.symbole_references = SymbolReferences()
            
    def ocr_ify_enigma(self, list_symbol_before, rgb_big_op, list_symbol_after):
        self.list_symbol = []
        self.list_signifiance = []
        
        list_signifiance_before = [ 
            self.symbole_references.find_signifiance(symb)
            for symb in list_symbol_before ]
        self.list_symbol.extend(list_symbol_before)
        self.list_signifiance.extend(list_signifiance_before)
        
        if rgb_big_op is not None:
            # osef, c'est juste pour avoir list_symbol et list_signifiance
            # cohérentes entre elles.
            symb_big_op = Symbol() 
            signifiance_big_op = self.DICT_OPERATOR_FROM_EXACT_RGB.get(
                rgb_big_op, 
                "!")
            self.list_symbol.append(symb_big_op)
            self.list_signifiance.append(signifiance_big_op)
        
        list_signifiance_after = [ 
            self.symbole_references.find_signifiance(symb)
            for symb in list_symbol_after ]
        self.list_symbol.extend(list_symbol_after)
        self.list_signifiance.extend(list_signifiance_after)
        
        self.enigma_text = "".join(self.list_signifiance)
        # TODO : foutre ce putain de point d'exclamation en constante globale.
        return "!" not in self.enigma_text
    
    # TODO : le nom de cette fonction est pas très bien choisi.    
    # TODO : renvoyer True/False pour dire si tout s'est bien passé ou pas.
    def record_enigma_text_complete(self, enigma_text_help):
        # Le but de ce premier gros tas de code est d'initialser la variable 
        # list_symb_and_sig_help. Il s'agit d'une liste de couple. Comme son
        # nom l'indique, chaque couple contient deux éléments :
        #  - Un symbole de l'énigme, un de ceux dont on n'a pas pu trouver
        #    la signifiance. (Il correspond actuellement à un point
        #    d'exclamation.
        #  - Un caractère, extrait du paramètre enigma_text_help. Ce 
        #    caractère est la signifiance à donner au symbole, que le joueur
        #    a gentiment bien voulu saisir.
        if len(enigma_text_help) == len(self.enigma_text):
            # Le joueur a resaisi tout le texte de l'énigme en entier.
            # Construction d'une liste de trouple : 
            #  - symbole de l'énigme.
            #  - signifiance du symbole, trouvée lors de la première 
            #    reconnaissance. Y'en a qui sont des points d'exclamation,
            #    y'en a des qui sont pas.
            #  - signifiance du symbole, donnée par le joueur.
            list_symb_and_sig_and_sig_help = zip(
                self.list_symbol, 
                self.list_signifiance, 
                list(enigma_text_help))
            # On vire de cette liste de trouple tout ce qui est déjà connu,
            # et on ne garde que le symbole et la signifiance donnée par le
            # joueur.
            list_symb_and_sig_help = [
                (symb, sig_help) 
                for (symb, sig_cur, sig_help) 
                in list_symb_and_sig_and_sig_help
                if sig_cur == "!" ]
        else:
            # Le joueur a, à priori, saisi uniquement les caractères inconnus.
            # Mais on n'en est pas si sûr.
            list_symb_and_sig = zip(self.list_symbol, self.list_signifiance)
            list_symb_and_sig_unknown = [ 
                symb_and_sig for symb_and_sig in list_symb_and_sig 
                if symb_and_sig[1] == "!" ]
            # list_symb_unknown contient la liste des symboles dont on ne 
            # connait pas encore la signifiance.
            list_symb_unknown = [ 
                symb_and_sig[0] for symb_and_sig 
                in list_symb_and_sig_unknown ]
            if len(list_symb_unknown) != len(enigma_text_help):
                # Le joueur a saisi un nombre de caractère différent du nombre
                # de symbole inconnus. C'est foutu, on ne peut rien en faire.
                msg("nb de car different du nb de symb qu'il faut determiner")
                return
            # On peut faire correspondre chaque symbole inconnu avec un 
            # caractère saisi par le joueur. Youpi !!
            list_symb_and_sig_help = zip(
                list_symb_unknown, 
                list(enigma_text_help))
                
        # Arrivé ici, on a initialisé la variable list_symb_and_sig_help.
        # C'est cool. Y'a plus qu'à contrôler les caractères de signifiance,
        # à assigner chaque caractère à chaque symbole, et à foutre le tout 
        # dans la bibliothèque, qui pourra les utiliser la prochaine fois.
        for (symb, sig_help) in list_symb_and_sig_help:
            if sig_help not in "0123456789/*-+=?x(),":
                msg("caractere incorrect dans la saisie : ", sig_help)
            else:
                if sig_help == "x":
                    sig_help = "*"
                symb.assign_signifiance(sig_help)
                self.symbole_references.add_reference(symb)
