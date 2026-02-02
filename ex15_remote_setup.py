#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Dépôt distant (clone et pull)".

Crée un dossier remote-repo.git (dépôt bare simulant un serveur distant),
puis clone ce dépôt dans ex15-remote. Le script peut aussi simuler une
mise à jour distante pour l'exercice de pull.

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
REMOTE_REPO = ROOT / "remote-repo.git"
EXERCISE_DIR = ROOT / "ex15-remote"


def build_readme_content() -> str:
    """Retourne le contenu du fichier README.md."""
    return dedent(
        """\
        # Projet Partagé

        Ce projet est partagé via un dépôt distant.

        ## Installation
        1. Cloner le dépôt
        2. Installer les dépendances
        3. Lancer l'application
        """
    )


def build_readme_updated() -> str:
    """Retourne le README mis à jour (simulation de commit distant)."""
    return dedent(
        """\
        # Projet Partagé

        Ce projet est partagé via un dépôt distant.

        ## Installation
        1. Cloner le dépôt
        2. Installer les dépendances
        3. Lancer l'application

        ## Nouveautés v1.1
        - Correction de bugs importants
        - Amélioration des performances
        - Nouvelle documentation
        """
    )


def build_exercise_readme() -> str:
    """Retourne le contenu du fichier EXERCICE.md."""
    return dedent(
        """\
        # 🌐 Exercice : Travailler avec un dépôt distant

        ## 🎯 Objectif
        Comprendre les notions de remote, fetch et pull.

        ## 📁 État initial
        - Un dépôt "distant" simulé : `remote-repo.git` (dépôt bare)
        - Votre copie locale : `ex15-remote` (clone du dépôt distant)
        - Le remote est configuré sous le nom `origin`

        ## 📋 Étapes à suivre

        ### Partie 1 : Explorer la configuration
        1. **Vérifier les remotes** : `git remote -v`
        2. **Voir les branches distantes** : `git branch -a`

        ### Partie 2 : Simuler une mise à jour distante
        3. Relancez le script avec `--update` pour simuler un push d'un collègue
        4. Votre dépôt local ne "sait" pas encore qu'il y a du nouveau !

        ### Partie 3 : Récupérer les changements
        5. **Fetch** : Téléchargez les infos du distant sans modifier vos fichiers
        6. **Observer** : Comparez votre branche locale avec `origin/main`
        7. **Pull** : Intégrez les changements dans votre branche

        ### Partie 4 : Vérifier
        8. Consultez l'historique pour voir le nouveau commit
        9. Vérifiez le contenu du README mis à jour

        ## 💡 Astuces
        - `git fetch` télécharge sans modifier votre code
        - `git pull` = `git fetch` + `git merge`
        - `git log origin/main` pour voir l'état du distant

        ## 🔑 Concepts clés
        - `git remote -v` : lister les dépôts distants
        - `git fetch` : télécharger sans fusionner
        - `git pull` : télécharger ET fusionner
        - Branches de suivi (tracking branches) : `origin/main`
        """
    )


def reset_dirs(force: bool) -> None:
    """Supprime et recrée les répertoires de l'exercice."""
    for dir_path in [REMOTE_REPO, EXERCISE_DIR]:
        if dir_path.exists():
            if not force:
                print(
                    f"⚠️  Le dossier {dir_path.name} existe déjà.\n"
                    "    Utilisez --force pour le recréer (attention : cela supprimera son contenu).",
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
    """Crée le dépôt bare (simulant un serveur distant)."""
    # Créer un dépôt temporaire pour initialiser
    temp_dir = ROOT / "_temp_init"
    temp_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Initialiser le dépôt temporaire
        run_git("init", "-b", "main", cwd=temp_dir)
        (temp_dir / "README.md").write_text(build_readme_content(), encoding="utf-8")
        run_git("add", ".", cwd=temp_dir)
        run_git("commit", "-m", "Initial commit : projet partagé", cwd=temp_dir)

        # Cloner en bare pour créer le dépôt "distant"
        subprocess.run(
            ["git", "clone", "--bare", str(temp_dir), str(REMOTE_REPO)],
            check=True,
            capture_output=True,
        )
    finally:
        shutil.rmtree(temp_dir)


def setup_local_clone() -> None:
    """Clone le dépôt distant dans ex15-remote."""
    subprocess.run(
        ["git", "clone", str(REMOTE_REPO), str(EXERCISE_DIR)],
        check=True,
        capture_output=True,
    )

    # Ajouter le README de l'exercice
    (EXERCISE_DIR / "EXERCICE.md").write_text(build_exercise_readme(), encoding="utf-8")
    run_git("add", "EXERCICE.md", cwd=EXERCISE_DIR)
    run_git("commit", "-m", "Ajout des consignes de l'exercice", cwd=EXERCISE_DIR)


def simulate_remote_update() -> None:
    """Simule une mise à jour sur le dépôt distant (un collègue a poussé)."""
    if not REMOTE_REPO.exists():
        print(
            "⚠️  Le dépôt distant n'existe pas.\n"
            "    Lancez d'abord le script sans --update pour créer l'exercice.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Créer un clone temporaire pour pusher
    temp_dir = ROOT / "_temp_push"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    try:
        subprocess.run(
            ["git", "clone", str(REMOTE_REPO), str(temp_dir)],
            check=True,
            capture_output=True,
        )

        # Modifier le README et pusher
        (temp_dir / "README.md").write_text(build_readme_updated(), encoding="utf-8")
        run_git("add", "README.md", cwd=temp_dir)
        run_git("commit", "-m", "Mise à jour v1.1 : nouveautés et corrections", cwd=temp_dir)
        run_git("push", "origin", "main", cwd=temp_dir)

    finally:
        shutil.rmtree(temp_dir)

    print("\n✅ Mise à jour distante simulée !")
    print("📡 Un nouveau commit a été ajouté au dépôt distant.")
    print("   Votre copie locale ne le sait pas encore...")
    print(
        "\n📚 Prochaines étapes :\n"
        "   1. Utilisez git fetch pour télécharger les nouveautés\n"
        "   2. Comparez avec git log origin/main\n"
        "   3. Intégrez avec git pull\n"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prépare l'exercice sur les dépôts distants (clone et pull)."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée les dossiers s'ils existent déjà.",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Simule une mise à jour sur le dépôt distant (un collègue a poussé).",
    )
    args = parser.parse_args(argv)

    if args.update:
        simulate_remote_update()
        return 0

    reset_dirs(force=args.force)
    setup_remote_repo()
    setup_local_clone()

    print("\n✅ Exercice prêt !")
    print(f"📡 Dépôt distant (bare) : {REMOTE_REPO}")
    print(f"📁 Votre copie locale : {EXERCISE_DIR}")
    print("🔗 Remote configuré : origin → remote-repo.git")
    print(
        "\n📚 Consignes :\n"
        "   1. Vérifiez la configuration du remote avec git remote -v\n"
        "   2. Relancez avec --update pour simuler un push distant\n"
        "   3. Récupérez les changements avec fetch puis pull\n"
        "   4. Vérifiez l'historique intégré\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
