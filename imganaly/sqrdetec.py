# -*- coding: utf-8 -*-

from enum import enum
from colrtool import hsv_from_rgb, is_same_hsv

PATTERN_SEARCH_STATE = enum(
    "PATTERN_SEARCH_STATE",
    "BEFORE_LEFT_BORDER",
    "IN_SQUARE",
    "RIGHT_BORDER_LIGHT_PIXEL",
    "AFTER_RIGHT_BORDER",
)


class GameSquareDetector():

    def __init__(self, size_x_img, size_y_img, dc_img, colour_searched):
        self.dc_img = dc_img
        
        column_x = size_x_img / 2
        min_y_colour = -1
        max_y_colour = -1
        for y_current in range(size_y_img):
            colour_current = dc_img.GetPixel(column_x, y_current)
            print y_current, colour_current
            if colour_current == colour_searched:
                if min_y_colour == -1:
                    min_y_colour = y_current
                max_y_colour = y_current
        
        print min_y_colour, max_y_colour
        
        
    def detect_pattern_in_line(self, x):
        pass
        # 32, 27, 23
    