# -*- coding: utf-8 -*-

""" 
créé par Réchèr. Licence CC-BY ou Art Libre.
https://github.com/darkrecher/Anti-Idle-Math-Solver
je prends les bitcoins : 12wF4PWLeVAoaU1ozD1cnQprSiKr6dYW1G

Module contenant la classe EnigmaZoneDetector, qui détermine la position de
la zone d'énigme affinée, en fonction de la zone d'énigme brute.

Mode d'emploi
=============
Détectez la zone d'énigme brute, à l'aide de la classe GameRectDetector.
Effectuez une capture d'écran de cette zone (pas tout l'écran, faut vraiment
prendre que la zone brute, sinon ça marchera pas).
Créez une instance de EnigmaZoneDetector.
Appeler la méthode detect_enigma_zone, en passant comme paramètres : le dc de 
la capture d'écran et ses dimensions.
Si la fonction renvoie True, la détection a bien fonctionnée. Il y a bien des
choses dignes d'intérêt dans le dc fourni. Sinon, y'a que de la daube.
Lorsque la fonction renvoie True, la zone brute a éventuellement été rognée en
haut et en bas. 
La variable membre y_proc_ez_top indique combien de lignes de pixels ont été
rognées en haut.
La variable membre y_proc_ez_bottom indique l'ordonnée de la plus basse ligne
restante, après le rognage par le bas.
La variable membre y_size_proc_ez indique la hauteur de la zone d'énigme 
affinée. 

Fonctionnement interne
======================

On commence par faire une petite vérification rapide de ce que contient la 
zone passée en paramètre. Bon en fait on teste juste le pixel inférieur 
gauche. Il doit être de la couleur de fond de la zone d'énigme. 
C'est à dire : RGB = (0, 0, 102).

On ne vérifie pas le coin supérieur gauche comme on ferait d'habitude, car 
en haut de la zone, il peut y avoir des pixels bleus clair, affichant des
indices pour le joueur.

Ensuite, on rogne les lignes en partant du haut, puis du bas.

Une ligne est rognée si elle ne contient aucun pixel intéressant. Un pixel est
intéressant si il est suffisamment jaune ou blanc <=> il fait partie du 
dessin d'un symbole.

"suffisamment jaune ou blanc", ça veut dire :
 - Soit le pixel est blanc, dans ce cas : red = green = blue
 - Soit le pixel est jaune, dans ce cas : red = green
 - Il faut en avoir "suffisamment", j'ai décidé arbitrairement que ça 
   correspondait à au moins 100 de red et de green.

Pour simplifier, on ne teste jamais la couleur bleue. On s'en branle que le
pixel soit jaune ou blanc, faut juste qu'il soit l'un des deux.

Si on rogne l'ensemble des lignes de la zone brute d'énigme, c'est un échec,
la zone ne contient rien d'intéressant. Dans ce cas, la fonction 
detect_enigma_zone renverra False.
"""

from log import log

class EnigmaZoneDetector():
    """ 
    """

    RGB_EXACT_ENIGMA_ZONE = (0, 0, 102)
    
    def __init__(self):
        pass
        
    # TODO : putain, homogénéité des x_size_truc et x_truc_size
    def detect_enigma_zone(self, dc_raw_enigma_zone, x_size_rez, y_size_rez):
        self.x_size_rez = x_size_rez
        self.y_size_rez = y_size_rez
        self.dc_raw_enigma_zone = dc_raw_enigma_zone
        # Vérifie la couleur du coin inférieur gauche.
        if self._get_pixel(x_size_rez-1, 0) != self.RGB_EXACT_ENIGMA_ZONE:
            return False
        # Rognage par le haut
        self.y_proc_ez_top = self._crop_lines(0, +1, self.y_size_rez-1)
        log("self.y_proc_ez_top", self.y_proc_ez_top)
        # Rognage par le bas
        self.y_proc_ez_bottom = self._crop_lines(self.y_size_rez-1, -1, 0)
        self.y_size_proc_ez = self.y_proc_ez_bottom - self.y_proc_ez_top + 1
        log("self.y_size_proc_ez", self.y_size_proc_ez)
        return self.y_size_proc_ez > 0
        
    def _get_pixel(self, x, y):
        return self.dc_raw_enigma_zone.GetPixel(x, y)[0:3]
        
    def _is_pixel_interesting(self, x, y):
        (red, grn, blu) = self._get_pixel(x, y)
        return red > 100 and red == grn
        
    def _is_line_interesting(self, y):
        return any( 
            ( self._is_pixel_interesting(x, y) 
              for x in range(self.x_size_rez) ) )

    def _crop_lines(self, y_start, direction, y_end):
        y_cur = y_start
        while not self._is_line_interesting(y_cur) and y_cur != y_end:
            y_cur += direction
        return y_cur
        