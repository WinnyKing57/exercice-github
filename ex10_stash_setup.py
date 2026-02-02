#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Stash : interrompre un travail".

Crée un dossier ex10-stash avec un dépôt Git sur une branche feature-form,
avec des modifications non commitées dans form.html et style.css simulant
un travail en cours.

Auteur : Nicolas NUNGE <nicolas@nicolasnunge.net>
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent
EXERCISE_DIR = ROOT / "ex10-stash"


def build_form_html_base() -> str:
    """Retourne le contenu initial de form.html."""
    return dedent(
        """\
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Formulaire de contact</title>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            <h1>Contactez-nous</h1>
            <form>
                <label for="name">Nom :</label>
                <input type="text" id="name" name="name">

                <label for="email">Email :</label>
                <input type="email" id="email" name="email">

                <button type="submit">Envoyer</button>
            </form>
        </body>
        </html>
        """
    )


def build_form_html_modified() -> str:
    """Retourne le contenu modifié de form.html (travail en cours)."""
    return dedent(
        """\
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Formulaire de contact</title>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            <h1>Contactez-nous</h1>
            <form>
                <label for="name">Nom :</label>
                <input type="text" id="name" name="name" required>

                <label for="email">Email :</label>
                <input type="email" id="email" name="email" required>

                <label for="subject">Sujet :</label>
                <input type="text" id="subject" name="subject">

                <label for="message">Message :</label>
                <textarea id="message" name="message" rows="5"></textarea>

                <!-- TODO: Ajouter la validation côté client -->

                <button type="submit">Envoyer</button>
            </form>
        </body>
        </html>
        """
    )


def build_style_css_base() -> str:
    """Retourne le contenu initial de style.css."""
    return dedent(
        """\
        /* Styles du formulaire */
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 2rem auto;
            padding: 0 1rem;
        }

        h1 {
            color: #333;
        }

        form {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        label {
            font-weight: bold;
        }

        input, button {
            padding: 0.5rem;
            font-size: 1rem;
        }

        button {
            background: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }
        """
    )


def build_style_css_modified() -> str:
    """Retourne le contenu modifié de style.css (travail en cours)."""
    return dedent(
        """\
        /* Styles du formulaire - EN COURS DE REFONTE */
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            max-width: 600px;
            margin: 2rem auto;
            padding: 0 1rem;
            background-color: #f5f5f5;
        }

        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.5rem;
        }

        form {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        label {
            font-weight: bold;
            color: #555;
        }

        input, textarea, button {
            padding: 0.75rem;
            font-size: 1rem;
            border: 1px solid #ddd;
            border-radius: 4px;
        }

        input:focus, textarea:focus {
            outline: none;
            border-color: #3498db;
            /* TODO: Ajouter box-shadow */
        }

        button {
            background: #3498db;
            color: white;
            border: none;
            cursor: pointer;
            transition: background 0.3s;
        }

        button:hover {
            background: #2980b9;
        }
        """
    )


def build_readme_content() -> str:
    """Retourne le contenu du fichier README.md."""
    return dedent(
        """\
        # 📦 Exercice : Utiliser git stash

        ## 🎯 Objectif
        Apprendre à mettre de côté des modifications non terminées pour y revenir plus tard.

        ## 📁 État initial
        - Branche `feature-form` avec un travail EN COURS (non commité)
        - `form.html` : nouveaux champs ajoutés + TODO
        - `style.css` : refonte du design en cours + TODO
        - Ces modifications ne sont PAS prêtes à être commitées

        ## 🎭 Scénario
        Vous êtes en train de développer le formulaire quand on vous demande
        de corriger un bug URGENT sur la branche `main`. Vous devez mettre
        votre travail de côté temporairement !

        ## 📋 Étapes à suivre

        1. **Constater le travail en cours** : Vérifiez l'état du dépôt et les modifications

        2. **Mettre de côté avec stash** : Sauvegardez temporairement votre travail

        3. **Vérifier le résultat** :
           - Le working directory doit être propre
           - Vos fichiers sont revenus à leur état commité

        4. **Simuler un travail urgent** : (Optionnel) Basculez sur main, faites un fix

        5. **Restaurer votre travail** : Récupérez vos modifications mises de côté

        6. **Finaliser** : Terminez le travail et créez un commit

        ## 💡 Astuces
        - `git stash list` pour voir les stashs sauvegardés
        - `git stash show` pour voir le contenu d'un stash
        - Vous pouvez avoir PLUSIEURS stashs (pile LIFO)

        ## 🔑 Concepts clés
        - `git stash` : sauvegarder temporairement
        - `git stash pop` : restaurer et supprimer le stash
        - `git stash apply` : restaurer sans supprimer le stash
        - Pile de stashs pour gérer plusieurs interruptions
        """
    )


def reset_exercise_dir(force: bool) -> None:
    """Crée un répertoire ex10-stash vierge."""
    if EXERCISE_DIR.exists():
        if not force:
            print(
                "⚠️  Le dossier ex10-stash existe déjà.\n"
                "    Utilisez --force pour le recréer (attention : cela supprimera son contenu).",
                file=sys.stderr,
            )
            sys.exit(1)
        shutil.rmtree(EXERCISE_DIR)

    EXERCISE_DIR.mkdir(parents=True, exist_ok=True)


def run_git(*args: str) -> None:
    """Exécute une commande Git dans le répertoire de l'exercice."""
    subprocess.run(
        ["git", *args],
        cwd=EXERCISE_DIR,
        check=True,
        capture_output=True,
    )


def setup_git_repo() -> None:
    """Initialise le dépôt avec un travail en cours non commité."""
    # Écrire les fichiers initiaux
    (EXERCISE_DIR / "README.md").write_text(build_readme_content(), encoding="utf-8")
    (EXERCISE_DIR / "form.html").write_text(build_form_html_base(), encoding="utf-8")
    (EXERCISE_DIR / "style.css").write_text(build_style_css_base(), encoding="utf-8")

    # Initialiser Git et créer le commit initial sur main
    run_git("init", "-b", "main")
    run_git("add", ".")
    run_git("commit", "-m", "Initial commit : formulaire de base")

    # Créer la branche feature-form
    run_git("checkout", "-b", "feature-form")

    # Appliquer les modifications non commitées (travail en cours)
    (EXERCISE_DIR / "form.html").write_text(build_form_html_modified(), encoding="utf-8")
    (EXERCISE_DIR / "style.css").write_text(build_style_css_modified(), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prépare le dossier ex10-stash pour l'exercice git stash."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée ex10-stash si le dossier existe déjà.",
    )
    args = parser.parse_args(argv)

    reset_exercise_dir(force=args.force)
    setup_git_repo()

    print("\n✅ Exercice prêt !")
    print(f"📁 Dossier créé : {EXERCISE_DIR}")
    print("🌿 Branche actuelle : feature-form")
    print("⚡ Travail en cours (non commité) dans form.html et style.css")
    print(
        "\n📚 Consignes :\n"
        "   1. Constatez les changements avec git status\n"
        "   2. Mettez de côté le travail avec git stash\n"
        "   3. Vérifiez que le working directory est propre\n"
        "   4. Restaurez les changements et finalisez avec un commit\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
