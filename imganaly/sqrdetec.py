# -*- coding: utf-8 -*-

class SquareDetector():

    def __init__(self, size_x_img, size_y_img, imgDc, colour_searched):
        column_x = size_x_img / 2
        min_y_colour = -1
        max_y_colour = -1
        for y_current in range(size_y_img):
            colour_current = imgDc.GetPixel(column_x, y_current)
            print y_current, colour_current
            if colour_current == colour_searched:
                if min_y_colour == -1:
                    min_y_colour = y_current
                max_y_colour = y_current
        
        print min_y_colour, max_y_colour
        