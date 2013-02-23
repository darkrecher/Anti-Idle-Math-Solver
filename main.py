# -*- coding: utf-8 -*-

import wx
from log import log
from srccapt import capture_screen, capture_screen_and_save
from imganaly.gamedtc import GameRectDetector
from imganaly.enizodtc import EnigmaZoneDetector


app = wx.App(False)
screen = wx.ScreenDC()
size = screen.GetSize()
log(size)

tsize = (size[0], size[1])
dc_img = capture_screen(screen, 0, 0, tsize[0], tsize[1])
log(dc_img)
game_square_detector = GameRectDetector(tsize[0], tsize[1], dc_img)
if not game_square_detector.detect_square():
    raise SystemExit(1)
    #return False
    
log("detection rectangle du jeu ok")
# juste pour vérifier qu'on a bien chopé le rectangle. À enlever après.
capture_screen_and_save(
    screen,
    game_square_detector.x_square_left,
    game_square_detector.y_square_up,
    game_square_detector.x_square_size,
    game_square_detector.y_square_size,
    "J:\\Recher\\infos_jeux_videos\\anti-idle\\screenshot.png")
        
rect_rez = game_square_detector.get_rect_raw_enigma_zone()
(x_scr_rez_left, y_scr_rez_top, x_rez_size, y_rez_size) = rect_rez

del dc_img

enigma_zone_detector = EnigmaZoneDetector()
dc_raw_enigma_zone = capture_screen(screen, x_scr_rez_left, y_scr_rez_top, x_rez_size, y_rez_size)
if not enigma_zone_detector.detect_enigma_zone(dc_raw_enigma_zone, x_rez_size, y_rez_size):
    log("enigma_zone_detector fail")
    raise SystemExit(1)
    #return False

capture_screen_and_save(
    screen,
    x_scr_rez_left, y_scr_rez_top, x_rez_size, y_rez_size,
    "J:\\Recher\\infos_jeux_videos\\anti-idle\\screenshot_rez.png")    
    
del dc_raw_enigma_zone

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