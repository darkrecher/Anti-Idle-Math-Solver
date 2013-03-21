# -*- coding: utf-8 -*-

""" 
créé par Réchèr. Licence CC-BY ou Art Libre.
https://github.com/darkrecher/Anti-Idle-Math-Solver
je prends les bitcoins : 12wF4PWLeVAoaU1ozD1cnQprSiKr6dYW1G

module contenant la classe EnigmaSolver, qui résout les énigmes et renvoie la
bonne réponse.

Mode d'emploi
=============

Rien de bien compliqué. Faut instancier un EnigmaSolver, puis exécuter la
fonction solve, en passant en paramètre le texte d'une énigme.

Si l'énigme est solvable, la fonction renvoie une chaîne de caractères,
correspondant à la bonne réponse. Sinon, la fonction renvoie None. C'est tout.

Fonctionnement interne
======================

On commence par virer toutes les virgules du texte d'énigme. À cause de ces
cons d'américains qui écrivent les grands nombres sous la forme 1,234,567.

Il y a 3 sortes d'énigmes :

1) 
Si ça finit par les caractères "égal", puis "point d'interrogation", c'est une
énigme de calcul. Par exemple : "2+2=?". Pour résoudre cette énigme, on 
évalue le texte qui se trouve avant le signe égal.

2)
Si l'énigme ne comporte pas de signe "égal", c'est une énigme de comparaison.
Par exemple : "3*5?17". Pour résoudre cette énigme, on sépare le texte en 2 :
la partie avant le point d'interrogation, et celle après. (Si le texte ne 
comporte pas de point d'interrogation, l'énigme n'est pas solvable). On évalue
les deux parties de texte, et on les compare. La comparaison (plus petit, 
égal ou plus grand) est la réponse à l'énigme.

3)
Si l'énigme comporte un point d'interrogation, puis un signe "égal", avec du
texte entre chacun de ces caractères, c'est une énigme de recherche 
d'opérateur. Par exemple : "5?7=35". On évalue le premier opérande (la partie
de texte situé avant le point d'interrogation), le deuxième (texte situé 
entre le point d'interrogaton et le "égal") et le résultat (texte situé après
le "égal").
Ensuite on essaie toutes les possibilités d'opérateur. On calcule 
opérande_1 + opérande_2. Si c'est égal au résultat, la réponse à l'énigme est
"+". On fait pareil avec les opérateurs de soustraction, multiplication et
division. Si aucun de ces calculs n'est égal au résultat, l'énigme n'est pas
solvable.

4)
Si l'énigme ne rentre dans aucun des 3 cas précédemment cités, elle n'est pas
solvable.

Pour les 3 sortes d'énigme, on doit évaluer des parties de texte. Cette action
est effectuée par la foncton _interpret_enigma_part. On doit calculer la 
valeur numérique représenté par l'expression de la partie de texte en 
question. Ça peut être quelque chose de très simple, comme "42", ou un peu 
plus compliqué, comme "(123-99)*74". Ces parties de texte à évaluer ne sont 
censées contenir que des chiffres, les 4 opérateurs, et des parenthèses.
Il n'est pas censé y avoir de point d'interrogation ou de signe "égal".

Pour évaluer ces parties de texte, on le fait à la gros bourrin : la fonction
python "eval", et vlan dans la gueule. Si ça pète en cours de route, on
considère que la partie de texte ne peut pas être évaluée, et que donc 
l'énigme n'est pas solvable. Sinon, c'est cool.
Avant d'exécuter la fonction "eval", on ne vérifie même pas si la partie de
texte ne contient que les caractères autorisés. On essaie direct, donc c'est
vraiment du bon gros bourrin. Mais j'aime ça.
"""

from log import log, msg


class EnigmaSolver():
    
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

