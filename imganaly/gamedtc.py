# -*- coding: utf-8 -*-

from log import log
from enum import enum
from colrtool import hsv_from_rgb, is_same_col

PATTERN_SEARCH_STATE = enum(
    "PATTERN_SEARCH_STATE",
    "NOTHING_FOUND",
    "BEFORE_LEFT_BORDER",
    "IN_SQUARE_COLOR_OK",
    "IN_SQUARE_COLOR_NO",
    "RIGHT_LIT_PIXEL",
    "AFTER_RIGHT_BORDER",
)

pss = PATTERN_SEARCH_STATE

class GameRectDetector():
    """ 
    """
    HSV_APPROX_EXTERN_BORDER = (32, 27, 23)
    # TRIP: 51 je t'aimeu, j'en boirais des tonneaux, 
    # à me rouler par terreu, dans tous les caniveaux
    RGB_EXACT_INSIDE_SQUARE = (51, 51, 51)
    RGB_EXACT_RIGHT_LIT_PIXEL = (102, 102, 102)
    STEP_Y_MIN_LIMIT_SEARCH_FIRST_PATTERN = 50
    PROPORTIONS = 1.5370370
    PROPORTIONS_MARGIN = 0.1

    def __init__(self, size_x_img, size_y_img, dc_img):
        self.dc_img = dc_img
        self.size_x_img = size_x_img
        self.size_y_img = size_y_img
        self.y_first_pattern = None
        self.x_square_left = None
        self.x_square_right = None
        self.y_square_up = None
        self.y_square_bottom = None
        self.x_square_size = None
        self.y_square_size = None
        self.square_detected = False
        
    def detect_square(self):
        if not self.find_first_line_pattern():
            log("first line pattern fail")
            return False
        self.y_square_up = self.detect_line_pattern_limit(-1)
        self.y_square_bottom = self.detect_line_pattern_limit(+1)
        self.x_square_size = self.x_square_right - self.x_square_left
        self.y_square_size = self.y_square_bottom - self.y_square_up
        log("size x", self.x_square_size, "size y", self.y_square_size)
        proportion = float(self.x_square_size) / self.y_square_size
        log("proportion", proportion)
        if abs(proportion - self.PROPORTIONS) > self.PROPORTIONS_MARGIN:
            log("proportion fail")
            return False
        if not self.check_square_border_colors():
            log("check square border fail")
            return False
        return True
        
    def get_pixel(self, x, y):
        return self.dc_img.GetPixel(x, y)[0:3]
        
    def is_approx_extern_border(self, rgb):
        hsv = hsv_from_rgb(*rgb)
        return is_same_col(hsv, self.HSV_APPROX_EXTERN_BORDER)
        
    def detect_line_pattern(self, y):
        """
        La ligne de pixel respecte le pattern si il est comme ça :
         - N'importe quoi
         - Un ou plusieurs pixels approximativement marron, du bord extérieur.
         - Un ou plusieurs pixels exactement gris foncé du rectangle de jeu.
         - N'importe quoi, (ça peut être que des pixels gris)
         - Éventuellement, un ou plusieurs pixels exactement gris clair. 
           (bord éclairé du rectangle de jeu).
         - Un ou plusieurs pixels approximativement marron, du bord extérieur.
         - N'importe quoi.
        La fonction renvoie None si le pattern n'est pas présent.
        Elle renvoie un tuple (x1, x2) si le pattern est présent.
          x1 = premier pixel gris foncé du rectangle de jeu.
          x2 = dernier pixel gris foncé du rectangle de jeu.
        """
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
                    pss_cur = pss.IN_SQUARE_COLOR_OK
                    x_pattern_start = x_cur
                elif not self.is_approx_extern_border(rgb_cur):
                    pss_cur = pss.NOTHING_FOUND
                    
            elif pss_cur == pss.IN_SQUARE_COLOR_OK:
                if rgb_cur == self.RGB_EXACT_RIGHT_LIT_PIXEL:
                    pss_cur = pss.RIGHT_LIT_PIXEL
                    x_pattern_end = x_cur - 1
                elif self.is_approx_extern_border(rgb_cur):
                    pss_cur = pss.AFTER_RIGHT_BORDER
                    x_pattern_end = x_cur - 1
                elif rgb_cur != self.RGB_EXACT_INSIDE_SQUARE:        
                    pss_cur = pss.IN_SQUARE_COLOR_NO
                
            elif pss_cur == pss.IN_SQUARE_COLOR_NO:
                if rgb_cur == self.RGB_EXACT_INSIDE_SQUARE:
                    pss_cur = pss.IN_SQUARE_COLOR_OK
                
            elif pss_cur == pss.RIGHT_LIT_PIXEL:
                if self.is_approx_extern_border(rgb_cur):
                    pss_cur = pss.AFTER_RIGHT_BORDER
                elif rgb_cur != self.RGB_EXACT_RIGHT_LIT_PIXEL:
                    pss_cur = pss.NOTHING_FOUND
        
            elif pss_cur == pss.AFTER_RIGHT_BORDER:
                return (x_pattern_start, x_pattern_end)
        
        return None
    
    def check_pattern(self, y):
        if y < 0 or y > self.size_y_img:
            return False
        if self.x_square_left is None or self.x_square_right is None:
            return False
        rgb_before = self.get_pixel(self.x_square_left - 1, y)
        if not self.is_approx_extern_border(rgb_before):
            return False
        rgb_left = self.get_pixel(self.x_square_left, y)
        if rgb_left != self.RGB_EXACT_INSIDE_SQUARE:
            return False
        rgb_right = self.get_pixel(self.x_square_right, y)
        if rgb_right != self.RGB_EXACT_INSIDE_SQUARE:
            return False
        x_cursor = self.x_square_right
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
                detect_result = self.detect_line_pattern(y_cursor)
                log("detect pattern:", y_cursor, "result:", detect_result)
                if detect_result is not None:
                    (self.x_square_left, self.x_square_right) = detect_result
                    self.y_first_pattern = y_cursor
                    return True
                y_cursor += y_step
        return False
    
    def detect_line_pattern_limit(self, y_direction):
        """y_direction doit valoir +1 ou -1, sinon ça fait nimp.
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
        
    def check_square_line_colors(self, y_line):
        return all( [ 
            self.get_pixel(x, y_line) == self.RGB_EXACT_INSIDE_SQUARE
            for x in range(self.x_square_left, self.x_square_right+1) ] )

    def check_square_column_colors(self, x_column):
        return all( [ 
            self.get_pixel(x_column, y) == self.RGB_EXACT_INSIDE_SQUARE
            for y in range(self.y_square_up, self.y_square_bottom+1) ] )
            
    def check_square_border_colors(self):
        if (self.x_square_left is None or 
            self.x_square_right is None or 
            self.y_square_bottom is None or 
            self.y_square_up is None
           ):
            return False
        if (not self.check_square_line_colors(self.y_square_up) or
            not self.check_square_line_colors(self.y_square_bottom) or
            not self.check_square_column_colors(self.x_square_left) or
            not self.check_square_column_colors(self.x_square_right)
        ):
            return False
        return True
        
    #def detect_top_and_bottom_line_pattern(self):
    
    