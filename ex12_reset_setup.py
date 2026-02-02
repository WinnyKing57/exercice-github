#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Reset soft et hard".

Crée un dossier ex12-reset avec un dépôt Git contenant 3 commits successifs
sur notes.md. L'étudiant expérimentera les différents modes de reset.

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
EXERCISE_DIR = ROOT / "ex12-reset"


def build_notes_v1() -> str:
    """Retourne le contenu initial de notes.md (commit 1)."""
    return dedent(
        """\
        # Mes Notes

        ## Introduction
        Ceci est mon fichier de notes pour le projet.
        """
    )


def build_notes_v2() -> str:
    """Retourne le contenu de notes.md après commit 2."""
    return dedent(
        """\
        # Mes Notes

        ## Introduction
        Ceci est mon fichier de notes pour le projet.

        ## Idées
        - Implémenter la fonctionnalité A
        - Refactorer le module B
        - Ajouter des tests unitaires
        """
    )


def build_notes_v3() -> str:
    """Retourne le contenu de notes.md après commit 3."""
    return dedent(
        """\
        # Mes Notes

        ## Introduction
        Ceci est mon fichier de notes pour le projet.

        ## Idées
        - Implémenter la fonctionnalité A
        - Refactorer le module B
        - Ajouter des tests unitaires

        ## TODO
        - [ ] Revoir l'architecture
        - [ ] Documenter l'API
        - [ ] Préparer la démo
        """
    )


def build_readme_content() -> str:
    """Retourne le contenu du fichier README.md."""
    return dedent(
        """\
        # 🔄 Exercice : Reset soft et hard

        ## 🎯 Objectif
        Comprendre les différents types de reset et leurs effets.

        ## 📁 État initial
        Le dépôt contient 3 commits sur `notes.md` :
        1. `Notes v1` — Introduction
        2. `Notes v2` — Ajout des idées
        3. `Notes v3` — Ajout des TODO

        ## 📊 Les 3 types de reset

        | Mode | HEAD | Index (staging) | Working directory |
        |------|------|-----------------|-------------------|
        | `--soft` | ✅ Déplacé | ❌ Inchangé | ❌ Inchangé |
        | `--mixed` (défaut) | ✅ Déplacé | ✅ Réinitialisé | ❌ Inchangé |
        | `--hard` | ✅ Déplacé | ✅ Réinitialisé | ✅ Réinitialisé |

        ## 📋 Étapes à suivre

        ### Partie 1 : Reset --soft
        1. Notez le hash du commit 1 avec `git log --oneline`
        2. Faites `git reset --soft <hash-commit-1>`
        3. Observez : `git status` montre les changements des commits 2 et 3 dans l'index
        4. Le fichier `notes.md` contient toujours le contenu v3 !

        ### Partie 2 : Recréer l'historique
        5. Créez un nouveau commit avec ces changements
        6. Vous avez "fusionné" les commits 2 et 3 en un seul !

        ### Partie 3 : Reset --hard (⚠️ DANGER)
        7. Ajoutez quelques modifications à `notes.md` (sans commiter)
        8. Faites `git reset --hard HEAD~1`
        9. Observez : les modifications ET le dernier commit sont PERDUS !

        ## ⚠️ Avertissement
        `git reset --hard` est DESTRUCTIF ! Les modifications non commitées sont perdues définitivement.

        ## 💡 Astuces
        - `HEAD~1` = le commit parent de HEAD
        - `HEAD~2` = 2 commits avant HEAD
        - Utilisez `git reflog` pour récupérer des commits "perdus"

        ## 🔑 Concepts clés
        - `git reset --soft` : garde tout sauf le pointeur HEAD
        - `git reset --mixed` : vide l'index mais garde les fichiers
        - `git reset --hard` : remet tout à l'état du commit cible
        """
    )


def reset_exercise_dir(force: bool) -> None:
    """Crée un répertoire ex12-reset vierge."""
    if EXERCISE_DIR.exists():
        if not force:
            print(
                "⚠️  Le dossier ex12-reset existe déjà.\n"
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
    """Initialise le dépôt avec 3 commits successifs."""
    # Initialiser Git
    run_git("init", "-b", "main")

    # README
    (EXERCISE_DIR / "README.md").write_text(build_readme_content(), encoding="utf-8")
    run_git("add", "README.md")
    run_git("commit", "-m", "Ajout du README")

    # Commit 1 : notes.md v1
    (EXERCISE_DIR / "notes.md").write_text(build_notes_v1(), encoding="utf-8")
    run_git("add", "notes.md")
    run_git("commit", "-m", "Notes v1 : introduction")

    # Commit 2 : notes.md v2
    (EXERCISE_DIR / "notes.md").write_text(build_notes_v2(), encoding="utf-8")
    run_git("add", "notes.md")
    run_git("commit", "-m", "Notes v2 : ajout des idées")

    # Commit 3 : notes.md v3
    (EXERCISE_DIR / "notes.md").write_text(build_notes_v3(), encoding="utf-8")
    run_git("add", "notes.md")
    run_git("commit", "-m", "Notes v3 : ajout des TODO")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prépare le dossier ex12-reset pour l'exercice git reset."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée ex12-reset si le dossier existe déjà.",
    )
    args = parser.parse_args(argv)

    reset_exercise_dir(force=args.force)
    setup_git_repo()

    print("\n✅ Exercice prêt !")
    print(f"📁 Dossier créé : {EXERCISE_DIR}")
    print("📄 Fichiers : README.md, notes.md")
    print("🔧 4 commits créés (README + 3 versions de notes.md)")
    print(
        "\n📚 Consignes :\n"
        "   1. Consultez l'historique avec git log\n"
        "   2. Expérimentez git reset --soft vers un commit antérieur\n"
        "   3. Observez l'état de l'index et du working directory\n"
        "   4. Testez git reset --hard (attention : destructif !)\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
