#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Revert d'un commit fautif".

Crée un dossier ex11-revert avec un dépôt Git contenant 3 commits, dont le
dernier introduit un fichier bug.js avec du code problématique. L'étudiant
devra utiliser git revert pour annuler ce commit.

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
EXERCISE_DIR = ROOT / "ex11-revert"


def build_index_html() -> str:
    """Retourne le contenu de index.html."""
    return dedent(
        """\
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Mon Application</title>
            <link rel="stylesheet" href="style.css">
            <script src="bug.js" defer></script>
        </head>
        <body>
            <h1>Mon Application</h1>
            <p>Une application simple et fonctionnelle.</p>
            <button id="action">Cliquez-moi</button>
        </body>
        </html>
        """
    )


def build_style_css() -> str:
    """Retourne le contenu de style.css."""
    return dedent(
        """\
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 2rem auto;
            padding: 0 1rem;
        }

        h1 {
            color: #2c3e50;
        }

        button {
            padding: 1rem 2rem;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        button:hover {
            background: #2980b9;
        }
        """
    )


def build_bug_js() -> str:
    """Retourne le contenu de bug.js (code buggé)."""
    return dedent(
        """\
        // Script de l'application
        // ⚠️ ATTENTION : Ce code contient un bug !

        document.getElementById('action').addEventListener('click', function() {
            // BUG: Cette ligne provoque une erreur !
            undefinedFunction();  // ReferenceError: undefinedFunction is not defined
            
            alert('Action effectuée !');
        });

        // Ce code ne devrait jamais avoir été commité...
        console.log('Debug mode activé - NE PAS DEPLOYER EN PRODUCTION');
        """
    )


def build_readme_content() -> str:
    """Retourne le contenu du fichier README.md."""
    return dedent(
        """\
        # ↩️ Exercice : Revert d'un commit fautif

        ## 🎯 Objectif
        Apprendre à annuler un commit sans réécrire l'historique.

        ## 📁 État initial
        Le dépôt contient 3 commits :
        1. `Ajout de index.html` — Structure de base ✅
        2. `Ajout de style.css` — Styles de l'application ✅
        3. `Ajout de bug.js` — ⚠️ Introduit du code buggé !

        ## 🐛 Le problème
        Le fichier `bug.js` contient :
        - Un appel à une fonction inexistante (`undefinedFunction()`)
        - Des logs de debug qui ne devraient pas être en production

        ## 📋 Étapes à suivre

        1. **Identifier le commit fautif** :
           - Consultez l'historique des commits
           - Repérez le commit qui a introduit `bug.js`

        2. **Annuler le commit avec revert** :
           - Utilisez `git revert` sur le commit identifié
           - Git créera un NOUVEAU commit qui annule les changements

        3. **Vérifier le résultat** :
           - Le fichier `bug.js` doit avoir été supprimé (ou son contenu annulé)
           - L'historique contient toujours le commit original + le revert

        ## 💡 Astuces
        - `git revert` ne supprime PAS le commit original
        - Il crée un nouveau commit qui "défait" les changements
        - C'est la méthode sûre pour corriger un historique partagé

        ## 🔑 Concepts clés
        - `git revert <commit>` : annuler un commit proprement
        - Historique immuable : on ajoute, on ne supprime pas
        - Différence avec `reset` : revert est sûr pour les dépôts partagés
        """
    )


def reset_exercise_dir(force: bool) -> None:
    """Crée un répertoire ex11-revert vierge."""
    if EXERCISE_DIR.exists():
        if not force:
            print(
                "⚠️  Le dossier ex11-revert existe déjà.\n"
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
    """Initialise le dépôt avec 3 commits dont un buggé."""
    # Initialiser Git
    run_git("init", "-b", "main")

    # Commit 1 : index.html
    (EXERCISE_DIR / "README.md").write_text(build_readme_content(), encoding="utf-8")
    (EXERCISE_DIR / "index.html").write_text(build_index_html(), encoding="utf-8")
    run_git("add", "README.md", "index.html")
    run_git("commit", "-m", "Ajout de index.html")

    # Commit 2 : style.css
    (EXERCISE_DIR / "style.css").write_text(build_style_css(), encoding="utf-8")
    run_git("add", "style.css")
    run_git("commit", "-m", "Ajout de style.css")

    # Commit 3 : bug.js (le commit fautif)
    (EXERCISE_DIR / "bug.js").write_text(build_bug_js(), encoding="utf-8")
    run_git("add", "bug.js")
    run_git("commit", "-m", "Ajout de bug.js")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prépare le dossier ex11-revert pour l'exercice git revert."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée ex11-revert si le dossier existe déjà.",
    )
    args = parser.parse_args(argv)

    reset_exercise_dir(force=args.force)
    setup_git_repo()

    print("\n✅ Exercice prêt !")
    print(f"📁 Dossier créé : {EXERCISE_DIR}")
    print("📄 Fichiers : index.html, style.css, bug.js")
    print("🔧 3 commits créés (le dernier introduit un bug)")
    print(
        "\n📚 Consignes :\n"
        "   1. Identifiez le commit qui introduit le bug\n"
        "   2. Utilisez git revert pour annuler ce commit\n"
        "   3. Vérifiez que le bug est corrigé\n"
        "   4. Observez que l'historique contient le revert\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
