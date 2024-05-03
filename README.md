# Résultats des joueuses et joueurs de l'ASBG

Cette application écrite en Python permet de visualiser les résultats des joueurs de l'ASBG en Interclubs.

## Prérequis

Il est nécessaire de disposer de Python (>= 3.10) sur son système d'exploitation.

## Installation

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

### Installation

Créez l'archive installable par `pip` :

```sh
pip install --upgrade build
python -m build
```

Un répertoire `dist/` devrait être créé avec deux fichiers :

- asbg-<version>.tar.gz
- asbg-<version>-py3-none-any.whl

Où <version> est le numéro de version du package (défini dans le fichier `pyproject.toml`).

Installer le package `asbg` :

```sh
pip install dist/asbg-<version>-py3-none-any.whl
```

### En mode "développement"

Plutôt que de `build` et `install`, une fois votre environnement virtuel actif, vous pouvez simplement utiliser la commande :

```sh
pip install -e .
```

## Utilisation

L'utilisation du package se fait via une `CLI`.

Il est possible de mettre à jour la base de données des résultats des Interclubs avec la commande :

```sh
asbg interclubs fetch
```

La commande ci-dessous permet de visualiser les résultats dans votre navigateur :

```sh
asbg dashboard
```
