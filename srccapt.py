# -*- coding: utf-8 -*-

"""
créé par Réchèr. Licence CC-BY ou Art Libre.
https://github.com/darkrecher/Anti-Idle-Math-Solver
je prends les bitcoins : 12wF4PWLeVAoaU1ozD1cnQprSiKr6dYW1G

Module permettant de faire des captures d'écran, en choisissant le rectangle
à capturer.

On peut également faire une capture d'écran + sauvegarde de l'image dans
un .png.

Pour que ce module fonctionne, il faut avoir initialisé wx, comme ça :
    app = wx.App(False)
    screen = wx.ScreenDC()
    size = screen.GetSize()

Et il faut passer la variable screen en paramètre aux fonctions de ce module.
Les captures d'écran sont renvoyées sous forme de wx.MemoryDC 
"""

import wx

# TODO : mettre le bazar d'init de wx ici ?
# TODO : factoriser ces 2 fonctions de merde. 

def capture_screen(
    screen, 
    x_screen, 
    y_screen, 
    size_x_screen, 
    size_y_screen
):
    bmp = wx.EmptyBitmap(size_x_screen, size_y_screen)
    mem = wx.MemoryDC(bmp)
    mem.Blit(0, 0, size_x_screen, size_y_screen, screen, x_screen, y_screen)
    return mem
    # ne pas oublier de deleter quand on aura fini les conneries
    # del mem
    
def capture_screen_and_save(
    screen, 
    x_screen, y_screen, 
    size_x_screen, size_y_screen,
    path_save
):
    bmp = wx.EmptyBitmap(size_x_screen, size_y_screen)
    mem = wx.MemoryDC(bmp)
    mem.Blit(0, 0, size_x_screen, size_y_screen, screen, x_screen, y_screen)
    bmp.SaveFile(path_save, wx.BITMAP_TYPE_PNG)
    del mem
    