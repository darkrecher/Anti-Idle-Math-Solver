# -*- coding: utf-8 -*-

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
        # On vérifie la couleur du coin inférieur gauche.
        # Pas le coin supérieur gauche. Car en haut de la zone, il peut y 
        # avoir des pixels bleus clair, montrant les indices de jeu.
        if self._get_pixel(x_size_rez-1, 0) != RGB_EXACT_ENIGMA_ZONE:
            return False
        # TODO : dérawer la zone.
        return True
        
    def _get_pixel(self, x, y):
        return self.dc_raw_enigma_zone.GetPixel(x, y)[0:3]
