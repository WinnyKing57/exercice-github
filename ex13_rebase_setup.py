#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Rebase simple".

Crée un dossier ex13-rebase avec un dépôt Git où main et feature-content
ont divergé. L'étudiant devra utiliser rebase pour aligner feature-content
sur main.

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
EXERCISE_DIR = ROOT / "ex13-rebase"


def build_index_html_base() -> str:
    """Retourne le contenu initial de index.html."""
    return dedent(
        """\
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Mon Blog</title>
        </head>
        <body>
            <h1>Mon Blog</h1>
        </body>
        </html>
        """
    )


def build_index_html_with_nav() -> str:
    """Retourne index.html avec navigation (commit main)."""
    return dedent(
        """\
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Mon Blog</title>
        </head>
        <body>
            <nav>
                <a href="/">Accueil</a>
                <a href="/articles">Articles</a>
            </nav>
            <h1>Mon Blog</h1>
        </body>
        </html>
        """
    )


def build_index_html_with_footer() -> str:
    """Retourne index.html avec footer (commit main après nav)."""
    return dedent(
        """\
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Mon Blog</title>
        </head>
        <body>
            <nav>
                <a href="/">Accueil</a>
                <a href="/articles">Articles</a>
            </nav>
            <h1>Mon Blog</h1>
            <footer>
                <p>© 2025 Mon Blog</p>
            </footer>
        </body>
        </html>
        """
    )


def build_content_md_v1() -> str:
    """Retourne content.md v1 (premier commit feature)."""
    return dedent(
        """\
        # Contenu du site

        ## Article 1 : Introduction à Git
        Git est un système de contrôle de version distribué.
        """
    )


def build_content_md_v2() -> str:
    """Retourne content.md v2 (deuxième commit feature)."""
    return dedent(
        """\
        # Contenu du site

        ## Article 1 : Introduction à Git
        Git est un système de contrôle de version distribué.

        ## Article 2 : Les branches
        Les branches permettent de travailler en parallèle sur différentes fonctionnalités.
        """
    )


def build_readme_content() -> str:
    """Retourne le contenu du fichier README.md."""
    return dedent(
        """\
        # 📐 Exercice : Rebase simple

        ## 🎯 Objectif
        Utiliser `git rebase` pour aligner une branche sur `main` et obtenir un historique linéaire.

        ## 📁 État initial
        ```
        main:           A --- B (nav) --- C (footer)
                         \\
        feature-content:  D (article 1) --- E (article 2)
        ```

        - `main` a avancé de 2 commits (navigation + footer)
        - `feature-content` a 2 commits (articles)
        - Les modifications touchent des fichiers DIFFÉRENTS → pas de conflit

        ## 📋 Étapes à suivre

        1. **Visualiser l'historique** :
           - `git log --oneline --graph --all`
           - Notez la divergence entre les branches

        2. **Se placer sur feature-content** : `git checkout feature-content`

        3. **Rebaser sur main** : `git rebase main`

        4. **Observer le résultat** :
           - `git log --oneline --graph --all`
           - L'historique est maintenant LINÉAIRE !

        ## 📊 Résultat attendu
        ```
        main:           A --- B --- C
                                     \\
        feature-content:              D' --- E'
        ```
        Les commits D et E ont été "rejoués" sur C (nouveaux hashs D' et E').

        ## 💡 Astuces
        - Rebase réécrit l'historique (nouveaux hashs de commit)
        - Ne JAMAIS rebaser des commits déjà poussés sur un dépôt partagé !
        - En cas de conflit, résolvez puis `git rebase --continue`

        ## 🔑 Concepts clés
        - `git rebase <branche>` : rejouer les commits sur une nouvelle base
        - Historique linéaire vs historique avec merges
        - Réécriture d'historique LOCAL uniquement
        """
    )


def reset_exercise_dir(force: bool) -> None:
    """Crée un répertoire ex13-rebase vierge."""
    if EXERCISE_DIR.exists():
        if not force:
            print(
                "⚠️  Le dossier ex13-rebase existe déjà.\n"
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
    """Initialise le dépôt avec des branches divergentes."""
    # Initialiser Git et commit initial
    run_git("init", "-b", "main")
    (EXERCISE_DIR / "README.md").write_text(build_readme_content(), encoding="utf-8")
    (EXERCISE_DIR / "index.html").write_text(build_index_html_base(), encoding="utf-8")
    run_git("add", ".")
    run_git("commit", "-m", "Initial commit")

    # Créer feature-content depuis ce point
    run_git("checkout", "-b", "feature-content")

    # Commits sur feature-content
    (EXERCISE_DIR / "content.md").write_text(build_content_md_v1(), encoding="utf-8")
    run_git("add", "content.md")
    run_git("commit", "-m", "Ajout article 1 : Introduction à Git")

    (EXERCISE_DIR / "content.md").write_text(build_content_md_v2(), encoding="utf-8")
    run_git("add", "content.md")
    run_git("commit", "-m", "Ajout article 2 : Les branches")

    # Revenir sur main et ajouter des commits
    run_git("checkout", "main")

    (EXERCISE_DIR / "index.html").write_text(build_index_html_with_nav(), encoding="utf-8")
    run_git("add", "index.html")
    run_git("commit", "-m", "Ajout de la navigation")

    (EXERCISE_DIR / "index.html").write_text(build_index_html_with_footer(), encoding="utf-8")
    run_git("add", "index.html")
    run_git("commit", "-m", "Ajout du footer")

    # Revenir sur feature-content pour l'exercice
    run_git("checkout", "feature-content")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prépare le dossier ex13-rebase pour l'exercice git rebase."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée ex13-rebase si le dossier existe déjà.",
    )
    args = parser.parse_args(argv)

    reset_exercise_dir(force=args.force)
    setup_git_repo()

    print("\n✅ Exercice prêt !")
    print(f"📁 Dossier créé : {EXERCISE_DIR}")
    print("🌿 Branche actuelle : feature-content (2 commits)")
    print("🌿 Branche main : 2 commits d'avance")
    print("🔧 Les branches ont divergé → prêt pour un rebase")
    print(
        "\n📚 Consignes :\n"
        "   1. Visualisez l'historique des deux branches\n"
        "   2. Depuis feature-content, rebasez sur main\n"
        "   3. Comparez l'historique avant et après\n"
        "   4. Observez l'historique linéaire obtenu\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
