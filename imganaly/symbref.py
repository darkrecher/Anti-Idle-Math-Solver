﻿# -*- coding: utf-8 -*-from log import log, msgfrom symbdata import LIST_SYMB_ALARRACHEfrom imganaly.symbol import Symbolclass SymbolReferences():    """     """    def __init__(self):        self.list_references = [             Symbol(saved_data=saved_data)             for saved_data in LIST_SYMB_ALARRACHE ]            def add_reference(self, new_symb_ref):        existing_signifiance = self.find_signifiance(new_symb_ref)        if existing_signifiance == "!":            self.list_references.append(new_symb_ref)            return        else:            if existing_signifiance == new_symb_ref.signifiance:                log(                    "Demande d'ajout d'un symbole existant :",                     existing_signifiance)            else:                log(                    "Demande d'ajout d'un symbole existant mais pas pareil",                    existing_signifiance,                    "!=",                    new_symb_ref.signifiance)            def find_signifiance(self, symbol):        for symb_ref in self.list_references:            if self._is_same_symbol(symb_ref, symbol):                return symb_ref.signifiance        return "!"        def _is_same_symbol(self, symb_1, symb_2):        if symb_1.width != symb_2.width or symb_1.height != symb_2.height:            return False        if symb_1.flat_list_ink != symb_2.flat_list_ink:            return False        return True              def msg_newly_added_symbols(self):        for symb in self.list_references:            if symb.comes_from_raw_symbol:                msg(str(symb))                msg("#" * 10)                