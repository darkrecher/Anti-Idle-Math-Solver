﻿# -*- coding: utf-8 -*-

""" 
créé par Réchèr. Licence CC-BY ou Art Libre.
https://github.com/darkrecher/Anti-Idle-Math-Solver
je prends les bitcoins : 12wF4PWLeVAoaU1ozD1cnQprSiKr6dYW1G

Module contenant la classe GameRectDetector, qui permet de repérer la position
et la taille de la zone de jeu à l'écran.

Mode d'emploi
=============

Effectuer une capture d'écran dans un wx.memoryDc.
Instancier une casse GameRectDetector, en lui passant en paramètre
le memoryDc et ses dimensions.

Appeler la fonction get_rect_raw_enigma_zone. Si la fonction renvoie True,
la détection de la zone de jeu a fonctionné. Dans ce cas, on peut récupérer 
les membres de l'instance : y_first_pattern, x_game_left, 
x_game_right, y_game_top, y_game_bottom, x_game_size, y_game_size.

Si la détection a fonctionné, on peut ensuite appeler la fonction
get_rect_raw_enigma_zone, qui renvoie un tuple de 4 valeurs, correspondant
au rectangle de la zone d'énigme brute.
Les valeurs du tuple sont : 
x_scr_rez_left, y_scr_rez_top, x_rez_size, y_rez_size

Les deux premières valeurs sont les coordonnées du coin supérieur gauche de 
la zone d'énigme brute. Elles sont définies par rapport au coin sup gauche
de l'écran, et non le coin sup gauche de la zone de jeu.

les deux dernières valeurs sont les dimensions de la zone d'énigme brute.

Fonctionnement interne (comme les tripes)
=========================================

Les lignes de pixels qui traverse la zone de jeu ont un motif spécifique, pour
plus de détail concernant ce motif, voir docstring de detect_line_pattern.

Lorsque le motif est présent, il permet de déduire la position des bords
gauche et droits de la zone de jeu.

Recherche de la 1ère ligne traversant la zone de jeu.
-----------------------------------------------------

Cette étape est réalisée par les fonctions detect_line_pattern et 
find_first_line_pattern.

On commence par chercher une première ligne de pixel, dans le dc de la capture
d'écran, qui posséderait ce motif. On regarde la ligne située au milieu de
l'écran. Puis celles situées au quart, aux deux quarts et aux trois quarts.
Puis celles situées aux huitième, deux huitièmes, etc...
Dès qu'on trouve une ligne contenant le motif, on arrête la recherche et on
passe à l'étape suivante.

Si on n'a toujours rien trouvé, même après avoir beaucoup diminué le pas de
déplacement, jusqu'à une certaine limite (en nombre absolu de pixel), on 
laisse tomber. La zone de jeu est introuvable, ou pas présente du tout, dans
la capture d'écran.

Recherche des bords haut et bas de la zone de jeu.
--------------------------------------------------

Cette étape est réalisée par les fonctions check_pattern et 
detect_line_pattern_limit.

Maintenant qu'on connait les bords gauche et droit, il est très rapide, sur
une ligne de pixel donnée, de vérifier si elle possède le motif ou pas. 

Pour une description précise de ce qu'on vérifie, voir docstring de 
check_pattern.

On part de y = y_de_la_ligne_de_pattern_trouvée. 
On commence par remonter. On fixe un pas y_step suffisamment grand, mais pas
trop (osef du pas initial). On avance de ce pas. 
Si on tombe sur une ligne respectant le motif, c'est cool. On garde ce y, et 
on avance du même pas.
Si on tombe sur une ligne ne respectant même pas le motif, c'est moins cool.
On divise le pas par deux, et on revient au y précédent. On aura peut-être 
plus de chances la prochaine fois.
Le pas diminue petit à petit, et le y remonte. Lorsque le pas est sur le point
d'atteindre 0, on fait obligatoirement une dernière remontée avec un pas de 1.
Quand c'est fini, on a trouvé le bord haut de l'aire de jeu.

Ensuite, on repart du y de départ, et on recommence en descendant, afin de 
trouver le le bord bas.

Vérification des proportions
----------------------------

Cette étape est réalisée directement dans la fonction detect_rect.

La proportion largeur / hauteur de la zone de jeu trouvée doit être égal à 
1.5370370, avec une marge de plus ou moins 0.1. Sinon, on ne considère pas
que les bords trouvés délimitent une zone de jeu, et on abandonne les
recherches. (Ça fait bizarre de dire "on abandonne les recherches").

Vérifications complètes des pixels sur les bords
------------------------------------------------

Cette étape est réalisée par la fonction check_game_border_colors.

On vérifie que tous les pixels des 4 bords de la zone de jeu sont tous de la
couleur gris foncé de la zone de jeu. Sinon, on abandonne.

Détermination de la zone d'énigme brute
---------------------------------------

Cette étape est réalisée par la fonction get_rect_raw_enigma_zone.
Rien de bien compliqué, on prend juste un rectangle situé à l'intérieur de
la zone de jeu, selon une position et une taille prédéfine, relative à la zone
de jeu.
"""

from log import log
from enum import enum
from colrtool import hsv_from_rgb, is_same_col

PATTERN_SEARCH_STATE = enum(
    "PATTERN_SEARCH_STATE",
    "NOTHING_FOUND",
    "BEFORE_LEFT_BORDER",
    "IN_GAME_COLOR_OK",
    "IN_GAME_COLOR_NO",
    "RIGHT_LIT_PIXEL",
    "AFTER_RIGHT_BORDER",
)

pss = PATTERN_SEARCH_STATE

class GameRectDetector():

    HSV_APPROX_EXTERN_BORDER = (32, 27, 23)
    # TRIP: 51 je t'aimeu, j'en boirais des tonneaux, 
    # à me rouler par terreu, dans tous les caniveaux
    RGB_EXACT_INSIDE_SQUARE = (51, 51, 51)
    RGB_EXACT_RIGHT_LIT_PIXEL = (102, 102, 102)
    STEP_Y_MIN_LIMIT_SEARCH_FIRST_PATTERN = 50
    PROPORTIONS = 1.5370370
    PROPORTIONS_MARGIN = 0.1    
    # REZ = Raw Enigma Zone
    RATIO_Y_REZ_TOP = 0.222222222   
    RATIO_Y_REZ_BOTTOM = 0.339506
    RATIO_X_REZ_LEFT = 0.05
    RATIO_X_REZ_RIGHT = 0.95
    
    def __init__(self, size_x_img, size_y_img, dc_img):
        self.dc_img = dc_img
        self.size_x_img = size_x_img
        self.size_y_img = size_y_img
        self.y_first_pattern = None
        self.x_game_left = None
        self.x_game_right = None
        self.y_game_top = None
        self.y_game_bottom = None
        self.x_game_size = None
        self.y_game_size = None
        self.square_detected = False
        
    # TODO : les param de la fonction init devrait être dans cette fonction.
    def detect_rect(self):
        if not self.find_first_line_pattern():
            log("first line pattern fail")
            return False
        self.y_game_top = self.detect_line_pattern_limit(-1)
        self.y_game_bottom = self.detect_line_pattern_limit(+1)
        self.x_game_size = self.x_game_right - self.x_game_left
        self.y_game_size = self.y_game_bottom - self.y_game_top
        log("size x", self.x_game_size, "size y", self.y_game_size)
        proportion = float(self.x_game_size) / self.y_game_size
        log("proportion", proportion)
        if abs(proportion - self.PROPORTIONS) > self.PROPORTIONS_MARGIN:
            log("proportion fail")
            return False
        if not self.check_game_border_colors():
            log("check square border fail")
            return False
        self.square_detected = True
        return True
        
    def get_rect_raw_enigma_zone(self):
        # rectangle de jeu : 498 * 324
        # zone "brute" de l'énigme (avec marge) : 
        # x = -5% de chaque côté. y1 = 72, y2 = 110.
        if not self.square_detected:
            return None
        x_depl_rez_left = int(self.x_game_size * self.RATIO_X_REZ_LEFT)
        x_scr_rez_left = self.x_game_left + x_depl_rez_left
        x_depl_rez_right = int(self.x_game_size * self.RATIO_X_REZ_RIGHT)
        x_scr_rez_right = self.x_game_left + x_depl_rez_right
            
        y_depl_rez_top = int(self.y_game_size * self.RATIO_Y_REZ_TOP)
        y_scr_rez_top = self.y_game_top + y_depl_rez_top
        y_depl_rez_bottom = int(self.y_game_size * self.RATIO_Y_REZ_BOTTOM)
        y_scr_rez_bottom = self.y_game_top + y_depl_rez_bottom
        
        x_rez_size = x_scr_rez_right - x_scr_rez_left
        y_rez_size = y_scr_rez_bottom - y_scr_rez_top
        return (x_scr_rez_left, y_scr_rez_top, x_rez_size, y_rez_size)
    
    # TODO : underscore au début des fonctions, 
    # pour les suivantes, jusqu'à la fin du module.
    def get_pixel(self, x, y):
        return self.dc_img.GetPixel(x, y)[0:3]
        
    def is_approx_extern_border(self, rgb):
        hsv = hsv_from_rgb(*rgb)
        return is_same_col(hsv, self.HSV_APPROX_EXTERN_BORDER)
        
    def detect_line_pattern(self, y):
        """
        Parcourt une ligne de pixel, et tente d'y trouver un motif (pattern)
        spécifique, qui correspondrait à la zone de jeu.
        
        :param y: ordonnée de la ligne de pixel à parcourir, dans self.dc_img.
        :return: None si le motif n'a pas été trouvé, un tuple de 2 entiers si
        le motif a été trouvé. Ces entiers indiquent les abscisses des 1er et
        dernier pixels gris foncé, censés correspondre aux bords gauche et 
        droit du rectangle de la zone de jeu.
        
        La ligne de pixel respecte le motif si, lorsqu'on la parcourt, on 
        rencontre des pixels dans cet ordre :
         - N'importe quoi
         - Un ou plusieurs pixels approximativement marron, du bord extérieur.
         - Un ou plusieurs pixels exactement gris foncé du rectangle de jeu.
         - N'importe quoi, (y compris des pixels gris foncé)
         - Un ou plusieurs pixels exactement gris foncé du rectangle de jeu.
         - Éventuellement, un ou plusieurs pixels exactement gris clair. 
           (bord éclairé du rectangle de jeu).
         - Un ou plusieurs pixels approximativement marron, du bord extérieur.
         - N'importe quoi.
         
        Pour savoir où on en est, on met en place une espèce de vague machine
        à état, dont les différents états sont définis par l'enum
        PATTERN_SEARCH_STATE.
        
         - NOTHING_FOUND : On est dans le n'importe quoi du début.
         - BEFORE_LEFT_BORDER : Les pixels à peu près marron, avant le bord
           gauche de la zone de jeu.
         - IN_GAME_COLOR_OK : Les pixels gris foncé dans la zone de jeu.
         - IN_GAME_COLOR_NO : Du n'importe quoi, pendant qu'on est dans la 
           zone de jeu.
         - RIGHT_LIT_PIXEL : Les éventuels pixels gris clair, à droite de la 
           zone de jeu.
         - AFTER_RIGHT_BORDER : Les pixels à peu près marron, après le bord 
           droit de la zone de jeu. Si on arrive à cet état, le motif a été 
           trouvé dans la ligne de pixel.
        
        Si on arrive à la fin de la ligne en étant dans un autre état que 
        AFTER_RIGHT_BORDER, le motif n'a pas été trouvé.
        """
        # TRIP: AAAAHHH aAHAAHAHAAAHAAAAHHHH !!! AAAHAAHAAAAAAHHH !!
        pss_cur = pss.NOTHING_FOUND
        x_pattern_start = None
        x_pattern_end = None
        for x_cur in range(self.size_x_img):
            rgb_cur = self.get_pixel(x_cur, y)
            
            if pss_cur == pss.NOTHING_FOUND:
                if self.is_approx_extern_border(rgb_cur):
                    pss_cur = pss.BEFORE_LEFT_BORDER
                    
            elif pss_cur == pss.BEFORE_LEFT_BORDER:
                if rgb_cur == self.RGB_EXACT_INSIDE_SQUARE:
                    pss_cur = pss.IN_GAME_COLOR_OK
                    x_pattern_start = x_cur
                elif not self.is_approx_extern_border(rgb_cur):
                    pss_cur = pss.NOTHING_FOUND
                    
            elif pss_cur == pss.IN_GAME_COLOR_OK:
                if rgb_cur == self.RGB_EXACT_RIGHT_LIT_PIXEL:
                    pss_cur = pss.RIGHT_LIT_PIXEL
                    x_pattern_end = x_cur - 1
                elif self.is_approx_extern_border(rgb_cur):
                    pss_cur = pss.AFTER_RIGHT_BORDER
                    x_pattern_end = x_cur - 1
                elif rgb_cur != self.RGB_EXACT_INSIDE_SQUARE:        
                    pss_cur = pss.IN_GAME_COLOR_NO
                
            elif pss_cur == pss.IN_GAME_COLOR_NO:
                if rgb_cur == self.RGB_EXACT_INSIDE_SQUARE:
                    pss_cur = pss.IN_GAME_COLOR_OK
                
            elif pss_cur == pss.RIGHT_LIT_PIXEL:
                if self.is_approx_extern_border(rgb_cur):
                    pss_cur = pss.AFTER_RIGHT_BORDER
                elif rgb_cur != self.RGB_EXACT_RIGHT_LIT_PIXEL:
                    pss_cur = pss.NOTHING_FOUND
        
            elif pss_cur == pss.AFTER_RIGHT_BORDER:
                return (x_pattern_start, x_pattern_end)
        
        return None
    
    def check_pattern(self, y):
        """
        Vérifie des pixels d'une ligne, afin de savoir si celle-ci traverse
        la zone de jeu ou pas. Cette fonction doit être appelée après qu'on
        ait trouvé une première ligne traversant la zone de jeu. Les variables
        membres self.x_game_left et self.x_game_right doivent avoir été 
        définies.
        
        :param y: ordonnée de la ligne de pixel à vérifier, dans self.dc_img.
        :return: False : La ligne ne contient pas le motif, elle ne traverse
        pas la zone de jeu. True : elle contient le motif.
        
        Les trucs qu'on vérifie : 
         - Les obviouseries de base : y est dans l'écran, les x_game_left et
           x_game_right sont définis.
         - Le pixel juste avant le bord gauche est approximativement de la
           couleur marron-bois-moche.
         - Le pixel du bord gauche est du gris foncé de zone de jeu.
         - Le pixel du bord droit est du gris foncé de zone de jeu.
         - Il y a 0, 1 ou plusieurs pixels gris clair juste après le bord 
           droit.
         - le pixel à droie des pixels gris clair est en marron-bois-moche.
        """
        if y < 0 or y > self.size_y_img:
            return False
        if self.x_game_left is None or self.x_game_right is None:
            return False
        rgb_before = self.get_pixel(self.x_game_left - 1, y)
        if not self.is_approx_extern_border(rgb_before):
            return False
        rgb_left = self.get_pixel(self.x_game_left, y)
        if rgb_left != self.RGB_EXACT_INSIDE_SQUARE:
            return False
        rgb_right = self.get_pixel(self.x_game_right, y)
        if rgb_right != self.RGB_EXACT_INSIDE_SQUARE:
            return False
        x_cursor = self.x_game_right
        in_right_lit_pix = True
        while in_right_lit_pix:
            x_cursor += 1
            rgb_after = self.get_pixel(x_cursor, y)
            in_right_lit_pix = (rgb_after == self.RGB_EXACT_RIGHT_LIT_PIXEL)
        if not self.is_approx_extern_border(rgb_after):
            return False
        return True
    
    def find_first_line_pattern(self):
        y_step = self.size_y_img
        while y_step > self.STEP_Y_MIN_LIMIT_SEARCH_FIRST_PATTERN:
            y_step = y_step / 2
            y_cursor = 0
            while y_cursor < self.size_y_img:
                # TODO : on risque de retenter une détection sur une ligne
                # déjà testée. 
                # Il faut mémoizer les résultats de detect_line_pattern.
                detect_result = self.detect_line_pattern(y_cursor)
                log("detect pattern:", y_cursor, "result:", detect_result)
                if detect_result is not None:
                    (self.x_game_left, self.x_game_right) = detect_result
                    self.y_first_pattern = y_cursor
                    return True
                y_cursor += y_step
        return False
    
    def detect_line_pattern_limit(self, y_direction):
        """
        y_direction doit valoir +1 ou -1, sinon ça fait nimp.
        """
        y_cursor = self.y_first_pattern
        y_last_pattern = self.y_first_pattern
        if y_direction == -1:
            y_step = -self.y_first_pattern
        else:
            y_step = self.size_y_img - self.y_first_pattern
        while y_step != 0:
            if self.check_pattern(y_cursor):
                log("pattern check ok :", y_cursor)
                y_last_pattern = y_cursor
                y_cursor += y_step
            else:
                log("pattern check fail :", y_cursor)
                y_cursor = y_last_pattern
                if y_step == y_direction:
                    y_step = 0
                else:
                    y_step = y_step / 2
                    if y_step == 0:
                        y_step == y_direction
        log("pattern last :", y_last_pattern)
        return y_last_pattern
        
    def check_game_line_colors(self, y_line):
        return all( [ 
            self.get_pixel(x, y_line) == self.RGB_EXACT_INSIDE_SQUARE
            for x in range(self.x_game_left, self.x_game_right+1) ] )

    def check_game_column_colors(self, x_column):
        return all( [ 
            self.get_pixel(x_column, y) == self.RGB_EXACT_INSIDE_SQUARE
            for y in range(self.y_game_top, self.y_game_bottom+1) ] )
            
    def check_game_border_colors(self):
        if (self.x_game_left is None or 
            self.x_game_right is None or 
            self.y_game_bottom is None or 
            self.y_game_top is None
           ):
            return False
        if (not self.check_game_line_colors(self.y_game_top) or
            not self.check_game_line_colors(self.y_game_bottom) or
            not self.check_game_column_colors(self.x_game_left) or
            not self.check_game_column_colors(self.x_game_right)
        ):
            return False
        return True
            
    