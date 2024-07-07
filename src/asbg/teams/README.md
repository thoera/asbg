# Tirage des équipes d'Interclubs

## Objectif

Le nombre de joueurs souhaitant participer aux Interclubs étant généralement supérieur aux nombre de places disponibles, cet outil permet d'assister les reponsables de compétition du CA et les capitaines des équipes dans la constitution de celles-ci.

## Algorithme de sélection

La sélection des joueurs se fait sur plusieurs critères renseignés lors de l'inscrition des adhérents pour la nouvelle saison.

Le premier critère est le choix de se déclarer intéressé par participer aux Interclubs.
Les joueurs ayant répondu positivement rentrent dans la suite du processus de sélection qui prend en compte les critères suivants :

* le genre (la sélection doit se faire par genre pour assurer l'équilibre nécessaire entre joueuses et joueurs dans les équipes mixtes) ;
* le classement (information récupérée via Poona pour chaque adhérent) ;
* des critères spécifiques, sportifs ou non, comme : l'assiduité aux entrainements, la participation à des tournoix fédéraux, la participation à des tournois non fédéraux ou encore la participation à la vie du club.

Tout adhérent va déclarer lors de sa réinscrinption sa propre note pour chacun des critères spécifiques qui auront été retenus.
De plus, un poids est également attribué aux différents critères permettant ainsi de calculer un score pondéré pour l'ensemble des adhérents désireux de participer aux Interclubs.

L'algorithme produit deux sorties :

* Un tri des adhérents par genre en fonction de leur classement en départageant les personnes de même classement par le score pondéré calculé grâce aux critères spécifiques ;
* Des propositions d'équipes en affectant les joueurs selon la répartition entre équipes mixtes et équipes masculines souhaitée (par exemple, deux équipes mixtes et deux équipes masculines ou bien trois équipes mixtes et une équipe masculine).

Les propositions d'équipes sont faites, par défaut, sur la base suivante :

* Équipe mixte : cinq joueuses et huit joueurs ;
* Équipe masculine : dix joueurs.

Pour pouvoir expérimenter avec différentes compositions, les paramètres configurables dans l'algorithme sont :

* les critères spécifiques à prendre en compte dans le calcul du score ;
* le poids de chacun de ces critères ;
* le nombre d'équipes mixtes et d'équipes masculines ;
* le nombre de joueuses et joueurs dans les équipes mixtes et masculines.

Chaque critère peut être composé de différents sous-critères permettant ainsi un regroupement logique de ceux-ci. Tout comme un poids est donné à chacun des critères, un poids est également accordé à chacun des sous-critères.

Les deux règles suivantes doivent être respectées :

* la somme des poids de l'ensemble des critères doit faire 1 ;
* la somme des sous-critères de chacun des critères doit également faire 1.

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

Un exemple de fichier est fourni (`asbg/teams/data/example-rankings.csv`) ou peut être généré avec la commande :

```sh
asbg teams generate-players-rankings
```

## Contrat d'interface pour les critères spécifiques

Les critères spécifiques sont attendus sous la forme d'un fichier "csv" respectant le contrat d'interface suivant :

* délimiteur ";"
* les champs suivants sont obligatoires : "licence", "genre" et "participation"
* tout critère paramétré dans le processus de sélection de l'algorithme doit être présent dans le fichier "csv"

Un exemple de fichier est fourni (`asbg/teams/data/example-criteria-wide.csv`) ou peut être généré avec les commandes suivantes :

```sh
asbg teams generate-players-criteria
asbg teams reshape-criteria
```

Le paramétrage des critères à prendre en compte et leur poids respectif se fait via le fichier de configuration "teams.yaml".
