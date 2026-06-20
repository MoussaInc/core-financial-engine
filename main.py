# main.py
# Orchestrateur principal
# Usage : python main.py --scenario Base

import argparse
import sys

from config.scenarios import get_scenario


def run(scenario_nom: str) -> None:
    """
    Point d'entrée principal du moteur de calcul.
    Orchestre l'exécution des 6 modules dans l'ordre.
    """
    print(f"\n{'=' * 55}")
    print(f"  CO-RE Financial Engine  |  Scénario : {scenario_nom}")
    print(f"{'=' * 55}\n")

    # Chargement du scénario
    scenario = get_scenario(scenario_nom)
    print(f"  {scenario['description']}\n")

    # --- Les modules seront branchés ici au fil des étapes ---
    # M1 : Revenus IPP        → à venir
    # M2 : Services           → à venir
    # M3 : HQ Standalone      → à venir
    # M4 : Financement        → à venir
    # M5 : Fiscalité          → à venir
    # M6 : Consolidation      → à venir

    print("  [OK] Scénario chargé avec succès.")
    print(f"\n{'=' * 55}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CO-RE Financial Engine")
    parser.add_argument(
        "--scenario",
        default="Base",
        choices=["Base", "High", "Stress"],
        help="Scénario de calcul (défaut : Base)",
    )
    args = parser.parse_args()

    run(scenario_nom=args.scenario)