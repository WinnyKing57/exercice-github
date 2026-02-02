#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Conflit complexe sur plusieurs blocs".

Crée un dossier ex09-conflict-complex avec un dépôt Git où deux branches
modifient le header ET le footer de page.html différemment, créant
plusieurs conflits à résoudre.

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
EXERCISE_DIR = ROOT / "ex09-conflict-complex"


def build_page_html_base() -> str:
    """Retourne le contenu initial de page.html."""
    return dedent(
        """\
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Ma Page</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; }
                header { padding: 1rem; background: #eee; }
                main { padding: 2rem; }
                footer { padding: 1rem; background: #eee; }
            </style>
        </head>
        <body>
            <header>
                <h1>Titre du site</h1>
            </header>
            <main>
                <p>Contenu principal de la page.</p>
            </main>
            <footer>
                <p>Pied de page</p>
            </footer>
        </body>
        </html>
        """
    )


def build_page_html_design_v1() -> str:
    """Retourne le contenu de page.html pour design-v1 (style moderne)."""
    return dedent(
        """\
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Ma Page</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; }
                header { padding: 1rem; background: #eee; }
                main { padding: 2rem; }
                footer { padding: 1rem; background: #eee; }
            </style>
        </head>
        <body>
            <header>
                <h1>🚀 Site Moderne</h1>
                <nav>
                    <a href="#accueil">Accueil</a>
                    <a href="#services">Services</a>
                </nav>
            </header>
            <main>
                <p>Contenu principal de la page.</p>
            </main>
            <footer>
                <p>© 2025 Site Moderne - Design V1</p>
                <p>Suivez-nous sur les réseaux sociaux</p>
            </footer>
        </body>
        </html>
        """
    )


def build_page_html_design_v2() -> str:
    """Retourne le contenu de page.html pour design-v2 (style corporate)."""
    return dedent(
        """\
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Ma Page</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; }
                header { padding: 1rem; background: #eee; }
                main { padding: 2rem; }
                footer { padding: 1rem; background: #eee; }
            </style>
        </head>
        <body>
            <header>
                <h1>Entreprise Corporate</h1>
                <p class="tagline">Votre partenaire de confiance depuis 1990</p>
            </header>
            <main>
                <p>Contenu principal de la page.</p>
            </main>
            <footer>
                <p>Entreprise Corporate SARL - Mentions légales</p>
                <p>Contact : contact@corporate.fr</p>
            </footer>
        </body>
        </html>
        """
    )


def build_readme_content() -> str:
    """Retourne le contenu du fichier README.md."""
    return dedent(
        """\
        # 🔥 Exercice : Conflits multiples

        ## 🎯 Objectif
        Résoudre un conflit impliquant PLUSIEURS sections d'un même fichier.

        ## 📁 État initial
        - Branche `design-v1` modifie le header ET le footer (style moderne avec emojis)
        - Branche `design-v2` modifie aussi le header ET le footer (style corporate)
        - Un merge a été tenté → CONFLITS MULTIPLES dans `page.html`

        ## 📊 Visualisation des conflits
        ```
        page.html contient 2 blocs en conflit :
        - CONFLIT 1 : dans le <header>
        - CONFLIT 2 : dans le <footer>
        ```

        ## 📋 Étapes à suivre

        1. **Identifier les conflits** :
           - Ouvrez `page.html`
           - Comptez le nombre de blocs `<<<<<<<` ... `>>>>>>>`

        2. **Résoudre chaque bloc** :
           - Pour le header : choisissez un style ou combinez les deux
           - Pour le footer : idem

        3. **Vérifier la cohérence** :
           - Le HTML doit rester valide
           - Le style doit être cohérent (ne pas mélanger moderne et corporate)

        4. **Finaliser le merge** :
           - Ajoutez le fichier résolu
           - Créez le commit de merge

        ## 💡 Astuces
        - Traitez les conflits UN PAR UN, de haut en bas
        - Gardez une vision globale : le résultat doit être cohérent
        - Vous pouvez créer une TROISIÈME version qui combine le meilleur des deux

        ## 🔑 Concepts clés
        - Conflits multiples dans un même fichier
        - Stratégie de résolution cohérente
        - Importance de tester le résultat final
        """
    )


def reset_exercise_dir(force: bool) -> None:
    """Crée un répertoire ex09-conflict-complex vierge."""
    if EXERCISE_DIR.exists():
        if not force:
            print(
                "⚠️  Le dossier ex09-conflict-complex existe déjà.\n"
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
    """Initialise le dépôt et crée les conflits multiples."""
    # Écrire les fichiers initiaux
    (EXERCISE_DIR / "README.md").write_text(build_readme_content(), encoding="utf-8")
    (EXERCISE_DIR / "page.html").write_text(build_page_html_base(), encoding="utf-8")

    # Initialiser Git et créer le commit initial sur main
    run_git("init", "-b", "main")
    run_git("add", ".")
    run_git("commit", "-m", "Initial commit : page de base")

    # Créer la branche design-v1
    run_git("checkout", "-b", "design-v1")
    (EXERCISE_DIR / "page.html").write_text(build_page_html_design_v1(), encoding="utf-8")
    run_git("add", "page.html")
    run_git("commit", "-m", "Design moderne avec navigation et réseaux sociaux")

    # Créer la branche design-v2 depuis main
    run_git("checkout", "main")
    run_git("checkout", "-b", "design-v2")
    (EXERCISE_DIR / "page.html").write_text(build_page_html_design_v2(), encoding="utf-8")
    run_git("add", "page.html")
    run_git("commit", "-m", "Design corporate avec tagline et contact")

    # Revenir sur design-v1 et tenter le merge (provoque les conflits)
    run_git("checkout", "design-v1")
    run_git("merge", "design-v2", check=False)  # Échouera avec conflits


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prépare le dossier ex09-conflict-complex pour l'exercice conflits multiples."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée ex09-conflict-complex si le dossier existe déjà.",
    )
    args = parser.parse_args(argv)

    reset_exercise_dir(force=args.force)
    setup_git_repo()

    print("\n✅ Exercice prêt !")
    print(f"📁 Dossier créé : {EXERCISE_DIR}")
    print("🌿 Branche actuelle : design-v1")
    print("🔥 CONFLITS MULTIPLES créés dans page.html (merge de design-v2 en cours)")
    print(
        "\n📚 Consignes :\n"
        "   1. Identifiez le nombre de blocs en conflit\n"
        "   2. Résolvez chaque conflit de manière cohérente\n"
        "   3. Vérifiez que le HTML final est valide\n"
        "   4. Finalisez le merge avec un commit\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
