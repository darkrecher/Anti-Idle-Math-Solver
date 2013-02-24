# -*- coding: utf-8 -*-

from log import log
from enum import enum

class Symbol():
    """ 
    """

    INIT_SYMBOL_DATA_TYPE = enum(
        "INIT_SYMBOL_DATA_TYPE",
        "RAW_SYMBOL_ARRAY_INKS",
        "SAVED_DATA",
    )
    
    def __init__(self, raw_symbol=None, saved_data=None):
        if raw_symbol is not None:
            self._init_with_raw_symbol(raw_symbol)
        elif saved_data is not None:
            self._init_with_saved_data(saved_data)
        else:
            self.width = 0
            self.height = 0
            self.signifiance = None
            self.flat_list_ink = []        
    
    def _init_with_raw_symbol(self, raw_symbol):
        self.array_inks = [
            ink_line for ink_line in raw_symbol
            if any( (ink > 0 for ink in ink_line) ) ]
        self.width = len(self.array_inks[0])
        self.height = len(self.array_inks)
        self.signifiance = None
        self.flat_list_ink = []
        for ink_line in self.array_inks:
            self.flat_list_ink.extend(ink_line)    
        self.flat_list_ink = tuple(self.flat_list_ink)
    
    def _init_with_saved_data(self, saved_data):
        list_saved_data = saved_data.split(" ")
        self.signifiance = list_saved_data.pop(0)
        self.width = int(list_saved_data.pop(0))
        self.height = int(list_saved_data.pop(0))
        self.flat_list_ink = [ int(ink) for ink in list_saved_data ]
        self.flat_list_ink = tuple(self.flat_list_ink)
        assert len(self.flat_list_ink) == self.width * self.height
    
    def assign_signifiance(self, signifiance):
        """ signifiance n'est peut être pas un mot qui existe. osef."""
        self.signifiance = signifiance
        
    def __str__(self):
        if self.signifiance is None:
            str_sig = "!"
        else:
            str_sig = self.signifiance
        list_data = [ str_sig, self.width, self.height ]
        list_data.extend(self.flat_list_ink)
        list_data_str = [ str(elem) for elem in list_data ]
        return " ".join(list_data_str)
        