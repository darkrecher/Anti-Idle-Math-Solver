# -*- coding: utf-8 -*-

from log import log, msg


class EnigmaSolver():
    """ 
    """
    
    DICT_ANSWER_FROM_COMPARRISON = {
        -1 : "<",
         0 : "=",
        +1 : ">",
    }
    
    def __init__(self):
        pass
        
    def solve(self, enigma_text):
        # suppression des virgules. Ces gros cons d'américains écrivent les 
        # grands nombres sous la forme 1,234,567. Putain, ils peuvent pas
        # foutre des espaces comme tout le monde ? Ça va quoi, on sait lire
        # des grands nombres. On n'est pas des gros débiles.
        list_enigma_text = [ 
            char for char in enigma_text 
            if char != "," ]
        self.enigma_text = "".join(list_enigma_text)
        if self.enigma_text.endswith("=?"):
            return self._solve_calculation()
        elif "=" not in self.enigma_text:
            return self._solve_comparrison()
        else:
            return self._solve_find_operator()
        
    def _solve_calculation(self):
        text_to_calculate = self.enigma_text[:-2]
        return self._interpret_enigma_part(text_to_calculate)
        
    def _solve_comparrison(self):
        left_term, question_mark, right_term = self.enigma_text.partition("?")
        if question_mark == "":
            return None
        left_val = self._interpret_enigma_part(left_term)
        right_val = self._interpret_enigma_part(right_term)
        if left_val is None or right_val is None:
            return None
        comparrison = cmp(left_val, right_val)
        answer = self.DICT_ANSWER_FROM_COMPARRISON[comparrison]
        log(left_val, answer, right_val)
        return answer
        
    def _solve_find_operator(self):
        operation, sign_equal, result = self.enigma_text.partition("=")
        if sign_equal == "":
                return None
        left_operand, question_mark, right_operand = operation.partition("?")
        if question_mark == "":
            return None
        result_val = self._interpret_enigma_part(result)
        left_op_val = self._interpret_enigma_part(left_operand)
        right_op_val = self._interpret_enigma_part(right_operand)
        if result_val is None or left_op_val is None or right_op_val is None:
            return None
        log(left_op_val, "?", right_op_val, "=", result_val)
        if left_op_val + right_op_val == result_val:
            return "+"
        elif left_op_val - right_op_val == result_val:
            return "-"
        elif left_op_val * right_op_val == result_val:
            return "*"
        elif left_op_val / right_op_val == result_val:
            return "/"
        else:
            return None
        
    def _interpret_enigma_part(self, enigma_part):
        val = None
        str_to_exec = "val=" + enigma_part
        # TODO : CHAOTIQUE MAUVAIS !! (doublement en plus)
        # Ne pas utiliser un exec pour un truc aussi simple,
        # Ne pas faire de try-except général.
        # J'ai fait ça comme ça parce que je voulais pas m'emmerder avec
        # l'interprétation des parenthèses et autres subtilités grammaticales.
        try:
            exec(str_to_exec)
        except:
            val = None
        return val

if __name__ == "__main__":
    enigma_solver = EnigmaSolver()
    enigma_solver.solve("17?9=8")

