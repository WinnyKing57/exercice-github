#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Cherry-pick d'un commit utile".

Crée un dépôt ex19-cherry-pick avec une branche feature-a contenant un bugfix
intéressant et une branche release qui a besoin de ce fix sans le reste.

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
EXERCISE_DIR = ROOT / "ex19-cherry-pick"


def build_utils_base() -> str:
    """Retourne utils.js version de base."""
    return dedent(
        """\
        // Utilitaires de l'application

        function formatDate(date) {
            return date.toLocaleDateString();
        }

        function calculateTotal(items) {
            let total = 0;
            for (let item of items) {
                total += item.price;  // BUG: ne gère pas les quantités !
            }
            return total;
        }

        function validateEmail(email) {
            return email.includes('@');
        }

        module.exports = { formatDate, calculateTotal, validateEmail };
        """
    )


def build_utils_feature_a_wip() -> str:
    """Retourne utils.js avec travail en cours sur feature-a."""
    return dedent(
        """\
        // Utilitaires de l'application - Feature A en cours

        function formatDate(date) {
            return date.toLocaleDateString();
        }

        function formatDateTime(date) {
            // Nouvelle fonctionnalité en cours de développement
            return date.toLocaleString();
        }

        function calculateTotal(items) {
            let total = 0;
            for (let item of items) {
                total += item.price;  // BUG: ne gère pas les quantités !
            }
            return total;
        }

        function validateEmail(email) {
            return email.includes('@');
        }

        module.exports = { formatDate, formatDateTime, calculateTotal, validateEmail };
        """
    )


def build_utils_feature_a_bugfix() -> str:
    """Retourne utils.js avec le bugfix (commit à cherry-pick)."""
    return dedent(
        """\
        // Utilitaires de l'application - Feature A en cours

        function formatDate(date) {
            return date.toLocaleDateString();
        }

        function formatDateTime(date) {
            // Nouvelle fonctionnalité en cours de développement
            return date.toLocaleString();
        }

        function calculateTotal(items) {
            let total = 0;
            for (let item of items) {
                // BUGFIX: prise en compte des quantités
                const quantity = item.quantity || 1;
                total += item.price * quantity;
            }
            return total;
        }

        function validateEmail(email) {
            return email.includes('@');
        }

        module.exports = { formatDate, formatDateTime, calculateTotal, validateEmail };
        """
    )


def build_utils_feature_a_more() -> str:
    """Retourne utils.js avec encore plus de features."""
    return dedent(
        """\
        // Utilitaires de l'application - Feature A

        function formatDate(date) {
            return date.toLocaleDateString();
        }

        function formatDateTime(date) {
            return date.toLocaleString();
        }

        function formatCurrency(amount) {
            // Encore une nouvelle fonctionnalité
            return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(amount);
        }

        function calculateTotal(items) {
            let total = 0;
            for (let item of items) {
                // BUGFIX: prise en compte des quantités
                const quantity = item.quantity || 1;
                total += item.price * quantity;
            }
            return total;
        }

        function validateEmail(email) {
            return email.includes('@');
        }

        module.exports = { formatDate, formatDateTime, formatCurrency, calculateTotal, validateEmail };
        """
    )


def build_readme_content() -> str:
    """Retourne le contenu du fichier README.md."""
    return dedent(
        """\
        # 🍒 Exercice : Cherry-pick d'un commit utile

        ## 🎯 Objectif
        Récupérer un commit spécifique d'une branche sans importer tout son historique.

        ## 📁 État initial
        - Branche `release` : version stable, mais contient un bug dans `calculateTotal`
        - Branche `feature-a` : développement en cours avec :
          - Nouvelles fonctionnalités (pas encore prêtes pour la release)
          - Un bugfix pour `calculateTotal` (celui-ci est nécessaire !)

        ## 🐛 Le problème
        Le bug : `calculateTotal` ne prend pas en compte les quantités.
        Le fix existe sur `feature-a`, mais cette branche n'est pas prête à être mergée.

        ## 📋 Étapes à suivre

        1. **Explorer les branches** :
           - `git log --oneline feature-a`
           - Identifiez le commit qui corrige le bug (message : "Bugfix: calculateTotal...")

        2. **Basculer sur release** :
           - `git checkout release`

        3. **Cherry-pick le commit** :
           - Récupérez UNIQUEMENT le commit du bugfix
           - `git cherry-pick <hash-du-commit>`

        4. **Vérifier le résultat** :
           - `git log --oneline` : le commit apparaît sur release
           - Vérifiez que `utils.js` contient le fix
           - Vérifiez que les AUTRES fonctionnalités de feature-a ne sont PAS là

        ## 💡 Astuces
        - Le cherry-pick copie un commit (nouveau hash)
        - En cas de conflit, résolvez puis `git cherry-pick --continue`
        - Pour annuler : `git cherry-pick --abort`

        ## 🔑 Concepts clés
        - `git cherry-pick <commit>` : appliquer un commit spécifique
        - Différence avec merge : sélection chirurgicale
        - Utile pour les hotfixes sur des branches de release
        """
    )


def reset_exercise_dir(force: bool) -> None:
    """Crée un répertoire ex19-cherry-pick vierge."""
    if EXERCISE_DIR.exists():
        if not force:
            print(
                "⚠️  Le dossier ex19-cherry-pick existe déjà.\n"
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
    """Initialise le dépôt avec les branches nécessaires."""
    run_git("init", "-b", "main")

    # Commit initial sur main
    (EXERCISE_DIR / "README.md").write_text(build_readme_content(), encoding="utf-8")
    (EXERCISE_DIR / "utils.js").write_text(build_utils_base(), encoding="utf-8")
    run_git("add", ".")
    run_git("commit", "-m", "Initial commit : utilitaires de base")

    # Créer la branche release depuis ce point
    run_git("branch", "release")

    # Créer et développer feature-a
    run_git("checkout", "-b", "feature-a")

    # Commit 1 : WIP
    (EXERCISE_DIR / "utils.js").write_text(build_utils_feature_a_wip(), encoding="utf-8")
    run_git("add", "utils.js")
    run_git("commit", "-m", "WIP: ajout de formatDateTime")

    # Commit 2 : BUGFIX (celui à cherry-pick)
    (EXERCISE_DIR / "utils.js").write_text(build_utils_feature_a_bugfix(), encoding="utf-8")
    run_git("add", "utils.js")
    run_git("commit", "-m", "Bugfix: calculateTotal prend en compte les quantités")

    # Commit 3 : Plus de features
    (EXERCISE_DIR / "utils.js").write_text(build_utils_feature_a_more(), encoding="utf-8")
    run_git("add", "utils.js")
    run_git("commit", "-m", "Ajout de formatCurrency")

    # Revenir sur release pour l'exercice
    run_git("checkout", "release")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prépare le dossier ex19-cherry-pick pour l'exercice cherry-pick."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée ex19-cherry-pick si le dossier existe déjà.",
    )
    args = parser.parse_args(argv)

    reset_exercise_dir(force=args.force)
    setup_git_repo()

    print("\n✅ Exercice prêt !")
    print(f"📁 Dossier créé : {EXERCISE_DIR}")
    print("🌿 Branche actuelle : release (contient le bug)")
    print("🌿 Branche feature-a : contient le bugfix + d'autres commits")
    print(
        "\n📚 Consignes :\n"
        "   1. Identifiez le commit du bugfix sur feature-a\n"
        "   2. Sur release, faites un cherry-pick de ce commit\n"
        "   3. Vérifiez que seul le fix est appliqué\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
