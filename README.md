# ASBG

Ce repository est composé de différents utilitaires dédiés au fonctionnement du club de l'[ASBG](https://www.asbg75.com/).

Il est ainsi possible de visualiser les résultats des différentes équipes lors des Interclubs ou bien de gérer le système de réservation des entrainements.

## Installation

Il est nécessaire de disposer de Python (>= 3.10) sur son système d'exploitation.

Clonez le package dans un répertoire :

```sh
git clone git@github.com:thoera/asbg.git
cd asbg
```

Créez et activez un environnement virtuel avec les commandes suivantes :

```sh
python3 -m venv venv
. venv/bin/activate
```

Créez l'archive installable par `pip` :

```sh
pip install --upgrade build
python -m build
```

Un répertoire `dist/` devrait être créé avec deux fichiers :

- `asbg-<version>.tar.gz`
- `asbg-<version>-py3-none-any.whl`

Où `<version>` est le numéro de version du package (défini dans le fichier `pyproject.toml`).

Installez le package avec la commande suivante :

```sh
pip install dist/asbg-<version>-py3-none-any.whl
```

### En mode "développement"

Plutôt que de `build` et `install`, une fois votre environnement virtuel actif, vous pouvez simplement utiliser la commande suivante pour installer le package en mode "développement" ou "éditable" :

```sh
pip install -e .
```

## Utilisation

L'utilisation du package se fait via une `CLI`. La commande suivante offre une vue globale des différentes sous-commandes existantes.

```sh
asbg
```

Il est toujours possible d'ajouter l'argument `--help` pour obtenir une description des commandes et des options possibles.

# Résultats des joueuses et joueurs de l'ASBG lors des Interclubs

Il est utile de mettre à jour régulièrement la base de données des résultats avec la commande :

```sh
asbg interclubs fetch
```

Les résultats peuvent être visualiser de manière textuelle dans un terminal avec la commande suivante :

```sh
asbg interclubs show
```

L'option `--competition` permet de filtrer les résultats si besoin.

La commande ci-dessous permet de visualiser les résultats des Interclubs dans votre navigateur de façon plus graphique :

```sh
asbg interclubs dashboard
```
