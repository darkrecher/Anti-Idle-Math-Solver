# -*- coding: utf-8 -*-

from log import log


class Symbol():
    """ 
    """

    def __init__(self, raw_symbol):
        self.array_inks = [
            ink_line for ink_line in raw_symbol
            if any( (ink > 0 for ink in ink_line) )
        ]
        self.width = len(self.array_inks[0])
        self.height = len(self.array_inks)
        self.signifiance = None
        self.flat_list_ink = []
        for ink_line in self.array_inks:
            self.flat_list_ink.extend(ink_line)
    
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
        