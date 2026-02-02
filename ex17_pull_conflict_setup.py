#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Conflit lors d'un pull".

Crée un dépôt bare, un clone local, puis simule une situation où le distant
et le local ont divergé sur la même ligne, provoquant un conflit lors du pull.

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
REMOTE_REPO = ROOT / "remote-ex17.git"
EXERCISE_DIR = ROOT / "ex17-pull-conflict"


def build_config_base() -> str:
    """Retourne le contenu initial de config.json."""
    return dedent(
        """\
        {
            "app": {
                "name": "MonApplication",
                "version": "1.0.0",
                "environment": "development"
            },
            "database": {
                "host": "localhost",
                "port": 5432
            }
        }
        """
    )


def build_config_remote() -> str:
    """Retourne config.json modifié par un collègue (distant)."""
    return dedent(
        """\
        {
            "app": {
                "name": "MonApplication",
                "version": "1.1.0",
                "environment": "production"
            },
            "database": {
                "host": "db.production.com",
                "port": 5432
            }
        }
        """
    )


def build_config_local() -> str:
    """Retourne config.json modifié localement."""
    return dedent(
        """\
        {
            "app": {
                "name": "MonApplication",
                "version": "1.0.1",
                "environment": "staging"
            },
            "database": {
                "host": "localhost",
                "port": 5432
            }
        }
        """
    )


def build_readme_content() -> str:
    """Retourne le contenu du fichier README.md."""
    return dedent(
        """\
        # ⚔️ Exercice : Conflit lors d'un pull

        ## 🎯 Objectif
        Comprendre et résoudre un conflit entre modifications locales et distantes.

        ## 📁 État initial
        - Un commit a été poussé sur `origin/main` (par un collègue)
        - Vous avez aussi modifié `config.json` localement et commité
        - Les deux modifications touchent les MÊMES lignes → CONFLIT !

        ## 📊 Situation
        ```
        origin/main:  A --- B (version 1.1.0, production)
                       \\
        local main:    A --- C (version 1.0.1, staging)
        ```

        ## 📋 Étapes à suivre

        1. **Observer l'état** :
           - `git status` : votre branche est "ahead" de origin
           - `git log --oneline origin/main` vs `git log --oneline`

        2. **Tenter un pull** :
           - `git pull` va échouer avec un conflit

        3. **Analyser le conflit** :
           - Ouvrez `config.json`
           - Repérez les marqueurs de conflit

        4. **Résoudre le conflit** :
           - Choisissez les bonnes valeurs (ou combinez)
           - Supprimez les marqueurs

        5. **Finaliser le merge** :
           - `git add config.json`
           - `git commit` (message de merge auto-généré)

        6. **Vérifier** :
           - `git log --oneline --graph` : voir les deux parents du merge

        ## 💡 Astuces
        - `git pull` = `git fetch` + `git merge`
        - Vous pouvez utiliser `git pull --rebase` pour rebaser au lieu de merger
        - En cas d'abandon : `git merge --abort`

        ## 🔑 Concepts clés
        - Conflit de pull : quand local et distant ont divergé
        - Résolution identique à un conflit de merge classique
        - Importance de `git fetch` pour voir l'état avant d'agir
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


def run_git(*args: str, cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
    """Exécute une commande Git dans le répertoire spécifié."""
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=check,
        capture_output=True,
    )


def setup_exercise() -> None:
    """Configure le dépôt avec un conflit prêt."""
    # Créer le dépôt initial temporaire
    temp_dir = ROOT / "_temp_ex17"
    temp_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Initialiser avec le contenu de base
        run_git("init", "-b", "main", cwd=temp_dir)
        (temp_dir / "config.json").write_text(build_config_base(), encoding="utf-8")
        (temp_dir / "README.md").write_text(build_readme_content(), encoding="utf-8")
        run_git("add", ".", cwd=temp_dir)
        run_git("commit", "-m", "Initial commit : configuration de base", cwd=temp_dir)

        # Créer le bare
        subprocess.run(
            ["git", "clone", "--bare", str(temp_dir), str(REMOTE_REPO)],
            check=True,
            capture_output=True,
        )
    finally:
        shutil.rmtree(temp_dir)

    # Cloner pour l'étudiant
    subprocess.run(
        ["git", "clone", str(REMOTE_REPO), str(EXERCISE_DIR)],
        check=True,
        capture_output=True,
    )

    # Simuler un push distant (collègue)
    temp_remote = ROOT / "_temp_remote_ex17"
    try:
        subprocess.run(
            ["git", "clone", str(REMOTE_REPO), str(temp_remote)],
            check=True,
            capture_output=True,
        )
        (temp_remote / "config.json").write_text(build_config_remote(), encoding="utf-8")
        run_git("add", "config.json", cwd=temp_remote)
        run_git("commit", "-m", "Mise en production v1.1.0", cwd=temp_remote)
        run_git("push", cwd=temp_remote)
    finally:
        shutil.rmtree(temp_remote)

    # Modification locale (avant pull)
    (EXERCISE_DIR / "config.json").write_text(build_config_local(), encoding="utf-8")
    run_git("add", "config.json", cwd=EXERCISE_DIR)
    run_git("commit", "-m", "Configuration staging v1.0.1", cwd=EXERCISE_DIR)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prépare l'exercice sur les conflits de pull."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée les dossiers s'ils existent déjà.",
    )
    args = parser.parse_args(argv)

    reset_dirs(force=args.force)
    setup_exercise()

    print("\n✅ Exercice prêt !")
    print(f"📡 Dépôt distant : {REMOTE_REPO}")
    print(f"📁 Votre copie locale : {EXERCISE_DIR}")
    print("⚔️  Conflit préparé : distant et local ont modifié config.json différemment")
    print(
        "\n📚 Consignes :\n"
        "   1. Tentez un git pull\n"
        "   2. Observez le conflit dans config.json\n"
        "   3. Résolvez le conflit\n"
        "   4. Finalisez le merge et vérifiez l'historique\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
