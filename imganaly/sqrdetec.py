# -*- coding: utf-8 -*-

from log import log
from enum import enum
from colrtool import hsv_from_rgb, is_same_col

PATTERN_SEARCH_STATE = enum(
    "PATTERN_SEARCH_STATE",
    "NOTHING_FOUND",
    "BEFORE_LEFT_BORDER",
    "IN_SQUARE_COL_OK",
    "IN_SQUARE_COL_NO",
    "RIGHT_LIT_PIXEL",
    "AFTER_RIGHT_BORDER",
)

pss = PATTERN_SEARCH_STATE

class GameSquareDetector():
    """ Ouais bon c'est pas un square, c'est un rect. Je me suis planté, osef.
    """
    HSV_APPROX_EXTERN_BORDER = (32, 27, 23)
    # TRIP: 51 je t'aimeu, j'en boirais des tonneaux, 
    # à me rouler par terreu, dans tous les caniveaux
    RGB_EXACT_INSIDE_SQUARE = (51, 51, 51)
    RGB_EXACT_RIGHT_LIT_PIXEL = (102, 102, 102)

    def __init__(self, size_x_img, size_y_img, dc_img):
        self.dc_img = dc_img
        self.size_x_img = size_x_img
        self.size_y_img = size_y_img
        
        
        
        #self.detect_pattern_in_line(size_y_img/2)
        
        #column_x = size_x_img / 2
        #min_y_colour = -1
        #max_y_colour = -1
        #for y_current in range(size_y_img):
        #    colour_current = dc_img.GetPixel(column_x, y_current)
        #    log(y_current, colour_current[0:3])
        #    if colour_current == colour_searched:
        #        if min_y_colour == -1:
        #            min_y_colour = y_current
        #        max_y_colour = y_current
        #
        #log(min_y_colour, max_y_colour)
        
    def is_approx_extern_border(self, rgb):
        hsv = hsv_from_rgb(*rgb)
        return is_same_col(hsv, self.HSV_APPROX_EXTERN_BORDER)
        
    def detect_pattern_in_line(self, y):
        pss_cur = pss.NOTHING_FOUND
        x_pattern_start = None
        x_pattern_end = None
        for x_cur in range(self.size_x_img):
            rgb_cur = self.dc_img.GetPixel(x_cur, y)[0:3]
            
            if pss_cur == pss.NOTHING_FOUND:
                if self.is_approx_extern_border(rgb_cur):
                    pss_cur = pss.BEFORE_LEFT_BORDER
                    
            elif pss_cur == pss.BEFORE_LEFT_BORDER:
                if rgb_cur == self.RGB_EXACT_INSIDE_SQUARE:
                    pss_cur = pss.IN_SQUARE_COL_OK
                    x_pattern_start = x_cur
                elif not self.is_approx_extern_border(rgb_cur):
                    pss_cur = pss.NOTHING_FOUND
                    
            elif pss_cur == pss.IN_SQUARE_COL_OK:
                if rgb_cur == self.RGB_EXACT_RIGHT_LIT_PIXEL:
                    pss_cur = pss.RIGHT_LIT_PIXEL
                elif self.is_approx_extern_border(rgb_cur):
                    pss_cur = pss.AFTER_RIGHT_BORDER
                    x_pattern_end = x_cur - 1
                elif rgb_cur != self.RGB_EXACT_INSIDE_SQUARE:        
                    pss_cur = pss.IN_SQUARE_COL_NO
                
            elif pss_cur == pss.IN_SQUARE_COL_NO:
                if rgb_cur == self.RGB_EXACT_INSIDE_SQUARE:
                    pss_cur = pss.IN_SQUARE_COL_OK
                
            elif pss_cur == pss.RIGHT_LIT_PIXEL:
                if self.is_approx_extern_border(rgb_cur):
                    pss_cur = pss.AFTER_RIGHT_BORDER
                    x_pattern_end = x_cur - 1
                elif rgb_cur != self.RGB_EXACT_RIGHT_LIT_PIXEL:
                    pss_cur = pss.NOTHING_FOUND
        
            elif pss_cur == pss.AFTER_RIGHT_BORDER:
                return (x_pattern_start, x_pattern_end)
        
        return None
    