# -*- coding: utf-8 -*-

import wx
from srccapt import capture_screen
from imganaly.sqrdetec import SquareDetector

app = wx.App(False)
screen = wx.ScreenDC()
size = screen.GetSize()

print size

tsize = (size[0], size[1])
imgDC = capture_screen(screen, 0, 0, tsize[0], tsize[1])
print imgDC
todo_a = SquareDetector(tsize[0], tsize[1], imgDC, wx.Colour(51, 51, 51, 255))



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