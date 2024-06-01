# Entrainements

## Objectif

Le nombre de joueurs souhaitant participer à l'entrainement étant parfois supérieur au nombre de places disponibles, il est souhaitable d'automatiser au maximum le processus de sélection avec des règles précises.

## Algorithme de sélection

Le processus de sélection passe par l'envoi de formulaires Google Forms pour chaque entrainement.

Ce formulaire (que l'on apelle `F1` pour celui pour le prochain entrainement) est simple, il ne permet de s'inscrire qu'à l'entrainement de la semaine à venir et est ouvert du samedi au lundi (12h).

Une fois le nombre de places atteint, `F1` renvoie les joueurs qui souhaitaient s'inscrire pour l'entrainement vers un nouveau formulaire `F2'`.

Ce formulaire `F2'` comprend deux questions :

* Souhaites-tu t'inscrire sur la liste d'attente pour l'entrainement à venir ?
* Souhaites-tu t'inscrire sur la liste prioritaire pour l'entrainement de la semaine suivante ?

La période d'ouverture du formulaire `F2'` est la même que celle de `F1`. Il n'est donc pas possible d'anticiper l'inscription pour le prochain entrainement.
Les joueurs s'inscrivant sur la liste prioritaire devront confirmer leur participation dans le formulaire envoyer le samedi suivant.

Les données en entrée de l'algorithme sont les suivantes :

* La liste des inscrits pour l'entrainement ;
* Les joueurs sélectionnés lors du dernier entrainement ;
* La liste des inscrits sur liste prioritaire pour l'entrainement de la semaine à venir ;
* La liste des inscrits sur liste d'attente pour l'entrainement de la semaine suivante.

Algorithme de sélection :

* On sélectionne d'abord les joueurs inscrits sur la liste prioritaire pour l'entrainement à venir et inscrits via le formulaire `F1` ;
* On complète par les joueurs inscrits via `F1` qui n'ont pas participé au dernier entrainement ;
* S'il reste des places disponibles, on complète :
    * Par les joueurs inscrits sur la liste d'attente qui n'ont pas participé au dernier entrainement ;
    * Puis par les joueurs inscrits via `F1` qui ont participé au dernier entrainement ;
    * Puis par les joueurs inscrits sur liste d'attente qui ont participé au dernier entrainement.

Les joueurs inscrits via `F1` et qui n'ont pas pu être sélectionnés sont automatiquement placés sur la liste prioritaire pour l'entrainement suivant.

En cas d'arbitrage à faire entre deux joueurs qui se retrouvent dans les mêmes conditions pour une place, on applique la règle du "premier arrivé, premier servi".
