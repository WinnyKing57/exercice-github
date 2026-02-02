#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Créer et basculer sur une branche".

Crée un dossier ex05-branch avec un dépôt Git initialisé contenant un commit
avec index.html. L'étudiant devra créer une branche, la modifier, puis
comparer avec main.

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
EXERCISE_DIR = ROOT / "ex05-branch"


def build_index_html() -> str:
    """Retourne le contenu initial de index.html."""
    return dedent(
        """\
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Ma page</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 2rem;
                    background-color: #f0f0f0;
                }
                main {
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 2rem;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
            </style>
        </head>
        <body>
            <main>
                <h1>Bienvenue</h1>
                <p>Ceci est le contenu principal de ma page.</p>
                <p>Cette page va évoluer grâce aux branches Git !</p>
            </main>
        </body>
        </html>
        """
    )


def build_readme_content() -> str:
    """Retourne le contenu du fichier README.md."""
    return dedent(
        """\
        # 🌿 Exercice : Travailler avec les branches

        ## 🎯 Objectif
        Comprendre la notion de branche et le travail isolé sur une fonctionnalité.

        ## 📁 État initial
        - Un dépôt Git initialisé sur la branche `main`
        - Un commit contenant `index.html`

        ## 📋 Étapes à suivre

        1. **Créer une branche** : Créez une nouvelle branche nommée `feature-header`

        2. **Basculer sur la branche** : Passez sur la branche `feature-header`

        3. **Modifier index.html** : Ajoutez un en-tête (header) à la page, par exemple :
           ```html
           <header>
               <nav>
                   <a href="#">Accueil</a>
                   <a href="#">À propos</a>
                   <a href="#">Contact</a>
               </nav>
           </header>
           ```

        4. **Commiter la modification** : Créez un commit sur la branche `feature-header`

        5. **Revenir sur main** : Basculez sur la branche `main`

        6. **Constater la différence** : Ouvrez `index.html` et observez que le header n'y est pas !

        ## 💡 Astuces
        - Utilisez `git branch` pour lister les branches
        - L'astérisque (*) indique la branche courante
        - Vous pouvez créer ET basculer en une seule commande !

        ## 🔑 Concepts clés
        - `git branch` : créer/lister des branches
        - `git switch` (moderne) ou `git checkout` (classique) : basculer
        - Travail parallèle : chaque branche a son propre historique
        - Les modifications sur une branche n'affectent pas les autres
        """
    )


def reset_exercise_dir(force: bool) -> None:
    """
    Crée un répertoire ex05-branch vierge.

    Si le répertoire existe déjà et que force est False, le script s'arrête
    pour éviter de supprimer le travail de l'étudiant.
    Avec --force, le répertoire est supprimé puis recréé.
    """
    if EXERCISE_DIR.exists():
        if not force:
            print(
                "⚠️  Le dossier ex05-branch existe déjà.\n"
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
    """Initialise le dépôt Git avec un premier commit sur main."""
    # Écrire les fichiers
    (EXERCISE_DIR / "README.md").write_text(build_readme_content(), encoding="utf-8")
    (EXERCISE_DIR / "index.html").write_text(build_index_html(), encoding="utf-8")

    # Initialiser Git et créer le premier commit
    run_git("init", "-b", "main")
    run_git("add", ".")
    run_git("commit", "-m", "Initial commit : page de base")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Prépare le dossier ex05-branch avec un dépôt Git pour l'exercice branches."
        )
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée ex05-branch si le dossier existe déjà.",
    )
    args = parser.parse_args(argv)

    reset_exercise_dir(force=args.force)
    setup_git_repo()

    print("\n✅ Exercice prêt !")
    print(f"📁 Dossier créé : {EXERCISE_DIR}")
    print("📄 Fichiers : README.md, index.html (déjà commités)")
    print("🔧 Dépôt Git initialisé sur la branche main avec 1 commit")
    print(
        "\n📚 Consignes :\n"
        "   1. Créez une branche feature-header\n"
        "   2. Basculez sur cette branche\n"
        "   3. Ajoutez un en-tête dans index.html\n"
        "   4. Commitez la modification\n"
        "   5. Revenez sur main et constatez la différence\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
