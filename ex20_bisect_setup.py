#!/usr/bin/env python3
"""
Prépare le répertoire de travail pour l'exercice "Déboguer avec git bisect".

Crée un dépôt ex20-bisect avec une série de commits dont l'un introduit
un bug dans une fonction. L'étudiant devra utiliser bisect pour le trouver.

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
EXERCISE_DIR = ROOT / "ex20-bisect"


def build_calc_v1() -> str:
    """Version 1 de calc.js - OK."""
    return dedent(
        """\
        // Calculatrice - v1

        function add(a, b) {
            return a + b;
        }

        function multiply(a, b) {
            return a * b;
        }

        // Test
        console.log('2 + 3 =', add(2, 3));        // Attendu: 5
        console.log('4 * 5 =', multiply(4, 5));  // Attendu: 20
        """
    )


def build_calc_v2() -> str:
    """Version 2 de calc.js - OK."""
    return dedent(
        """\
        // Calculatrice - v2

        function add(a, b) {
            return a + b;
        }

        function subtract(a, b) {
            return a - b;
        }

        function multiply(a, b) {
            return a * b;
        }

        // Test
        console.log('2 + 3 =', add(2, 3));        // Attendu: 5
        console.log('10 - 4 =', subtract(10, 4)); // Attendu: 6
        console.log('4 * 5 =', multiply(4, 5));  // Attendu: 20
        """
    )


def build_calc_v3() -> str:
    """Version 3 de calc.js - OK."""
    return dedent(
        """\
        // Calculatrice - v3

        function add(a, b) {
            return a + b;
        }

        function subtract(a, b) {
            return a - b;
        }

        function multiply(a, b) {
            return a * b;
        }

        function divide(a, b) {
            if (b === 0) return 'Error';
            return a / b;
        }

        // Test
        console.log('2 + 3 =', add(2, 3));        // Attendu: 5
        console.log('10 - 4 =', subtract(10, 4)); // Attendu: 6
        console.log('4 * 5 =', multiply(4, 5));  // Attendu: 20
        console.log('20 / 4 =', divide(20, 4));  // Attendu: 5
        """
    )


def build_calc_v4_buggy() -> str:
    """Version 4 de calc.js - BUG INTRODUIT !"""
    return dedent(
        """\
        // Calculatrice - v4

        function add(a, b) {
            return a + b;
        }

        function subtract(a, b) {
            return a - b;
        }

        function multiply(a, b) {
            return a + b;  // BUG ! Devrait être a * b
        }

        function divide(a, b) {
            if (b === 0) return 'Error';
            return a / b;
        }

        // Test
        console.log('2 + 3 =', add(2, 3));        // Attendu: 5
        console.log('10 - 4 =', subtract(10, 4)); // Attendu: 6
        console.log('4 * 5 =', multiply(4, 5));  // BUGGY: retourne 9 au lieu de 20 !
        console.log('20 / 4 =', divide(20, 4));  // Attendu: 5
        """
    )


def build_calc_v5() -> str:
    """Version 5 de calc.js - Bug toujours présent."""
    return dedent(
        """\
        // Calculatrice - v5

        function add(a, b) {
            return a + b;
        }

        function subtract(a, b) {
            return a - b;
        }

        function multiply(a, b) {
            return a + b;  // BUG toujours là !
        }

        function divide(a, b) {
            if (b === 0) return 'Error';
            return a / b;
        }

        function power(a, b) {
            return Math.pow(a, b);
        }

        // Test
        console.log('2 + 3 =', add(2, 3));
        console.log('10 - 4 =', subtract(10, 4));
        console.log('4 * 5 =', multiply(4, 5));  // BUGGY
        console.log('20 / 4 =', divide(20, 4));
        console.log('2 ^ 8 =', power(2, 8));
        """
    )


def build_calc_v6() -> str:
    """Version 6 de calc.js - Bug toujours présent."""
    return dedent(
        """\
        // Calculatrice - v6

        function add(a, b) {
            return a + b;
        }

        function subtract(a, b) {
            return a - b;
        }

        function multiply(a, b) {
            return a + b;  // BUG toujours là !
        }

        function divide(a, b) {
            if (b === 0) return 'Error';
            return a / b;
        }

        function power(a, b) {
            return Math.pow(a, b);
        }

        function modulo(a, b) {
            return a % b;
        }

        // Test
        console.log('2 + 3 =', add(2, 3));
        console.log('10 - 4 =', subtract(10, 4));
        console.log('4 * 5 =', multiply(4, 5));  // BUGGY
        console.log('20 / 4 =', divide(20, 4));
        console.log('2 ^ 8 =', power(2, 8));
        console.log('17 % 5 =', modulo(17, 5));
        """
    )


def build_test_script() -> str:
    """Script de test pour aider à tester pendant le bisect."""
    return dedent(
        """\
        #!/bin/bash
        # Script de test pour git bisect
        # Usage: ./test.sh
        # Retourne 0 si OK, 1 si bug détecté

        # Exécuter le test de multiply
        result=$(node -e "
            const code = require('fs').readFileSync('calc.js', 'utf8');
            eval(code.replace(/console\\.log.*$/gm, ''));
            const result = multiply(4, 5);
            process.exit(result === 20 ? 0 : 1);
        " 2>/dev/null)

        exit $?
        """
    )


def build_readme_content() -> str:
    """Retourne le contenu du fichier README.md."""
    return dedent(
        """\
        # 🔍 Exercice : Déboguer avec git bisect

        ## 🎯 Objectif
        Utiliser `git bisect` pour retrouver le commit qui a introduit un bug.

        ## 📁 État initial
        - 6 commits dans l'historique
        - La fonction `multiply` est bugguée : elle fait une addition au lieu d'une multiplication !
        - Le bug a été introduit à un moment donné dans l'historique

        ## 🐛 Le bug
        ```javascript
        multiply(4, 5)  // Retourne 9 au lieu de 20 !
        ```

        ## 📋 Étapes à suivre

        1. **Constater le bug** :
           - `node calc.js`
           - Observez que `4 * 5` donne un mauvais résultat

        2. **Trouver un commit "bon"** :
           - `git log --oneline` pour voir l'historique
           - Le premier commit devrait être correct

        3. **Lancer bisect** :
           - `git bisect start`
           - `git bisect bad` (HEAD est mauvais)
           - `git bisect good <hash-premier-commit>`

        4. **Tester chaque étape** :
           - Git vous place sur un commit au milieu
           - Testez : `node calc.js`
           - Si OK : `git bisect good`
           - Si bug : `git bisect bad`

        5. **Trouver le coupable** :
           - Git annonce le commit fautif
           - Notez son hash et son message

        6. **Terminer** :
           - `git bisect reset` pour revenir à HEAD

        ## 💡 Astuces
        - Bisect utilise une recherche binaire (très rapide !)
        - Vous pouvez automatiser avec : `git bisect run ./test.sh`
        - Le script `test.sh` est fourni pour l'automatisation

        ## 🔑 Concepts clés
        - `git bisect start` : démarrer la recherche
        - `git bisect good/bad` : marquer les commits
        - `git bisect reset` : terminer et revenir à HEAD
        - Recherche binaire : O(log n) au lieu de O(n)
        """
    )


def reset_exercise_dir(force: bool) -> None:
    """Crée un répertoire ex20-bisect vierge."""
    if EXERCISE_DIR.exists():
        if not force:
            print(
                "⚠️  Le dossier ex20-bisect existe déjà.\n"
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
    """Initialise le dépôt avec l'historique contenant le bug."""
    run_git("init", "-b", "main")

    # Commit 1 : v1 (OK)
    (EXERCISE_DIR / "README.md").write_text(build_readme_content(), encoding="utf-8")
    (EXERCISE_DIR / "calc.js").write_text(build_calc_v1(), encoding="utf-8")
    (EXERCISE_DIR / "test.sh").write_text(build_test_script(), encoding="utf-8")
    (EXERCISE_DIR / "test.sh").chmod(0o755)
    run_git("add", ".")
    run_git("commit", "-m", "v1: add et multiply de base")

    # Commit 2 : v2 (OK)
    (EXERCISE_DIR / "calc.js").write_text(build_calc_v2(), encoding="utf-8")
    run_git("add", "calc.js")
    run_git("commit", "-m", "v2: ajout de subtract")

    # Commit 3 : v3 (OK)
    (EXERCISE_DIR / "calc.js").write_text(build_calc_v3(), encoding="utf-8")
    run_git("add", "calc.js")
    run_git("commit", "-m", "v3: ajout de divide")

    # Commit 4 : v4 (BUG INTRODUIT)
    (EXERCISE_DIR / "calc.js").write_text(build_calc_v4_buggy(), encoding="utf-8")
    run_git("add", "calc.js")
    run_git("commit", "-m", "v4: refactoring du code")

    # Commit 5 : v5 (bug toujours là)
    (EXERCISE_DIR / "calc.js").write_text(build_calc_v5(), encoding="utf-8")
    run_git("add", "calc.js")
    run_git("commit", "-m", "v5: ajout de power")

    # Commit 6 : v6 (bug toujours là)
    (EXERCISE_DIR / "calc.js").write_text(build_calc_v6(), encoding="utf-8")
    run_git("add", "calc.js")
    run_git("commit", "-m", "v6: ajout de modulo")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prépare le dossier ex20-bisect pour l'exercice git bisect."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Supprime puis recrée ex20-bisect si le dossier existe déjà.",
    )
    args = parser.parse_args(argv)

    reset_exercise_dir(force=args.force)
    setup_git_repo()

    print("\n✅ Exercice prêt !")
    print(f"📁 Dossier créé : {EXERCISE_DIR}")
    print("📝 6 commits créés, un bug a été introduit...")
    print("🔧 Script test.sh fourni pour automatiser les tests")
    print(
        "\n📚 Consignes :\n"
        "   1. Constatez le bug avec node calc.js\n"
        "   2. Utilisez git bisect pour trouver le commit fautif\n"
        "   3. Testez manuellement ou avec ./test.sh\n"
        "   4. Identifiez le commit responsable\n"
        "\n💡 Bon courage !\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
