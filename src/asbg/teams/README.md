# Équipes

## Objectif

Le nombre de joueurs souhaitant participer aux Interclubs étant généralement supérieur aux nombre de places disponibles, cet outil permet d'assister les reponsables de compétition et capitaines dans la constitution des équipes.

## Algorithme de sélection

La sélection des joueurs se fait sur plusieurs critères renseignés lors de l'inscrition des adhérents pour la nouvelle saison.

Le premier critère est le choix de se déclarer intéressé par participer aux Interclubs. Tout joueur ayant répondu "Non" à cette question est immédiatement exclu de la suite du processus de sélection.

Les joueurs ayant répondu positivement rentrent dans la suite du processus. Celui-ci prend en compte les critères suivants :

* le genre (la sélection doit se faire par genre pour assurer l'équilibre nécessaire entre joueuses et joueurs dans les équipes mixtes) ;
* le classement (information récupérée via Poona pour chaque adhérent) ;
* des critères spécifiques comme l'assiduité aux entrainements, la participation à des tournoix fédéraux, la participation à des tournois non fédéraux ou encore la participation à la vie du club permettant de calculer pour chaque adhérent un score.

L'algorithme produit deux sorties :

* Un tri des adhérents par genre en fonction de leur classement en départageant les personnes de même classement par la note de score calculée grâce aux critères spécifiques ;
* Des propositions d'équipes en affectant les joueurs selon la répartition entre équipes mixtes et équipes masculines souhaitée (par exemple, deux équipes mixtes et deux équipes masculines ou bien trois équipes mixtes et une équipe masculine).

Les propositions d'équipes sont faites, par défaut, sur la base suivante :

* Équipe mixte : quatre joueuses et cinq joueurs ;
* Équipe masculine : huit joueurs.

Plusieurs paramètres sont configurables dans l'algorithme :

* les critères spécifiques à prendre en compte dans le calcul du score ;
* le poids de chacun de ces critères ;
* le nombre d'équipes mixtes et d'équipes masculines ;
* le nombre de joueuses et joueurs dans les équipes mixtes et masculines.

## Contrat d'interface pour le classement

Le classement de chaque adhérent est attendu sous la forme d'un fichier "csv" respectant le contrat d'interface suivant :

* délimiteur ";"
* les champs suivants sont obligatoires : "licence", "nom", "prenom", "simple", "double" et "mixte"

Le classement est celui utilisé par la Fédération Française de Badminton :

* NC
* P12
* P11
* P10
* D9
* D8
* D7
* R6
* R5
* R4
* N3
* N2
* N1

Le fichier peut être exporté depuis https://poona.ffbad.org/.

Un exemple de fichier fictif est fourni (`asbg/teams/data/example-rankings.csv`) ou peut être généré avec la commande :

```sh
asbg teams generate-players-rankings
```

## Contrat d'interface pour les critères spécifiques

Les critères spécifiques sont attendus sous la forme d'un fichier "csv" respectant le contrat d'interface suivant :

* délimiteur ";"
* les champs suivants sont obligatoires : "licence", "nom" et "prenom"
* tout critère paramétré dans le processus de sélection de l'algorithme doit être présent dans le fichier "csv"

Le paramétrage des critères à prendre en compte et leur poids respectif se fait via le fichier de configuration "teams.yaml".
