# Document de conception du script Anti-Idle Math Solver #

## Trucs intéressants de ce script, récupérables pour d'autres projets ##

 - Conversion de couleurs RGB vers HSV, sans jamais utiliser de float, donc rapide. Fichier `colrtool.py`

 - Capture d'écran avec la librairie wx. Fichier `srccapt.py`
 
 - Enregistrement de fichier image, au format png, avec wx. Fichier `srccapt.py`
 
 - Lecture de pixel dans une image ou un dc, avec wx. Fichier `gamedtc.py` et autres.
 
 - Vague idée d'un crawler générique, parcourant une ligne ou une colonne de pixels, afin de trouver celui ou ceux répondant ou ne répondant pas à une condition donnée. (Y'a que l'idée, sans le code).
 
## Macro-description du script ##

TRIP: Les macros sont des poissons. Ou des gestionnaires de putes. C'est au choix.

### Détection de la zone de jeu ###

Cette action est réalisée par la classe `GameRectDetector`, du fichier `gamedtc.py`

La zone de jeu peut être n'importe où. Si elle est visible entièrement sur l'écran, le script est censé la détecter.

La "zone de jeu" représente le rectangle affichant Math Master. Il ne s'agit pas de la zone de tout le jeu Anti-Idle. 

Exemple de zone de jeu : 

![Intro jeu](https://raw.github.com/darkrecher/Anti-Idle-Math-Solver/master/doc_img_readme/screenshot-intro.png)

### Estimation de la zone d'énigme brute ###

Cette action est réalisée par la classe `GameRectDetector`.

"Zone d'énigme" = rectangle, à l'écran, affichant la question mathématique posée au joueur. Au début cette zone est brute, puis elle est affinée.

Exemple de zone brute : 

![Intro jeu](https://raw.github.com/darkrecher/Anti-Idle-Math-Solver/master/doc_img_readme/screenshot-rez.png)

Exemple de zone affinée :

![Intro jeu](https://raw.github.com/darkrecher/Anti-Idle-Math-Solver/master/doc_img_readme/screenshot-ez.png)

La zone d'énigme brute se déduit de la zone de jeu, par un simple rognage de l'image, selon des proportions prédéfinies. 

### Détection du début du jeu, et estimation de la zone d'énigme pas-brute ###

Ces actions sont réalisées par la classe `EnigmaZoneDetector`, du fichier `enizodtc`.

On teste périodiquement la couleur du pixel en bas à gauche de la zone d'énigme brute. Si c'est le bleu du fond du jeu, on considère que la partie a commencée.

Dès que ça commencé, on affine la zone d'énigme, en rognant des lignes en haut et en bas. Une ligne est à rogner si elle ne contient aucun pixel "intéressant", c'est à dire aucun pixel suffisamment jaune ou blanc (les deux couleurs utilisées pour afficher les symboles). 

Un "symbole" = la représentation graphique de l'un des caractères du texte de l'énigme. Par exemple, le dessin du "3", celui de la parenthèse "(", celui du point d'interrogation, ...

Les symboles ont un détourage noir. L'affinage de la zone d'énigme a pour conséquence de rogner le haut et le bas de ce détourage, mais ça ne dérange pas. 

La zone d'énigme n'est rognée ni à gauche ni à droite, car on ne peut pas présumer de la longeur d'affichage d'une énigme.

### Extraction des symboles bruts et de la couleur du gros opérateur ###

Ces actions sont effectuées par la classe `SymbolExtractor`, dans le fichier `symbextr.py`.

Un "symbole brut" = comme un symbole, sauf que le rognage éventuel de lignes de pixels en haut et en bas n'a pas encore été fait. Par exemple, le signe "=" a une hauteur plus petite que la zone d'énigme (même après affinage de cettedite zone). Lorsqu'on affinera le symbole du "=", on enlèvera des lignes en haut en en bas.

Le "gros opérateur" = L'opérateur que l'on voit parfois dans le texte d'une énigme, dans un cadre coloré. Dans les images ci-dessus, c'est le "+" vert.

Le jeu écrit les symboles en les espaçant suffisamment, et on a toujours au moins une colonne de pixels pas intéressants entre deux symboles. (Du moins avec une résolution d'écran pas trop dégueux). Ça arrange bien les choses.

Dans la zone d'énigme, on considère donc que lorsqu'on trouve plusieurs colonnes adjacentes, comportant chacune au moins un pixel intéressant, alors cela constitue un symbole unique.

L'extraction de symboles renvoie 3 informations :

 - la liste des symboles trouvées avant le gros opérateur.
 
 - la couleur d'un pixel du gros opérateur. On n'a pas besoin de son dessin complet. On déduira quel opérateur c'est à partir de cette simple couleur.
 
 - la liste des symboles trouvées après le gros opérateur. 
 
Certains textes d'énigme ne comportent pas de gros opérateur. Par exemple : 2?3=5. Dans ce cas, la première liste contient tous les symboles de l'énigme, la couleur du gros opérateur est indéfinie, et la dernière liste est vide.

### Conversion couleur -> valeur d'encre ###

Cette action est effectuée durant l'extraction des symboles bruts (voir étape précédente), par la fonction `SymbolExtractor._get_ink_of_pixel`, dans le fichier `symbextr.py`.

Un symbole est un dessin, et peut donc se définir par un tableau en 2D, contenant des couleurs rgb. Mais le script remplace ces couleurs par des valeurs d'encre. 

Une "valeur d'encre" = un nombre entre 0 et 255, représentant, pour un pixel donné, son intensité en couleur jaune ou blanche. La valeur d'encre n'indique vraiment que l'intensité, et pas le fait que ce soit du jaune ou du blanc, car on n'en a pas besoin.

Un pixel qui n'est ni jaune ni blanc a une valeur d'encre de 0.

Un pixel est dit "intéressant" si il est suffisamment jaune ou blanc. Sa valeur d'encre doit être supérieure à 100. (Seuil fixé de manière empirico-arbitraire).

### Construction des symboles affinés ###

Cette action est réalisée par la classe `Symbol`, dans le fichier `symbol.py`.

On rogne les lignes en haut et en bas du symbole, qui n'ont que des valeurs d'encre à 0.

### Reconnaissance des symboles et du gros opérateur ###

Cette action est réalisée par les fichiers `symbdata.py`, `symbref.py`, et `eniocr.py`.

On tente de trouver les caractères constituant le texte de l'énigme. Un symbole produit toujours un et un seul caractère. Le gros opérateur produit également un et un seul caractère.

Le script possède une bibliothèque de symboles connus, dans le fichier `symbdata.py`. Son chargement en mémoire a été effectuée au début, par la classe `SymbolReferences`, du fichier `symbref.py`.

Les actions de reconnaissance des symboles et du gros opérateur sont effectuées par la classe `EnigmaOcr`, du fichier `eniocr.py`.

Le script tente de faire correspondre des symboles de sa bibliothèque avec les symboles de l'énigme, via une égalité parfaite. Les tableaux 2D des valeurs d'encres doivent être rigoureusement égaux. 

Lorsqu'un symbole de l'énigme ne peut pas être reconnu (il n'y a pas son équivalent dans la bibliothèque des symboles), on considère que son caractère est le point d'exclamation. Les textes d'énigme affichés par le jeu ne comportent jamais de point d'exclamation. Il n'y a donc pas de risque de confusion.

Une énigme est dite "solvable" si son texte ne comporte aucun point d'exclamation.

### Demande des symboles non reconnus ###

Cette action (ainsi que les 2 suivantes) ne sont effectuées que si l'énigme n'est pas solvable.

Cette action est effectuée directement dans le fichier `main.py`. (Voir la ligne contenant un appel à `raw_input`).

Le script écrit sur la console le texte actuel de l'énigme (avec les points d'exclamation), et demande à l'utilisateur de saisir soit le texte complet, soit les caractères correspondants aux points d'exclamations. Le script reste en attente tant que l'utilisateur n'a rien saisi. 

Si l'utilisateur saisi un nombre de caractères différents du nombre total de caractères de l'énigme, et différent du nombre de points d'exclamation dans l'énigme, le script ne fait rien avec cette saisie. Mais il passe quand même à l'étape suivante. Ce qui est un peu crétin, je le reconnais.

### remplacement des points d'exclamation par la saisie de l'utilisateur, et mise à jour de la bibliothèque ###

Cette action est effectuée par la classe `EnigmaOcr`, ainsi que par l'instance de `SymbolReferences` contenue dans `EnigmaOcr`.

On associe les symboles inconnus avec leurs caractères correspondants de la saisie utilisateur. On complète la bibliothèque avec ces nouveaux symboles. 

La bibliothèque de symboles accepte plusieurs symboles différents associés à un même caractère. C'est nécessaire, car certains caractères ne sont pas toujours affichés exactement de la même manière.

Si l'utilisateur saisit un caractère différent de *0123456789 / * - + = ? x ( ) ,* , on ne l'associe pas à son symbole et on ne l'ajoute pas dans la bibliothèque. Les textes d'énigmes sont censés être constitués uniquement de ces caractères.
 
### Seconde tentative de reconnaissance des symboles ###

Cette action consiste à répéter l'étape "Reconnaissance des symboles et du gros opérateur".

Elle est effectuée, même si la saisie utilisateur a été identifiée comme invalide. (crétin bis).

Si tout s'est bien passé, et que la bibliothèque des symboles a été correctement mise à jour lors de l'étape précédente, alors cette seconde tentative doit aboutir à un texte d'énigme solvable. 

Si ce nouveau texte d'énigme n'est pas solvable, on reste bloqué dessus (crétin ter).

Les crétineries de cette étape sont à l'origine du bug "blocage sur la question en cours suite à un échec", décrit dans le fichier readme.md. J'ai la flemme de le corriger.

### Résolution de l'énigme ###

À partir de cette étape, on n'a plus besoin des symboles. Le texte de l'énigme suffit.

Cette action est effectuée par la classe `EnigmaSolver`, dans le fichier `enisolvr.py`.

Elle est effectuée quel que soit ce qu'il s'est passé avant :

 - La reconnaissance des symboles a marché du premier coup et a immédiatement donné un texte d'énigme solvable.
 
 - La reconnaissance a marché au deuxième coup, et le texte de l'énigme est maintenant solvable.

 - La reconnaissance a échoué deux fois de suite, et le texte n'est pas solvable.
 
Un texte d'énigme solvable ne va pas forcément aboutir à une réponse. Si la bibliothèque des symboles est incorrecte (parce que l'utilisateur a saisi des conneries), on peut très bien avoir un texte sans points d'exclamation, mais qui ne veut rien dire. Par exemple : "5=3=8(2".

Si la résolution de l'énigme aboutit à une réponse, elle est affichée dans la console. Sinon, le message *resolution de l'enigme : fail* est affiché.

Que l'énigme ait abouti à une réponse ou pas, on passe aux étapes suivantes. C'est re-re-re-crétin, et ça contribue au bug précédemment mentionné. (Flemme de corriger, comme toujours).

### Vérification que le jeu est fini ou pas ###

Cette action est effectuée directement dans `main.py`. (voir la ligne définssant la variable `rgb_bottom_left`, et les quelques lignes suivantes)

On refait une capture d'écran de la zone d'énigme affinée. Si le pixel en bas à gauche n'est plus le bleu de fond du jeu, on considère que c'est terminé, le script s'arrête.

### Attente de la prochaine énigme ###

Cette action est effectuée par la classe `SymbolExtractor` (Même si c'est pas vraiment son rôle et qu'il aurait mieux valu créer une autre classe pour ça). 

Le script refait périodiquement des captures d'écran de la zone d'énigme, et compare l'image obtenue avec celle de l'énigme précédente. (Tous les pixels ne sont pas systématiquement comparé, il y a un maillage). Dès qu'on trouve un pixel différent, n'importe où, on considère qu'il y a une nouvelle énigme. On reprend le traitement à l'étape "Extraction des symboles bruts et de la couleur du gros opérateur".

Cette action est effectuée conjointement avec l'action précédente. On fait une capture d'écran, on vérifie que le jeu est fini ou pas, on vérifie que l'énigme a changé ou pas, et on recommence, jusqu'à ce qu'il se passe quelque chose.

### Dump des symboles nouvellement ajoutés ###

Cette action est effectuée par la classe `SymbolReferences`, lorsque le script a détecté la fin du jeu. 

Le script ne sauvegarde rien (flemme), à la place, il écrit les nouveaux symboles sur la sortie standard. 

Chaque ligne correspond à un symbole. Le script n'écrit que les symboles ajoutés dans la bibliothèque suite aux saisies utilisateurs. Il ne réécrit pas les symboles déjà connus par `symbdata.py`.

Chacune de ces lignes doit donc être manuellement recopiées dans `symbdata.py`, en tant qu'élément supplémentaire du tuple `LIST_SYMB_ALARRACHE`. 

Pour les branques qui ne connaissent pas la syntaxe du python : il faut ajouter 3 double guillemets `"""` au début de chaque ligne, et 3 double guillemets suivi d'une virgule `""",` à la fin de chaque ligne.

## Mots de vocabulaire utilisés pour composer les noms de variables dans le code. ##

`x_ y_ _size_ _top _bottom _left _right line column` : les trucs habituels : coordonnées, taille, côtés de rectangle, ...

`_scr_` : une coordonnée définie par rapport à l'écran, et non pas par rapport à un dc quelconque.

`rez`, `raw_enigma_zone` : rectangle représentant la zone d'énigme brute

`ez`, `enigma_zone` :rRectangle représentant la zone d'énigme affinée.

`dc_` : dc (drawing context), de la librairie wx.

`dtc` : non ce n'est pas "dans ton cul". C'est "detector". Un detector est une classe analysant un dc provenant d'une capture d'écran, pour y trouver des trucs.

`_raw_` : brut. (zone d'énigme, symbole, etc)

`_proc_` : processed. Affiné. le contraire de brut. Je ne mets pas systématiquement ce mot dans les noms de variables. Uniquement dans les situations où on veut montrer qu'on passe du brut à l'affiné. Quand y'a ni "raw", ni "proc", c'est que c'est affiné.

`screen` : le dc correspondant à l'écran du n'ordinateur.

`list_` : un tuple ou une liste, on fait pas la différence. (duck typing, tout ça).

`_big_op` : le gros opérateur, qui est parfois présent dans les zones d'énigme.

`ocr` : truc qui veut dire reconnaissance d'écriture. Je sais pas d'où ça sort ce nom, et mon script ne fait absolument pas d'OCR, mais c'est pas grave.

`ocr_ify` : action d'ocrifier (appliquer de l'ocr). Oui c'est moche et c'est n'importe quoi.

`rgb_` : trouple (tuple de 3 entiers). Composantes Red-Green-Blue d'une couleur.

`hsv_` : trouple d'entiers. Composantes Hue-Saturation-Value d'une couleur.

`red grn blu hue sat val` : les composantes spécifiques des trouples rgb et hsv.

`comp` : composante. Nom générique pour désigner une composante (n'importe laquelle) d'une couleur rgb ou hsv.

`col` : couleur. Terme générique pour dire que ça peut être du hsv ou du rgb.

`_EXACT_` : couleur de référence d'un "truc" spécifique . (Par exemple, la couleur de fond de la zone d'énigme, la couleur verte du gros opérateur '+', ...). Cette couleur de référence est comparée avec la couleur d'un pixel de l'écran. Pour que le "truc" en question soit repéré, les couleurs doivent être rigoureusement égales.

`_APPROX_` : couleur de référence d'un "truc" spécifique. (Par exemple, la couleur marron-bois-moche délimitant l'extérieur de la zone de jeu). Pour que le "truc" en question soit repéré, la couleur de référence et la couleur d'un pixel de l'écran doivent être à peu près égales. On autorise un certain écart (prédéfini). 

`enigma_text` : le texte de l'énigme

`enigma_text_help` : le texte saisi par l'utilisateur, qui doit permettre de compléter les caractères inconnus du texte de l'énigme. (un caractère inconnu = un point d'exclamation).

`enigma_text_complete` : texte complet de l'énigme, sans caractère inconnus.

`answer` : string. La réponse de l'énigme, que le script doit trouver et afficher.

`msg` : envoi de message sur la sortie standard, dont l'utilisateur a vraiment besoin.

`log` : envoi de message verbose. l'utilisateur n'en a pas vraiment besoin, mais le développeur en a eu besoin à un moment donné de sa vie. TRIP: sa vie qui est super (ou pas).

`_game_`, `_square_` : rectangle de la zone du jeu Math Master. C'est très vilain d'avoir pris deux nommages différets, d'autant plus qu'un rectangle, c'est pas vraiment un square. Il faudra changer ça.

`border` : les pixels extérieurs à la zone de jeu (haut bas gauche droite), qui ont une couleur marron-bois-moche.

`lit_pixel` : la ou les colonnes de pixels gris clair, qui se trouvent entre le côté droit de la zone de jeu, et les pixels extérieurs.

`_depl_` : valeur de déplacement à appliquer à une coordonnée x ou y, pour la faire bouger de ici vers autre part. (Ça c'est de l'explication !)

`step` : valeur de déplacement à appliquer à une coordonnée, quand on veut la faire bouger plusieurs fois, dans une boucle. 

`pattern` : ligne ou colonne de pixel, correspondant à un motif précis. Par exemple : "un ou plusieurs pixels rouge, puis 10 pixels verts, puis éventuellement un pixel violet".

`cursor` : une coordonnée x ou y, qu'on fait avancer, pour vérifier où chercher des trucs dans des pixels.

`cur` : valeur courante. Une valeur qu'on fait avancer dans une boucle.

`crop` : rognage. Action de supprimer une ligne ou une colonne située au bord d'une image, parce que y'a rien dedans de ce qu'on veut garder.

`ink` ou `inks` : une valeur d'encre d'un pixel, ou les valeurs d'encres d'un tableau de pixel.

`array_inks` : tableau 2D des encres d'un symbole, rangées comme il faut. C'est une liste. Chaque élément est une sous-liste. Chaque sous-liste représente une ligne de valeur d'encre.

`raw_symbol` : tableau 2D des encres d'un symbole. Il peut y avoir, dans une ou plusieurs lignes du début, et dans une ou plusieurs lignes de la fin, des valeurs d'encres toutes à zéro.

`columord_symb`: "column-ordered symbol". tableau 2D des encres d'un symbole, rangés par colonne. (c'est comme ça qu'on récupère les symboles au départ, car on analyse la zone d'énigme colonne par colonne). C'est une liste. Chaque élément est une sous-liste. Chaque sous-liste représente une **colonne** de valeur d'encre. Un tableau columord_symb est "raw", et non pas "affiné". C'est à dire que des lignes du haut et du bas peuvent avoir des valeurs d'encres toutes à zéro. Mais c'est difficilement détectable en l'état, puisque c'est rangé par colonne.

`flat_list_ink` : grande liste 1D des valeurs d'encres d'un symbole. Correspond à array_inks, sauf que toutes les valeurs sont mises bout à bout. Une variable flat_list_ink ne permet pas de connaître les dimensions (largeur, hauteur) d'un symbole. Il faut avoir stocké ces infos autre part.

`sig`, `signifiance` : string de un seul caractère, représentant ce que signifie un symbole. C'est ce qui permet de passer d'une liste de symbole au texte d'une énigme.

`saved_data` : grande string, contenant les informations permettant de sauvegarder un symbole. Chaque élément de LIST_SYMB_ALARRACHE est une saved_data. Une saved_data contient plusieurs sous-élément (le séparateur est le caractère espace). On y trouve, dans cet ordre : 
 - la signifiance (un caractère)
 - la largeur et la hauteur du symbole. (deux valeurs numériques, converties en string).
 - la flat_list_ink du symbole. (plusieurs valeurs numériques, converties en string).
 
`comes_from_raw_symbol` : booléen permettant de savoir d'où vient un symbole. 
 - True : le symbole a été défini par un `raw_symbol`. C'était un symbole inconnu au départ, on l'a trouvé dans une énigme posée par le jeu, et l'utilisateur a saisi sa signifiance.
 - False : le symbole était connu au départ. ses dimensions, ses valeurs d'encre et sa signifiance se trouvaient tous dans une saved_data.
 
`ref`, `reference` : symbole de référence, dont la signifiance est connue. On essaie de faire correspondre chaque symbole d'une énigme à un symbole de référence, pour déterminer le texte de l'énigme.

`calculation` : type d'énigme, pour laquelle il faut calculer une valeur numérique. Exemple : *2 + 2 = ?*

`comparrison` : type d'énigme, pour laquelle il faut comparer deux valeurs numériques (en faisant plus ou moins de calcul intermédiaire). Par exemple : *12+3 ? 28/2*. Il faut trouver si 12+3 est plus grand, égal ou plus petit que 28/2.

`find_operator` : type d'énigme, pour laquelle il faut trouver l'opérateur manquant, afin de vérifier l'égalité mentionnée. Par exemple : *3 ? 2 = 6*. Il faut trouver quelle égalité est vraie, parmi les 4 possibilités : *3 + 2 = 6* ; *3 - 2 = 6* ; *3 * 2 = 6* ; *3 / 2 = 6*.

`_enigma_part` : string. morceau de texte d'énigme, contenant une opération mathématique que l'on peut calculer immédiatement. Une _enigma_part ne doit contenir que des chiffres, des parenthèses et les 4 opérations. Elle ne doit pas contenir de signe égal ou de point d'interrogation.

`_val` : valeur numérique. Résultat du calcul d'une `_enigma_part`.
 
## Description détaillée de chaque module ##

Voir les docstrings.

## Améliorations possibles ##

 - Essayer d'être un peu plus homogène dans les noms parce que c'est parfois le bordel.

 - Utiliser la librairie logging pour faire du log digne de ce nom, avec différents niveaux. (verbose, log, error, ...).
 
 - Arrêter de passer les dimensions d'un DC en même temps que le DC.
 
 - Reconnaissance de symbole un peu mieux foutue. Calculer les différences d'encre entre le symbole en cours d'analyse, et les symboles de la bibliothèque. Si on en trouve un qui n'a pas beaucoup de différence (seuil à déterminer), on considère que c'est le même symbole.
 
 - Essayer de s'affranchir complètement de la résolution de l'écran. Mettre à l'échelle les symboles de la bibliothèque pour que la taille corresponde au symbole en cours d'analyse (avec une espèce d'extrapolation 2D du tableau des valeurs d'encre). Tout en memoizant le truc, comme ça si exactement le même symbole revient, on le retrouve tout de suite.
 
 - Sauvegarder automatiquement dans un fichier les nouveaux symboles saisis par l'utilisateur.
 
 - Tous les TODO indiqués dans le code. 

 - Trouver une solution pour les bugs connus.