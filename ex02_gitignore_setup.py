#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Suivi de plusieurs fichiers et .gitignore".

Crée un dossier ex02-ignore contenant plusieurs fichiers (index.html, style.css,
notes.txt, secret.txt) sans dépôt Git initialisé. L'étudiant devra créer un
.gitignore pour exclure secret.txt du suivi.

Auteur : Nicolas NUNGE <nicolas@nicolasnunge.net>
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent
EXERCISE_DIR = ROOT / "ex02-ignore"


def build_index_html() -> str:
    """Retourne le contenu du fichier index.html."""
    return dedent(
        """\
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Mon site</title>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            <h1>Bienvenue sur mon site</h1>
            <p>Ceci est un exercice Git.</p>
        </body>
        </html>
        """
    )


def build_style_css() -> str:
    """Retourne le contenu du fichier style.css."""
    return dedent(
        """\
        /* Styles de base */
        body {
            font-family: Arial, sans-serif;
            margin: 2rem;
            background-color: #f5f5f5;
        }

        h1 {
            color: #333;
        }

        p {
            color: #666;
        }
        """
    )


def build_notes_txt() -> str:
    """Retourne le contenu du fichier notes.txt."""
    return dedent(
        """\
        Notes de développement
        ======================

        - Penser à ajouter une navigation
        - Créer une page "À propos"
        - Optimiser les images
        """
    )


def build_secret_txt() -> str:
    """Retourne le contenu du fichier secret.txt (à ignorer)."""
    return dedent(
        """\
        ⚠️ FICHIER CONFIDENTIEL ⚠️

        Ce fichier contient des informations sensibles.
        Il ne doit JAMAIS être versionné dans Git !

        Mot de passe admin : SuperSecret123
        Clé API : sk-1234567890abcdef
        """
    )


def build_readme_content() -> str:
    """Retourne le contenu du fichier README.md."""
    return dedent(
        """\
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
        """
    )


def reset_exercise_dir(force: bool) -> None:
    """
    Crée un répertoire ex02-ignore vierge.

    Si le répertoire existe déjà et que force est False, le script s'arrête
    pour éviter de supprimer le travail de l'étudiant.
    Avec --force, le répertoire est supprimé puis recréé.
    """
    if EXERCISE_DIR.exists():
        if not force:
            print(
                "⚠️  Le dossier ex02-ignore existe déjà.\n"
                "    Utilisez --force pour le recréer (attention : cela supprimera son contenu).",
                file=sys.stderr,
            )
            sys.exit(1)
        shutil.rmtree(EXERCISE_DIR)

    EXERCISE_DIR.mkdir(parents=True, exist_ok=True)


def write_files() -> None:
    """Écrit tous les fichiers de l'exercice."""
    files = {
        "README.md": build_readme_content(),
        "index.html": build_index_html(),
        "style.css": build_style_css(),
        "notes.txt": build_notes_txt(),
        "secret.txt": build_secret_txt(),
    }

    for filename, content in files.items():
        file_path = EXERCISE_DIR / filename
        file_path.write_text(content, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Prépare le dossier ex02-ignore avec plusieurs fichiers pour l'exercice .gitignore."
        )
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée ex02-ignore si le dossier existe déjà.",
    )
    args = parser.parse_args(argv)

    reset_exercise_dir(force=args.force)
    write_files()

    print("\n✅ Exercice prêt !")
    print(f"📁 Dossier créé : {EXERCISE_DIR}")
    print("📄 Fichiers générés : README.md, index.html, style.css, notes.txt, secret.txt")
    print(
        "\n📚 Consignes :\n"
        "   1. Entrez dans le dossier ex02-ignore\n"
        "   2. Initialisez un nouveau dépôt Git\n"
        "   3. Créez un fichier .gitignore pour ignorer secret.txt\n"
        "   4. Ajoutez tous les fichiers suivis au staging\n"
        "   5. Créez un commit avec un message descriptif\n"
        "   6. Vérifiez que secret.txt n'est pas versionné\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
