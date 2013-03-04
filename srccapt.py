# -*- coding: utf-8 -*-

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
    