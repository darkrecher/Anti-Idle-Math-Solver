**Edit 2013-12-14:** Ce script ne fonctionne plus depuis la version 1,652 de Anti-Idle. Ce serait assez simple à corriger, il suffit de mettre à jour les définitions de couleurs. Si vous voulez que je le fasse, envoyez un message ou un signalement de bug. En attendant, j'ai la flemme de le faire.

# Anti-Idle Math Solver #

Ceci est un espèce de script pour avoir des gros scores au sous-jeu "Math Master", du jeu Flash "Anti-Idle", jouable sur Kongregate. (http://www.kongregate.com/games/Tukkun/anti-idle-the-game)

Le jeu Math Master se présente comme ceci :

![My screenshot](https://raw.github.com/darkrecher/Anti-Idle-Math-Solver/master/doc_img_readme/screenshot-example.png)

Vous avez une minute pour répondre à des questions existentielles telles que "123/3 est-il plus grand, plus petit ou égal à 30+5 ?".

Je pensais être suffisamment fort en calcul mental, et arriver sans trop de difficultés à l'honorable score de 300 000 points, (nécessaire pour un achievement). Or il se trouve que non, je suis une grosse tanche.

J'ai donc créé ce petit script, et suis arrivé, sans forcer, jusqu'à 800 000 points.

# Principe de fonctionnement #

Vous démarrez une partie de Math Master, et en même temps, vous lancez le script. Celui-ci effectue périodiquement des copies d'écran et réalise une (très vague) reconnaissance de caractères, afin d'en déduire la question qui est affichée. Puis, il calcule et affiche la réponse. Vous n'avez plus qu'à cliquer dessus dans le jeu. Plus besoin de faire de calculs compliqués avec votre cerveau !

Le script ne clique pas de lui-même sur la bonne réponse. Ceci pour plusieurs raisons :

 - Je sais pas le faire et j'ai la flemme de chercher.
 
 - Il vaut mieux que les actions sur le jeu restent effectuées par un humain. Si c'est automatique, le jeu pourrait détecter une éventuelle tricherie. (Par exemple, les clics sont faits à intervalle réguliers, ou toujours aux mêmes positions).
 
# Comment installer et utiliser le script ? #

**Avertissement :** c'est du "Chez moi, ça marche." J'ai codé ça vite fait, sans prendre le temps de le mettre à la portée des gens qui pataugent avec difficultés dans l'informatique. Je n'ai pas l'intention d'y apporter une quelconque amélioration, sauf demande expresse accompagnée d'argent ou de chocolat.

Le script est censé fonctionner quelle que soit la résolution de votre/vos écrans, mais je n'ai pas testé. "Chez moi ça marche". J'ai un seul écran, en 1280*720.

De plus, la reconnaissance de caractères est faite à la bourrine. Il faut indiquer et sauvegarder manuellement les symboles durant les premières exécutions du script.

Ceci étant dit, place aux étapes :

 - Installez python (chez moi c'est la version 2.6.6)
 
 - Installez la librairie wx (chez moi : 2.8.12.1)

 - Copiez tout le repository quelque part sur votre disque.

 - Si vous avez la chance d'avoir la même résolution que moi, vous pourrez peut-être profiter des définitions de symboles que je me suis enregistrées. Sinon il faudra les faire vous même. Pour supprimer les définitions existantes, éditer le fichier symbdata.py, et effacer tout le contenu du tuple "LIST_SYMB_ALARRACHE". Le tuple doit rester présent, mais vide.
 
 - Lancez Anti-Idle, mettez-vous en Ranked Mode et allez à l'écran d'intro de Math Master. Le script ne marche pas en Unranked Mode (les couleurs du jeu ne sont pas tout à fait les mêmes, et j'avais la flemme de gérer les deux modes).
 
 - Assurez-vous que la zone grise du jeu est entièrement visible à l'écran, et qu'il y a un peu de pixel marron-bois sur les bords. Il faut qu'on voit ça en entier :
 
![Intro jeu](https://raw.github.com/darkrecher/Anti-Idle-Math-Solver/master/doc_img_readme/screenshot-intro.png)
 
 - Ouvrez une console et lancez le script avec la commande : *python main.py*
 
 - Attendez un peu. La console va blablater quelques trucs, puis répéter le message : *en attente. tralala.*

 - À partir de maintenant, il ne faut plus bouger le navigateur internet, ni scroller la fenêtre afichant le jeu. Sinon le script ne retrouvera plus sa position.
 
 - Lancer la partie de Math Master.
 
 - Dès la première question, le script devrait avoir repéré les symboles affichés. Mais il ne connait pas encore leur signification. C'est à vous de les lui indiquer. Par exemple, si le jeu pose la question suivante :
 
![Example question](https://raw.github.com/darkrecher/Anti-Idle-Math-Solver/master/doc_img_readme/screenshot-question.png)
 
 - Vous verrez apparaître, dans la console, le texte : *!!/!!! Saisissez la question posee par le jeu :* . Cela signifie que le script a repéré 2 symboles inconnus (représentés par les 2 premiers points d'exclamation), puis le signe "/", puis 3 autres symboles inconnus. 
 
 - Saisissez le texte *98/7=?* dans la console. Le script vous donnera la réponse, que vous pourrez alors sélectionner dans le jeu.
 
 - Faites la même chose pour les questions suivantes. (Oui c'est chiant).
 
 - Lorsque la partie est terminée, le script va s'arrêter tout seul, et écrire dans la console un tas de chiffres, représentant les symboles qu'il a appris.
 
 - Copier-collez ces infos dans le fichier symbdata.py. Chaque ligne doit constituer un élément du tuple "LIST_SYMB_ALARRACHE". Si vous ne connaissez pas la syntaxe du python, inspirez-vous du fichier symbdata.py initial, et surtout, débrouillez-vous.
 
 - Relancez une partie de Math Master, et refaites de même. (Oui, c'est SUPER chiant, et au début vous allez gâcher quelques parties).
 
 - Au fur et à mesure que le script apprend les symboles, il y aura de moins en moins de points d'exclamation, et de plus en plus de caractères connus. Vous pouvez saisir uniquement les inconnus. Par exemple, si le script vous demande : *(19+13!/2?!6* , indiquez juste les deux caractères *)1*, ça lui suffit, et il parviendra à reconstituer la question : *(19+13)/2?16* .
 
 - Les points d'interrogation indiqués dans la console correspondent directement aux points d'interrogations dans le jeu. Ce sont les points d'exclamation qui indiquent les symboles à définir. Oui c'est pas clair, je sais.
 
 - Certains caractères devront être indiqués et sauvegardés plusieurs fois, car le jeu a plusieurs façons de les écrire. Dès qu'un micro-poil de cul de pixel change, le script ne reconnaît pas le symbole et vous le redemande. 
 
 - Au bout d'un moment, on finit par y arriver. Lorsque le jeu pose une question dont tous les symboles sont connus, la réponse s'affiche immédiatement dans la console. Cette réponse peut être une valeur numérique, un opérateur / * - +, ou un signe de comparaison < = >. 
 
 - Cliquer sur la bonne réponse dans le jeu, continuez ainsi au fur et à mesure des questions, et gavez-vous !
 
# Bugs connus #

## Blocage sur la question en cours suite à un échec ##

Dans les deux cas suivants :

 - Le script n'a pas réussi à reconnaître tous les symboles d'une énigme, a demandé une saisie à l'utilisateur, et l'utilisateur a saisi des conneries.
 
 - Le script a reconnu tous les symboles, mais ça a donné une énigme sans aucun sens. Cela peut arriver si les définitions de symboles sont incorrectes. (Par exemple, le dessin d'un "5" est identifié comme le caractère "/").
 
Le script indiquera en sortie : *resolution de l'enigme : fail*, et restera bloqué. Il ne demandera pas de nouvelle saisie. L'utilisateur n'a pas d'autre choix que de trouver la réponse avec son propre cerveau. 

Lorsque l'énigme suivante s'affiche à l'écran, le script se débloque et continue comme si rien de terrible ne s'était passé.

## Risque de mauvaise détection de la zone d'énigme. ##

Supposons que les symboles aient des hauteurs vraiment disparates. Par exemple, le "8" fait 20 pixel de haut, tous les autres symboles font 15 maximum.

Si la première énigme posée ne comporte pas de "8", le script croira que la zone d'énigme fait 15 pixels de haut. Et si il y a un ou plusieurs "8" dans les énigmes suivantes, ils ne seront pas détectés.

C'est un bug "qui n'est pas censé arriver". Tous les symboles de chiffres ont la même hauteur. Et tous les autres symboles sont soit plus petits, soit de hauteur égales. Et il y a toujours au moins un chiffre dans une énigme.

## Cafouillage sur les couleurs du gros opérateur ##

Si la zone d'énigme comporte des pixels de couleurs RGB = (76, 76, 76), ça va planter. Il y a quelques autres couleurs pour lesquelles ça plantera aussi. Pour une explication plus détaillée, voir le TODO dans le fichier `symbextr.py`, au-dessus de la fonction `is_rgb_big_op`.

# Voili voilà #

Pour une description détaillée du code, des algorithmes, et des bidouillages employés, se référer au fichier DOC_CONCEPTION.md de ce repository.

Bon courage et amusez-vous bien ! Prochaine étape : un script d'assistance au jeu de pêche (J'y suis également une grosse tanche, ce qui est assez ironique pour un jeu de pêche).

# Crédits #

Créé par Réchèr. 

Le code et cette doc sont sous la double licence : Art Libre ou Creative Commons CC-BY (au choix).

Repository : https://github.com/darkrecher/Anti-Idle-Math-Solver

Mon blog : http://recher.wordpress.com