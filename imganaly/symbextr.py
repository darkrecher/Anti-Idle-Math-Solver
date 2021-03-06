﻿# -*- coding: utf-8 -*-

"""
créé par Réchèr. Licence CC-BY ou Art Libre.
https://github.com/darkrecher/Anti-Idle-Math-Solver
je prends les bitcoins : 12wF4PWLeVAoaU1ozD1cnQprSiKr6dYW1G

Module contenant la classe SymbolExtractor, qui extrait les symboles et le 
gros opérateur d'une zone d'énigme, et qui permet également de savoir si une 
nouvelle énigme s'est affichée dans la zone.

Mode d'emploi
=============

Extraction de symboles
----------------------
Instancier un SymbolExtractor.

Exécuter la fonction extract_symbols_data, en passant en paramètre le dc de la
zone d'énigme, et ses dimensions width et height. (voir module gamedtc.py et 
enizodtc.py pour détecter une zone d'énigme). La fonction va tenter de 
détecter l'éventuelle présence du gros opérateur, ainsi que les dessins de 
symbole situés avant et après. 

Les dessins de symbole se récupèrent  sous la forme de "raw_symbol" (tableaux 
brut, en 2D, de valeurs d'encre). On pourra créer des objets Symbole à partir 
de ces tableaux bruts (voir module symbole.py).

Après l'appel à extract_symbols_data, le résultat est placé dans les 3 
variables membres suivantes :
 - list_raw_symbols_before : raw_symbol trouvés avant le gros opérateur.
 - rgb_big_op : trouple de valeur (red, green, blue), correspondant à la 
   couleur de fond du gros opérateur. (on ne récupère pas le symbole du gros
   opérateur, car y'en n'a pas besoin).
 - list_raw_symbols_after : raw_symbol trouvés après le gros opérateur.

Si la zone d'énigme ne contient pas de gros opérateur, la variables rgb_big_op
vaut None, et list_raw_symbols_after vaut une chaîne vide. Tous les symboles
trouvés sont dans list_raw_symbols_before.

Détection de changements dans la zone d'énigme
----------------------------------------------
Après avoir instancié un SymbolExtractor et exécuté une première fois la 
fonction extract_symbols_data, la classe conserve en mémoire le dc qu'on lui
a passé en paramètre.

On peut alors exécuter la fonction is_new_image, en passant en paramètre une
nouvelle capture d'écran de la zone d'énigme. (Pas besoin de redonner les
dimensions, on garde celles indiqués lors de l'exécution de 
extract_symbols_data). La fonction cherche si il y a eu un quelconque 
changement dans les pixels, entre la zone d'énigme utilisée lors de la 
détection de symbole, et la nouvelle zone d'énigme passée en paramètre. Elle
renvoie un booléen. True : il y a eu un changement, False, y'en n'a pas eu.

Fonctionnement interne
======================

Détection du gros opérateur
---------------------------
Cette action est effectuée par la fonction _detect_big_op.

On doit détecter la zone de pixel dans laquelle se trouve le gros opérateur. 
Celui-ci est dans un cadre, avec une couleur de fond spécifique. Le cadre 
prend toute la hauteur de la zone d'énigme (et même un peu plus, mais osef). 

Les couleurs possibles, pour le fond des gros opérateur, sont les suivantes : 
RGB = (76, 140, 76) ou (140, 76, 76) ou (140, 140, 76) ou (76, 76, 140).
On se prend pas la tête, et on établit qu'un pixel est un fond de gros 
opérateur si toutes ses composantes RGB valent 76 ou 140.

Un gros opérateur s'affiche avec une bordure d'une certaine couleur, et d'une 
certaine épaisseur. Il faut essayer de faire abstraction de cette bordure, car
elle n'est peut-être pas pareil selon la résolution d'écran.

Donc voici comment on fait :
On se positionne à y="milieu de la zone d'énigme".
On avance, à partir de x=0, en allant vers la droite. On analyse les couleurs
des pixels rencontrés.
Dès qu'on trouve une couleur de fond de gros opérateur, on enregistre la 
position x actuelle, et on passe à l'étape suivante.
À partir de cette position x, on recule jusqu'à retrouver la couleur de fond
de zone d'énigme. Cela permet de passer la bordure gauche du cadre du gros
opérateur. On enregistre la position atteinte dans la variable membre 
x_big_op_start. 
On repart de la position actuelle, et on va vers la droite, jusqu'à retrouver
la couleur de fond de zone d'énigme. Cela permet de passer le fond du gros
opérateur, le symbole du gros opérateur (on s'en tape), et la bordure de 
droite.  On enregistre la position atteinte dans x_big_op_end.
Et si on n'est arrivé jusqu'au bout de la zone d'énigme sans rencontrer de 
couleur de fond de gros opérateur, on considère que y'en n'a pas.

Conversion couleur -> encre
-------------------------------
Cette action est effectuée par la fonction _get_ink_of_pixel.

Les symboles sont affichés à l'écran en jaune ou en blanc, avec un détourage
noir, le tout sur le fond bleu de la zone d'énigme. Tout ça se mélange un peu
et donne des pixels de couleur différente. Pour les dessins de symboles, on
ne s'intéresse pas au fond ni au détourage. 

L'encre représente la quantité de jaune/blanc dans un pixel. 
 - Si red = green = blue, alors le pixel est blanc. La quantité de blanc
   peut être représenté par la composante red. ink = red.
 - Si red = green, alors le pixel est jaune. La quantité de jaune peut être
   représentée par la composante red. ink = red
 - Si red != green, le pixel est une autre couleur. Dans ce cas on s'en branle
   et ink = 0.

Un pixel est intéressant si il est jaune ou blanc, et que son encre est 
supérieure à 100.

Attention, y'a une subtilité, un pixel peut avoir une valeur d'encre, et ne
pas être considéré comme intéressant, car l'encre est trop faible.

Extraction des symboles
-----------------------
Cette action est effectuée par la fonction _extract_columord_symbols. Elle est
effectuée après la détection du gros opérateur.

Si le gros opérateur n'est pas présent, on extrait les symboles sur toute la
zone d'énigme. Sinon, on les extrait sur les deux morceaux de zones, situés
avant et après le gros opérateur. La méthode est la suivante :

On part de x=0, et on inspecte les pixels colonne par colonne. Si on
trouve plusieurs colonnes de pixels consécutives, contenant au moins un pixel
intéressant, alors cela constitue le dessin d'un symbole.

Au passage, ce parcours permet de fixer la valeur de la variable membre
x_first_interesting_column. Contient l'absisse de la première colonne
contenant au moins un pixel intéressant. (On en a besoin pour plus tard).

À chaque fois qu'on trouve, ne serait-ce qu'une seule colonne, ne contenant
aucun pixel intéressant, cette ou ces colonnes constitue une séparation entre
deux symboles différents.

Quand on extrait un symbole, on prend les encres de tous les pixels, y compris
ceux qui ne sont pas intéressant. Dans le tableau des valeurs d'encre, on 
peut donc avoir des nombres inférieurs à 100. Par contre, y'a aucune colonne
ne contenant que des nombres inférieurs à 100. Ça veut dire qu'on rogne le
détourage sur les côtés, mais on rogne pas le détourage interne. Oui je sais,
on s'en fout complètement et c'est juste un détail à la con. Mais je tenais à
le dire, pour bien montrer que j'ai pensé à tous, et que j'ai prévu toutes les
conséquences, même minimes, de mes supers algorithmes de *teuheu teuheu* 
analyse d'image.

Pendant que j'y suis à être verbeux sur les détails : la fonction 
_extract_columord_symbols renvoie une liste de "columord_symbol". C'est à dire
des tableaux 2D de valeurs d'encres, mais rangés par colonne. (Puisque pour
l'extraction, on avance colonne par colonne). Un columord_symbol est une liste
de liste d'entiers. Chaque entier est une encre. Chaque liste d'entier est une
colonne (et non pas une ligne). Le tableau est une ligne de colonne. 

Conversion "columord_symbol" -> "raw_symbol"
--------------------------------------------
Cette action est effectuée directement dans la fonction extract_symbols_data.
On fait une rotation à 90 degrés des tableaux 2D. Du coup c'est rangé par 
ligne, et ce sera plus facile pour virer les lignes ne contenant que des 
encres valant 0. (Mais cette tâche est effectuée par un autre bout de code).

Détection de changement dans la zone d'énigme
---------------------------------------------
Cette action est réalisée par la fonction extract_symbols_data. 

Bon c'est pas compliqué. Y'a deux dc : celui enregistré lors de la dernière
exécution de extract_symbols_data, et le nouveau passé en paramètre. Si y'a un
pixel avec une couleur différente (même un tout petit peu), on considère qu'il
y a eu un changement.

En fait on se prend pas la tête, on n'inspecte qu'une colonne sur 3, et qu'une
ligne sur 2. De toutes façons si le texte d'énigme change, l'impact est censé
être suffisamment étendu, et on le détectera forcément même en n'inspectant
pas tous les pixels.

de plus, pour détecter plus vite les changements, on ne parcourt pas les 
colonne en partant de x=0 jusqu'à x=size-1. Mais on part de 
x=x_first_interesting_column jusqu'à x=size-1. Puis on repart à l'envers, 
de x=0 jusqu'à x=x_first_interesting_column. car si y'a un changement, il a 
plus de chances d'être près des pixels intéressants, plutôt que sur les bords
droits ou gauche de la zone d'énigme, où il ne se passe pas grand-chose.

TRIP: Putain il étail long le blablatage verbeux de ce module. Pas fâché de
l'avoir fini bordel à queue !
"""

from log import log


class SymbolExtractor():
    """ 
    """
    
    # TODO : factoriser ça
    RGB_EXACT_ENIGMA_ZONE = (0, 0, 102)
    
    def __init__(self):
        pass
        
    # TODO : la taille change jamais. Faut la donner une seule fois au début.
    def extract_symbols_data(self, dc_enigma_zone, x_size_ez, y_size_ez):
        """ crée des symboles "raw". C'est à dire qu'il peut y avoir des 
        lignes vides au dessus et en dessous."""
        self.x_size_ez = x_size_ez
        self.y_size_ez = y_size_ez
        self.dc_enigma_zone = dc_enigma_zone
        # colonne, dans le dc d'une enigma zone, à partir de laquelle est 
        # dessiné le gros opérateur. (peut rester None si pas de gros
        # opérateur dans l'énigme).
        self.x_big_op_start = None
        # colonne, dans le dc d'une enigma zone, jusqu'à laquelle est 
        # dessiné le gros opérateur. (peut aussi rester None).
        self.x_big_op_end = None
        self.rgb_big_op = None
        # liste des symboles présents avant le gros opérateur.
        self.list_raw_symbols_before = []
        # liste des symboles présents après le gros opérateur. (reste vide
        # si pas de gros opérateur dans l'énigme).
        self.list_raw_symbols_after = []
        self.x_first_interesting_column = None
        
        self._detect_big_op()
        log(self.x_big_op_start, self.x_big_op_end, self.rgb_big_op)
        if self.rgb_big_op is not None:
            list_columord_symbols_before = self._extract_columord_symbols(
                0, self.x_big_op_start)
            list_columord_symbols_after = self._extract_columord_symbols(
                self.x_big_op_end+1, self.x_size_ez)
        else:
            list_columord_symbols_before = self._extract_columord_symbols(
                0, self.x_size_ez)
            list_columord_symbols_after = []
            
        # réordonnancement des valeurs d'ink, dans les symboles. 
        # Au lieu qu'ils soient par colonne, on les met par lignes.
        self.list_raw_symbols_before = [ 
            zip(*columord_symb) 
            for columord_symb in list_columord_symbols_before ]
        self.list_raw_symbols_after = [ 
            zip(*columord_symb) 
            for columord_symb in list_columord_symbols_after ]
        
    # TODO : n'a pas grand chose à faire là. Ça devrait être dans 
    # une classe dédiée. (avec des step X et Y configurables)
    def is_new_image(self, dc_refreshed):
        for x in xrange(self.x_first_interesting_column, self.x_size_ez, 3):
            for y in xrange(0, self.y_size_ez, 2):
                rgb_refreshed = dc_refreshed.GetPixel(x, y)[0:3]
                rgb_cur = self._get_pixel(x, y)
                if rgb_refreshed != rgb_cur:
                    return True
        # TODO : vilain copier-coller
        for x in xrange(self.x_first_interesting_column, 0, -3):
            for y in xrange(0, self.y_size_ez, 2):
                rgb_refreshed = dc_refreshed.GetPixel(x, y)[0:3]
                rgb_cur = self._get_pixel(x, y)
                if rgb_refreshed != rgb_cur:
                    return True        
        return False
        
    # TODO : factoriser ça avec les autres classes.
    def _get_pixel(self, x, y):
        return self.dc_enigma_zone.GetPixel(x, y)[0:3]
        
    # TODO : factoriser ça aussi.
    def _is_pixel_interesting(self, x, y):
        (red, grn, blu) = self._get_pixel(x, y)
        return red > 100 and red == grn
    
    def _get_ink_of_pixel(self, x, y):
        (red, grn, blu) = self._get_pixel(x, y)
        # Attention, c'est pas tout à fait pareil que _is_pixel_interesting.
        # On vérifie pas si c'est plus de 100. 
        if red == grn:
            return red
        else:
            return 0
    
    def _get_column_ink(self, x):
        return [ 
            self._get_ink_of_pixel(x, y_cur) 
            for y_cur in xrange(0, self.y_size_ez) ]
    
    # TODO : une classe commune SymbolExtractor + EnigmaZoneDetector
    # Avec ces fonctions de base dedans.
    def _is_column_interesting(self, x):
        return any( 
            ( self._is_pixel_interesting(x, y) 
              for y in range(self.y_size_ez) ) )
        
    # TODO : oulala, c'est pas bien ça. Pas cohérent avec le dictionnaire 
    # eniocr.EnigmaOcr.DICT_OPERATOR_FROM_EXACT_RGB.
    # Par exemple, la couleur (76, 76, 76), est true d'après is_rgb_big_op.
    # Mais elle n'est pas définie dans le DICT_OPERATOR_FROM_EXACT_RGB ! 
    # Du coup on va se retrouver avec des couleurs qu'on croit que c'est du 
    # gros opérateur, alors que pas du tout. Et ça peut tout faire péter.
    def is_rgb_big_op(self, rgb):
        return all( ( comp_rgb in (76, 140) for comp_rgb in rgb) )
        
    # TODO : fonction générique find_first ? 
    # on recule/avance sur une ligne/colonne, jusqu'à rencontrer un pixel 
    # qui correspond à une condition, passée en paramètre.
    def _detect_big_op(self):
        y = self.y_size_ez / 2
        # TODO : renommer x_cur en x_cursor.
        x_cur = 0
        # Putain, pourquoi y'a pas de repeat until comme en Pascal ? 
        # C'était cool ce truc.
        while True:
            rgb_cur = self._get_pixel(x_cur, 0)
            if self.is_rgb_big_op(rgb_cur):
                break
            x_cur += 1
            if x_cur >= self.x_size_ez:
                return False
        
        self.rgb_big_op = rgb_cur
        x_rgb_big_op = x_cur
        while self._get_pixel(x_cur, 0) != self.RGB_EXACT_ENIGMA_ZONE:
            x_cur -= 1
        self.x_big_op_start = x_cur + 1
        x_cur = x_rgb_big_op 
        while self._get_pixel(x_cur, 0) != self.RGB_EXACT_ENIGMA_ZONE:
            x_cur += 1
        self.x_big_op_end = x_cur - 1
        return True
    
    def _extract_columord_symbols(self, x_start, x_end):
        """ columord symbols = column ordered symbols.
        C'est à dire : les symboles, dont les encres sont rangées par colonne.
        """
        # bourrin. On checke tous les pixels. On stock au fur et à mesure.
        # TRIP: j'ai toujours trouvé bizarre ce mot : "fur". D'où il vient ?
        list_column_inks_of_current_symbol = []
        list_columord_symbols = []
        inside_symbol = False
        
        for x_cur in xrange(x_start, x_end):
            if self._is_column_interesting(x_cur):
                if self.x_first_interesting_column is None:
                    self.x_first_interesting_column = x_cur
                inside_symbol = True
                column_ink = self._get_column_ink(x_cur)
                list_column_inks_of_current_symbol.append(column_ink)
            else:
                if inside_symbol:
                    list_columord_symbols.append(
                        list_column_inks_of_current_symbol)
                    list_column_inks_of_current_symbol = []
                    inside_symbol = False
                    
        if inside_symbol:
            list_columord_symbols.append(
                list_column_inks_of_current_symbol)
                
        return list_columord_symbols        
    
    