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

Il suffit de rogner les lignes inint�ressantes en haut et en bas du symbole. C'est � dire d'enlever les lignes comportante des valeurs d'encre toutes � 0.

Cete action est r�alis�e par la classe Symbol, dans le fichier symbol.py

### Reconnaissance des symboles et du gros op�rateur ###

On tente de trouver les caract�res correspondant � chaque symbole de l'�nigme, et de trouver le caract�re correspondant au gros op�rateur, afin d'obtenir le texte de l'�nigme.

Un symbole produit toujours un et un seul caract�re. Le gros op�rateur produit �galement un et un seul caract�re.

Le script poss�de une biblioth�que des symboles existants. Il tente de retrouver, dans cette biblioth�que, des symboles de l'�nigme. L'�galit� doit �tre parfaite. C'est � dire que la taille (hauteur et largeur), et le tableau en 2D des encres doivent �tre rigoureusement �gaux. 

Lorsqu'un symbole de l'�nigme ne peut pas �tre reconnu (il n'y a pas son �quivalent dans la biblioth�que des symboles), on consid�re que son caract�re correspondant est le point d'exclamation. Les textes d'�nigme ne comportent jamais de point d'exclamation, donc pas de risque de confusion.

Une �nigme est "solvable" si son texte ne comporte aucun point d'exclamation.

La biblioth�que des symboles connus se trouve dans le fichier symbdata.py.

Le chargement en m�moire de cette biblioth�que est effectu�e par la classe SymbolReferences, dans le fichier symbref.py

L'action de reconnaissance des symboles d'une �nigme est effectu�e par la classe EnigmaOcr, dans le fichier eniocr.py. Cette classe utilise une instance de SymbolReferences.

La reconnaissance du gros op�rateur est effectu�e par la classe EnigmaOcr.

### Demande des symboles non reconnus ###

Cette action (ainsi que les 2 actions suivantes) ne sont effectu�es que si l'�nigme n'est pas solvable.

Le script �crit le texte actuelle de l'�nigme sur la console (avec les points d'exclamation), et demande � l'utilisateur de saisir le texte complet de l'�nigme, ou bien les caract�res correspondants au points d'exclamations. Le script reste en attente tante que l'utilisateur n'a rien saisi.

Cette action est effectu�e directement dans le fichier main.py. (voir la ligne contenant un appel � `raw_input`)

### remplacement des points d'exclamation par la saisie de l'utilisateur, et mise � jour de la biblioth�que ###

On reconstitue le texte complet de l'�nigme, sans point d'exclamation, � partir des �ventuels symboles reconnus d�s le d�part, et de la saisie utilisateur.

Pour qu'une saisie utilisateur soit valide, elle doit respecter les contraintes suivantes :

 - Le nombre de caract�res saisis est soit �gal au nombre total de caract�re du texte de l'�nigme, soit �gal au nombre de point d'exclamation dans le texte de l'�nigme.
 
 - Seuls les caract�res "0123456789/*-+=?x()," sont autoris�s.
 
Si la saisie n'est pas valide, la biblioth�que des symboles n'est pas mise � jour (du moins pas enti�rement, voir description d�taill�e de cette �tape, un peu plus loin). 

Si la saisie est valide, on fait correspondre chaque symbole non reconnu avec son caract�re saisi par l'utilisateur, et on met ajoute les symboles nouvellement cr�� dans la biblioth�que.

La biblioth�que de symbole accepte que plusieurs symboles diff�rents correspondent au m�me caract�re. C'est n�cessaire, car certains symboles ne sont pas toujours affich� exactement de la m�me mani�re.

Cette action est effectu�e par la classe EnigmaOcr, ainsi que par l'instance de SymbolReferences contenues dans EnigmaOcr.

### Seconde tentative de reconnaissance des symboles ###

Cette action est exactement la m�me que celle d�crite dans l'�tape "Reconnaissance des symboles et du gros op�rateur".

Elle est effectu�e, m�me si la saisie utilisateur a �t� identifi�e comme invalide. Ce qui est un peu cr�tin, je le reconnais.

Si tout s'est bien pass�, la biblioth�que des symboles a �t� correctement mise � jour par la saisie utilisateur. Et cette seconde tentative de reconnaissance doit aboutir � un texte d'�nigme sans solvable. 

M�me si ce nouveau texte n'est pas solvable, on passe quand m�me � l'�tape suivante.

Les actions cr�tines de cette �tape sont � l'origine du bug "blocage sur la question en cours suite � un �chec", d�crit dans le fichier readme.md. J'ai la flemme de le corriger.

### R�solution de l'�nigme ###

� partir de cette �tape, on n'a plus besoin des symboles. Le texte de l'�nigme suffit.

Cette action est effectu�e quel que soit ce qu'il s'est pass� avant. C'est � dire, dans les cas suivants :

 - La reconnaissance des symboles a march� du premier coup et a donn� un texte d'�nigme solvable.
 
 - La reconnaissance a march� au deuxi�me coup (apr�s la saisie utilisateur), et a le texte de l'�nigme est maintenant solvable.

 - La reconnaissance a �chou� deux fois de suite, le texte n'est pas solvable.
 
Un texte d'�nigme solvable (sans point d'exclamation) ne va pas forc�ment aboutir � une r�ponse. Si la biblioth�que des symboles est incorrecte (parce que l'utilisateur a saisi des conneries), on peut tr�s bien avoir un texte d'�nigme consid�r� comme solvable, mais qui ne veut rien dire. Par exemple : "5=3=8(2".

On tente donc de r�soudre l'�nigme, cela aboutit � une r�ponse, ou pas. Si il y a une r�ponse, elle est affich�e dans la console. Sinon, le message "resolution de l'enigme : fail" est affich�.

Que l'�nigme ait abouti � une r�ponse ou pas, on passe aux �tapes suivantes. C'est un peu cr�tin, et �a contribue au bug pr�c�demment mentionn�. (Flemme de corriger, comme toujours).

Cette action est effectu�e par la classe EnigmaSolver, dans le fichier enisolvr.py.

### V�rification que le jeu est fini ou pas ###

On refait une capture d'�cran de la zone d'�nigme, si le pixel en bas � gauche n'est plus le bleu de la couleur de fond du jeu, on consid�re que le jeu est termin�, le script s'arr�te.

Cette action est effectu�e directement dans le fichier main.py. (voir la ligne d�finssant la variable `rgb_bottom_left`, et les quelques lignes suivantes)

### Attente de la prochaine �nigme ###

Le script refait p�riodiquement des captures d'�cran de la zone d'�nigme, et compare l'image obtenue avec l'image de l'�nigme pr�c�dente. (Tous les pixels ne sont pas syst�matiquement compar�, il y a un maillage). D�s qu'on trouve un pixel diff�rent, n'importe o� dans la zone d'�nigme, on consid�re qu'il y a une nouvelle �nigme. On reprend le traitement � l'�tape "Extraction des symboles bruts et de la couleur du gros op�rateur".

Cette action est effectu�e conjointement avec l'action pr�c�dente. On v�rifie que le jeu est fini ou pas, puis on v�rifie que l'�nigme a chang� ou pas, etc. jusqu'� ce que l'un des 2 �v�nements survienne.

Cette action est effectu�e par la classe SymbolExtractor (M�me si c'est pas vraiment son r�le et qu'il aurait mieux fallu cr�er une autre classe pour �a). 

### Dump des symboles nouvellement ajout�s ###

Cette action est effectu�e lorsque le script a d�tect� que le jeu �tait fini. 

On ne sauvegarde pas automatiquement ces nouveaux symboles. � la place, on les �crit sur la sortie standard. 

Chaque ligne correspond � un symbole qui a �t� ajout� dans la biblioth�que durant cette ex�cution du script, suite aux saisies utilisateurs.

Chacune de ces lignes doit �tre copi� et coll� dans le fichier symbdata.py, en tant qu'�l�ment suppl�mentaire du tuple LIST_SYMB_ALARRACHE. 

Pour les branques qui ne connaissent pas la syntaxe du python, il faut ajouter 3 double guillemets : """ au d�but de la ligne, et 3 double guillemets suivi d'une virgule : """, � la fin de la ligne, pour en faire un �l�ment de tuple valide.

Cette action est effectu�e par la classe SymbolReferences (la classe contenant la biblioth�que des symboles).


## Mots de vocabulaire utilis� pour composer les noms de variables dans le code. ##

� �tre continu�.


## Description d�taill�e de chaque classe ##

Putain, va y'en avoir encore pour une tartine de blabla. J'aime �tre verbeux, que voulez-vous.


## Am�liorations possibles ##


