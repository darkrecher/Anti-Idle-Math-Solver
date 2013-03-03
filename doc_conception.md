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

Il suffit de rogner les lignes inintéressantes en haut et en bas du symbole. C'est à dire d'enlever les lignes comportante des valeurs d'encre toutes à 0.

Cete action est réalisée par la classe Symbol, dans le fichier symbol.py

### Reconnaissance des symboles et du gros opérateur ###

On tente de trouver les caractères correspondant à chaque symbole de l'énigme, et de trouver le caractère correspondant au gros opérateur, afin d'obtenir le texte de l'énigme.

Un symbole produit toujours un et un seul caractère. Le gros opérateur produit également un et un seul caractère.

Le script possède une bibliothèque des symboles existants. Il tente de retrouver, dans cette bibliothèque, des symboles de l'énigme. L'égalité doit être parfaite. C'est à dire que la taille (hauteur et largeur), et le tableau en 2D des encres doivent être rigoureusement égaux. 

Lorsqu'un symbole de l'énigme ne peut pas être reconnu (il n'y a pas son équivalent dans la bibliothèque des symboles), on considère que son caractère correspondant est le point d'exclamation. Les textes d'énigme ne comportent jamais de point d'exclamation, donc pas de risque de confusion.

Une énigme est "solvable" si son texte ne comporte aucun point d'exclamation.

La bibliothèque des symboles connus se trouve dans le fichier symbdata.py.

Le chargement en mémoire de cette bibliothèque est effectuée par la classe SymbolReferences, dans le fichier symbref.py

L'action de reconnaissance des symboles d'une énigme est effectuée par la classe EnigmaOcr, dans le fichier eniocr.py. Cette classe utilise une instance de SymbolReferences.

La reconnaissance du gros opérateur est effectuée par la classe EnigmaOcr.

### Demande des symboles non reconnus ###

Cette action (ainsi que les 2 actions suivantes) ne sont effectuées que si l'énigme n'est pas solvable.

Le script écrit le texte actuelle de l'énigme sur la console (avec les points d'exclamation), et demande à l'utilisateur de saisir le texte complet de l'énigme, ou bien les caractères correspondants au points d'exclamations. Le script reste en attente tante que l'utilisateur n'a rien saisi.

Cette action est effectuée directement dans le fichier main.py. (voir la ligne contenant un appel à `raw_input`)

### remplacement des points d'exclamation par la saisie de l'utilisateur, et mise à jour de la bibliothèque ###

On reconstitue le texte complet de l'énigme, sans point d'exclamation, à partir des éventuels symboles reconnus dès le départ, et de la saisie utilisateur.

Pour qu'une saisie utilisateur soit valide, elle doit respecter les contraintes suivantes :

 - Le nombre de caractères saisis est soit égal au nombre total de caractère du texte de l'énigme, soit égal au nombre de point d'exclamation dans le texte de l'énigme.
 
 - Seuls les caractères "0123456789/*-+=?x()," sont autorisés.
 
Si la saisie n'est pas valide, la bibliothèque des symboles n'est pas mise à jour (du moins pas entièrement, voir description détaillée de cette étape, un peu plus loin). 

Si la saisie est valide, on fait correspondre chaque symbole non reconnu avec son caractère saisi par l'utilisateur, et on met ajoute les symboles nouvellement créé dans la bibliothèque.

La bibliothèque de symbole accepte que plusieurs symboles différents correspondent au même caractère. C'est nécessaire, car certains symboles ne sont pas toujours affiché exactement de la même manière.

Cette action est effectuée par la classe EnigmaOcr, ainsi que par l'instance de SymbolReferences contenues dans EnigmaOcr.

### Seconde tentative de reconnaissance des symboles ###

Cette action est exactement la même que celle décrite dans l'étape "Reconnaissance des symboles et du gros opérateur".

Elle est effectuée, même si la saisie utilisateur a été identifiée comme invalide. Ce qui est un peu crétin, je le reconnais.

Si tout s'est bien passé, la bibliothèque des symboles a été correctement mise à jour par la saisie utilisateur. Et cette seconde tentative de reconnaissance doit aboutir à un texte d'énigme sans solvable. 

Même si ce nouveau texte n'est pas solvable, on passe quand même à l'étape suivante.

Les actions crétines de cette étape sont à l'origine du bug "blocage sur la question en cours suite à un échec", décrit dans le fichier readme.md. J'ai la flemme de le corriger.

### Résolution de l'énigme ###

À partir de cette étape, on n'a plus besoin des symboles. Le texte de l'énigme suffit.

Cette action est effectuée quel que soit ce qu'il s'est passé avant. C'est à dire, dans les cas suivants :

 - La reconnaissance des symboles a marché du premier coup et a donné un texte d'énigme solvable.
 
 - La reconnaissance a marché au deuxième coup (après la saisie utilisateur), et a le texte de l'énigme est maintenant solvable.

 - La reconnaissance a échoué deux fois de suite, le texte n'est pas solvable.
 
Un texte d'énigme solvable (sans point d'exclamation) ne va pas forcément aboutir à une réponse. Si la bibliothèque des symboles est incorrecte (parce que l'utilisateur a saisi des conneries), on peut très bien avoir un texte d'énigme considéré comme solvable, mais qui ne veut rien dire. Par exemple : "5=3=8(2".

On tente donc de résoudre l'énigme, cela aboutit à une réponse, ou pas. Si il y a une réponse, elle est affichée dans la console. Sinon, le message "resolution de l'enigme : fail" est affiché.

Que l'énigme ait abouti à une réponse ou pas, on passe aux étapes suivantes. C'est un peu crétin, et ça contribue au bug précédemment mentionné. (Flemme de corriger, comme toujours).

Cette action est effectuée par la classe EnigmaSolver, dans le fichier enisolvr.py.

### Vérification que le jeu est fini ou pas ###

On refait une capture d'écran de la zone d'énigme, si le pixel en bas à gauche n'est plus le bleu de la couleur de fond du jeu, on considère que le jeu est terminé, le script s'arrête.

Cette action est effectuée directement dans le fichier main.py. (voir la ligne définssant la variable `rgb_bottom_left`, et les quelques lignes suivantes)

### Attente de la prochaine énigme ###

Le script refait périodiquement des captures d'écran de la zone d'énigme, et compare l'image obtenue avec l'image de l'énigme précédente. (Tous les pixels ne sont pas systématiquement comparé, il y a un maillage). Dès qu'on trouve un pixel différent, n'importe où dans la zone d'énigme, on considère qu'il y a une nouvelle énigme. On reprend le traitement à l'étape "Extraction des symboles bruts et de la couleur du gros opérateur".

Cette action est effectuée conjointement avec l'action précédente. On vérifie que le jeu est fini ou pas, puis on vérifie que l'énigme a changé ou pas, etc. jusqu'à ce que l'un des 2 événements survienne.

Cette action est effectuée par la classe SymbolExtractor (Même si c'est pas vraiment son rôle et qu'il aurait mieux fallu créer une autre classe pour ça). 

### Dump des symboles nouvellement ajoutés ###

Cette action est effectuée lorsque le script a détecté que le jeu était fini. 

On ne sauvegarde pas automatiquement ces nouveaux symboles. À la place, on les écrit sur la sortie standard. 

Chaque ligne correspond à un symbole qui a été ajouté dans la bibliothèque durant cette exécution du script, suite aux saisies utilisateurs.

Chacune de ces lignes doit être copié et collé dans le fichier symbdata.py, en tant qu'élément supplémentaire du tuple LIST_SYMB_ALARRACHE. 

Pour les branques qui ne connaissent pas la syntaxe du python, il faut ajouter 3 double guillemets : """ au début de la ligne, et 3 double guillemets suivi d'une virgule : """, à la fin de la ligne, pour en faire un élément de tuple valide.

Cette action est effectuée par la classe SymbolReferences (la classe contenant la bibliothèque des symboles).


## Mots de vocabulaire utilisé pour composer les noms de variables dans le code. ##

À être continué.


## Description détaillée de chaque classe ##

Putain, va y'en avoir encore pour une tartine de blabla. J'aime être verbeux, que voulez-vous.


## Améliorations possibles ##


