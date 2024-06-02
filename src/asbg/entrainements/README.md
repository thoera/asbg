# Entrainements

## Objectif

Le nombre de joueurs souhaitant participer à l'entrainement étant parfois supérieur au nombre de places disponibles, il est souhaitable d'automatiser au maximum le processus de sélection avec des règles précises.

## Algorithme de sélection

Le processus de sélection passe par l'envoi de formulaires Google Forms pour chaque entrainement.

Ce formulaire `F1` est simple, il ne permet de s'inscrire qu'à l'entrainement de la semaine à venir et est ouvert du samedi au lundi (12h).

Une fois le nombre de places atteint, `F1` renvoie les joueurs qui souhaitaient s'inscrire pour l'entrainement vers un nouveau formulaire `F2'`.

Ce formulaire `F2'` comprend deux questions :

* Souhaites-tu t'inscrire sur la liste d'attente pour l'entrainement à venir ?
* Souhaites-tu t'inscrire sur la liste prioritaire pour l'entrainement de la semaine suivante ?

La période d'ouverture du formulaire `F2'` est la même que celle de `F1`. Il n'est donc pas possible d'anticiper l'inscription pour le prochain entrainement.
Les joueurs s'inscrivant sur la liste prioritaire devront confirmer leur participation dans le formulaire envoyer le samedi suivant.

Les données en entrée de l'algorithme sont les suivantes :

* La liste des joueurs inscrits pour l'entrainement à venir ;
* Les joueurs inscrits sur liste prioritaire pour l'entrainement à venir ;
* Les joueurs inscrits sur liste d'attente pour l'entrainement à venir.
* Les joueurs qui étaient sélectionnés pour l'entrainement précédent (présents ou non) ;

Algorithme de sélection :

* On sélectionne d'abord les joueurs inscrits sur la liste prioritaire pour l'entrainement à venir et inscrits via le formulaire `F1` ;
* On complète par les joueurs inscrits via `F1` qui n'ont pas participé au dernier entrainement ;
* S'il reste des places disponibles, on complète :
    * Par les joueurs inscrits sur la liste d'attente qui n'ont pas participé au dernier entrainement ;
    * Puis par les joueurs inscrits qui ont participé au dernier entrainement ;
    * Puis par les joueurs inscrits sur liste d'attente qui ont participé au dernier entrainement.

Les joueurs inscrits via `F1` et qui n'ont pas pu être sélectionnés sont automatiquement placés sur la liste prioritaire pour l'entrainement suivant.

En cas d'arbitrage à faire entre deux joueurs qui se retrouvent dans les mêmes conditions pour une place, on applique la règle du "premier arrivé, premier servi".

## Ordonnancement de l'envoi des mails et des Google Forms

Semaine 0 :

* Envoi du mail permettant de s'inscrire pour l'entrainement à venir le samedi à 18h ;
* Le Google Forms est ouvert de samedi 18h à lundi 12h ;
* Le Google Forms permettant de s'inscrire sur la liste d'attente pour l'entrainement à venir et sur la liste prioritaire pour l'entrainement suivant est ouvert à partir du moment où le nombre de places maximum est atteint et ce jusqu'au lundi 12h ;
* Envoi du mail de confirmation de participation le lundi à 14h ;
* Envoi du mail de rejet de participation le lundi à 14h ;

Semaine 1 :

* Envoi du mail permettant de s'inscrire pour l'entrainement à venir pour les joueurs sur la liste prioritaire le vendredi à 18h ;
* Envoi du mail permettant de s'inscrire pour l'entrainement à venir le samedi à 18h ;
* Le Google Forms est ouvert de vendredi 18h à lundi 12h pour les joueurs sur la liste prioritaire ;
* Le Google Forms est ouvert de samedi 18h à lundi 12h pour les autres joueurs ;
* Le Google Forms permettant de s'inscrire sur la liste d'attente pour l'entrainement à venir et sur la liste prioritaire pour l'entrainement suivant est ouvert à partir du moment où le nombre de places maximum est atteint et ce jusqu'au lundi 12h ;
* Envoi du mail de confirmation de participation le lundi à 14h ;
* Envoi du mail de rejet de participation le lundi à 14h ;
