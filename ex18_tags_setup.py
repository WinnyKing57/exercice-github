#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Tags pour versionner une release".

Crée un dépôt ex18-tags avec plusieurs commits et un tag v0.9.0 existant.
L'étudiant devra créer un tag v1.0.0 et explorer les tags.

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
EXERCISE_DIR = ROOT / "ex18-tags"


def build_app_v1() -> str:
    """Retourne app.js version 0.1."""
    return dedent(
        """\
        // Application v0.1 - Version initiale
        console.log('App démarrée');

        function init() {
            console.log('Initialisation...');
        }

        init();
        """
    )


def build_app_v2() -> str:
    """Retourne app.js version 0.5."""
    return dedent(
        """\
        // Application v0.5 - Ajout des fonctionnalités de base
        console.log('App démarrée');

        function init() {
            console.log('Initialisation...');
            loadConfig();
        }

        function loadConfig() {
            console.log('Configuration chargée');
        }

        init();
        """
    )


def build_app_v3() -> str:
    """Retourne app.js version 0.9 (pré-release)."""
    return dedent(
        """\
        // Application v0.9 - Beta
        console.log('App v0.9 démarrée');

        function init() {
            console.log('Initialisation...');
            loadConfig();
            setupUI();
        }

        function loadConfig() {
            console.log('Configuration chargée');
        }

        function setupUI() {
            console.log('Interface utilisateur prête');
        }

        init();
        """
    )


def build_app_v4() -> str:
    """Retourne app.js version 1.0 (release)."""
    return dedent(
        """\
        // Application v1.0 - Release stable
        console.log('App v1.0 démarrée');

        function init() {
            console.log('Initialisation...');
            loadConfig();
            setupUI();
            console.log('Application prête !');
        }

        function loadConfig() {
            console.log('Configuration chargée');
            return { env: 'production' };
        }

        function setupUI() {
            console.log('Interface utilisateur prête');
        }

        init();
        """
    )


def build_readme_content() -> str:
    """Retourne le contenu du fichier README.md."""
    return dedent(
        """\
        # 🏷️ Exercice : Tags pour versionner une release

        ## 🎯 Objectif
        Utiliser les tags Git pour identifier des versions stables.

        ## 📁 État initial
        - Plusieurs commits représentant l'évolution de l'application
        - Un tag `v0.9.0` existe déjà (version beta)
        - Le dernier commit est prêt pour une release `v1.0.0`

        ## 📋 Étapes à suivre

        1. **Lister les tags existants** :
           - `git tag` ou `git tag -l`

        2. **Voir les détails d'un tag** :
           - `git show v0.9.0`

        3. **Créer un tag annoté v1.0.0** :
           - Créez un tag annoté sur le commit actuel (HEAD)
           - Incluez un message descriptif

        4. **Vérifier la création** :
           - Listez à nouveau les tags
           - Affichez les détails de v1.0.0

        5. **Revenir temporairement à v0.9.0** :
           - Faites un checkout sur le tag v0.9.0
           - Observez l'état "detached HEAD"
           - Vérifiez le contenu de app.js

        6. **Revenir sur main** :
           - Retournez sur la branche principale

        ## 💡 Astuces
        - Tag léger : `git tag v1.0.0` (juste un pointeur)
        - Tag annoté : `git tag -a v1.0.0 -m "Message"` (recommandé)
        - Les tags annotés contiennent : auteur, date, message

        ## 🔑 Concepts clés
        - `git tag` : lister les tags
        - `git tag -a <nom> -m "message"` : créer un tag annoté
        - `git checkout <tag>` : revenir à un état passé
        - Tags vs branches : les tags sont des points fixes
        """
    )


def reset_exercise_dir(force: bool) -> None:
    """Crée un répertoire ex18-tags vierge."""
    if EXERCISE_DIR.exists():
        if not force:
            print(
                "⚠️  Le dossier ex18-tags existe déjà.\n"
                "    Utilisez --force pour le recréer.",
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
    """Initialise le dépôt avec l'historique de versions."""
    run_git("init", "-b", "main")

    # Commit 1 : v0.1
    (EXERCISE_DIR / "README.md").write_text(build_readme_content(), encoding="utf-8")
    (EXERCISE_DIR / "app.js").write_text(build_app_v1(), encoding="utf-8")
    run_git("add", ".")
    run_git("commit", "-m", "Initial commit : version 0.1")

    # Commit 2 : v0.5
    (EXERCISE_DIR / "app.js").write_text(build_app_v2(), encoding="utf-8")
    run_git("add", "app.js")
    run_git("commit", "-m", "Ajout du chargement de configuration (v0.5)")

    # Commit 3 : v0.9 + tag
    (EXERCISE_DIR / "app.js").write_text(build_app_v3(), encoding="utf-8")
    run_git("add", "app.js")
    run_git("commit", "-m", "Version beta avec interface UI (v0.9)")
    run_git("tag", "-a", "v0.9.0", "-m", "Version 0.9.0 - Beta")

    # Commit 4 : v1.0 (sans tag, à créer par l'étudiant)
    (EXERCISE_DIR / "app.js").write_text(build_app_v4(), encoding="utf-8")
    run_git("add", "app.js")
    run_git("commit", "-m", "Release stable v1.0")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prépare le dossier ex18-tags pour l'exercice sur les tags."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée ex18-tags si le dossier existe déjà.",
    )
    args = parser.parse_args(argv)

    reset_exercise_dir(force=args.force)
    setup_git_repo()

    print("\n✅ Exercice prêt !")
    print(f"📁 Dossier créé : {EXERCISE_DIR}")
    print("🏷️  Tag existant : v0.9.0")
    print("📝 Dernier commit prêt pour le tag v1.0.0")
    print(
        "\n📚 Consignes :\n"
        "   1. Listez les tags existants\n"
        "   2. Créez un tag annoté v1.0.0 sur HEAD\n"
        "   3. Revenez temporairement à v0.9.0\n"
        "   4. Revenez sur la branche main\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
