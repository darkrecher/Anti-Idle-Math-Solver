# Document de conception du script Anti-Idle Math Solver #

## Trucs int�ressants de ce script, r�cup�rables pour d'autres projets ##

 - Conversion de couleurs RGB vers HSV, sans jamais utiliser de float, donc rapide. Fichier `colrtool.py`

 - Capture d'�cran avec la librairie wx. Fichier `srccapt.py`
 
 - Enregistrement de fichier image, au format png, avec wx. Fichier `srccapt.py`
 
 - Lecture de pixel dans une image ou un dc, avec wx. Fichier `gamedtc.py` et autres.
 
 - Vague id�e d'un crawler g�n�rique, parcourant une ligne ou une colonne de pixels, afin de trouver celui ou ceux r�pondant ou ne r�pondant pas � une condition donn�e. (Y'a que l'id�e, sans le code).
 
## Macro-description du script ##

TRIP: Les macros sont des poissons. Ou des gestionnaires de putes. C'est au choix.

### D�tection de la zone de jeu ###

Cette action est r�alis�e par la classe `GameRectDetector`, du fichier `gamedtc.py`

La zone de jeu peut �tre n'importe o�. Si elle est visible enti�rement sur l'�cran, le script est cens� la d�tecter.

La "zone de jeu" repr�sente le rectangle affichant Math Master. Il ne s'agit pas de la zone de tout le jeu Anti-Idle. 

Exemple de zone de jeu : 

![Intro jeu](https://raw.github.com/darkrecher/Anti-Idle-Math-Solver/master/doc_img_readme/screenshot-intro.png)

### Estimation de la zone d'�nigme brute ###

Cette action est r�alis�e par la classe `GameRectDetector`.

"Zone d'�nigme" = rectangle, � l'�cran, affichant la question math�matique pos�e au joueur. Au d�but cette zone est brute, puis elle est affin�e.

Exemple de zone brute : 

![Intro jeu](https://raw.github.com/darkrecher/Anti-Idle-Math-Solver/master/doc_img_readme/screenshot-rez.png)

Exemple de zone affin�e :

![Intro jeu](https://raw.github.com/darkrecher/Anti-Idle-Math-Solver/master/doc_img_readme/screenshot-ez.png)

La zone d'�nigme brute se d�duit de la zone de jeu, par un simple rognage de l'image, selon des proportions pr�d�finies. 

### D�tection du d�but du jeu, et estimation de la zone d'�nigme pas-brute ###

Ces actions sont r�alis�es par la classe `EnigmaZoneDetector`, du fichier `enizodtc`.

On teste p�riodiquement la couleur du pixel en bas � gauche de la zone d'�nigme brute. Si c'est le bleu du fond du jeu, on consid�re que la partie a commenc�e.

D�s que �a commenc�, on affine la zone d'�nigme, en rognant des lignes en haut et en bas. Une ligne est � rogner si elle ne contient aucun pixel "int�ressant", c'est � dire aucun pixel suffisamment jaune ou blanc (les deux couleurs utilis�es pour afficher les symboles). 

Un "symbole" = la repr�sentation graphique de l'un des caract�res du texte de l'�nigme. Par exemple, le dessin du "3", celui de la parenth�se "(", celui du point d'interrogation, ...

Les symboles ont un d�tourage noir. L'affinage de la zone d'�nigme a pour cons�quence de rogner le haut et le bas de ce d�tourage, mais �a ne d�range pas. 

La zone d'�nigme n'est rogn�e ni � gauche ni � droite, car on ne peut pas pr�sumer de la longeur d'affichage d'une �nigme.

### Extraction des symboles bruts et de la couleur du gros op�rateur ###

Ces actions sont effectu�es par la classe `SymbolExtractor`, dans le fichier `symbextr.py`.

Un "symbole brut" = comme un symbole, sauf que le rognage �ventuel de lignes de pixels en haut et en bas n'a pas encore �t� fait. Par exemple, le signe "=" a une hauteur plus petite que la zone d'�nigme (m�me apr�s affinage de cettedite zone). Lorsqu'on affinera le symbole du "=", on enl�vera des lignes en haut en en bas.

Le "gros op�rateur" = L'op�rateur que l'on voit parfois dans le texte d'une �nigme, dans un cadre color�. Dans les images ci-dessus, c'est le "+" vert.

Le jeu �crit les symboles en les espa�ant suffisamment, et on a toujours au moins une colonne de pixels pas int�ressants entre deux symboles. (Du moins avec une r�solution d'�cran pas trop d�gueux). �a arrange bien les choses.

Dans la zone d'�nigme, on consid�re donc que lorsqu'on trouve plusieurs colonnes adjacentes, comportant chacune au moins un pixel int�ressant, alors cela constitue un symbole unique.

L'extraction de symboles renvoie 3 informations :

 - la liste des symboles trouv�es avant le gros op�rateur.
 
 - la couleur d'un pixel du gros op�rateur. On n'a pas besoin de son dessin complet. On d�duira quel op�rateur c'est � partir de cette simple couleur.
 
 - la liste des symboles trouv�es apr�s le gros op�rateur. 
 
Certains textes d'�nigme ne comportent pas de gros op�rateur. Par exemple : 2?3=5. Dans ce cas, la premi�re liste contient tous les symboles de l'�nigme, la couleur du gros op�rateur est ind�finie, et la derni�re liste est vide.

### Conversion couleur -> valeur d'encre ###

Cette action est effectu�e durant l'extraction des symboles bruts (voir �tape pr�c�dente), par la fonction `SymbolExtractor._get_ink_of_pixel`, dans le fichier `symbextr.py`.

Un symbole est un dessin, et peut donc se d�finir par un tableau en 2D, contenant des couleurs rgb. Mais le script remplace ces couleurs par des valeurs d'encre. 

Une "valeur d'encre" = un nombre entre 0 et 255, repr�sentant, pour un pixel donn�, son intensit� en couleur jaune ou blanche. La valeur d'encre n'indique vraiment que l'intensit�, et pas le fait que ce soit du jaune ou du blanc, car on n'en a pas besoin.

Un pixel qui n'est ni jaune ni blanc a une valeur d'encre de 0.

Un pixel est dit "int�ressant" si il est suffisamment jaune ou blanc. Sa valeur d'encre doit �tre sup�rieure � 100. (Seuil fix� de mani�re empirico-arbitraire).

### Construction des symboles affin�s ###

Cette action est r�alis�e par la classe `Symbol`, dans le fichier `symbol.py`.

On rogne les lignes en haut et en bas du symbole, qui n'ont que des valeurs d'encre � 0.

### Reconnaissance des symboles et du gros op�rateur ###

Cette action est r�alis�e par les fichiers `symbdata.py`, `symbref.py`, et `eniocr.py`.

On tente de trouver les caract�res constituant le texte de l'�nigme. Un symbole produit toujours un et un seul caract�re. Le gros op�rateur produit �galement un et un seul caract�re.

Le script poss�de une biblioth�que de symboles connus, dans le fichier `symbdata.py`. Son chargement en m�moire a �t� effectu�e au d�but, par la classe `SymbolReferences`, du fichier `symbref.py`.

Les actions de reconnaissance des symboles et du gros op�rateur sont effectu�es par la classe `EnigmaOcr`, du fichier `eniocr.py`.

Le script tente de faire correspondre des symboles de sa biblioth�que avec les symboles de l'�nigme, via une �galit� parfaite. Les tableaux 2D des valeurs d'encres doivent �tre rigoureusement �gaux. 

Lorsqu'un symbole de l'�nigme ne peut pas �tre reconnu (il n'y a pas son �quivalent dans la biblioth�que des symboles), on consid�re que son caract�re est le point d'exclamation. Les textes d'�nigme affich�s par le jeu ne comportent jamais de point d'exclamation. Il n'y a donc pas de risque de confusion.

Une �nigme est dite "solvable" si son texte ne comporte aucun point d'exclamation.

### Demande des symboles non reconnus ###

Cette action (ainsi que les 2 suivantes) ne sont effectu�es que si l'�nigme n'est pas solvable.

Cette action est effectu�e directement dans le fichier `main.py`. (Voir la ligne contenant un appel � `raw_input`).

Le script �crit sur la console le texte actuel de l'�nigme (avec les points d'exclamation), et demande � l'utilisateur de saisir soit le texte complet, soit les caract�res correspondants aux points d'exclamations. Le script reste en attente tant que l'utilisateur n'a rien saisi. 

Si l'utilisateur saisi un nombre de caract�res diff�rents du nombre total de caract�res de l'�nigme, et diff�rent du nombre de points d'exclamation dans l'�nigme, le script ne fait rien avec cette saisie. Mais il passe quand m�me � l'�tape suivante. Ce qui est un peu cr�tin, je le reconnais.

### remplacement des points d'exclamation par la saisie de l'utilisateur, et mise � jour de la biblioth�que ###

Cette action est effectu�e par la classe `EnigmaOcr`, ainsi que par l'instance de `SymbolReferences` contenue dans `EnigmaOcr`.

On associe les symboles inconnus avec leurs caract�res correspondants de la saisie utilisateur. On compl�te la biblioth�que avec ces nouveaux symboles. 

La biblioth�que de symboles accepte plusieurs symboles diff�rents associ�s � un m�me caract�re. C'est n�cessaire, car certains caract�res ne sont pas toujours affich�s exactement de la m�me mani�re.

Si l'utilisateur saisit un caract�re diff�rent de *0123456789 / * - + = ? x ( ) ,* , on ne l'associe pas � son symbole et on ne l'ajoute pas dans la biblioth�que. Les textes d'�nigmes sont cens�s �tre constitu�s uniquement de ces caract�res.
 
### Seconde tentative de reconnaissance des symboles ###

Cette action consiste � r�p�ter l'�tape "Reconnaissance des symboles et du gros op�rateur".

Elle est effectu�e, m�me si la saisie utilisateur a �t� identifi�e comme invalide. (cr�tin bis).

Si tout s'est bien pass�, et que la biblioth�que des symboles a �t� correctement mise � jour lors de l'�tape pr�c�dente, alors cette seconde tentative doit aboutir � un texte d'�nigme solvable. 

Si ce nouveau texte d'�nigme n'est pas solvable, on reste bloqu� dessus (cr�tin ter).

Les cr�tineries de cette �tape sont � l'origine du bug "blocage sur la question en cours suite � un �chec", d�crit dans le fichier readme.md. J'ai la flemme de le corriger.

### R�solution de l'�nigme ###

� partir de cette �tape, on n'a plus besoin des symboles. Le texte de l'�nigme suffit.

Cette action est effectu�e par la classe `EnigmaSolver`, dans le fichier `enisolvr.py`.

Elle est effectu�e quel que soit ce qu'il s'est pass� avant :

 - La reconnaissance des symboles a march� du premier coup et a imm�diatement donn� un texte d'�nigme solvable.
 
 - La reconnaissance a march� au deuxi�me coup, et le texte de l'�nigme est maintenant solvable.

 - La reconnaissance a �chou� deux fois de suite, et le texte n'est pas solvable.
 
Un texte d'�nigme solvable ne va pas forc�ment aboutir � une r�ponse. Si la biblioth�que des symboles est incorrecte (parce que l'utilisateur a saisi des conneries), on peut tr�s bien avoir un texte sans points d'exclamation, mais qui ne veut rien dire. Par exemple : "5=3=8(2".

Si la r�solution de l'�nigme aboutit � une r�ponse, elle est affich�e dans la console. Sinon, le message *resolution de l'enigme : fail* est affich�.

Que l'�nigme ait abouti � une r�ponse ou pas, on passe aux �tapes suivantes. C'est re-re-re-cr�tin, et �a contribue au bug pr�c�demment mentionn�. (Flemme de corriger, comme toujours).

### V�rification que le jeu est fini ou pas ###

Cette action est effectu�e directement dans `main.py`. (voir la ligne d�finssant la variable `rgb_bottom_left`, et les quelques lignes suivantes)

On refait une capture d'�cran de la zone d'�nigme affin�e. Si le pixel en bas � gauche n'est plus le bleu de fond du jeu, on consid�re que c'est termin�, le script s'arr�te.

### Attente de la prochaine �nigme ###

Cette action est effectu�e par la classe `SymbolExtractor` (M�me si c'est pas vraiment son r�le et qu'il aurait mieux valu cr�er une autre classe pour �a). 

Le script refait p�riodiquement des captures d'�cran de la zone d'�nigme, et compare l'image obtenue avec celle de l'�nigme pr�c�dente. (Tous les pixels ne sont pas syst�matiquement compar�, il y a un maillage). D�s qu'on trouve un pixel diff�rent, n'importe o�, on consid�re qu'il y a une nouvelle �nigme. On reprend le traitement � l'�tape "Extraction des symboles bruts et de la couleur du gros op�rateur".

Cette action est effectu�e conjointement avec l'action pr�c�dente. On fait une capture d'�cran, on v�rifie que le jeu est fini ou pas, on v�rifie que l'�nigme a chang� ou pas, et on recommence, jusqu'� ce qu'il se passe quelque chose.

### Dump des symboles nouvellement ajout�s ###

Cette action est effectu�e par la classe `SymbolReferences`, lorsque le script a d�tect� la fin du jeu. 

Le script ne sauvegarde rien (flemme), � la place, il �crit les nouveaux symboles sur la sortie standard. 

Chaque ligne correspond � un symbole. Le script n'�crit que les symboles ajout�s dans la biblioth�que suite aux saisies utilisateurs. Il ne r��crit pas les symboles d�j� connus par `symbdata.py`.

Chacune de ces lignes doit donc �tre manuellement recopi�es dans `symbdata.py`, en tant qu'�l�ment suppl�mentaire du tuple `LIST_SYMB_ALARRACHE`. 

Pour les branques qui ne connaissent pas la syntaxe du python : il faut ajouter 3 double guillemets `"""` au d�but de chaque ligne, et 3 double guillemets suivi d'une virgule `""",` � la fin de chaque ligne.

## Mots de vocabulaire utilis�s pour composer les noms de variables dans le code. ##

`x_ y_ _size_ _top _bottom _left _right line column` : les trucs habituels : coordonn�es, taille, c�t�s de rectangle, ...

`_scr_` : une coordonn�e d�finie par rapport � l'�cran, et non pas par rapport � un dc quelconque.

`rez`, `raw_enigma_zone` : rectangle repr�sentant la zone d'�nigme brute

`ez`, `enigma_zone` :rRectangle repr�sentant la zone d'�nigme affin�e.

`dc_` : dc (drawing context), de la librairie wx.

`dtc` : non ce n'est pas "dans ton cul". C'est "detector". Un detector est une classe analysant un dc provenant d'une capture d'�cran, pour y trouver des trucs.

`_raw_` : brut. (zone d'�nigme, symbole, etc)

`_proc_` : processed. Affin�. le contraire de brut. Je ne mets pas syst�matiquement ce mot dans les noms de variables. Uniquement dans les situations o� on veut montrer qu'on passe du brut � l'affin�. Quand y'a ni "raw", ni "proc", c'est que c'est affin�.

`screen` : le dc correspondant � l'�cran du n'ordinateur.

`list_` : un tuple ou une liste, on fait pas la diff�rence. (duck typing, tout �a).

`_big_op` : le gros op�rateur, qui est parfois pr�sent dans les zones d'�nigme.

`ocr` : truc qui veut dire reconnaissance d'�criture. Je sais pas d'o� �a sort ce nom, et mon script ne fait absolument pas d'OCR, mais c'est pas grave.

`ocr_ify` : action d'ocrifier (appliquer de l'ocr). Oui c'est moche et c'est n'importe quoi.

`rgb_` : trouple (tuple de 3 entiers). Composantes Red-Green-Blue d'une couleur.

`hsv_` : trouple d'entiers. Composantes Hue-Saturation-Value d'une couleur.

`red grn blu hue sat val` : les composantes sp�cifiques des trouples rgb et hsv.

`comp` : composante. Nom g�n�rique pour d�signer une composante (n'importe laquelle) d'une couleur rgb ou hsv.

`col` : couleur. Terme g�n�rique pour dire que �a peut �tre du hsv ou du rgb.

`_EXACT_` : couleur de r�f�rence d'un "truc" sp�cifique . (Par exemple, la couleur de fond de la zone d'�nigme, la couleur verte du gros op�rateur '+', ...). Cette couleur de r�f�rence est compar�e avec la couleur d'un pixel de l'�cran. Pour que le "truc" en question soit rep�r�, les couleurs doivent �tre rigoureusement �gales.

`_APPROX_` : couleur de r�f�rence d'un "truc" sp�cifique. (Par exemple, la couleur marron-bois-moche d�limitant l'ext�rieur de la zone de jeu). Pour que le "truc" en question soit rep�r�, la couleur de r�f�rence et la couleur d'un pixel de l'�cran doivent �tre � peu pr�s �gales. On autorise un certain �cart (pr�d�fini). 

`enigma_text` : le texte de l'�nigme

`enigma_text_help` : le texte saisi par l'utilisateur, qui doit permettre de compl�ter les caract�res inconnus du texte de l'�nigme. (un caract�re inconnu = un point d'exclamation).

`enigma_text_complete` : texte complet de l'�nigme, sans caract�re inconnus.

`answer` : string. La r�ponse de l'�nigme, que le script doit trouver et afficher.

`msg` : envoi de message sur la sortie standard, dont l'utilisateur a vraiment besoin.

`log` : envoi de message verbose. l'utilisateur n'en a pas vraiment besoin, mais le d�veloppeur en a eu besoin � un moment donn� de sa vie. TRIP: sa vie qui est super (ou pas).

`_game_`, `_square_` : rectangle de la zone du jeu Math Master. C'est tr�s vilain d'avoir pris deux nommages diff�rets, d'autant plus qu'un rectangle, c'est pas vraiment un square. Il faudra changer �a.

`border` : les pixels ext�rieurs � la zone de jeu (haut bas gauche droite), qui ont une couleur marron-bois-moche.

`lit_pixel` : la ou les colonnes de pixels gris clair, qui se trouvent entre le c�t� droit de la zone de jeu, et les pixels ext�rieurs.

`_depl_` : valeur de d�placement � appliquer � une coordonn�e x ou y, pour la faire bouger de ici vers autre part. (�a c'est de l'explication !)

`step` : valeur de d�placement � appliquer � une coordonn�e, quand on veut la faire bouger plusieurs fois, dans une boucle. 

`pattern` : ligne ou colonne de pixel, correspondant � un motif pr�cis. Par exemple : "un ou plusieurs pixels rouge, puis 10 pixels verts, puis �ventuellement un pixel violet".

`cursor` : une coordonn�e x ou y, qu'on fait avancer, pour v�rifier o� chercher des trucs dans des pixels.

`cur` : valeur courante. Une valeur qu'on fait avancer dans une boucle.

`crop` : rognage. Action de supprimer une ligne ou une colonne situ�e au bord d'une image, parce que y'a rien dedans de ce qu'on veut garder.

`ink` ou `inks` : une valeur d'encre d'un pixel, ou les valeurs d'encres d'un tableau de pixel.

`array_inks` : tableau 2D des encres d'un symbole, rang�es comme il faut. C'est une liste. Chaque �l�ment est une sous-liste. Chaque sous-liste repr�sente une ligne de valeur d'encre.

`raw_symbol` : tableau 2D des encres d'un symbole. Il peut y avoir, dans une ou plusieurs lignes du d�but, et dans une ou plusieurs lignes de la fin, des valeurs d'encres toutes � z�ro.

`columord_symb`: "column-ordered symbol". tableau 2D des encres d'un symbole, rang�s par colonne. (c'est comme �a qu'on r�cup�re les symboles au d�part, car on analyse la zone d'�nigme colonne par colonne). C'est une liste. Chaque �l�ment est une sous-liste. Chaque sous-liste repr�sente une **colonne** de valeur d'encre. Un tableau columord_symb est "raw", et non pas "affin�". C'est � dire que des lignes du haut et du bas peuvent avoir des valeurs d'encres toutes � z�ro. Mais c'est difficilement d�tectable en l'�tat, puisque c'est rang� par colonne.

`flat_list_ink` : grande liste 1D des valeurs d'encres d'un symbole. Correspond � array_inks, sauf que toutes les valeurs sont mises bout � bout. Une variable flat_list_ink ne permet pas de conna�tre les dimensions (largeur, hauteur) d'un symbole. Il faut avoir stock� ces infos autre part.

`sig`, `signifiance` : string de un seul caract�re, repr�sentant ce que signifie un symbole. C'est ce qui permet de passer d'une liste de symbole au texte d'une �nigme.

`saved_data` : grande string, contenant les informations permettant de sauvegarder un symbole. Chaque �l�ment de LIST_SYMB_ALARRACHE est une saved_data. Une saved_data contient plusieurs sous-�l�ment (le s�parateur est le caract�re espace). On y trouve, dans cet ordre : 
 - la signifiance (un caract�re)
 - la largeur et la hauteur du symbole. (deux valeurs num�riques, converties en string).
 - la flat_list_ink du symbole. (plusieurs valeurs num�riques, converties en string).
 
`comes_from_raw_symbol` : bool�en permettant de savoir d'o� vient un symbole. 
 - True : le symbole a �t� d�fini par un `raw_symbol`. C'�tait un symbole inconnu au d�part, on l'a trouv� dans une �nigme pos�e par le jeu, et l'utilisateur a saisi sa signifiance.
 - False : le symbole �tait connu au d�part. ses dimensions, ses valeurs d'encre et sa signifiance se trouvaient tous dans une saved_data.
 
`ref`, `reference` : symbole de r�f�rence, dont la signifiance est connue. On essaie de faire correspondre chaque symbole d'une �nigme � un symbole de r�f�rence, pour d�terminer le texte de l'�nigme.

`calculation` : type d'�nigme, pour laquelle il faut calculer une valeur num�rique. Exemple : *2 + 2 = ?*

`comparrison` : type d'�nigme, pour laquelle il faut comparer deux valeurs num�riques (en faisant plus ou moins de calcul interm�diaire). Par exemple : *12+3 ? 28/2*. Il faut trouver si 12+3 est plus grand, �gal ou plus petit que 28/2.

`find_operator` : type d'�nigme, pour laquelle il faut trouver l'op�rateur manquant, afin de v�rifier l'�galit� mentionn�e. Par exemple : *3 ? 2 = 6*. Il faut trouver quelle �galit� est vraie, parmi les 4 possibilit�s : *3 + 2 = 6* ; *3 - 2 = 6* ; *3 * 2 = 6* ; *3 / 2 = 6*.

`_enigma_part` : string. morceau de texte d'�nigme, contenant une op�ration math�matique que l'on peut calculer imm�diatement. Une _enigma_part ne doit contenir que des chiffres, des parenth�ses et les 4�op�rations. Elle ne doit pas contenir de signe �gal ou de point d'interrogation.

`_val` : valeur num�rique. R�sultat du calcul d'une `_enigma_part`.
 
## Description d�taill�e de chaque module ##

Voir les docstrings.

## Am�liorations possibles ##

 - Essayer d'�tre un peu plus homog�ne dans les noms parce que c'est parfois le bordel.

 - Utiliser la librairie logging pour faire du log digne de ce nom, avec diff�rents niveaux. (verbose, log, error, ...).
 
 - Arr�ter de passer les dimensions d'un DC en m�me temps que le DC.
 
 - Reconnaissance de symbole un peu mieux foutue. Calculer les diff�rences d'encre entre le symbole en cours d'analyse, et les symboles de la biblioth�que. Si on en trouve un qui n'a pas beaucoup de diff�rence (seuil � d�terminer), on consid�re que c'est le m�me symbole.
 
 - Essayer de s'affranchir compl�tement de la r�solution de l'�cran. Mettre � l'�chelle les symboles de la biblioth�que pour que la taille corresponde au symbole en cours d'analyse (avec une esp�ce d'extrapolation 2D du tableau des valeurs d'encre). Tout en memoizant le truc, comme �a si exactement le m�me symbole revient, on le retrouve tout de suite.
 
 - Sauvegarder automatiquement dans un fichier les nouveaux symboles saisis par l'utilisateur.
 
 - Tous les TODO indiqu�s dans le code. 

 - Trouver une solution pour les bugs connus.