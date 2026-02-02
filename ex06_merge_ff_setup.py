#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Merge fast-forward".

Crée un dossier ex06-merge-ff avec un dépôt Git contenant une branche main
et une branche feature-footer avec un commit supplémentaire. La branche main
n'a pas évolué, permettant un merge fast-forward.

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
EXERCISE_DIR = ROOT / "ex06-merge-ff"


def build_index_html_base() -> str:
    """Retourne le contenu initial de index.html."""
    return dedent(
        """\
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Mon site</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 2rem; }
                main { max-width: 800px; margin: 0 auto; }
            </style>
        </head>
        <body>
            <main>
                <h1>Bienvenue sur mon site</h1>
                <p>Contenu principal de la page.</p>
            </main>
        </body>
        </html>
        """
    )


def build_index_html_with_footer() -> str:
    """Retourne le contenu de index.html avec le footer ajouté."""
    return dedent(
        """\
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Mon site</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 2rem; }
                main { max-width: 800px; margin: 0 auto; }
                footer { margin-top: 3rem; padding: 1rem; background: #333; color: white; text-align: center; }
            </style>
        </head>
        <body>
            <main>
                <h1>Bienvenue sur mon site</h1>
                <p>Contenu principal de la page.</p>
            </main>
            <footer>
                <p>&copy; 2025 Mon Site. Tous droits réservés.</p>
            </footer>
        </body>
        </html>
        """
    )


def build_readme_content() -> str:
    """Retourne le contenu du fichier README.md."""
    return dedent(
        """\
        # ⚡ Exercice : Merge fast-forward

        ## 🎯 Objectif
        Comprendre le merge fast-forward, le cas le plus simple de fusion.

        ## 📁 État initial
        - Branche `main` avec un commit initial
        - Branche `feature-footer` avec un commit supplémentaire (ajout d'un footer)
        - `main` n'a PAS de nouveaux commits depuis la création de `feature-footer`

        ## 📋 Étapes à suivre

        1. **Observer l'état initial** :
           - Listez les branches
           - Consultez l'historique de chaque branche

        2. **Se placer sur main** : Assurez-vous d'être sur la branche `main`

        3. **Fusionner feature-footer** : Intégrez la branche `feature-footer` dans `main`

        4. **Observer le résultat** :
           - Consultez l'historique après le merge
           - Notez qu'il n'y a PAS de commit de merge supplémentaire

        ## 💡 Astuces
        - Un merge fast-forward se produit quand la branche cible n'a pas divergé
        - Git "avance" simplement le pointeur de la branche
        - L'historique reste linéaire

        ## 🔑 Concepts clés
        - **Fast-forward** : avance rapide du pointeur de branche
        - Pas de commit de merge créé
        - Historique linéaire conservé
        """
    )


def reset_exercise_dir(force: bool) -> None:
    """Crée un répertoire ex06-merge-ff vierge."""
    if EXERCISE_DIR.exists():
        if not force:
            print(
                "⚠️  Le dossier ex06-merge-ff existe déjà.\n"
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
    """Initialise le dépôt avec main et feature-footer."""
    # Écrire les fichiers initiaux
    (EXERCISE_DIR / "README.md").write_text(build_readme_content(), encoding="utf-8")
    (EXERCISE_DIR / "index.html").write_text(build_index_html_base(), encoding="utf-8")

    # Initialiser Git et créer le commit initial sur main
    run_git("init", "-b", "main")
    run_git("add", ".")
    run_git("commit", "-m", "Initial commit : page de base")

    # Créer la branche feature-footer et ajouter un commit
    run_git("checkout", "-b", "feature-footer")
    (EXERCISE_DIR / "index.html").write_text(build_index_html_with_footer(), encoding="utf-8")
    run_git("add", "index.html")
    run_git("commit", "-m", "Ajout du footer")

    # Revenir sur main (sans nouveaux commits)
    run_git("checkout", "main")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prépare le dossier ex06-merge-ff pour l'exercice merge fast-forward."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée ex06-merge-ff si le dossier existe déjà.",
    )
    args = parser.parse_args(argv)

    reset_exercise_dir(force=args.force)
    setup_git_repo()

    print("\n✅ Exercice prêt !")
    print(f"📁 Dossier créé : {EXERCISE_DIR}")
    print("🌿 Branches : main (actuelle), feature-footer (1 commit d'avance)")
    print("🔧 Dépôt prêt pour un merge fast-forward")
    print(
        "\n📚 Consignes :\n"
        "   1. Observez l'historique des deux branches\n"
        "   2. Placez-vous sur main\n"
        "   3. Fusionnez feature-footer dans main\n"
        "   4. Observez l'historique après le merge\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
