# -*- coding: utf-8 -*-

import wx
from log import log
from srccapt import capture_screen, capture_screen_and_save
from imganaly.gamedtc import GameRectDetector

app = wx.App(False)
screen = wx.ScreenDC()
size = screen.GetSize()

log(size)

tsize = (size[0], size[1])
dc_img = capture_screen(screen, 0, 0, tsize[0], tsize[1])
log(dc_img)
game_square_detector = GameRectDetector(tsize[0], tsize[1], dc_img)
if game_square_detector.detect_square():
    log("detection rectangle du jeu ok")
    # juste pour vérifier qu'on a bien chopé le rectangle. À enlever après.
    capture_screen_and_save(
        screen,
        game_square_detector.x_square_left,
        game_square_detector.y_square_up,
        game_square_detector.x_square_size,
        game_square_detector.y_square_size)


del dc_img

## #print "ouaiche"
## wx.App()  # Need to create an App instance before doing anything
## screen = wx.ScreenDC()
## size = screen.GetSize()
## bmp = wx.EmptyBitmap(size[0], size[1])
## mem = wx.MemoryDC(bmp)
## mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
## del mem  # Release bitmap
## bmp.SaveFile('screenshot.png', wx.BITMAP_TYPE_PNG)
## print "voilache"