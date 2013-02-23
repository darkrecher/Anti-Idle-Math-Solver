# -*- coding: utf-8 -*-

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
        # On vérifie la couleur du coin inférieur gauche.
        # Pas le coin supérieur gauche. Car en haut de la zone, il peut y 
        # avoir des pixels bleus clair, montrant les indices de jeu.
        if self._get_pixel(x_size_rez-1, 0) != self.RGB_EXACT_ENIGMA_ZONE:
            return False
        self.y_proc_ez_top = self._crop_line(0, +1, self.y_size_rez-1)
        log("self.y_proc_ez_top", self.y_proc_ez_top)
        self.y_proc_ez_bottom = self._crop_line(self.y_size_rez-1, -1, 0)
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

    def _crop_line(self, y_start, direction, end):
        y_cur = y_start
        while not self._is_line_interesting(y_cur) and y_cur != end:
            y_cur += direction
        return y_cur
        
        