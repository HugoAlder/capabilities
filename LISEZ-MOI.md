#SDS - Sécurité de Linux

##Objectif

L'objectif de ce TP est d'écrire un script capable d'écouter sur le port 80 et de renvoyer "hello" comme réponse à "GET / HTTP/1.1". La difficulté principale est la suivante : nous devons être capable de dropper les droits root lors du déroulement du programme. De plus, ce dernier ne doit pas utiliser plus de 150Mo de mémoire et se voir réserver a minima 10% de puissance CPU.

##Etape 1

Nous avons décidé d'utiliser le langage de programmation Python. Nous avons commencé par utiliser SimpleHTTPServer en python2 pour développer le serveur HTTP. Nous avons ensuite utilisé BaseHTTPRequestHandler avec python3 afin de pouvoir utiliser la bibliothèque cgroups.
