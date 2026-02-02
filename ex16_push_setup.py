#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Pousser une branche vers un dépôt distant".

Crée un dépôt bare (remote-ex16.git) et un clone (ex16-push) avec seulement
la branche main. L'étudiant devra créer une branche et la publier.

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
REMOTE_REPO = ROOT / "remote-ex16.git"
EXERCISE_DIR = ROOT / "ex16-push"


def build_index_html() -> str:
    """Retourne le contenu de index.html."""
    return dedent(
        """\
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Mon Site</title>
        </head>
        <body>
            <h1>Bienvenue</h1>
            <nav>
                <a href="index.html">Accueil</a>
                <a href="about.html">À propos</a>
                <!-- TODO: Ajouter un lien vers la page contact -->
            </nav>
            <p>Ceci est la page d'accueil.</p>
        </body>
        </html>
        """
    )


def build_about_html() -> str:
    """Retourne le contenu de about.html."""
    return dedent(
        """\
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>À propos</title>
        </head>
        <body>
            <h1>À propos</h1>
            <p>Nous sommes une équipe passionnée.</p>
        </body>
        </html>
        """
    )


def build_readme_content() -> str:
    """Retourne le contenu du fichier README.md."""
    return dedent(
        """\
        # 📤 Exercice : Pousser une branche vers un dépôt distant

        ## 🎯 Objectif
        Créer une branche locale et la publier sur le dépôt distant.

        ## 📁 État initial
        - Clone d'un dépôt distant (`origin` → `remote-ex16.git`)
        - Seule la branche `main` existe pour l'instant

        ## 📋 Étapes à suivre

        1. **Vérifier l'état initial** :
           - `git branch` : voir les branches locales
           - `git branch -r` : voir les branches distantes

        2. **Créer une branche feature-contact** :
           - Créez et basculez sur la nouvelle branche

        3. **Ajouter du contenu** :
           - Créez un fichier `contact.html` avec un formulaire de contact
           - Commitez ce nouveau fichier

        4. **Publier la branche sur origin** :
           - Poussez la branche vers le dépôt distant
           - Configurez le suivi (upstream) pour les futurs push/pull

        5. **Vérifier le résultat** :
           - `git branch -r` : la branche doit apparaître sur origin
           - `git branch -vv` : vérifier le suivi (tracking)

        ## 💡 Astuces
        - Premier push d'une branche : `git push -u origin <branche>`
        - `-u` (ou `--set-upstream`) configure le suivi automatique
        - Après ça, un simple `git push` suffit

        ## 🔑 Concepts clés
        - `git push` : envoyer des commits vers le distant
        - `git push -u origin <branche>` : publier une nouvelle branche
        - Branches de suivi (upstream tracking)
        """
    )


def reset_dirs(force: bool) -> None:
    """Supprime et recrée les répertoires de l'exercice."""
    for dir_path in [REMOTE_REPO, EXERCISE_DIR]:
        if dir_path.exists():
            if not force:
                print(
                    f"⚠️  Le dossier {dir_path.name} existe déjà.\n"
                    "    Utilisez --force pour le recréer.",
                    file=sys.stderr,
                )
                sys.exit(1)
            shutil.rmtree(dir_path)


def run_git(*args: str, cwd: Path) -> None:
    """Exécute une commande Git dans le répertoire spécifié."""
    subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
    )


def setup_remote_repo() -> None:
    """Crée le dépôt bare."""
    temp_dir = ROOT / "_temp_ex16"
    temp_dir.mkdir(parents=True, exist_ok=True)

    try:
        run_git("init", "-b", "main", cwd=temp_dir)
        (temp_dir / "index.html").write_text(build_index_html(), encoding="utf-8")
        (temp_dir / "about.html").write_text(build_about_html(), encoding="utf-8")
        run_git("add", ".", cwd=temp_dir)
        run_git("commit", "-m", "Initial commit : pages accueil et about", cwd=temp_dir)

        subprocess.run(
            ["git", "clone", "--bare", str(temp_dir), str(REMOTE_REPO)],
            check=True,
            capture_output=True,
        )
    finally:
        shutil.rmtree(temp_dir)


def setup_local_clone() -> None:
    """Clone le dépôt distant."""
    subprocess.run(
        ["git", "clone", str(REMOTE_REPO), str(EXERCISE_DIR)],
        check=True,
        capture_output=True,
    )

    (EXERCISE_DIR / "README.md").write_text(build_readme_content(), encoding="utf-8")
    run_git("add", "README.md", cwd=EXERCISE_DIR)
    run_git("commit", "-m", "Ajout du README", cwd=EXERCISE_DIR)
    run_git("push", cwd=EXERCISE_DIR)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prépare l'exercice sur le push de branches."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée les dossiers s'ils existent déjà.",
    )
    args = parser.parse_args(argv)

    reset_dirs(force=args.force)
    setup_remote_repo()
    setup_local_clone()

    print("\n✅ Exercice prêt !")
    print(f"📡 Dépôt distant : {REMOTE_REPO}")
    print(f"📁 Votre copie locale : {EXERCISE_DIR}")
    print("🌿 Seule la branche main existe sur origin")
    print(
        "\n📚 Consignes :\n"
        "   1. Créez une branche feature-contact\n"
        "   2. Ajoutez contact.html et commitez\n"
        "   3. Publiez la branche sur origin\n"
        "   4. Vérifiez avec git branch -r\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
