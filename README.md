# API LANGUAGE LOCAL (Langlocal)

C'est notre api Language qui gère le **speech to text**, le **text to speech** en fon,yoruba,français
## Installation

### Pré-requis

- Installer un environnement virtuel Python :

```bash
python -m venv env
source env/bin/activate  # Pour Linux/MacOS
env\Scripts\activate  # Pour Windows
```


### Dépendances

- Installer les dépendances du projet avec la commande suivante :

```bash
pip install -r requirements.txt
```

### Lancer le serveur

- Pour lancer le serveur, utilisez la commande suivante :

```bash
uvicorn main:app --host 0.0.0.0 --port 9500
```

Vous pouvez ensuite accéder à la documentation en utilisant votre navigateur web à l'adresse suivante : `http://127.0.0.1:9500`.
