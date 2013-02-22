# -*- coding: utf-8 -*-

def log(*list_msg):
    """ Bon, ça fait juste un print.
    Si ça c'est pas la classe !"""
    for elem in list_msg:
        print elem,
    print ""
    
def msg(*list_msg):
    """oui je sais, y'a la librairie logger pour ça.
    M'emmerdez pas."""
    for elem in list_msg:
        print elem,
    print ""
