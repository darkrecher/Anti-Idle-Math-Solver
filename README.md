# Anti-Idle Math Solver #

Ceci est un espèce de script pour avoir des gros scores au sous-jeu "Math Master", du jeu "Flash Anti-Idle", jouable sur Kongregate. (http://www.kongregate.com/games/Tukkun/anti-idle-the-game)

Le jeu Math Master se présente comme ceci :

(screenshot)

Vous avez une minute pour répondre à des questions existentielles telles que "est-ce que 123/3 est plus grand, plus petit ou égal à 30+5 ?".

Je pensais être suffisamment fort en calcul mental, et arriver sans trop de difficultés à l'honorable score de 300 000 points, (nécessaire pour un achievement). Or il se trouve que non, je suis une grosse tanche.

J'ai donc créé ce petit script, et je suis arrivé, sans forcer, jusqu'au score de 800 000 points.

# Principe de fonctionnement #

Vous démarrez une partie de Math Master, et en même temps, vous lancez le script. Celui-ci effectue périodiquement des copies d'écran, analyse l'image obtenue, trouve l'emplacement de la fenêtre du jeu, et effectue une (très vague) reconnaissance de caractères, afin d'en déduire la question qui est affichée. Ensuite, le script résout cette question, et vous indique la réponse. Vous n'avez plus qu'à cliquer dessus dans le jeu, sans faire de calculs compliqués avec votre cerveau.

Le script n'effectue pas automatiquement le clic sur la bonne réponse. Ceci pour plusieurs raisons :
 - Je sais pas le faire et j'avais la flemme de chercher comment le faire.
 - Il vaut mieux que les actions sur le jeu restent effectuées par un humain. Si c'est automatique, le jeu pourrait détecter une éventuelle tricherie. (Par exemple, si les clics sont faits à intervalle réguliers, ou toujours aux mêmes positions, ...
 
# Comment installer et utiliser le script ? #

**Avertissement :** c'est du "Chez moi, ça marche." J'ai codé ça vite fait, sans prendre le temps de le mettre à la portée des gens qui ont des difficultés à patauger dans le monde fabuleux de l'informatique. Je n'ai pas l'intention d'y apporter une quelconque amélioration, sauf demande expresse de gens divers.

De plus, la reconnaissance de caractères est faite à la bourrine. Il faut indiquer et sauvegarder manuellement les symboles durant les premières exécutions du script.

Ceci étant dit, place aux étapes :

 - Installez python (chez moi c'est la version 2.6.6)
 
 - Installez la librairie wx (chez moi c'est la version 2.8.12.1)

 - Copiez tout le repository quelque part sur votre disque.

 - Si vous avez la chance d'avoir la même résolution d'écran que moi (1280*720), vous pourrez peut-être profiter des définitions de symboles que je me suis faite pour moi. Sinon il faudra les faire vous même. Pour supprimer les définitions existantes, éditer le fichier symbdata.py, et effacer tout le contenu du tuple "LIST_SYMB_ALARRACHE". Le tuple doit toujous être présent, mais vide.
 
 - Lancez Anti-Idle, mettez-vous en Ranked Mode et allez à l'écran d'intro de Math Master. Le script ne marche pas en Unranked Mode (les couleurs du jeu ne sont pas tout à fait les mêmes, et j'avais la flemme de gérer les deux modes).
 
 - Assurez-vous que la zone grise du jeu est entièrement visible à l'écran, et qu'il y a un peu de pixel marron-bois sur les bords. Il faut qu'on voit ça en entier :
 
 (img)
 
 - Ouvrez une console et lancez le script : *python main.py*
 
 - Attendez un peu. La console va blablater quelques trucs, puis répéter le message : "*en attente. tralala.*"

 - À partir de maintenant, il ne faut plus bouger le navigateur internet, ni scroller la fenêtre afichant le jeu. Sinon le script ne retrouvera plus sa position.
 
 - Lancer la partie de Math Master.
 
 - Dès la première question, le script devrait avoir repéré les caractères. Mais il ne connait pas leur signification. Vous devez lui indiquer vous-même. Par exemple, si le jeu pose la question suivante :
 
 (img)
 
 - Vous verrez apparaître dans la console le texte : "*!!/!!! Saisissez la question posee par le jeu : *". Cela signifie que le script a repéré 2 symboles inconnus (représenté par les points d'exclamation), puis le signe "/", puis 3 symboles inconnus. Saisissez le texte "98/7=?" dans la console. Le script vous donnera la réponse, que vous pourrez alors sélectionner dans le jeu.
 
 - Faites la même chose pour les questions suivantes. (Oui c'est chiant).
 
 - Lorsque la partie est terminée, le script va s'arrêter tout seul, et écrire dans la console un tas de chiffres, représentant les symboles appris.
 
 - Copier-collez ces infos dans le fichier symbdata.py. Chaque ligne écrite dans la console va définir un élément de "LIST_SYMB_ALARRACHE". Si vous ne connaissez pas la syntaxe du python, inspirez-vous du fichier symbdata.py initial, et surtout, débrouillez-vous.
 
 - Relancer une partie de Math Master, et refaites de même. (Oui, c'est SUPER chiant, et vous allez gâcher quelques parties à faire des scores tout pourris).
 
 - Au fur et à mesure, le script reconnaîtra de plus en plus de symboles. Lorsqu'il vous demandera de saisir une question, il y aura de moins en moins de points d'exclamation, et de plus en plus de caractères connus. Vous pouvez ne saisir dans la console que les symboles inconnus, au lieu de toute la question. Par exemple, si le script vous demande : (19+13!/2?!6 vous pouvez saisir les deux caractères ")1", ce qui correspondra à la question (19+13)/2?16.
 
 - Les points d'interrogation indiqués dans la console correspondent directement aux points d'interrogations dans le jeu. Ce sont les points d'exclamation qui indiquent les symboles à définir. Oui c'est pas clair, je sais.
 
 - Certains caractères devront être indiqués et sauvegardés plusieurs fois, car le jeu a plusieurs façons de les écrire. Dès qu'un micro-poil de cul de pixel change, le script ne reconnaît pas le symbole et le demande. Je vous ais déjà dit que c'était chiant ?
 
 - Au bout d'un moment, on finit par y arriver. Lorsque le script connaît tous les symboles d'une question, il affiche automatiquement la réponse dans la console. Cette réponse peut être une valeur numérique, un opérateur / * - +, ou un signe de comparaison < = >. C'est à vous de cliquer sur le bouton correspondant dans le jeu.
 
 
Voilà, amusez-vous bien ! Et si quelqu'un connaît un bon deck de TukkunFCG pour battre les bots de niveau 7, je suis preneur.

Le code et cette doc sont sous licence Creative Commons CC-BY.