# Document de conception du script Anti-Idle Math Solver #

## Trucs intéressants présents dans ce script, récupérables pour d'autres projets ##

 - Conversion de couleurs RGB vers HSV, sans jamais utiliser de float. (Donc rapide).

 - Capture d'écran avec la librairie wx.
 
 - Enregistrement de fichier image, au format png, avec wx.
 
 - Lecture de pixel dans une image / un dc, avec wx.
 
 - Vague idée d'un crawler, qui parcoure une ligne/colonne de pixel, afin de trouver le premier pixel répondant ou ne répondant pas à une condition donnée. (Y'a que l'idée, sans le code).
 
## Macro-description du script ##

TRIP: Les macros sont des poissons. Ou des gestionnaires de putes. C'est au choix.

### Détection de la zone de jeu ###

La zone de jeu peut être n'importe où à l'écran. Si elle est affichée entièrement, et n'est cachée par aucune autre fenêtre, le script est censé la détecter.

La "zone de jeu" représente le rectangle affichant Math Master. Il ne s'agit pas de la zone affichant le jeu Anti-Idle en entier. 

Exemple de zone de jeu : 
![Intro jeu](https://raw.github.com/darkrecher/Anti-Idle-Math-Solver/master/doc_img_readme/screenshot-intro.png)

Cette action est réalisée par la classe `GameRectDetector`, du fichier `gamedtc.py`

### Estimation de la zone d'énigme brute ###

"Zone d'énigme" = rectangle, à l'écran, affichant la question mathématique posée au joueur par le jeu Math Master. Au début elle est brute, et ensuite on l'affine.

Exemple de zone d'énigme brute : 

![Intro jeu](https://raw.github.com/darkrecher/Anti-Idle-Math-Solver/master/doc_img_readme/screenshot-rez.png)

Exemple de zone d'énigme :

![Intro jeu](https://raw.github.com/darkrecher/Anti-Idle-Math-Solver/master/doc_img_readme/screenshot-ez.png)

La zone d'énigme brute se déduit de la zone de jeu, par un simple rognage de l'image, selon des proportions prédéfinies. 

Cette action est réalisée par la classe GameRectDetector, dans le fichier gamedtc.py

### Détection du début du jeu, et estimation de la zone d'énigme pas brute ###

Pour savoir si le jeu a commencé, on teste la couleur du pixel en bas à gauche de la zone d'énigme brute. Si il correspond au bleu du fond du jeu, on considère que ça a commencé.

Dès que ça commencé, on détecte la zone d'énigme. On rogne des lignes de la zone d'énigme brute, en partant du haut et en partant du bas. Une ligne est à rogner si elle ne contient aucun pixel "intéressant". C'est à dire un pixel suffisamment jaune ou blanc. (Par conséquent, le contour noir en haut et en bas des symboles est rogné). 

La zone n'est pas rognée à gauche ni à droite, car on ne peut pas présumer de la largeur que prendra l'affichage d'une énigme.

Ces actions sont réalisées par la classe EnigmaZoneDetector, du fichier enizodtc.

### Extraction des symboles bruts et de la couleur du gros opérateur ###

Un "symbole" = la représentation graphique de l'un des caractères du texte de l'énigme. Par exemple, le dessin du "1", celui de la parenthèse "(", celui du point d'interrogation, ...

Le "gros opérateur" = L'opérateur que l'on voit parfois dans le texte d'une énigme, dans un gros cadre coloré. Dans les images ci-dessus, le gros opérateur, c'est le "+" vert.

Un "symbole brut" = comme un symbole, sauf que les lignes de pixels pas intéressants, éventuellement présentes en haut et en bas, ne sont pas rognées. Par exemple, le signe "=" a une hauteur plus petite que la zone d'énigme. Il faudra donc le rogner.

Dans la zone de l'énigme, on considère que lorsqu'on trouve plusieurs colonne adjacentes, comportant chacune au moins un pixel "intéressant", alors cela constitue un symbole.

Le jeu écrit les symboles en les espaçant suffisamment, et on a toujours au moins une colonne de pixels non intéressants entre deux symboles. (Du moins avec une résolution d'écran pas trop dégueux).

L'extraction de symboles renvoie 3 informations :

 - la liste des symboles trouvées avant le gros opérateur.
 
 - la couleur d'un pixel du gros opérateur. On n'a pas besoin du dessin complet du gros opérateur. On déduira l'opérateur correspondant à partir de cette simple couleur.
 
 - la liste des symboles trouvées après le gros opérateur. 
 
Certains textes d'énigme ne comportent pas de gros opérateur. Par exemple : 2?3=5. Dans ce cas, la première liste contient tous les symboles du texte de l'énigme. La couleur du gros opérateur est indéfinie, et la dernière liste est vide.

Ces actions sont effectuées par la classe SymbolExtractor, dans le fichier symbextr.py.

### Conversion couleur -> valeur d'encre ###

Un symbole est un dessin, et peut donc se définir par un tableau en 2D, contenant des valeurs de couleur rgb. Mais dans le script, on définit un symbole par un tableau en 2D, contenant des valeurs "d'encre". 

Une "valeur d'encre" = une valeur entre 0 et 255, représentant, pour un pixel donné, l'intensité de couleur jaune ou de couleur blanche de ce pixel. Le jaune et le blanc étant les 2 couleurs utilisées par le jeu pour afficher le texte de l'énigme. Une encre ne permet pas de savoir si le pixel est jaune ou blanc, mais on n'a pas besoin de cette info.

La conversion couleur rgb -> encre est effectuée durant l'étape d'extraction des symboles bruts (voir la partie précédente). Cette conversion est effectuée par la fonction SymbolExtractor._get_ink_of_pixel, dans le fichier symbextr.py

### Construction des symboles non bruts ###





