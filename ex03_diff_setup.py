#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Modifier, comparer et corriger".

Crée un dossier ex03-diff avec un dépôt Git initialisé contenant un premier
commit avec article.md. L'étudiant devra modifier le fichier et observer
les différences avec git diff.

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
EXERCISE_DIR = ROOT / "ex03-diff"


def build_article_content() -> str:
    """Retourne le contenu initial du fichier article.md."""
    return dedent(
        """\
        # Mon article de blog

        ## Introduction

        Bienvenue dans cet article où nous allons découvrir les bases de Git.
        Git est un outil de versionnement distribué créé par Linus Torvalds en 2005.

        ## Pourquoi utiliser Git ?

        Git permet de :
        - Suivre l'historique des modifications
        - Collaborer efficacement en équipe
        - Revenir en arrière en cas d'erreur

        ## Conclusion

        Git est un outil indispensable pour tout développeur moderne.
        """
    )


def build_readme_content() -> str:
    """Retourne le contenu du fichier README.md."""
    return dedent(
        """\
        # 📝 Exercice : Modifier et comparer

        ## 🎯 Objectif
        Utiliser `git status` et `git diff` pour comprendre les modifications apportées à un fichier.

        ## 📁 État initial
        - Un dépôt Git initialisé avec un commit contenant `article.md`

        ## 📋 Étapes à suivre

        1. **Modifier article.md** :
           - Ajoutez un nouveau paragraphe dans une section existante
           - Changez le titre d'une section (par exemple "Pourquoi utiliser Git ?" → "Les avantages de Git")

        2. **Observer les changements** :
           - Vérifiez l'état du dépôt
           - Affichez les différences ligne par ligne

        3. **Valider les modifications** :
           - Ajoutez le fichier à l'index
           - Créez un commit avec un message descriptif

        4. **Consulter l'historique** :
           - Affichez le log des commits
           - Affichez le diff du dernier commit

        ## 💡 Astuces
        - `git diff` montre les changements non indexés
        - `git diff --staged` montre les changements indexés (prêts à être commités)
        - Les lignes supprimées apparaissent en rouge, les ajoutées en vert

        ## 🔑 Concepts clés
        - `git diff` : voir les modifications
        - `git log -p` : historique avec les diffs
        - Cycle : modification → index → commit
        """
    )


def reset_exercise_dir(force: bool) -> None:
    """
    Crée un répertoire ex03-diff vierge.

    Si le répertoire existe déjà et que force est False, le script s'arrête
    pour éviter de supprimer le travail de l'étudiant.
    Avec --force, le répertoire est supprimé puis recréé.
    """
    if EXERCISE_DIR.exists():
        if not force:
            print(
                "⚠️  Le dossier ex03-diff existe déjà.\n"
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
    """Initialise le dépôt Git avec un premier commit."""
    # Écrire les fichiers
    (EXERCISE_DIR / "README.md").write_text(build_readme_content(), encoding="utf-8")
    (EXERCISE_DIR / "article.md").write_text(build_article_content(), encoding="utf-8")

    # Initialiser Git et créer le premier commit
    run_git("init")
    run_git("add", "README.md", "article.md")
    run_git("commit", "-m", "Initial commit : ajout de article.md")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Prépare le dossier ex03-diff avec un dépôt Git et article.md pour l'exercice diff."
        )
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée ex03-diff si le dossier existe déjà.",
    )
    args = parser.parse_args(argv)

    reset_exercise_dir(force=args.force)
    setup_git_repo()

    print("\n✅ Exercice prêt !")
    print(f"📁 Dossier créé : {EXERCISE_DIR}")
    print("📄 Fichiers : README.md, article.md (déjà commités)")
    print("🔧 Dépôt Git initialisé avec 1 commit")
    print(
        "\n📚 Consignes :\n"
        "   1. Modifiez article.md (ajoutez un paragraphe et changez un titre)\n"
        "   2. Observez les changements avec les commandes appropriées\n"
        "   3. Ajoutez le fichier à l'index et créez un commit\n"
        "   4. Affichez l'historique et le diff du dernier commit\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
