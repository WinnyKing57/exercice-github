#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Rebase interactif".

Crée un dossier ex14-rebase-i avec un dépôt Git contenant une branche
feature-navbar avec 5 petits commits peu parlants. L'étudiant devra
utiliser rebase -i pour nettoyer l'historique.

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
EXERCISE_DIR = ROOT / "ex14-rebase-i"


def build_navbar_v1() -> str:
    """Version 1 de navbar.html."""
    return dedent(
        """\
        <nav>
        </nav>
        """
    )


def build_navbar_v2() -> str:
    """Version 2 de navbar.html."""
    return dedent(
        """\
        <nav>
            <a href="/">Home</a>
        </nav>
        """
    )


def build_navbar_v3() -> str:
    """Version 3 de navbar.html."""
    return dedent(
        """\
        <nav>
            <a href="/">Accueil</a>
        </nav>
        """
    )


def build_navbar_v4() -> str:
    """Version 4 de navbar.html."""
    return dedent(
        """\
        <nav>
            <a href="/">Accueil</a>
            <a href="/about">About</a>
        </nav>
        """
    )


def build_navbar_v5() -> str:
    """Version 5 de navbar.html."""
    return dedent(
        """\
        <nav class="main-nav">
            <a href="/">Accueil</a>
            <a href="/about">À propos</a>
            <a href="/contact">Contact</a>
        </nav>
        """
    )


def build_readme_content() -> str:
    """Retourne le contenu du fichier README.md."""
    return dedent(
        """\
        # ✨ Exercice : Rebase interactif

        ## 🎯 Objectif
        Utiliser `git rebase -i` pour nettoyer l'historique : fusionner des commits, renommer des messages.

        ## 📁 État initial
        La branche `feature-navbar` contient 5 commits peu parlants :
        1. `wip` — Navbar vide
        2. `wip2` — Ajout d'un lien
        3. `fix typo` — Correction Home → Accueil
        4. `wip` — Ajout d'un autre lien
        5. `done` — Version finale avec classe CSS

        Ces messages ne sont pas professionnels et l'historique est pollué !

        ## 📋 Étapes à suivre

        1. **Examiner l'historique** : `git log --oneline`

        2. **Lancer le rebase interactif** : `git rebase -i HEAD~5`

        3. **Dans l'éditeur, vous pouvez** :
           - `pick` : garder le commit tel quel
           - `reword` (ou `r`) : modifier le message du commit
           - `squash` (ou `s`) : fusionner avec le commit précédent
           - `fixup` (ou `f`) : fusionner sans garder le message
           - `drop` (ou `d`) : supprimer le commit

        4. **Suggestion de nettoyage** :
           - Fusionner les commits 1-4 en un seul
           - Garder le commit 5 avec un bon message
           - Résultat : 1 ou 2 commits propres

        5. **Vérifier le résultat** : `git log --oneline`

        ## 💡 Astuces
        - Sauvegardez et fermez l'éditeur pour appliquer les changements
        - En cas d'erreur : `git rebase --abort` pour annuler
        - Les commits sont listés du plus ancien au plus récent (ordre inverse du log)

        ## 🔑 Concepts clés
        - `git rebase -i` : réécriture interactive de l'historique
        - `squash` : fusionner des commits
        - `reword` : renommer un message
        - Qualité de l'historique pour la collaboration
        """
    )


def reset_exercise_dir(force: bool) -> None:
    """Crée un répertoire ex14-rebase-i vierge."""
    if EXERCISE_DIR.exists():
        if not force:
            print(
                "⚠️  Le dossier ex14-rebase-i existe déjà.\n"
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
    """Initialise le dépôt avec des commits mal nommés."""
    # Initialiser Git
    run_git("init", "-b", "main")

    # Commit initial sur main
    (EXERCISE_DIR / "README.md").write_text(build_readme_content(), encoding="utf-8")
    (EXERCISE_DIR / "index.html").write_text("<html><body></body></html>", encoding="utf-8")
    run_git("add", ".")
    run_git("commit", "-m", "Initial commit")

    # Créer la branche feature-navbar
    run_git("checkout", "-b", "feature-navbar")

    # Série de commits "mal nommés"
    (EXERCISE_DIR / "navbar.html").write_text(build_navbar_v1(), encoding="utf-8")
    run_git("add", "navbar.html")
    run_git("commit", "-m", "wip")

    (EXERCISE_DIR / "navbar.html").write_text(build_navbar_v2(), encoding="utf-8")
    run_git("add", "navbar.html")
    run_git("commit", "-m", "wip2")

    (EXERCISE_DIR / "navbar.html").write_text(build_navbar_v3(), encoding="utf-8")
    run_git("add", "navbar.html")
    run_git("commit", "-m", "fix typo")

    (EXERCISE_DIR / "navbar.html").write_text(build_navbar_v4(), encoding="utf-8")
    run_git("add", "navbar.html")
    run_git("commit", "-m", "wip")

    (EXERCISE_DIR / "navbar.html").write_text(build_navbar_v5(), encoding="utf-8")
    run_git("add", "navbar.html")
    run_git("commit", "-m", "done")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prépare le dossier ex14-rebase-i pour l'exercice rebase interactif."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée ex14-rebase-i si le dossier existe déjà.",
    )
    args = parser.parse_args(argv)

    reset_exercise_dir(force=args.force)
    setup_git_repo()

    print("\n✅ Exercice prêt !")
    print(f"📁 Dossier créé : {EXERCISE_DIR}")
    print("🌿 Branche actuelle : feature-navbar")
    print("📝 5 commits avec des messages peu parlants (wip, wip2, fix typo...)")
    print(
        "\n📚 Consignes :\n"
        "   1. Examinez l'historique de feature-navbar\n"
        "   2. Lancez un rebase interactif pour nettoyer\n"
        "   3. Fusionnez et renommez les commits\n"
        "   4. Vérifiez le nouvel historique propre\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
