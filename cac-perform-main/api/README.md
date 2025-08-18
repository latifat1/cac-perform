# 📘 Guide d'installation Backend

Ce dossier contient le code source du backend de l’outil CAC-Perform. Il constitue l’API qui gère la logique métier, les accès aux données, ainsi que la communication avec le frontend.

## ⚙️ Étapes d’installation

### 1. 🧪 Création d'un ennvironnement virtuel Python

Afin d’isoler les dépendances du projet et éviter les conflits avec d’autres environnements Python présents sur votre machine, il est recommandé de créer un environnement virtuel dédié.

Depuis le dossier ``api``, exécutez :

```sh
python -m venv virtualenv
```

#### **➤ Activation de l’environnement virtuel**

* **Sous Windows :**

```sh
.\virtualenv\Scripts\activate
```

* **Sous Linux / macOS :**

```sh
source virtualenv/bin/activate
```

#### **➤ Désactivation**

Lorsque vous avez terminé, vous pouvez quitter l’environnement virtuel avec :

```sh
deactivate
```

> ⚠️ **Important :** Le nom de l’environnement virtuel doit être exactement ``virtualenv`` afin d’être automatiquement exclu par Git via le ``.gitignore``.

### 2. 📦 Installation des dépendances Python

Une fois l’environnement virtuel activé, installez les bibliothèques nécessaires au projet avec :

```sh
pip install -r requirements.txt
```

Cette commande installera toutes les dépendances listées, assurant ainsi le bon fonctionnement du backend.

### 3. 🚀 Lancement du serveur (mode développement)

Pour démarrer le serveur backend en mode développement :

```sh
python app.py
```

Le serveur sera accessible à l’adresse suivante : <http://localhost:5000>.

Il interagit avec la base de données MongoDB et communique avec le frontend via des routes API REST.

## 📝 Remarques

* Assurez-vous que **MongoDB** est bien installé et en cours d’exécution sur ``localhost:27017``.

## 🤝 Besoin d’aide ?

Pour toute question ou problème lié au backend, vous pouvez contacter :

**Axel Hamilton AHOUMOUAN - <axelhamilton02@gmail.com>**
