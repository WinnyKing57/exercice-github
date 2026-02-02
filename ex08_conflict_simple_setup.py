#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Conflit simple sur une ligne".

Crée un dossier ex08-conflict-simple avec un dépôt Git où deux branches
modifient la même ligne de message.txt, provoquant un conflit lors du merge.

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
EXERCISE_DIR = ROOT / "ex08-conflict-simple"


def build_message_base() -> str:
    """Retourne le contenu initial de message.txt."""
    return dedent(
        """\
        Bienvenue sur notre application !

        Notre slogan : Nous rendons votre vie plus simple.

        Merci de votre confiance.
        """
    )


def build_message_client() -> str:
    """Retourne le contenu de message.txt pour version-client."""
    return dedent(
        """\
        Bienvenue sur notre application !

        Notre slogan : La simplicité au service de nos clients.

        Merci de votre confiance.
        """
    )


def build_message_interne() -> str:
    """Retourne le contenu de message.txt pour version-interne."""
    return dedent(
        """\
        Bienvenue sur notre application !

        Notre slogan : L'innovation au cœur de notre mission.

        Merci de votre confiance.
        """
    )


def build_readme_content() -> str:
    """Retourne le contenu du fichier README.md."""
    return dedent(
        """\
        # ⚔️ Exercice : Résoudre un conflit simple

        ## 🎯 Objectif
        Apprendre à résoudre un conflit trivial sur une seule ligne.

        ## 📁 État initial
        - Branche `main` avec `message.txt` contenant un slogan original
        - Branche `version-client` modifie le slogan d'une façon
        - Branche `version-interne` modifie le slogan d'une autre façon
        - Vous êtes sur `version-client` et un merge de `version-interne` a été tenté → CONFLIT !

        ## 📋 Étapes à suivre

        1. **Observer le conflit** : Vérifiez l'état du dépôt

        2. **Analyser le fichier** : Ouvrez `message.txt` et repérez les marqueurs de conflit :
           ```
           <<<<<<< HEAD
           (votre version actuelle)
           =======
           (la version entrante)
           >>>>>>> version-interne
           ```

        3. **Résoudre le conflit** :
           - Choisissez UNE des deux versions, OU
           - Combinez les deux pour créer un nouveau slogan

        4. **Supprimer les marqueurs** : Effacez les lignes `<<<<<<<`, `=======` et `>>>>>>>`

        5. **Finaliser le merge** :
           - Ajoutez le fichier résolu à l'index
           - Créez le commit de merge

        ## 💡 Astuces
        - Les marqueurs de conflit sont du TEXTE ajouté par Git
        - Vous devez les supprimer manuellement
        - Testez que le fichier final est cohérent avant de commiter

        ## 🔑 Concepts clés
        - Marqueurs de conflit : `<<<<<<<`, `=======`, `>>>>>>>`
        - Résolution manuelle des conflits
        - `git add` pour marquer un conflit comme résolu
        """
    )


def reset_exercise_dir(force: bool) -> None:
    """Crée un répertoire ex08-conflict-simple vierge."""
    if EXERCISE_DIR.exists():
        if not force:
            print(
                "⚠️  Le dossier ex08-conflict-simple existe déjà.\n"
                "    Utilisez --force pour le recréer (attention : cela supprimera son contenu).",
                file=sys.stderr,
            )
            sys.exit(1)
        shutil.rmtree(EXERCISE_DIR)

    EXERCISE_DIR.mkdir(parents=True, exist_ok=True)


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    """Exécute une commande Git dans le répertoire de l'exercice."""
    return subprocess.run(
        ["git", *args],
        cwd=EXERCISE_DIR,
        check=check,
        capture_output=True,
    )


def setup_git_repo() -> None:
    """Initialise le dépôt et crée le conflit."""
    # Écrire les fichiers initiaux
    (EXERCISE_DIR / "README.md").write_text(build_readme_content(), encoding="utf-8")
    (EXERCISE_DIR / "message.txt").write_text(build_message_base(), encoding="utf-8")

    # Initialiser Git et créer le commit initial sur main
    run_git("init", "-b", "main")
    run_git("add", ".")
    run_git("commit", "-m", "Initial commit : message de base")

    # Créer la branche version-client
    run_git("checkout", "-b", "version-client")
    (EXERCISE_DIR / "message.txt").write_text(build_message_client(), encoding="utf-8")
    run_git("add", "message.txt")
    run_git("commit", "-m", "Slogan orienté client")

    # Créer la branche version-interne depuis main
    run_git("checkout", "main")
    run_git("checkout", "-b", "version-interne")
    (EXERCISE_DIR / "message.txt").write_text(build_message_interne(), encoding="utf-8")
    run_git("add", "message.txt")
    run_git("commit", "-m", "Slogan orienté innovation")

    # Revenir sur version-client et tenter le merge (provoque le conflit)
    run_git("checkout", "version-client")
    run_git("merge", "version-interne", check=False)  # Échouera avec conflit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prépare le dossier ex08-conflict-simple pour l'exercice résolution de conflit."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée ex08-conflict-simple si le dossier existe déjà.",
    )
    args = parser.parse_args(argv)

    reset_exercise_dir(force=args.force)
    setup_git_repo()

    print("\n✅ Exercice prêt !")
    print(f"📁 Dossier créé : {EXERCISE_DIR}")
    print("🌿 Branche actuelle : version-client")
    print("⚔️  CONFLIT créé dans message.txt (merge de version-interne en cours)")
    print(
        "\n📚 Consignes :\n"
        "   1. Observez le conflit avec git status\n"
        "   2. Ouvrez message.txt et analysez les marqueurs de conflit\n"
        "   3. Éditez le fichier pour résoudre le conflit\n"
        "   4. Marquez le conflit comme résolu et finalisez le merge\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
