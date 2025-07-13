# Déploiement du bot sur PythonAnywhere

Suivez ces étapes pour héberger votre bot sur PythonAnywhere :

## 1. Créer un compte

1. Inscrivez-vous sur https://www.pythonanywhere.com/.
2. Connectez-vous à votre espace personnel.

## 2. Importer votre code depuis Git

1. Assurez-vous d'avoir poussé votre code sur GitHub (ou un autre service Git) et copiez l'URL du dépôt.
2. Dans une **Bash console** de PythonAnywhere, clonez le dépôt :

```bash
git clone https://github.com/<votre-utilisateur>/<votre-repo>.git botTelegram
```

## 3. Créer et activer un environnement virtuel (facultatif mais recommandé)

Ouvrez une **Bash console** sur PythonAnywhere et exécutez :

```bash
mkvirtualenv guide-etude-bot --python=python3.12
workon guide-etude-bot
```

> Si `mkvirtualenv` n’est pas disponible, installez `virtualenv` : `pip install --user virtualenv virtualenvwrapper`.

## 4. Installer les dépendances

Toujours dans la console :

```bash
cd ~/botTelegram
pip install -r requirements.txt
```

## 5. Configurer la variable d’environnement

1. Dans l’onglet **Account** > **Environment Variables** de PythonAnywhere.
2. Ajoutez une variable `TELEGRAM_TOKEN` avec la valeur de votre token.

## 6. Démarrer le bot en tâche "Always-on"

1. Allez dans l’onglet **Tasks** > **Always-on tasks**.
2. Cliquez sur **Create a new task**.
3. En commande, saisissez :

```bash
workon guide-etude-bot && python ~/botTelegram/bot.py
```

4. Sauvegardez. Le bot sera lancé automatiquement et redémarré en cas d’arrêt.

---

Votre bot est maintenant en ligne en continu sur PythonAnywhere ! 🚀
