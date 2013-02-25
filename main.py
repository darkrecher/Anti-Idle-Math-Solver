# -*- coding: utf-8 -*-

import wx
import time
from log import log, msg
from srccapt import capture_screen, capture_screen_and_save
from imganaly.gamedtc import GameRectDetector
from imganaly.enizodtc import EnigmaZoneDetector
from imganaly.symbextr import SymbolExtractor
from imganaly.symbol import Symbol
from imganaly.eniocr import EnigmaOcr

def main():

    TIME_REFRESH_SECONDS = 0.25
    # TODO : factoriser ça
    RGB_EXACT_ENIGMA_ZONE = (0, 0, 102)

    app = wx.App(False)
    screen = wx.ScreenDC()
    size = screen.GetSize()
    log(size)
    tsize = (size[0], size[1])
    
    dc_img = capture_screen(screen, 0, 0, tsize[0], tsize[1])
    game_square_detector = GameRectDetector(tsize[0], tsize[1], dc_img)
    if not game_square_detector.detect_square():
        msg("Impossible de trouver l'image du jeu a l'ecran.")
        return False
    msg("Detection rectangle du jeu ok.")
    msg("Ne bougez plus vos fenetres. Ne scrollez plus")
    # juste pour vérifier qu'on a bien chopé le rectangle.
    #capture_screen_and_save(
    #    screen,
    #    game_square_detector.x_game_left,
    #    game_square_detector.y_game_top,
    #    game_square_detector.x_game_size,
    #    game_square_detector.y_game_size,
    #    "screenshot.png")
            
    rect_rez = game_square_detector.get_rect_raw_enigma_zone()
    (x_scr_rez_left, y_scr_rez_top, x_rez_size, y_rez_size) = rect_rez
    del dc_img
    
    enigma_zone_detector = EnigmaZoneDetector()
    found_enigma_zone = False
    msg("En attente du demarrage du jeu.")
    while not found_enigma_zone:
        time.sleep(TIME_REFRESH_SECONDS)
        dc_raw_enigma_zone = capture_screen(
            screen, 
            x_scr_rez_left, y_scr_rez_top, 
            x_rez_size, y_rez_size)
        found_enigma_zone = enigma_zone_detector.detect_enigma_zone(
            dc_raw_enigma_zone, 
            x_rez_size, y_rez_size)
        log("en attente. tralala.")
    msg("OK. Le jeu est en cours.")
    
    capture_screen_and_save(
        screen,
        x_scr_rez_left, y_scr_rez_top, x_rez_size, y_rez_size,
        "J:\\Recher\\infos_jeux_videos\\anti-idle\\screenshot_rez.png")    
        
    y_proc_ez_top = enigma_zone_detector.y_proc_ez_top
    y_scr_ez_top = y_scr_rez_top + y_proc_ez_top
    y_size_ez = enigma_zone_detector.y_size_proc_ez
    x_scr_ez_left = x_scr_rez_left
    x_size_ez = x_rez_size
        
    capture_screen_and_save(
        screen,
        x_scr_ez_left, y_scr_ez_top, x_size_ez, y_size_ez,
        "J:\\Recher\\infos_jeux_videos\\anti-idle\\screenshot_ez.png")        
        
    del dc_raw_enigma_zone
    
    symbole_extractor = SymbolExtractor()
    enigma_ocr = EnigmaOcr()
    dc_enigma_zone = capture_screen(
        screen, 
        x_scr_ez_left, y_scr_ez_top, x_size_ez, y_size_ez)
        
    while True:            
        symbole_extractor.extract_symbols_data(
            dc_enigma_zone, x_size_ez, y_size_ez)    
        list_raw_symbols_before = symbole_extractor.list_raw_symbols_before
        rgb_big_op = symbole_extractor.rgb_big_op
        list_raw_symbols_after = symbole_extractor.list_raw_symbols_after
        list_symbols_before = [ 
            Symbol(raw_symbol=raw_symbol) 
            for raw_symbol in list_raw_symbols_before ]
        list_symbols_after = [ 
            Symbol(raw_symbol=raw_symbol) 
            for raw_symbol in list_raw_symbols_after ]
        is_enigma_solvable = enigma_ocr.ocr_ify_enigma(
            list_symbols_before, 
            rgb_big_op, 
            list_symbols_after)
        msg(enigma_ocr.enigma_text)
        if not is_enigma_solvable:
            enigma_text_help = raw_input(
                "Saisissez la question posee par le jeu : ")
            enigma_ocr.record_enigma_text_complete(enigma_text_help)
            # réinterpreation de l'énigme, avec les nouveaux symboles acquis.
            # Y'aurait sûrement moins bourrin que de tout recalculer. osef.
            is_enigma_solvable = enigma_ocr.ocr_ify_enigma(
                list_symbols_before, 
                rgb_big_op, 
                list_symbols_after)
            msg(enigma_ocr.enigma_text)
            
        # TODO : résoudre l'énigme et balancer la réponse.
        
        dc_is_the_same = True
        while dc_is_the_same:
            time.sleep(TIME_REFRESH_SECONDS)
            dc_refreshed = capture_screen(
                screen, 
                x_scr_ez_left, y_scr_ez_top, x_size_ez, y_size_ez)
            # TODO : une fonction, voire une classe, pour ça.
            rgb_bottom_left = dc_refreshed.GetPixel(0, y_size_ez-1)[0:3]
            if rgb_bottom_left != RGB_EXACT_ENIGMA_ZONE:
                msg("Il semblerait que le jeu soit fini.")
                enigma_ocr.symbole_references.msg_newly_added_symbols()
                return True
            dc_is_the_same = not symbole_extractor.is_new_image(dc_refreshed)
            
        del dc_enigma_zone
        dc_enigma_zone = dc_refreshed

        
if __name__ == "__main__":
    if main():
        raise SystemExit(0)
    else:
        raise SystemExit(1)
    