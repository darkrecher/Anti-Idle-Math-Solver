# -*- coding: utf-8 -*-


def hsv_from_rgb(red, grn, blu):
    """
    Personne utilise jamais le même standard pour ces putains de trucs.
    J'y pige que d'alle. Je me calque sur les valeurs que me renvoie mon logiciel de dessin
    préféré : Paint.NET.
    N'utilise que des nombres entiers. Depuis quand on a besoin de nombres décimaux de merde
    pour calculer un truc aussi simple ! Bande de gros clampins !
    Renvoie un trouple (hue, sat, val), avec hue entre 0 et 359. sat et val entre 0 et 100.
    """
    maxc = max(red, grn, blu)
    minc = min(red, grn, blu)    
    if maxc == minc:
        hue = 0
        sat = 0
        val = (maxc * 100) / 255
        return hue, sat, val
        
    dif = maxc - minc
    if maxc == red:
        hue = (60 * (grn-blu)) / dif  +  360
        if hue >= 360:
            hue -= 360
    elif maxc == grn:
        hue = (60 * (blu-red)) / dif  +  120
    elif maxc == blu:
        hue = (60 * (red-grn)) / dif  +  240
        
    if maxc == 0:
        sat = 0
    else:
        sat = (dif * 100) / maxc
        
    val = (maxc * 100) / 255
    return hue, sat, val

    
def is_same_col(col_1, col_2, tolerance=(8, 8, 8)):
    """Marche aussi bien avec le hsv que le rgb. Vu que c'est que des nombres,
    on s'en tape. Faut juste adapter la tolérance au type des couleurs comparées
    """
    for index_col in range(3):
        dist = abs(col_1[index_col] - col_2[index_col])
        if dist > tolerance[index_col]:
            return False
    return True
        
    
if __name__ == "__main__":

    # test unitaire qui tue, pour vérifier si ma fonction correspond bien à la version officielle
    # de mes couilles qui utilise des floats.
    
    def hsv_from_rgb_crap(r, g, b):
        """
        piqué ici : http://code.activestate.com/recipes/576919-python-rgb-and-hsv-conversion/
        """
        r, g, b = r/255.0, g/255.0, b/255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx-mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g-b)/df) + 360) % 360
        elif mx == g:
            h = (60 * ((b-r)/df) + 120) % 360
        elif mx == b:
            h = (60 * ((r-g)/df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = df/mx
        v = mx
        return h, s*100, v*100

    # bourrin, mais on aime ça.
    # Y'a tout qui passe bien. Par contre c'est un peu long.
    for red in range(256):
        for grn in range(256):
            for blu in range(256):
                hsv_1 = hsv_from_rgb(red, grn, blu)
                hsv_2 = hsv_from_rgb_crap(red, grn, blu)
                # conversion super dégueux. C'est le seul moyen que j'ai trouvé pour que
                # des conneries genre 89.99999999 se changent bien en 90, et non pas 89.
                # Bordel, voilà pourquoi j'essais d'utiliser ces cons de float le moins possible !
                hsv_2 = tuple( [ int(float(str(elem))) for elem in hsv_2 ] )
                if hsv_1 != hsv_2:
                    print red, grn, blu
                    print "mine : ", hsv_1
                    print "official : ", hsv_2
                    print "official : ", hsv_from_rgb_crap(red, grn, blu)
                    assert False
        print red
        
                
                