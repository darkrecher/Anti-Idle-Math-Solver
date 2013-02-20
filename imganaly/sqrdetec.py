# -*- coding: utf-8 -*-

from log import log
from enum import enum
from colrtool import hsv_from_rgb, is_same_col

PATTERN_SEARCH_STATE = enum(
    "PATTERN_SEARCH_STATE",
    "NOTHING_FOUND",
    "JUST_BEFORE_LEFT_BORDER",
    "IN_SQUARE",
    "RIGHT_COLUMN_LIGHT_PIXEL",
    "AFTER_RIGHT_BORDER",
)

pss = PATTERN_SEARCH_STATE

class GameSquareDetector():

    HSV_APPROXIMATE_SQUARE_BORDER = (32, 27, 23)

    def __init__(self, size_x_img, size_y_img, dc_img, colour_searched):
        self.dc_img = dc_img
        self.size_x_img = size_x_img
        self.size_y_img = size_y_img
        
        self.detect_pattern_in_line(size_y_img/2)
        
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
        
        
    def detect_pattern_in_line(self, y):
        pss_cur = pss.NOTHING_FOUND
        for x_cur in range(self.size_x_img):
            rgb_cur = self.dc_img.GetPixel(x_cur, y)
            
            if pss_cur in (pss.NOTHING_FOUND, pss.JUST_BEFORE_LEFT_BORDER):
                hsv_cur = hsv_from_rgb(*rgb_cur)
                if is_same_col(hsv_cur, self.HSV_APPROXIMATE_SQUARE_BORDER):
                    pss_cur = pss.JUST_BEFORE_LEFT_BORDER
                    log(x_cur)
        
        
        
    