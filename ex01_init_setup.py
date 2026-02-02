#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Initialiser un dépôt".

Crée un dossier ex01-init contenant un fichier README.md non versionné,
permettant à l'étudiant de s'exercer aux commandes git init, git status,
git add, git commit et git log.

Auteur : Nicolas NUNGE <nicolas@nicolasnunge.net>
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent
EXERCISE_DIR = ROOT / "ex01-init"
README_PATH = EXERCISE_DIR / "README.md"


def build_readme_content() -> str:
    """Retourne le contenu initial du fichier README.md."""
    return dedent(
        """\
        # 🚀 Exercice : Mon premier commit

        ## 🎯 Objectif
        Initialiser un dépôt Git, suivre le fichier README.md et créer votre premier commit.

        ## 📋 Étapes à suivre

        1. **Initialiser le dépôt** : `git init`
        2. **Vérifier l'état** : `git status` (README.md doit apparaître en rouge)
        3. **Ajouter le fichier** : `git add README.md`
        4. **Créer le commit** : `git commit -m "Mon premier commit"`
        5. **Consulter l'historique** : `git log`

        💡 **Astuce** : Utilisez `git status` après chaque commande pour observer les changements !
        """
    )


def reset_exercise_dir(force: bool) -> None:
    """
    Crée un répertoire ex01-init vierge.

    Si le répertoire existe déjà et que force est False, le script s'arrête
    pour éviter de supprimer le travail de l'étudiant.
    Avec --force, le répertoire est supprimé puis recréé.
    """
    if EXERCISE_DIR.exists():
        if not force:
            print(
                "⚠️  Le dossier ex01-init existe déjà.\n"
                "    Utilisez --force pour le recréer (attention : cela supprimera son contenu).",
                file=sys.stderr,
            )
            sys.exit(1)
        shutil.rmtree(EXERCISE_DIR)

    EXERCISE_DIR.mkdir(parents=True, exist_ok=True)


def write_readme() -> None:
    """Écrit le fichier README initial."""
    README_PATH.write_text(build_readme_content(), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Prépare le dossier ex01-init avec un README.md non versionné pour l'exercice Git."
        )
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée ex01-init si le dossier existe déjà.",
    )
    args = parser.parse_args(argv)

    reset_exercise_dir(force=args.force)
    write_readme()

    print("\n✅ Exercice prêt !")
    print(f"📁 Dossier créé : {EXERCISE_DIR}")
    print("📄 README.md généré (non versionné).")
    print(
        "\n📚 Consignes :\n"
        "   1. Entrez dans le dossier ex01-init\n"
        "   2. Initialisez un nouveau dépôt Git\n"
        "   3. Vérifiez l'état du dépôt\n"
        "   4. Ajoutez le fichier README.md au suivi\n"
        "   5. Créez votre premier commit avec un message descriptif\n"
        "   6. Consultez l'historique des commits\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
