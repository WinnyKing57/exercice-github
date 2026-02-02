# 🔒 Exercice : Gérer .gitignore

## 🎯 Objectif
Apprendre à gérer plusieurs fichiers et à ignorer certains fichiers sensibles avec `.gitignore`.

## 📁 Fichiers présents
- `index.html` — Page HTML principale
- `style.css` — Feuille de styles
- `notes.txt` — Notes de développement
- `secret.txt` — ⚠️ Fichier confidentiel à NE PAS versionner !

## 📋 Étapes à suivre

1. **Initialiser le dépôt** : Créez un nouveau dépôt Git
2. **Vérifier l'état** : Observez quels fichiers sont détectés (4 fichiers non suivis)
3. **Créer .gitignore** : Créez un fichier `.gitignore` pour exclure `secret.txt`
4. **Vérifier à nouveau** : `secret.txt` ne doit plus apparaître dans les fichiers non suivis
5. **Ajouter tous les fichiers** : Ajoutez tous les fichiers en une seule commande
6. **Créer le commit** : Commitez avec un message descriptif
7. **Vérifier le résultat** : Consultez l'historique et assurez-vous que `secret.txt` n'est pas inclus

## 💡 Astuces
- Le fichier `.gitignore` doit lui-même être versionné !
- Utilisez `git status` régulièrement pour voir l'effet de vos actions
- Pour ajouter tous les fichiers d'un coup : cherchez la bonne option de `git add`

## 🔑 Concepts clés
- `.gitignore` : fichier listant les patterns à ignorer
- Ajout en masse avec `git add`
- Contrôle de ce qui est versionné
