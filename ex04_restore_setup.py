#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Revenir en arrière".

Crée un dossier ex04-restore avec un dépôt Git initialisé, un commit propre,
puis applique des modifications non indexées dans config.yml et README.md.
L'étudiant devra annuler sélectivement certaines modifications.

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
EXERCISE_DIR = ROOT / "ex04-restore"


def build_config_original() -> str:
    """Retourne le contenu original de config.yml."""
    return dedent(
        """\
        # Configuration de l'application
        app:
          name: MonApp
          version: 1.0.0
          debug: false

        database:
          host: localhost
          port: 5432
          name: production_db

        logging:
          level: info
          file: /var/log/app.log
        """
    )


def build_config_modified() -> str:
    """Retourne le contenu modifié de config.yml (modifications à annuler)."""
    return dedent(
        """\
        # Configuration de l'application
        app:
          name: MonApp
          version: 1.0.0
          debug: true  # ERREUR : debug activé en prod !

        database:
          host: localhost
          port: 5432
          name: test_db  # ERREUR : mauvaise base de données !

        logging:
          level: debug
          file: /var/log/app.log
        """
    )


def build_readme_original() -> str:
    """Retourne le contenu original de README.md (projet)."""
    return dedent(
        """\
        # MonApp

        Application de démonstration pour l'exercice Git.

        ## Installation

        1. Cloner le dépôt
        2. Configurer config.yml
        3. Lancer l'application
        """
    )


def build_readme_modified() -> str:
    """Retourne le contenu modifié de README.md (modifications à conserver)."""
    return dedent(
        """\
        # MonApp

        Application de démonstration pour l'exercice Git.

        ## Installation

        1. Cloner le dépôt
        2. Configurer config.yml
        3. Lancer l'application

        ## Nouveautés v1.1

        - Ajout de nouvelles fonctionnalités
        - Amélioration des performances
        """
    )


def build_exercise_readme() -> str:
    """Retourne le contenu du fichier EXERCICE.md."""
    return dedent(
        """\
        # ↩️ Exercice : Annuler des modifications

        ## 🎯 Objectif
        Apprendre à annuler des modifications non indexées de manière sélective.

        ## 📁 État initial
        - Un dépôt Git avec un commit propre
        - Deux fichiers modifiés mais NON ajoutés à l'index :
          - `config.yml` : modifications accidentelles (à annuler ❌)
          - `README.md` : modifications voulues (à conserver ✅)

        ## 📋 Étapes à suivre

        1. **Vérifier l'état du dépôt** : Observez les fichiers modifiés

        2. **Analyser les différences** : Regardez ce qui a changé dans chaque fichier

        3. **Annuler sélectivement** : Restaurez uniquement `config.yml` à sa version commitée

        4. **Vérifier le résultat** :
           - `config.yml` doit être revenu à l'état original
           - `README.md` doit rester modifié

        ## 💡 Astuces
        - Regardez bien les modifications avant de les annuler !
        - La restauration d'un fichier est DÉFINITIVE (les modifications sont perdues)
        - Vous pouvez restaurer un seul fichier sans affecter les autres

        ## 🔑 Concepts clés
        - Restauration partielle de fichiers
        - `git restore` (Git moderne) ou `git checkout -- fichier` (ancienne méthode)
        - Différence entre modifications indexées et non indexées
        """
    )


def reset_exercise_dir(force: bool) -> None:
    """
    Crée un répertoire ex04-restore vierge.

    Si le répertoire existe déjà et que force est False, le script s'arrête
    pour éviter de supprimer le travail de l'étudiant.
    Avec --force, le répertoire est supprimé puis recréé.
    """
    if EXERCISE_DIR.exists():
        if not force:
            print(
                "⚠️  Le dossier ex04-restore existe déjà.\n"
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
    """Initialise le dépôt Git avec un commit propre, puis applique des modifications."""
    # Écrire les fichiers originaux
    (EXERCISE_DIR / "EXERCICE.md").write_text(build_exercise_readme(), encoding="utf-8")
    (EXERCISE_DIR / "config.yml").write_text(build_config_original(), encoding="utf-8")
    (EXERCISE_DIR / "README.md").write_text(build_readme_original(), encoding="utf-8")

    # Initialiser Git et créer le commit initial
    run_git("init")
    run_git("add", ".")
    run_git("commit", "-m", "Initial commit : configuration de base")

    # Appliquer les modifications NON indexées
    (EXERCISE_DIR / "config.yml").write_text(build_config_modified(), encoding="utf-8")
    (EXERCISE_DIR / "README.md").write_text(build_readme_modified(), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Prépare le dossier ex04-restore avec des modifications non indexées."
        )
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée ex04-restore si le dossier existe déjà.",
    )
    args = parser.parse_args(argv)

    reset_exercise_dir(force=args.force)
    setup_git_repo()

    print("\n✅ Exercice prêt !")
    print(f"📁 Dossier créé : {EXERCISE_DIR}")
    print("📄 Fichiers : EXERCICE.md, config.yml, README.md")
    print("🔧 Dépôt Git initialisé avec 1 commit")
    print("⚡ Modifications appliquées (non indexées) dans config.yml et README.md")
    print(
        "\n📚 Consignes :\n"
        "   1. Vérifiez l'état du dépôt\n"
        "   2. Analysez les modifications dans chaque fichier\n"
        "   3. Annulez uniquement les modifications de config.yml\n"
        "   4. Vérifiez que README.md reste modifié\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
