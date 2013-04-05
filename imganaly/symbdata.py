﻿# -*- coding: utf-8 -*-

""" 
créé par Réchèr. Licence CC-BY ou Art Libre.
https://github.com/darkrecher/Anti-Idle-Math-Solver
je prends les bitcoins : 12wF4PWLeVAoaU1ozD1cnQprSiKr6dYW1G

Module contenant la définition de tous les symboles connus. Moche et créé à 
l'arrache, mais c'est pas grave.

Les symboles définis dans ce fichier correspondent à la configuration suivante : 
 - Résolution écran : 1280*720
 - Version du Flash : 11.5.502.149
 - Version de Anti-Idle : 1.564
 
L'utilisateur du script doit peupler manuellement la liste de symboles, avec
ceux de sa propre configuration.

TRIP: "peupler manuellement", c'est trop la classe. Je parle bullshit !

Chaque élément du tuple LIST_SYMB_ALARRACHE définit un symbole.

Chaque élément est une chaîne de caractères composée de sous-éléments, 
séparés par des espaces. On doit trouver, dans cet ordre :
 - un élément de type caractère, correspondant à la signification du symbole,
   on utilise cet élémet pour construire le texte d'une énigme, à partir de sa
   liste de symbole.
 - deux éléments numériques : taille X et Y du symbole, en pixel.
 - un gros tas d'éléments numériques (octets) : liste des valeurs d'encre du
   symbole. Il faut X * Y valeurs d'encres, sinon ça ne marchera pas.

"""

# TODO : un stockage en hexa, ce serait peut-être un peu mieux non ?
# TODO : écrire/lire automatiquement ces infos dans un fichier, au lieu
# que ce soit l'utilisateur qui doivent les copier-coller lui-même tel le
# pauvre forçat de l'informatique.
# TODO : Et puis faudrait me trier tout ça aussi.

LIST_SYMB_ALARRACHE = (

    """, 4 4 0 83 142 142 0 83 254 254 82 254 249 249 249 169 3 3""",
##########

    """- 7 4 6 6 6 6 6 6 6 251 251 251 251 251 251 251 254 254 254 254 254 254 254 165 165 165 165 165 165 165""",
##########

    """( 5 19 183 239 192 13 13 183 254 192 0 0 183 254 192 0 0 183 254 192 0 0 183 254 192 0 0 183 254 192 0 0 183 254 192 0 0 183 254 192 0 0 183 254 192 0 0 183 254 192 0 0 183 254 192 0 0 183 254 192 0 0 183 254 192 0 0 183 254 192 0 0 183 254 192 0 0 183 254 192 0 0 183 254 192 0 0 183 249 192 3 3 3 59 254 249 249""",
##########

    """) 6 24 125 132 132 4 0 0 125 254 249 4 0 0 125 254 254 245 3 0 13 13 13 248 239 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 3 3 3 248 249 127 125 249 249 249 3 3 125 254 249 9 0 0 125 142 142 4 0 0""",
##########
    """- 8 4 6 6 6 6 6 6 6 6 164 251 251 251 251 251 251 210 164 254 254 254 254 254 254 210 164 165 165 165 165 165 165 165""",
##########

    """+ 13 13 0 0 0 0 0 242 242 132 0 0 0 0 0 0 0 0 0 0 243 254 132 0 0 0 0 0 0 0 0 0 0 243 254 132 0 0 0 0 0 0 0 0 0 0 243 254 132 0 0 0 0 0 0 0 0 0 0 243 254 132 0 0 0 0 0 243 244 244 244 244 254 254 120 244 244 244 244 132 243 254 254 254 254 253 253 120 254 254 254 254 132 134 134 134 134 134 122 122 122 134 134 134 134 132 0 0 0 0 0 243 254 132 0 0 0 0 0 0 0 0 0 0 243 254 132 0 0 0 0 0 0 0 0 0 0 243 254 132 0 0 0 0 0 0 0 0 0 0 243 254 132 0 0 0 0 0 0 0 0 0 0 127 127 127 0 0 0 0 0""",
##########
    """( 5 19 239 240 110 13 13 254 254 110 0 0 254 254 110 0 0 254 254 110 0 0 254 254 110 0 0 254 254 110 0 0 254 254 110 0 0 254 254 110 0 0 254 254 110 0 0 254 254 110 0 0 254 254 110 0 0 254 254 110 0 0 254 254 110 0 0 254 254 110 0 0 254 254 110 0 0 254 254 110 0 0 254 254 110 0 0 249 250 110 3 3 3 141 249 249 233""",
##########
    """) 5 19 13 13 166 239 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 3 3 166 249 208 249 249 254 85 3""",
##########
    """- 8 4 6 6 6 6 6 6 6 6 246 251 251 251 251 251 251 129 246 254 254 254 254 254 254 129 165 165 165 165 165 165 165 129""",
##########

    """4 13 19 0 0 0 0 0 119 239 239 239 239 133 0 0 0 0 0 0 0 119 254 254 254 254 133 0 0 0 0 0 100 100 119 157 157 246 254 133 0 0 0 0 0 242 254 133 0 0 242 254 133 0 0 0 0 0 242 254 133 0 0 242 254 133 0 0 0 0 0 242 254 45 0 0 242 254 133 0 0 0 0 73 242 254 11 0 0 242 254 133 0 0 67 68 241 59 59 0 0 0 242 254 133 0 0 119 254 254 10 0 0 0 0 242 254 133 0 0 119 254 254 10 0 0 0 0 242 254 133 0 0 119 254 254 174 174 174 174 174 251 254 119 174 174 119 254 254 254 254 254 254 254 254 254 119 254 254 119 222 222 222 222 222 222 222 91 91 119 222 222 0 0 0 0 0 0 0 0 242 254 133 0 0 0 0 0 0 0 0 0 0 242 254 133 0 0 0 0 0 0 0 0 0 0 242 254 133 0 0 0 0 0 0 0 0 0 0 242 254 133 0 0 0 0 0 0 0 0 0 0 242 249 133 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0""",
##########
    """) 6 19 13 13 13 248 239 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 3 3 3 248 249 127 125 249 249 249 3 3""",
##########


    """9 13 19 0 0 123 239 239 239 239 239 239 239 6 0 0 0 105 123 254 254 254 254 254 254 251 105 3 0 100 122 152 152 152 152 152 152 152 152 249 100 100 246 254 129 0 0 0 0 0 0 1 246 254 128 246 254 129 0 0 0 0 0 0 1 246 254 128 246 254 129 0 0 0 0 0 0 1 246 254 128 246 254 129 0 0 0 0 0 0 1 246 254 128 184 184 129 68 68 68 68 68 68 68 246 254 128 0 122 190 254 254 254 254 254 254 254 254 254 128 0 0 123 254 254 254 254 254 254 254 254 254 128 0 0 77 78 78 78 78 78 78 78 246 254 128 0 0 0 0 0 0 0 0 0 1 246 254 128 0 0 0 0 0 0 0 0 0 1 246 254 128 0 0 0 0 0 0 0 0 0 1 246 254 128 0 0 0 0 0 0 0 0 0 1 246 254 128 0 122 142 142 142 142 142 142 142 142 247 110 110 0 115 123 254 254 254 254 254 254 251 115 4 0 0 0 123 249 249 249 249 249 249 249 6 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0""",
##########
    """+ 12 13 0 0 0 0 79 242 242 50 0 0 0 0 0 0 0 0 79 254 254 50 0 0 0 0 0 0 0 0 79 254 254 50 0 0 0 0 0 0 0 0 79 254 254 50 0 0 0 0 0 0 0 0 79 254 254 50 0 0 0 0 244 244 244 244 244 254 173 202 244 244 244 244 254 254 254 254 254 253 173 202 254 254 254 254 134 134 134 134 134 122 122 134 134 134 134 134 0 0 0 0 79 254 254 50 0 0 0 0 0 0 0 0 79 254 254 50 0 0 0 0 0 0 0 0 79 254 254 50 0 0 0 0 0 0 0 0 79 254 254 50 0 0 0 0 0 0 0 0 79 127 127 50 0 0 0 0""",
##########
    """( 6 19 101 239 254 28 13 13 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 249 254 28 3 3 1 3 223 249 249 151""",
##########
    """) 5 19 13 13 84 246 239 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 3 3 84 254 249 207 249 249 167 3""",
##########

    """6 13 19 0 0 123 239 239 239 239 239 239 239 239 5 0 0 105 123 254 254 254 254 254 254 251 18 0 0 100 122 152 152 152 152 152 152 152 152 6 0 0 246 254 129 0 0 0 0 0 0 0 0 0 0 246 254 129 0 0 0 0 0 0 0 0 0 0 246 254 129 0 0 0 0 0 0 0 0 0 0 246 254 129 0 0 0 0 0 0 0 0 0 0 246 254 129 68 68 68 68 68 68 68 0 0 0 246 254 254 254 254 254 254 254 254 251 6 0 0 246 254 254 254 254 254 254 254 254 254 180 5 0 246 254 129 78 78 78 78 78 78 78 246 174 128 246 254 129 0 0 0 0 0 0 1 246 254 128 246 254 129 0 0 0 0 0 0 1 246 254 128 246 254 129 0 0 0 0 0 0 1 246 254 128 246 254 129 0 0 0 0 0 0 1 246 254 128 110 122 142 142 142 142 142 142 142 142 247 110 110 0 115 123 254 254 254 254 254 254 251 115 4 0 0 0 123 249 249 249 249 249 249 249 6 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0""",
##########

    """6 12 19 0 0 205 239 239 239 239 239 239 239 168 0 0 105 205 254 254 254 254 254 254 169 18 0 100 204 152 152 152 152 152 152 152 152 0 0 254 254 47 0 0 0 0 0 0 0 0 0 254 254 47 0 0 0 0 0 0 0 0 0 254 254 47 0 0 0 0 0 0 0 0 0 254 254 47 0 0 0 0 0 0 0 0 0 254 254 68 68 68 68 68 68 68 68 0 0 254 254 254 254 254 254 254 254 254 169 0 0 254 254 254 254 254 254 254 254 254 195 168 0 254 254 78 78 78 78 78 78 78 83 190 174 254 254 47 0 0 0 0 0 0 83 254 254 254 254 47 0 0 0 0 0 0 83 254 254 254 254 47 0 0 0 0 0 0 83 254 254 254 254 47 0 0 0 0 0 0 83 254 254 110 204 142 142 142 142 142 142 142 142 168 110 0 115 205 254 254 254 254 254 254 169 115 0 0 0 205 249 249 249 249 249 249 169 0 0 0 0 3 3 3 3 3 3 3 3 0 0""",
##########
    """7 12 19 239 239 239 239 239 239 239 239 239 239 239 239 254 254 254 254 254 254 254 254 254 254 254 254 152 152 152 152 152 152 152 152 152 152 254 177 0 0 0 0 0 0 0 0 0 83 254 170 0 0 0 0 0 0 0 0 82 185 165 165 0 0 0 0 0 0 0 205 207 169 0 0 0 0 0 0 0 0 0 205 254 169 0 0 0 0 0 0 0 0 0 205 254 169 0 0 0 0 0 0 0 0 0 205 254 47 0 0 0 0 0 0 0 0 180 198 198 47 0 0 0 0 0 0 82 174 218 47 0 0 0 0 0 0 0 0 82 254 254 47 0 0 0 0 0 0 0 0 82 254 227 47 0 0 0 0 0 0 0 0 82 254 170 0 0 0 0 0 0 0 0 81 148 230 170 0 0 0 0 0 0 0 142 142 170 0 0 0 0 0 0 0 0 0 205 254 170 0 0 0 0 0 0 0 0 0 205 249 170 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0""",
##########
    """2 13 19 239 239 239 239 239 239 239 239 239 239 6 0 0 246 254 254 254 254 254 254 254 254 251 105 3 0 152 152 152 152 152 152 152 152 152 152 249 100 100 0 0 0 0 0 0 0 0 0 1 246 254 128 0 0 0 0 0 0 0 0 0 1 246 254 128 0 0 0 0 0 0 0 0 0 1 246 254 128 0 0 0 0 0 0 0 0 0 1 246 254 128 0 0 68 68 68 68 68 68 68 68 246 184 128 0 0 123 254 254 254 254 254 254 254 190 5 0 0 122 180 254 254 254 254 254 254 251 6 0 0 174 174 129 78 78 78 78 78 78 78 0 0 0 246 254 129 0 0 0 0 0 0 0 0 0 0 246 254 129 0 0 0 0 0 0 0 0 0 0 246 254 129 0 0 0 0 0 0 0 0 0 0 246 254 129 0 0 0 0 0 0 0 0 0 0 246 254 142 142 142 142 142 142 142 142 142 142 128 246 254 254 254 254 254 254 254 254 254 254 254 128 246 249 249 249 249 249 249 249 249 249 249 249 128 3 3 3 3 3 3 3 3 3 3 3 3 3""",
##########


    """8 13 19 0 0 123 239 239 239 239 239 239 239 6 0 0 0 105 123 254 254 254 254 254 254 251 105 3 0 100 122 152 152 152 152 152 152 152 152 249 100 100 246 254 129 0 0 0 0 0 0 1 246 254 128 246 254 129 0 0 0 0 0 0 1 246 254 128 246 254 129 0 0 0 0 0 0 1 246 254 128 246 254 129 0 0 0 0 0 0 1 246 254 128 184 184 129 68 68 68 68 68 68 68 246 184 128 0 122 190 254 254 254 254 254 254 254 190 5 0 0 0 123 254 254 254 254 254 254 251 6 0 0 174 174 129 82 82 82 82 82 82 82 174 174 128 246 254 129 0 0 0 0 0 0 1 246 254 128 246 254 129 0 0 0 0 0 0 1 246 254 128 246 254 129 0 0 0 0 0 0 1 246 254 128 246 254 129 0 0 0 0 0 0 1 246 254 128 110 122 142 142 142 142 142 142 142 142 247 110 110 0 115 123 254 254 254 254 254 254 251 115 4 0 0 0 123 249 249 249 249 249 249 249 6 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0""",
##########
    """3 13 19 239 239 239 239 239 239 239 239 239 239 6 0 0 246 254 254 254 254 254 254 254 254 251 105 3 0 152 152 152 152 152 152 152 152 152 152 249 100 100 0 0 0 0 0 0 0 0 0 1 246 254 128 0 0 0 0 0 0 0 0 0 1 246 254 128 0 0 0 0 0 0 0 0 0 1 246 254 128 0 0 0 0 0 0 0 0 0 1 246 254 128 0 68 68 68 68 68 68 68 68 68 246 184 128 0 122 190 254 254 254 254 254 254 254 190 5 0 0 0 123 254 254 254 254 254 254 251 6 0 0 0 0 82 82 82 82 82 82 82 82 174 174 128 0 0 0 0 0 0 0 0 0 1 246 254 128 0 0 0 0 0 0 0 0 0 1 246 254 128 0 0 0 0 0 0 0 0 0 1 246 254 128 0 0 0 0 0 0 0 0 0 1 246 254 128 142 142 142 142 142 142 142 142 142 142 247 110 110 246 254 254 254 254 254 254 254 254 251 115 4 0 246 249 249 249 249 249 249 249 249 249 6 0 0 3 3 3 3 3 3 3 3 3 3 0 0 0""",
##########
    """2 13 19 164 239 239 239 239 239 239 239 239 239 88 0 0 164 254 254 254 254 254 254 254 254 254 105 82 0 152 152 152 152 152 152 152 152 152 152 172 100 100 0 0 0 0 0 0 0 0 0 0 164 254 210 0 0 0 0 0 0 0 0 0 0 164 254 210 0 0 0 0 0 0 0 0 0 0 164 254 210 0 0 0 0 0 0 0 0 0 0 164 254 210 0 0 23 68 68 68 68 68 68 68 164 184 184 0 0 41 254 254 254 254 254 254 254 190 87 0 0 40 180 254 254 254 254 254 254 254 88 0 0 164 174 211 78 78 78 78 78 78 78 64 0 0 164 254 211 0 0 0 0 0 0 0 0 0 0 164 254 211 0 0 0 0 0 0 0 0 0 0 164 254 211 0 0 0 0 0 0 0 0 0 0 164 254 211 0 0 0 0 0 0 0 0 0 0 164 254 212 142 142 142 142 142 142 142 142 142 142 164 254 254 254 254 254 254 254 254 254 254 254 210 164 249 249 249 249 249 249 249 249 249 249 249 210 3 3 3 3 3 3 3 3 3 3 3 3 3""",
##########

    """0 12 19 0 0 212 239 239 239 239 239 239 159 0 0 0 105 212 254 254 254 254 254 254 159 105 0 100 211 152 152 152 152 152 152 152 152 157 100 254 254 40 0 0 0 0 0 0 93 254 254 254 254 40 0 0 0 0 0 0 93 254 254 254 254 40 0 0 0 0 0 0 93 254 254 254 254 40 0 0 0 0 0 0 93 254 254 254 254 40 0 0 0 0 0 0 93 254 254 254 254 40 0 0 0 0 0 0 93 254 254 254 254 40 0 0 0 0 0 0 93 254 254 254 254 40 0 0 0 0 0 0 93 254 254 254 254 40 0 0 0 0 0 0 93 254 254 254 254 40 0 0 0 0 0 0 93 254 254 254 254 40 0 0 0 0 0 0 93 254 254 254 254 40 0 0 0 0 0 0 93 254 254 110 211 142 142 142 142 142 142 142 142 157 110 0 115 212 254 254 254 254 254 254 159 115 0 0 0 212 249 249 249 249 249 249 159 0 0 0 0 3 3 3 3 3 3 3 3 0 0""",
##########
    """8 13 19 0 0 41 239 239 239 239 239 239 239 88 0 0 0 38 105 254 254 254 254 254 254 254 105 82 0 100 100 215 152 152 152 152 152 152 152 172 100 100 164 254 211 0 0 0 0 0 0 0 164 254 210 164 254 211 0 0 0 0 0 0 0 164 254 210 164 254 211 0 0 0 0 0 0 0 164 254 210 164 254 211 0 0 0 0 0 0 0 164 254 210 164 184 211 68 68 68 68 68 68 68 164 184 184 0 40 190 254 254 254 254 254 254 254 190 87 0 0 0 41 254 254 254 254 254 254 254 88 0 0 164 174 174 82 82 82 82 82 82 82 164 174 174 164 254 211 0 0 0 0 0 0 0 164 254 210 164 254 211 0 0 0 0 0 0 0 164 254 210 164 254 211 0 0 0 0 0 0 0 164 254 210 164 254 211 0 0 0 0 0 0 0 164 254 210 110 110 212 142 142 142 142 142 142 142 168 110 110 0 40 115 254 254 254 254 254 254 254 115 85 0 0 0 41 249 249 249 249 249 249 249 88 0 0 0 0 0 3 3 3 3 3 3 3 0 0 0""",
##########
    """7 13 19 239 239 239 239 239 239 239 239 239 239 239 239 128 246 254 254 254 254 254 254 254 254 254 254 254 128 152 152 152 152 152 152 152 152 152 152 249 254 128 0 0 0 0 0 0 0 0 0 1 246 252 6 0 0 0 0 0 0 0 0 0 212 165 165 6 0 0 0 0 0 0 0 123 207 251 6 0 0 0 0 0 0 0 0 0 123 254 251 6 0 0 0 0 0 0 0 0 0 123 254 184 6 0 0 0 0 0 0 0 0 0 123 254 129 0 0 0 0 0 0 0 0 0 122 180 198 129 0 0 0 0 0 0 0 0 174 174 129 0 0 0 0 0 0 0 0 0 0 246 254 129 0 0 0 0 0 0 0 0 0 0 246 254 129 0 0 0 0 0 0 0 0 0 0 246 252 6 0 0 0 0 0 0 0 0 0 148 230 230 6 0 0 0 0 0 0 0 123 142 246 6 0 0 0 0 0 0 0 0 0 123 254 252 6 0 0 0 0 0 0 0 0 0 123 249 249 6 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0 0""",
##########
    """5 12 19 239 239 239 239 239 239 239 239 239 239 239 239 254 254 254 254 254 254 254 254 254 254 254 254 254 254 152 152 152 152 152 152 152 152 152 152 254 254 41 0 0 0 0 0 0 0 0 0 254 254 41 0 0 0 0 0 0 0 0 0 254 254 41 0 0 0 0 0 0 0 0 0 254 254 41 0 0 0 0 0 0 0 0 0 254 254 68 68 68 68 68 68 68 68 0 0 254 254 254 254 254 254 254 254 254 163 0 0 254 254 254 254 254 254 254 254 254 192 162 0 78 78 78 78 78 78 78 78 78 89 187 174 0 0 0 0 0 0 0 0 0 89 254 254 0 0 0 0 0 0 0 0 0 89 254 254 0 0 0 0 0 0 0 0 0 89 254 254 0 0 0 0 0 0 0 0 0 89 254 254 142 142 142 142 142 142 142 142 142 142 162 110 254 254 254 254 254 254 254 254 254 163 115 0 249 249 249 249 249 249 249 249 249 163 0 0 3 3 3 3 3 3 3 3 3 3 0 0""",
##########

    """? 11 16 239 239 239 239 239 239 239 239 239 162 0 254 254 254 254 254 254 254 254 254 162 105 152 152 152 152 152 152 152 152 152 152 161 0 0 0 0 0 0 0 0 0 90 254 0 0 0 0 0 0 0 0 0 90 254 0 0 0 0 0 0 0 0 0 90 254 0 0 0 0 0 0 0 0 0 90 254 0 0 0 0 0 0 0 68 68 90 194 0 0 0 0 0 0 0 213 254 199 161 0 0 0 0 0 0 180 228 254 162 0 0 0 0 0 90 174 225 78 78 78 0 0 0 0 0 90 254 254 39 0 0 0 0 0 0 0 90 217 217 39 0 0 0 0 0 0 0 90 142 142 39 0 0 0 0 0 0 0 90 254 254 39 0 0 0 0 0 0 0 90 249 249 39 0 0 0""",
##########
    """6 13 19 0 0 41 239 239 239 239 239 239 239 239 87 0 0 38 105 254 254 254 254 254 254 254 88 11 0 100 100 215 152 152 152 152 152 152 152 88 0 0 164 254 211 0 0 0 0 0 0 0 0 0 0 164 254 211 0 0 0 0 0 0 0 0 0 0 164 254 211 0 0 0 0 0 0 0 0 0 0 164 254 211 0 0 0 0 0 0 0 0 0 0 164 254 211 68 68 68 68 68 68 68 56 0 0 164 254 254 254 254 254 254 254 254 254 88 0 0 164 254 254 254 254 254 254 254 254 254 180 87 0 164 254 211 78 78 78 78 78 78 78 164 174 174 164 254 211 0 0 0 0 0 0 0 164 254 210 164 254 211 0 0 0 0 0 0 0 164 254 210 164 254 211 0 0 0 0 0 0 0 164 254 210 164 254 211 0 0 0 0 0 0 0 164 254 210 110 110 212 142 142 142 142 142 142 142 168 110 110 0 40 115 254 254 254 254 254 254 254 115 85 0 0 0 41 249 249 249 249 249 249 249 88 0 0 0 0 0 3 3 3 3 3 3 3 0 0 0""",
##########
    """4 12 19 0 0 0 0 37 239 239 239 239 215 0 0 0 0 0 0 37 254 254 254 254 215 0 0 0 0 100 100 100 157 157 172 254 215 0 0 0 0 160 254 215 0 0 160 254 215 0 0 0 0 160 254 215 0 0 160 254 215 0 0 0 0 160 254 93 0 0 160 254 215 0 0 0 73 160 254 93 0 0 160 254 215 0 0 68 159 92 59 51 0 0 160 254 215 0 0 254 254 92 0 0 0 0 160 254 215 0 0 254 254 92 0 0 0 0 160 254 215 0 0 254 254 174 174 174 174 174 185 254 93 174 174 254 254 254 254 254 254 254 254 254 93 254 254 222 222 222 222 222 222 222 92 91 78 222 222 0 0 0 0 0 0 0 160 254 215 0 0 0 0 0 0 0 0 0 160 254 215 0 0 0 0 0 0 0 0 0 160 254 215 0 0 0 0 0 0 0 0 0 160 254 215 0 0 0 0 0 0 0 0 0 160 249 215 0 0 0 0 0 0 0 0 0 3 3 3 0 0""",
##########
    """1 6 19 125 239 239 239 239 127 125 254 254 254 254 127 125 152 152 251 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 254 127 0 0 3 248 249 127 0 0 0 3 3 3""",
##########
    """0 13 19 0 0 131 239 239 239 239 239 239 239 0 0 0 0 105 131 254 254 254 254 254 254 241 105 0 0 100 129 152 152 152 152 152 152 152 152 239 100 98 252 254 121 0 0 0 0 0 0 11 254 254 117 252 254 121 0 0 0 0 0 0 11 254 254 117 252 254 121 0 0 0 0 0 0 11 254 254 117 252 254 121 0 0 0 0 0 0 11 254 254 117 252 254 121 0 0 0 0 0 0 11 254 254 117 252 254 121 0 0 0 0 0 0 11 254 254 117 252 254 121 0 0 0 0 0 0 11 254 254 117 252 254 121 0 0 0 0 0 0 11 254 254 117 252 254 121 0 0 0 0 0 0 11 254 254 117 252 254 121 0 0 0 0 0 0 11 254 254 117 252 254 121 0 0 0 0 0 0 11 254 254 117 252 254 121 0 0 0 0 0 0 11 254 254 117 110 129 142 142 142 142 142 142 142 142 239 110 107 0 115 131 254 254 254 254 254 254 241 115 0 0 0 0 131 249 249 249 249 249 249 241 0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0""",
##########
    """5 13 19 239 239 239 239 239 239 239 239 239 239 239 239 122 252 254 254 254 254 254 254 254 254 254 254 254 122 252 254 152 152 152 152 152 152 152 152 152 152 122 252 254 123 0 0 0 0 0 0 0 0 0 0 252 254 123 0 0 0 0 0 0 0 0 0 0 252 254 123 0 0 0 0 0 0 0 0 0 0 252 254 123 0 0 0 0 0 0 0 0 0 0 252 254 123 68 68 68 68 68 68 68 0 0 0 252 254 254 254 254 254 254 254 254 245 0 0 0 252 254 254 254 254 254 254 254 254 254 180 0 0 78 78 78 78 78 78 78 78 78 78 253 174 122 0 0 0 0 0 0 0 0 0 7 253 254 122 0 0 0 0 0 0 0 0 0 7 253 254 122 0 0 0 0 0 0 0 0 0 7 253 254 122 0 0 0 0 0 0 0 0 0 7 253 254 122 142 142 142 142 142 142 142 142 142 142 244 110 109 252 254 254 254 254 254 254 254 254 245 115 0 0 249 249 249 249 249 249 249 249 249 245 0 0 0 3 3 3 3 3 3 3 3 3 3 0 0 0""",
########## desordre


##########
    """0 13 19 0 0 49 239 239 239 239 239 239 239 77 0 0 0 45 105 254 254 254 254 254 254 254 105 71 0 100 100 208 152 152 152 152 152 152 152 182 100 100 170 254 203 0 0 0 0 0 0 0 175 254 199 170 254 203 0 0 0 0 0 0 0 175 254 199 170 254 203 0 0 0 0 0 0 0 175 254 199 170 254 203 0 0 0 0 0 0 0 175 254 199 170 254 203 0 0 0 0 0 0 0 175 254 199 170 254 203 0 0 0 0 0 0 0 175 254 199 170 254 203 0 0 0 0 0 0 0 175 254 199 170 254 203 0 0 0 0 0 0 0 175 254 199 170 254 203 0 0 0 0 0 0 0 175 254 199 170 254 203 0 0 0 0 0 0 0 175 254 199 170 254 203 0 0 0 0 0 0 0 175 254 199 170 254 203 0 0 0 0 0 0 0 175 254 199 110 110 205 142 142 142 142 142 142 142 178 110 110 0 46 115 254 254 254 254 254 254 254 115 74 0 0 0 49 249 249 249 249 249 249 249 77 0 0 0 0 0 3 3 3 3 3 3 3 0 0 0""",
##########
    """1 5 19 207 239 239 239 239 207 254 254 254 254 152 152 152 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 249 249 0 0 0 3 3""",
##########
    """1 5 19 239 239 239 239 208 254 254 254 254 208 152 152 174 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 254 208 0 0 166 249 208 0 0 3 3 3""",
##########
    """2 12 19 239 239 239 239 239 239 239 239 239 169 0 0 254 254 254 254 254 254 254 254 254 169 105 0 152 152 152 152 152 152 152 152 152 152 168 100 0 0 0 0 0 0 0 0 0 83 254 254 0 0 0 0 0 0 0 0 0 83 254 254 0 0 0 0 0 0 0 0 0 83 254 254 0 0 0 0 0 0 0 0 0 83 254 254 0 0 68 68 68 68 68 68 68 83 198 184 0 0 205 254 254 254 254 254 254 203 168 0 0 180 222 254 254 254 254 254 254 169 0 0 174 218 78 78 78 78 78 78 78 78 0 0 254 254 47 0 0 0 0 0 0 0 0 0 254 254 47 0 0 0 0 0 0 0 0 0 254 254 47 0 0 0 0 0 0 0 0 0 254 254 47 0 0 0 0 0 0 0 0 0 254 254 142 142 142 142 142 142 142 142 142 142 254 254 254 254 254 254 254 254 254 254 254 254 249 249 249 249 249 249 249 249 249 249 249 249 3 3 3 3 3 3 3 3 3 3 3 3""",
##########
    """3 12 19 239 239 239 239 239 239 239 239 239 169 0 0 254 254 254 254 254 254 254 254 254 169 105 0 152 152 152 152 152 152 152 152 152 152 168 100 0 0 0 0 0 0 0 0 0 83 254 254 0 0 0 0 0 0 0 0 0 83 254 254 0 0 0 0 0 0 0 0 0 83 254 254 0 0 0 0 0 0 0 0 0 83 254 254 0 68 68 68 68 68 68 68 68 83 198 184 0 190 228 254 254 254 254 254 254 203 168 0 0 0 205 254 254 254 254 254 254 169 0 0 0 0 82 82 82 82 82 82 82 83 174 174 0 0 0 0 0 0 0 0 0 83 254 254 0 0 0 0 0 0 0 0 0 83 254 254 0 0 0 0 0 0 0 0 0 83 254 254 0 0 0 0 0 0 0 0 0 83 254 254 142 142 142 142 142 142 142 142 142 142 168 110 254 254 254 254 254 254 254 254 254 169 115 0 249 249 249 249 249 249 249 249 249 169 0 0 3 3 3 3 3 3 3 3 3 3 0 0""",
##########
    """3 13 19 164 239 239 239 239 239 239 239 239 239 88 0 0 164 254 254 254 254 254 254 254 254 254 105 82 0 152 152 152 152 152 152 152 152 152 152 172 100 100 0 0 0 0 0 0 0 0 0 0 164 254 210 0 0 0 0 0 0 0 0 0 0 164 254 210 0 0 0 0 0 0 0 0 0 0 164 254 210 0 0 0 0 0 0 0 0 0 0 164 254 210 0 22 68 68 68 68 68 68 68 68 164 184 184 0 40 190 254 254 254 254 254 254 254 190 87 0 0 0 41 254 254 254 254 254 254 254 88 0 0 0 0 31 82 82 82 82 82 82 82 164 174 174 0 0 0 0 0 0 0 0 0 0 164 254 210 0 0 0 0 0 0 0 0 0 0 164 254 210 0 0 0 0 0 0 0 0 0 0 164 254 210 0 0 0 0 0 0 0 0 0 0 164 254 210 142 142 142 142 142 142 142 142 142 142 168 110 110 164 254 254 254 254 254 254 254 254 254 115 85 0 164 249 249 249 249 249 249 249 249 249 88 0 0 3 3 3 3 3 3 3 3 3 3 0 0 0""",    
##########
    """4 13 19 0 0 0 0 0 201 239 239 239 239 51 0 0 0 0 0 0 0 201 254 254 254 254 51 0 0 0 0 71 100 100 157 157 157 254 254 51 0 0 0 0 78 254 254 51 0 78 254 254 51 0 0 0 0 78 254 254 51 0 78 254 254 51 0 0 0 0 78 254 175 16 0 78 254 254 51 0 0 0 54 78 254 175 0 0 78 254 254 51 0 0 68 77 174 59 59 0 0 78 254 254 51 0 0 201 254 174 0 0 0 0 78 254 254 51 0 0 201 254 174 0 0 0 0 78 254 254 51 0 0 201 254 194 174 174 174 174 174 254 175 174 174 174 201 254 254 254 254 254 254 254 254 175 201 254 174 201 222 222 222 222 222 222 174 91 91 201 222 174 0 0 0 0 0 0 0 78 254 254 51 0 0 0 0 0 0 0 0 0 78 254 254 51 0 0 0 0 0 0 0 0 0 78 254 254 51 0 0 0 0 0 0 0 0 0 78 254 254 51 0 0 0 0 0 0 0 0 0 78 249 249 51 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0""",    
##########    
    """5 13 19 170 239 239 239 239 239 239 239 239 239 239 239 204 170 254 254 254 254 254 254 254 254 254 254 254 204 170 254 209 152 152 152 152 152 152 152 152 152 152 170 254 205 0 0 0 0 0 0 0 0 0 0 170 254 205 0 0 0 0 0 0 0 0 0 0 170 254 205 0 0 0 0 0 0 0 0 0 0 170 254 205 0 0 0 0 0 0 0 0 0 0 170 254 205 68 68 68 68 68 68 68 53 0 0 170 254 254 254 254 254 254 254 254 254 81 0 0 170 254 254 254 254 254 254 254 254 254 180 80 0 78 78 78 78 78 78 78 78 78 78 171 174 174 0 0 0 0 0 0 0 0 0 0 171 254 204 0 0 0 0 0 0 0 0 0 0 171 254 204 0 0 0 0 0 0 0 0 0 0 171 254 204 0 0 0 0 0 0 0 0 0 0 171 254 204 142 142 142 142 142 142 142 142 142 142 173 110 110 170 254 254 254 254 254 254 254 254 254 115 79 0 170 249 249 249 249 249 249 249 249 249 81 0 0 3 3 3 3 3 3 3 3 3 3 0 0 0""",
##########
    """7 13 19 164 239 239 239 239 239 239 239 239 239 239 239 210 164 254 254 254 254 254 254 254 254 254 254 254 210 152 152 152 152 152 152 152 152 152 152 172 254 152 0 0 0 0 0 0 0 0 0 0 164 254 88 0 0 0 0 0 0 0 0 0 163 165 165 88 0 0 0 0 0 0 0 42 207 215 88 0 0 0 0 0 0 0 0 0 42 254 254 88 0 0 0 0 0 0 0 0 0 42 254 229 88 0 0 0 0 0 0 0 0 0 42 254 211 0 0 0 0 0 0 0 0 0 41 180 198 198 0 0 0 0 0 0 0 0 164 174 210 0 0 0 0 0 0 0 0 0 0 164 254 210 0 0 0 0 0 0 0 0 0 0 164 254 210 0 0 0 0 0 0 0 0 0 0 164 254 88 0 0 0 0 0 0 0 0 0 148 170 230 88 0 0 0 0 0 0 0 41 142 167 88 0 0 0 0 0 0 0 0 0 41 254 254 88 0 0 0 0 0 0 0 0 0 41 249 249 88 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 0""",    
##########
    """8 12 19 0 0 205 239 239 239 239 239 239 169 0 0 0 105 205 254 254 254 254 254 254 169 105 0 100 204 152 152 152 152 152 152 152 152 168 100 254 254 47 0 0 0 0 0 0 83 254 254 254 254 47 0 0 0 0 0 0 83 254 254 254 254 47 0 0 0 0 0 0 83 254 254 254 254 47 0 0 0 0 0 0 83 254 254 184 224 68 68 68 68 68 68 68 83 198 184 0 190 228 254 254 254 254 254 254 203 168 0 0 0 205 254 254 254 254 254 254 169 0 0 174 174 82 82 82 82 82 82 82 83 174 174 254 254 47 0 0 0 0 0 0 83 254 254 254 254 47 0 0 0 0 0 0 83 254 254 254 254 47 0 0 0 0 0 0 83 254 254 254 254 47 0 0 0 0 0 0 83 254 254 110 204 142 142 142 142 142 142 142 142 168 110 0 115 205 254 254 254 254 254 254 169 115 0 0 0 205 249 249 249 249 249 249 169 0 0 0 0 3 3 3 3 3 3 3 3 0 0""",    
##########
    """9 13 19 0 0 41 239 239 239 239 239 239 239 88 0 0 0 38 105 254 254 254 254 254 254 254 105 82 0 100 100 215 152 152 152 152 152 152 152 172 100 100 164 254 211 0 0 0 0 0 0 0 164 254 210 164 254 211 0 0 0 0 0 0 0 164 254 210 164 254 211 0 0 0 0 0 0 0 164 254 210 164 254 211 0 0 0 0 0 0 0 164 254 210 164 184 211 68 68 68 68 68 68 68 164 254 210 0 40 190 254 254 254 254 254 254 254 254 254 210 0 0 41 254 254 254 254 254 254 254 254 254 210 0 0 28 78 78 78 78 78 78 78 164 254 210 0 0 0 0 0 0 0 0 0 0 164 254 210 0 0 0 0 0 0 0 0 0 0 164 254 210 0 0 0 0 0 0 0 0 0 0 164 254 210 0 0 0 0 0 0 0 0 0 0 164 254 210 0 40 142 142 142 142 142 142 142 142 168 110 110 0 40 115 254 254 254 254 254 254 254 115 85 0 0 0 41 249 249 249 249 249 249 249 88 0 0 0 0 0 3 3 3 3 3 3 3 0 0 0""",
##########
    """9 12 19 0 0 205 239 239 239 239 239 239 169 0 0 0 105 205 254 254 254 254 254 254 169 105 0 100 204 152 152 152 152 152 152 152 152 168 100 254 254 47 0 0 0 0 0 0 83 254 254 254 254 47 0 0 0 0 0 0 83 254 254 254 254 47 0 0 0 0 0 0 83 254 254 254 254 47 0 0 0 0 0 0 83 254 254 184 224 68 68 68 68 68 68 68 83 254 254 0 190 228 254 254 254 254 254 254 254 254 254 0 0 205 254 254 254 254 254 254 254 254 254 0 0 78 78 78 78 78 78 78 83 254 254 0 0 0 0 0 0 0 0 0 83 254 254 0 0 0 0 0 0 0 0 0 83 254 254 0 0 0 0 0 0 0 0 0 83 254 254 0 0 0 0 0 0 0 0 0 83 254 254 0 142 142 142 142 142 142 142 142 142 168 110 0 115 205 254 254 254 254 254 254 169 115 0 0 0 205 249 249 249 249 249 249 169 0 0 0 0 3 3 3 3 3 3 3 3 0 0""",    
##########
    """? 12 16 239 239 239 239 239 239 239 239 239 162 0 0 254 254 254 254 254 254 254 254 254 162 105 0 152 152 152 152 152 152 152 152 152 152 161 100 0 0 0 0 0 0 0 0 0 90 254 254 0 0 0 0 0 0 0 0 0 90 254 254 0 0 0 0 0 0 0 0 0 90 254 254 0 0 0 0 0 0 0 0 0 90 254 254 0 0 0 0 0 0 0 68 68 90 194 184 0 0 0 0 0 0 0 213 254 199 161 0 0 0 0 0 0 0 180 228 254 162 0 0 0 0 0 0 90 174 225 78 78 78 0 0 0 0 0 0 90 254 254 39 0 0 0 0 0 0 0 0 90 217 217 39 0 0 0 0 0 0 0 0 90 142 142 39 0 0 0 0 0 0 0 0 90 254 254 39 0 0 0 0 0 0 0 0 90 249 249 39 0 0 0 0""",    
##########
    """? 12 17 239 239 239 239 239 239 239 239 239 162 0 0 254 254 254 254 254 254 254 254 254 162 105 0 152 152 152 152 152 152 152 152 152 152 161 100 0 0 0 0 0 0 0 0 0 90 254 254 0 0 0 0 0 0 0 0 0 90 254 254 0 0 0 0 0 0 0 0 0 90 254 254 0 0 0 0 0 0 0 0 0 90 254 254 0 0 0 0 0 0 0 68 68 90 194 184 0 0 0 0 0 0 0 213 254 199 161 0 0 0 0 0 0 0 180 228 254 162 0 0 0 0 0 0 90 174 225 78 78 78 0 0 0 0 0 0 90 254 254 39 0 0 0 0 0 0 0 0 90 217 217 39 0 0 0 0 0 0 0 0 90 142 142 39 0 0 0 0 0 0 0 0 90 254 254 39 0 0 0 0 0 0 0 0 90 249 249 39 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0 0""",    
##########
    """? 11 17 239 239 239 239 239 239 239 239 239 162 0 254 254 254 254 254 254 254 254 254 162 105 152 152 152 152 152 152 152 152 152 152 161 0 0 0 0 0 0 0 0 0 90 254 0 0 0 0 0 0 0 0 0 90 254 0 0 0 0 0 0 0 0 0 90 254 0 0 0 0 0 0 0 0 0 90 254 0 0 0 0 0 0 0 68 68 90 194 0 0 0 0 0 0 0 213 254 199 161 0 0 0 0 0 0 180 228 254 162 0 0 0 0 0 90 174 225 78 78 78 0 0 0 0 0 90 254 254 39 0 0 0 0 0 0 0 90 217 217 39 0 0 0 0 0 0 0 90 142 142 39 0 0 0 0 0 0 0 90 254 254 39 0 0 0 0 0 0 0 90 249 249 39 0 0 0 0 0 0 0 0 3 3 0 0 0 0""",    
##########    
    """+ 13 13 0 0 0 0 0 161 242 214 0 0 0 0 0 0 0 0 0 0 161 254 214 0 0 0 0 0 0 0 0 0 0 161 254 214 0 0 0 0 0 0 0 0 0 0 161 254 214 0 0 0 0 0 0 0 0 0 0 161 254 214 0 0 0 0 0 161 244 244 244 244 249 254 91 244 244 244 244 214 161 254 254 254 254 253 253 91 254 254 254 254 214 134 134 134 134 134 122 122 122 134 134 134 134 134 0 0 0 0 0 161 254 214 0 0 0 0 0 0 0 0 0 0 161 254 214 0 0 0 0 0 0 0 0 0 0 161 254 214 0 0 0 0 0 0 0 0 0 0 161 254 214 0 0 0 0 0 0 0 0 0 0 127 127 127 0 0 0 0 0""",    
##########
    """= 8 6 164 244 244 244 244 244 244 210 164 254 254 254 254 254 254 210 155 155 155 155 155 155 155 155 164 197 197 197 197 197 197 197 164 254 254 254 254 254 254 210 164 202 202 202 202 202 202 202""",   
##########
    """( 6 24 0 0 0 132 132 132 0 0 0 224 254 151 0 0 223 254 254 151 101 239 254 28 13 13 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 254 254 28 0 0 101 249 254 28 3 3 1 3 223 249 249 151 0 0 9 224 254 151 0 0 0 142 142 142""",
##########
    """) 5 24 132 132 132 0 0 207 254 168 0 0 207 254 252 167 0 13 13 84 246 239 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 0 0 84 254 254 3 3 84 254 249 207 249 249 167 3 207 254 168 9 0 142 142 142 0 0""",    
)