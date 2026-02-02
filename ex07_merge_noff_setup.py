#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Merge avec commit de fusion".

Crée un dossier ex07-merge-noff avec un dépôt Git où main et feature-cta
ont divergé (chacune a un commit après leur séparation). Les modifications
touchent des parties différentes du fichier, donc pas de conflit.

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
EXERCISE_DIR = ROOT / "ex07-merge-noff"


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
                .cta { padding: 1rem 2rem; background: #007bff; color: white; border: none; cursor: pointer; }
            </style>
        </head>
        <body>
            <header>
                <h1>Mon Site Web</h1>
            </header>
            <main>
                <p>Bienvenue sur notre site.</p>
            </main>
            <footer>
                <p>Contact : email@example.com</p>
            </footer>
        </body>
        </html>
        """
    )


def build_index_html_main_update() -> str:
    """Retourne le contenu de index.html après modification sur main (footer amélioré)."""
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
                .cta { padding: 1rem 2rem; background: #007bff; color: white; border: none; cursor: pointer; }
            </style>
        </head>
        <body>
            <header>
                <h1>Mon Site Web</h1>
            </header>
            <main>
                <p>Bienvenue sur notre site.</p>
            </main>
            <footer>
                <p>Contact : email@example.com</p>
                <p>&copy; 2025 Mon Site - Tous droits réservés</p>
            </footer>
        </body>
        </html>
        """
    )


def build_index_html_feature_cta() -> str:
    """Retourne le contenu de index.html sur feature-cta (bouton CTA ajouté)."""
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
                .cta { padding: 1rem 2rem; background: #007bff; color: white; border: none; cursor: pointer; }
            </style>
        </head>
        <body>
            <header>
                <h1>Mon Site Web</h1>
            </header>
            <main>
                <p>Bienvenue sur notre site.</p>
                <button class="cta">Découvrir nos services</button>
            </main>
            <footer>
                <p>Contact : email@example.com</p>
            </footer>
        </body>
        </html>
        """
    )


def build_readme_content() -> str:
    """Retourne le contenu du fichier README.md."""
    return dedent(
        """\
        # 🔀 Exercice : Merge avec commit de fusion

        ## 🎯 Objectif
        Comprendre le merge non fast-forward avec création d'un commit de merge explicite.

        ## 📁 État initial
        - Branche `main` avec un commit ajouté APRÈS la création de `feature-cta`
        - Branche `feature-cta` avec un commit ajoutant un bouton CTA
        - Les modifications touchent des parties DIFFÉRENTES de `index.html` → pas de conflit

        ## 📊 Visualisation
        ```
        main:        A --- B (footer amélioré)
                      \\
        feature-cta:   C (bouton CTA ajouté)
        ```

        ## 📋 Étapes à suivre

        1. **Inspecter l'historique** :
           - Consultez l'historique de `main`
           - Consultez l'historique de `feature-cta`
           - Notez que les deux branches ont divergé

        2. **Depuis main, fusionner feature-cta** : Effectuez le merge

        3. **Examiner le commit de merge** :
           - Un nouveau commit de merge a été créé automatiquement
           - Il a DEUX parents (les deux branches fusionnées)

        4. **Vérifier le contenu final** : `index.html` doit contenir les deux modifications

        ## 💡 Astuces
        - Utilisez `git log --oneline --graph` pour visualiser l'historique
        - Le commit de merge montre les deux parents avec `git log`
        - Vous pouvez personnaliser le message de merge

        ## 🔑 Concepts clés
        - **Merge non fast-forward** : création d'un commit de fusion
        - Les deux historiques sont préservés
        - Git fusionne automatiquement les modifications non conflictuelles
        """
    )


def reset_exercise_dir(force: bool) -> None:
    """Crée un répertoire ex07-merge-noff vierge."""
    if EXERCISE_DIR.exists():
        if not force:
            print(
                "⚠️  Le dossier ex07-merge-noff existe déjà.\n"
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
    # Écrire les fichiers initiaux
    (EXERCISE_DIR / "README.md").write_text(build_readme_content(), encoding="utf-8")
    (EXERCISE_DIR / "index.html").write_text(build_index_html_base(), encoding="utf-8")

    # Initialiser Git et créer le commit initial sur main
    run_git("init", "-b", "main")
    run_git("add", ".")
    run_git("commit", "-m", "Initial commit : structure de base")

    # Créer la branche feature-cta et ajouter le bouton CTA
    run_git("checkout", "-b", "feature-cta")
    (EXERCISE_DIR / "index.html").write_text(build_index_html_feature_cta(), encoding="utf-8")
    run_git("add", "index.html")
    run_git("commit", "-m", "Ajout du bouton Call-to-Action")

    # Revenir sur main et ajouter un commit (footer amélioré)
    run_git("checkout", "main")
    (EXERCISE_DIR / "index.html").write_text(build_index_html_main_update(), encoding="utf-8")
    run_git("add", "index.html")
    run_git("commit", "-m", "Amélioration du footer avec copyright")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prépare le dossier ex07-merge-noff pour l'exercice merge avec commit de fusion."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée ex07-merge-noff si le dossier existe déjà.",
    )
    args = parser.parse_args(argv)

    reset_exercise_dir(force=args.force)
    setup_git_repo()

    print("\n✅ Exercice prêt !")
    print(f"📁 Dossier créé : {EXERCISE_DIR}")
    print("🌿 Branches : main (actuelle, 2 commits), feature-cta (divergée, 2 commits)")
    print("🔧 Les branches ont divergé → merge créera un commit de fusion")
    print(
        "\n📚 Consignes :\n"
        "   1. Inspectez l'historique des deux branches\n"
        "   2. Depuis main, fusionnez feature-cta\n"
        "   3. Examinez le commit de merge créé\n"
        "   4. Vérifiez le contenu final de index.html\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
