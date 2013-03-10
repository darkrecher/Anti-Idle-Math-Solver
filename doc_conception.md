# Document de conception du script Anti-Idle Math Solver #

## Trucs intéressants de ce script, récupérables pour d'autres projets ##

 - Conversion de couleurs RGB vers HSV, sans jamais utiliser de float, donc rapide. Fichier colrtool.py

 - Capture d'écran avec la librairie wx. Fichier srccapt.py
 
 - Enregistrement de fichier image, au format png, avec wx. Fichier srccapt.py
 
 - Lecture de pixel dans une image ou un dc, avec wx. Fichier gamedtc.py et autres.
 
 - Vague idée d'un crawler, parcourant une ligne ou une colonne de pixels, afin de trouver celui ou ceux répondant ou ne répondant pas à une condition donnée. (Y'a que l'idée, sans le code).
 
## Macro-description du script ##

TRIP: Les macros sont des poissons. Ou des gestionnaires de putes. C'est au choix.

### Détection de la zone de jeu ###

Cette action est réalisée par la classe `GameRectDetector`, du fichier `gamedtc.py`

La zone de jeu peut être n'importe où. Si elle est visible entièrement sur l'écran, le script est censé la détecter.

La "zone de jeu" représente le rectangle affichant Math Master. Il ne s'agit pas de la zone de tout Anti-Idle. 

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

Dès que ça commencé, on affine la zone d'énigme, en rognant des lignes en haut et en bas. Une ligne est à rogner si elle ne contient aucun pixel "intéressant", c'est à dire aucun pixel suffisamment jaune ou blanc (les deux couleurs utilisées pour afficher les symboles). Cela a pour conséquence de rogner les contours noir en haut et en bas, mais ça dérange pas. 

La zone n'est pas rognée à gauche ni à droite, car on ne peut pas présumer de la longeur d'affichage d'une énigme.

### Extraction des symboles bruts et de la couleur du gros opérateur ###

Ces actions sont effectuées par la classe `SymbolExtractor`, dans le fichier `symbextr.py`.

Un "symbole" = la représentation graphique de l'un des caractères du texte de l'énigme. Par exemple, le dessin du "3", celui de la parenthèse "(", celui du point d'interrogation, ...

Le "gros opérateur" = L'opérateur que l'on voit parfois dans le texte d'une énigme, dans un cadre coloré. Dans les images ci-dessus, c'est le "+" vert.

Un "symbole brut" = comme un symbole, sauf que les lignes de pixels pas intéressants, éventuellement présentes en haut et en bas, ne sont pas encore rognées. Par exemple, le signe "=" a une hauteur plus petite que la zone d'énigme (même après affinage de cettedite zone).

Le jeu écrit les symboles en les espaçant suffisamment, et on a toujours au moins une colonne de pixels pas intéressants entre deux symboles. (Du moins avec une résolution d'écran pas trop dégueux). Ça arrange bien les choses.

Dans la zone de l'énigme, on considère donc que lorsqu'on trouve plusieurs colonne adjacentes, comportant chacune au moins un pixel intéressant, alors cela constitue un symbole.

L'extraction de symboles renvoie 3 informations :

 - la liste des symboles trouvées avant le gros opérateur.
 
 - la couleur d'un pixel du gros opérateur. On n'a pas besoin de son dessin complet. On déduira l'opérateur correspondant à partir de cette simple couleur.
 
 - la liste des symboles trouvées après le gros opérateur. 
 
Certains textes d'énigme ne comportent pas de gros opérateur. Par exemple : 2?3=5. Dans ce cas, la première liste contient tous les symboles du texte de l'énigme. La couleur du gros opérateur est indéfinie, et la dernière liste est vide.

### Conversion couleur -> valeur d'encre ###

Cette action est effectuée durant l'extraction des symboles bruts (voir étape précédente), par la fonction `SymbolExtractor._get_ink_of_pixel`, dans le fichier `symbextr.py`.

Un symbole est un dessin, et peut donc se définir par un tableau en 2D, contenant des valeurs de couleur rgb. Mais dans le script, on utilise des valeurs d'encre à la place des couleurs. 

Une "valeur d'encre" = une valeur entre 0 et 255, représentant, pour un pixel donné, son intensité en couleur jaune ou blanche. Lorsqu'on convertit une couleur en un valeur d'encre, on perd l'information qui dit si c'est du jaune ou du blanc. Mais ça ne dérange pas, on n'a besoin que de l'intensité.

### Construction des symboles affinés ###

Cette action est réalisée par la classe `Symbol`, dans le fichier `symbol.py`.

Il suffit de rogner les lignes pas intéressantes en haut et en bas du symbole, c'est à dire enlever celles ayant des valeurs d'encre toutes à 0.

### Reconnaissance des symboles et du gros opérateur ###

Cette action est réalisée par les fichiers `symbdata.py`, `symbref.py`, et `eniocr.py`.

On tente de trouver les caractères constituant le texte de l'énigme. Un symbole produit toujours un et un seul caractère. Le gros opérateur produit également un et un seul caractère.

Le script possède une bibliothèque de symboles connus, dans le fichier `symbdata.py`. Son chargement en mémoire a été effectuée au début, par la classe `SymbolReferences`, dans le fichier `symbref.py`.

Le script tente de retrouver, dans cette bibliothèque, des symboles de l'énigme, en faisant une comparaison d''égalité parfaite. Les dimensions (hauteur et largeur), et les tableaux 2D des encres doivent être rigoureusement égaux. 

Lorsqu'un symbole de l'énigme ne peut pas être reconnu (il n'y a pas son équivalent dans la bibliothèque des symboles), on considère que son caractère est le point d'exclamation. Les textes d'énigme ne comportant jamais de point d'exclamation, pas de risque de confusion.

Une énigme est "solvable" si son texte ne comporte aucun point d'exclamation.

L'action de reconnaissance des symboles est effectuée par la classe `EnigmaOcr`, dans le fichier `eniocr.py`.

La reconnaissance du gros opérateur est également effectuée par la classe `EnigmaOcr`.

### Demande des symboles non reconnus ###

Cette action (ainsi que les 2 suivantes) ne sont effectuées que si l'énigme n'est pas solvable.

Cette action est effectuée directement dans le fichier `main.py`. (voir la ligne contenant un appel à `raw_input`).

Le script écrit sur la console le texte actuel de l'énigme (avec les points d'exclamation), et demande à l'utilisateur de saisir soit le texte complet, soit les caractères correspondants au points d'exclamations. Le script reste en attente tant que l'utilisateur n'a rien saisi.

### remplacement des points d'exclamation par la saisie de l'utilisateur, et mise à jour de la bibliothèque ###

Cette action est effectuée par la classe `EnigmaOcr`, ainsi que par l'instance de `SymbolReferences` contenue dans `EnigmaOcr`.

On reconstitue le texte complet de l'énigme, sans point d'exclamation, à partir des symboles reconnus dès le départ, et de la saisie utilisateur.

Pour qu'une saisie utilisateur soit valide, elle doit respecter les contraintes suivantes :

 - Le nombre de caractères saisis est soit égal au nombre total de caractère de l'énigme, soit égal au nombre de point d'exclamation dans l'énigme.
 
 - Seuls les caractères "0123456789/*-+=?x()," sont autorisés.
 
Si la saisie n'est pas valide, la bibliothèque des symboles n'est pas mise à jour (du moins pas entièrement, voir docstring de EniOcr, quand je l'aurais faite). 

Si la saisie est valide, on fait correspondre chaque symbole non reconnu avec le caractère saisi par l'utilisateur, et on ajoute les symboles nouvellement créés dans la bibliothèque.

La bibliothèque de symboles accepte plusieurs symboles différents pour un même caractère. C'est nécessaire, car certains symboles ne sont pas toujours affiché de la même manière.

### Seconde tentative de reconnaissance des symboles ###

Cette action consiste à répéter l'étape "Reconnaissance des symboles et du gros opérateur".

Elle est effectuée, même si la saisie utilisateur a été identifiée comme invalide. Ce qui est un peu crétin, je le reconnais.

Si tout s'est bien passé, et que la bibliothèque des symboles a été correctement mise à jour, alors cette seconde tentative doit aboutir à un texte d'énigme solvable. 

Sauf que, même si ce nouveau texte d'énigme n'est pas solvable, on passe à l'étape suivante (crétin bis).

Les crétineries de cette étape sont à l'origine du bug "blocage sur la question en cours suite à un échec", décrit dans le fichier readme.md. J'ai la flemme de le corriger.

### Résolution de l'énigme ###

À partir de cette étape, on n'a plus besoin des symboles. Le texte de l'énigme suffit.

Cette action est effectuée par la classe `EnigmaSolver`, dans le fichier `enisolvr.py`.

Elle est effectuée quel que soit ce qu'il s'est passé avant :

 - La reconnaissance des symboles a marché du premier coup et a immédiatement donné un texte d'énigme solvable.
 
 - La reconnaissance a marché au deuxième coup, et le texte de l'énigme est maintenant solvable.

 - La reconnaissance a échoué deux fois de suite, et le texte n'est pas solvable.
 
Un texte d'énigme solvable ne va pas forcément aboutir à une réponse. Si la bibliothèque des symboles est incorrecte (parce que l'utilisateur a saisi des conneries), on peut très bien avoir un texte considéré sans points d'exclamation, mais qui ne veut rien dire. Par exemple : "5=3=8(2".

Si la résolution de l'énigme aboutit à une réponse, elle est affichée dans la console. Sinon, le message *resolution de l'enigme : fail* est affiché.

Que l'énigme ait abouti à une réponse ou pas, on passe aux étapes suivantes. C'est un peu crétin, et ça contribue au bug précédemment mentionné. (Flemme de corriger, comme toujours).

### Vérification que le jeu est fini ou pas ###

Cette action est effectuée directement dans `main.py`. (voir la ligne définssant la variable `rgb_bottom_left`, et les quelques lignes suivantes)

On refait une capture d'écran de la zone d'énigme affinée. Si le pixel en bas à gauche n'est plus le bleu de fond du jeu, on considère que c'est terminé, le script s'arrête.

### Attente de la prochaine énigme ###

Cette action est effectuée par la classe `SymbolExtractor` (Même si c'est pas vraiment son rôle et qu'il aurait mieux valu créer une autre classe pour ça). 

Le script refait périodiquement des captures d'écran de la zone d'énigme, et compare l'image obtenue avec celle de l'énigme précédente, tous les pixels ne sont pas systématiquement comparé, il y a un maillage. Dès qu'on trouve un pixel différent, n'importe où, on considère qu'il y a une nouvelle énigme. On reprend le traitement à l'étape "Extraction des symboles bruts et de la couleur du gros opérateur".

Cette action est effectuée conjointement avec l'action précédente. On fait une capture d'écran, on vérifie que le jeu est fini ou pas, on vérifie que l'énigme a changé ou pas, et on recommence, jusqu'à ce qu'il se passe quelque chose.

### Dump des symboles nouvellement ajoutés ###

Cette action est effectuée par la classe `SymbolReferences`, lorsque le script a détecté la fin du jeu. 

Le script ne sauvegarde rien (flemme), à la place, il écrit les nouveaux symboles sur la sortie standard. 

Chaque ligne écrite correspond à un symbole. Le script n'écrit que les symboles ajoutés dans la bibliothèque suite aux saisies utilisateurs. Il ne réécrit pas les symboles déjà connus par `symbdata.py`.

Chacune de ces lignes doit donc être manuellement recopiées dans `symbdata.py`, en tant qu'élément supplémentaire du tuple `LIST_SYMB_ALARRACHE`. 

Pour les branques qui ne connaissent pas la syntaxe du python : il faut ajouter 3 double guillemets `"""` au début de chaque ligne, et 3 double guillemets suivi d'une virgule `""",` à la fin de chaque ligne.

## Mots de vocabulaire utilisés pour composer les noms de variables dans le code. ##

`x_ y_ _size_ _top _bottom _left _right line column` : les trucs habituels : coordonnées, taille, côtés de rectangle, ...

`_game_` : zone du jeu Math Master.

`_scr_` : une coordonnée définie par rapport à l'écran, et non pas par rapport à un dc quelconque.

`rez`, `raw_enigma_zone` : Rectangle représentant la zone d'énigme brute

`ez`, `enigma_zone` : Rectangle représentant la zone d'énigme affinée.

`dc_` : dc (drawing context), de la librairie wx.

`dtc` : non ce n'est pas "dans ton cul". C'est "detector". Une classe analysant un dc provenant d'une capture d'écran, pour y trouver des trucs dedans.

`_raw_` : brut. (zone d'énigme, symbole, etc)

`_proc_` : processed. Affiné. le contraire de brut. Je ne mets pas systématiquement ce mot dans les noms de variables. Uniquement dans les situations où on veut bien montrer qu'on passe du brut à l'affiné. Sinon, en général, quand ni "raw", ni "proc", c'est que c'est affiné

`screen` : le dc correspondant à l'écran du n'ordinateur.

`list_` : peut être un tuple ou une liste, on fait pas la différence on s'en tape. (duck typing, tout ça).

`_big_op` : le gros opérateur, qui est parfois présent dans les zones d'énigme.

`ocr` : truc qui veut dire reconnaissance d'écriture. Je sais pas d'où ça sort ce nom, et mon script ne fait absolument pas d'ocr, mais c'est pas grave.

`ocr_ify` : action d'ocrifier (appliquer de l'ocr). Oui c'est moche et c'est n'importe quoi.

`rgb_` : trouple (tuple de 3 entiers). Composantes Red-Green-Blue d'une couleur.

`hsv_` : trouple de 3 entiers. Composante Hue-Saturation-Value d'une couleur.

`red grn blu hue sat val` : les composantes spécifiques des trouples rgb et hsv.

`comp` : composante. Nom générique pour désigner une composante (n'importe laquelle) d'une couleur rgb ou hsv.

`col` : couleur. Terme générique pour dire que ça peut être du hsv ou du rgb.

`_EXACT_` : couleur de référence d'un "truc" spécifique . (Par exemple, la couleur de fond de la zone d'énigme, la couleur verte du gros opérateur '+', ...). Cette couleur de référence est comparée avec la couleur d'un pixel de l'écran, et elles doivent être rigoureusement exacte, pour repérer le "truc" en question.

`_APPROX_` : couleur de référence d'un "truc" spécifique. (Par exemple, la couleur marron-bois-moche délimitant l'extérieur de la zone de jeu). On autorise un certain écart (prédéfini) entre cette couleur de référence et la couleur d'un pixel de l'écran, pour repérer le "truc" en question.

`enigma_text` : le texte de l'énigme

`enigma_text_help` : le texte saisi par l'utilisateur, qui doit permettre de compléter les caractères inconnus du texte de l'énigme

`enigma_text_complete` : texte complet de l'énigme, sans caractère inconnus (points d'exclamation).

`answer` : string. La réponse de l'énigme, que le script doit trouver automatiquement.

`msg` : envoi de message sur la sortie standard, dont l'utilisateur a vraiment besoin.

`log` : envoi de message verbose. l'utilisateur n'en a pas vraiment besoin, mais le développeur en a eu besoin à un moment donné de sa vie qui est super (ou pas).

`_square_` : rectangle de la zone de jeu. C'est très vilain comme nommage, car c'est pas du tout un square. Il faudra changer ça.

`border` : les pixels extérieurs à la zone de jeu (haut bas gauche droite), qui ont une couleur marron-bois-moche.

`lit_pixel` : la ou les colonnes de pixels gris clair, qui se trouvent entre le côté droit de la zone de jeu, et les pixels extérieurs.

`_depl_` : valeur de déplacement à appliquer à une coordonnée x ou y, pour la faire bouger de ici vers autre part. (Ça c'est de l'explication !)

`step` : valeur de déplacement à appliquer à une coordonnée, quand on veut la faire bouger plusieurs fois, dans une boucle. 

`pattern` : ligne ou colonne de pixel, correspondant à un motif précis. Par exemple : "un ou plusieurs pixels rouge, puis 10 pixels verts, puis éventuellement un pixel violet".

`cursor` : une coordonnée x ou y, qu'on fait avancer, pour vérifier ou chercher des trucs dans des pixels.

`cur` : valeur courante. Une valeur qu'on fait avancer dans une boucle.

`crop` : rognage. Action de supprimer une ligne ou une colonne située au bord d'une image, parce qu'elle n'est pas intéressante.

`ink` ou `inks` : une valeur d'encre d'un pixel, ou les valeurs d'encres d'un tableau de pixel.

`array_inks` : tableau 2D des encres d'un symbole, rangés comme il faut. C'est une liste. Chaque élément est une sous-liste. Chaque sous-liste représente une ligne de valeur d'encre.

`raw_symbol` : tableau 2D des encres d'un symbole. Il peut y avoir, dans une ou plusieurs lignes du début, et dans une ou plusieurs lignes de la fin, des valeurs d'encres toutes à zéro.

`columord_symb`: "column-ordered symbol". tableau 2D des encres d'un symbole, rangés par colonne. (c'est comme ça qu'on récupère les symboles au départ, car on analyse la zone d'énigme colonne par colonne). C'est une liste. Chaque élément est une sous-liste. Chaque sous-liste représente une colonne de valeur d'encre. Un tableau columord_symb est "raw", et non pas "affiné". C'est à dire que des lignes du haut et du bas peuvent avoir des valeurs d'encres toutes à zéro. Mais c'est difficilement détectable en l'état, puisque les valeurs d'encre d'une ligne sont dispersés dans le tableau.

`flat_list_ink` : grande liste (en une dimension) des valeurs d'encres d'un symbole. Correspond à array_inks, sauf que toutes les valeurs sont mises bout à bout. Une variable flat_list_ink ne permet pas de connaître les dimensions (largeur, hauteur) d'un symbole. Il faut avoir stockées ces infos autre part.

`sig`, `signifiance` : string de un seul caractère, représentant ce que signifie un symbole. C'est ce qui permet de passer d'une liste de symbole au texte d'une énigme.

`saved_data` : grande string, contenant les informations permettant de sauvegarder un symbole. Chaque élément de LIST_SYMB_ALARRACHE est une saved_data. Une saved_data contient, dans cet ordre : 
 - la signifiance (un caractère)
 - la largeur et la hauteur du symbole. (deux valeurs numériques, converties en string).
 - la flat_list_ink du symbole. (plusieurs valeurs numériques, converties en string).
Le séparateur est le caractère espace.
 
`comes_from_raw_symbol` : booléen permettant de savoir d'où vient un symbole. 
 - True : le symbole a été défini par un `raw_symbol`. C'était un symbole inconnu au départ, on l'a trouvé dans une énigme posée par le jeu, et l'utilisateur a saisi sa `signifiance`.
 - False : le symbole était connu au départ. ses dimensions, ses valeurs d'encre et sa `signifiance` se trouvaient tous dans une `saved_data`.
 
`ref`, `reference` : symbole de référence, dont la signifiance est connue. On essaie de faire correspondre chaque symbole d'une énigme à un symbole de référence, pour déterminer le texte de l'énigme.

`calculation` : type d'énigme, pour laquelle il faut calculer une valeur numérique. Exemple : *2 + 2 = ?*

`comparrison` : type d'énigme, pour laquelle il faut comparer deux valeurs numériques (en faisant plus ou moins de calcul intermédiaire). Par exemple : *12+3 ? 28/2 *. Il faut trouver si 12+3 est plus grand, égal ou plus petit que 28/2.

`find_operator` : type d'énigme, pour laquelle il faut trouver l'opérateur manquant, afin de vérifier l'égalité mentionnée. Par exemple : *3 ? 2 = 6*. Il faut trouver quelle égalité est vraie, parmi les 4 possibilités : *3 + 2 = 6*, *3 - 2 = 6*, *3 * 2 = 6*, *3 / 2 = 6*.

`_enigma_part` : string. morceau de texte d'énigme, contenant une opération mathématique que l'on peut calculer immédiatement. Une _enigma_part ne doit contenir que des chiffres, des parenthèses et les 4 opérations. Elle ne doit pas contenir de signe égal ou de point d'interrogation.

`_val` : valeur numérique. Résultat du calcul d'une `_enigma_part`.
 
## Description détaillée de chaque classe ##

Putain, va y'en avoir encore pour une tartine de blabla. J'aime être verbeux, que voulez-vous.


## Améliorations possibles ##

 - Essayer d'être un peu plus homogène dans les noms parce que c'est parfois le bordel.

 - Utiliser logging pour faire du log digne de ce nom, avec différents niveaux. (verbose, log, error, ...).
 
 - Arrêter de passer les dimensions d'un DC en même temps que le DC.
 
 - Tous les TODO indiqués dans le code.
