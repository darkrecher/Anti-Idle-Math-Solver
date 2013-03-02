# Document de conception du script Anti-Idle Math Solver #

## Trucs int�ressants pr�sents dans ce script, r�cup�rables pour d'autres projets ##

 - Conversion de couleurs RGB vers HSV, sans jamais utiliser de float. (Donc rapide).

 - Capture d'�cran avec la librairie wx.
 
 - Enregistrement de fichier image, au format png, avec wx.
 
 - Lecture de pixel dans une image / un dc, avec wx.
 
 - Vague id�e d'un crawler, qui parcoure une ligne/colonne de pixel, afin de trouver le premier pixel r�pondant ou ne r�pondant pas � une condition donn�e. (Y'a que l'id�e, sans le code).
 
## Macro-description du script ##

TRIP: Les macros sont des poissons. Ou des gestionnaires de putes. C'est au choix.

### D�tection de la zone de jeu ###

La zone de jeu peut �tre n'importe o� � l'�cran. Si elle est affich�e enti�rement, et n'est cach�e par aucune autre fen�tre, le script est cens� la d�tecter.

La "zone de jeu" repr�sente le rectangle affichant Math Master. Il ne s'agit pas de la zone affichant le jeu Anti-Idle en entier. 

Exemple de zone de jeu : 
![Intro jeu](https://raw.github.com/darkrecher/Anti-Idle-Math-Solver/master/doc_img_readme/screenshot-intro.png)

Cette action est r�alis�e par la classe `GameRectDetector`, du fichier `gamedtc.py`

### Estimation de la zone d'�nigme brute ###

"Zone d'�nigme" = rectangle, � l'�cran, affichant la question math�matique pos�e au joueur par le jeu Math Master. Au d�but elle est brute, et ensuite on l'affine.

Exemple de zone d'�nigme brute : 

![Intro jeu](https://raw.github.com/darkrecher/Anti-Idle-Math-Solver/master/doc_img_readme/screenshot-rez.png)

Exemple de zone d'�nigme :

![Intro jeu](https://raw.github.com/darkrecher/Anti-Idle-Math-Solver/master/doc_img_readme/screenshot-ez.png)

La zone d'�nigme brute se d�duit de la zone de jeu, par un simple rognage de l'image, selon des proportions pr�d�finies. 

Cette action est r�alis�e par la classe GameRectDetector, dans le fichier gamedtc.py

### D�tection du d�but du jeu, et estimation de la zone d'�nigme pas brute ###

Pour savoir si le jeu a commenc�, on teste la couleur du pixel en bas � gauche de la zone d'�nigme brute. Si il correspond au bleu du fond du jeu, on consid�re que �a a commenc�.

D�s que �a commenc�, on d�tecte la zone d'�nigme. On rogne des lignes de la zone d'�nigme brute, en partant du haut et en partant du bas. Une ligne est � rogner si elle ne contient aucun pixel "int�ressant". C'est � dire un pixel suffisamment jaune ou blanc. (Par cons�quent, le contour noir en haut et en bas des symboles est rogn�). 

La zone n'est pas rogn�e � gauche ni � droite, car on ne peut pas pr�sumer de la largeur que prendra l'affichage d'une �nigme.

Ces actions sont r�alis�es par la classe EnigmaZoneDetector, du fichier enizodtc.

### Extraction des symboles bruts et de la couleur du gros op�rateur ###

Un "symbole" = la repr�sentation graphique de l'un des caract�res du texte de l'�nigme. Par exemple, le dessin du "1", celui de la parenth�se "(", celui du point d'interrogation, ...

Le "gros op�rateur" = L'op�rateur que l'on voit parfois dans le texte d'une �nigme, dans un gros cadre color�. Dans les images ci-dessus, le gros op�rateur, c'est le "+" vert.

Un "symbole brut" = comme un symbole, sauf que les lignes de pixels pas int�ressants, �ventuellement pr�sentes en haut et en bas, ne sont pas rogn�es. Par exemple, le signe "=" a une hauteur plus petite que la zone d'�nigme. Il faudra donc le rogner.

Dans la zone de l'�nigme, on consid�re que lorsqu'on trouve plusieurs colonne adjacentes, comportant chacune au moins un pixel "int�ressant", alors cela constitue un symbole.

Le jeu �crit les symboles en les espa�ant suffisamment, et on a toujours au moins une colonne de pixels non int�ressants entre deux symboles. (Du moins avec une r�solution d'�cran pas trop d�gueux).

L'extraction de symboles renvoie 3�informations :

 - la liste des symboles trouv�es avant le gros op�rateur.
 
 - la couleur d'un pixel du gros op�rateur. On n'a pas besoin du dessin complet du gros op�rateur. On d�duira l'op�rateur correspondant � partir de cette simple couleur.
 
 - la liste des symboles trouv�es apr�s le gros op�rateur. 
 
Certains textes d'�nigme ne comportent pas de gros op�rateur. Par exemple : 2?3=5. Dans ce cas, la premi�re liste contient tous les symboles du texte de l'�nigme. La couleur du gros op�rateur est ind�finie, et la derni�re liste est vide.

Ces actions sont effectu�es par la classe SymbolExtractor, dans le fichier symbextr.py.

### Conversion couleur -> valeur d'encre ###

Un symbole est un dessin, et peut donc se d�finir par un tableau en 2D, contenant des valeurs de couleur rgb. Mais dans le script, on d�finit un symbole par un tableau en 2D, contenant des valeurs "d'encre". 

Une "valeur d'encre" = une valeur entre 0 et 255, repr�sentant, pour un pixel donn�, l'intensit� de couleur jaune ou de couleur blanche de ce pixel. Le jaune et le blanc �tant les 2 couleurs utilis�es par le jeu pour afficher le texte de l'�nigme. Une encre ne permet pas de savoir si le pixel est jaune ou blanc, mais on n'a pas besoin de cette info.

La conversion couleur rgb -> encre est effectu�e durant l'�tape d'extraction des symboles bruts (voir la partie pr�c�dente). Cette conversion est effectu�e par la fonction SymbolExtractor._get_ink_of_pixel, dans le fichier symbextr.py

### Construction des symboles non bruts ###





