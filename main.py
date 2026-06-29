# main.py
# Orchestrateur principal
# Usage : python main.py --scenario Base

import argparse
import sys

from config.scenarios import get_scenario
from modules.m1_revenus_ipp import calculer_revenus_ipp, aggreger_total as ipp_total
from modules.m2_services import calculer_revenus_services, aggreger_total as services_total


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

    # --- M1 : Revenus IPP ---
    print("▶ M1 - Calcul des revenus IPP (35 projets)...")
    df_ipp  = calculer_revenus_ipp(scenario)
    rev_ipp = ipp_total(df_ipp)
    print(f"   EBITDA IPP 2026 : {rev_ipp[2026]:>10,.0f} k€")
    print(f"   EBITDA IPP 2031 : {rev_ipp[2031]:>10,.0f} k€\n")

    # --- M2 : Revenus Services ---
    print("▶ M2 - Calcul des revenus services...")
    df_services  = calculer_revenus_services(scenario)
    rev_services = services_total(df_services)
    print(f"   Revenus services 2026 : {rev_services[2026]:>10,.0f} k€")
    print(f"   Revenus services 2031 : {rev_services[2031]:>10,.0f} k€\n")

    # --- Sous-total M1 + M2 ---
    print("─" * 55)
    sous_total_2026 = rev_ipp[2026] + rev_services[2026]
    sous_total_2031 = rev_ipp[2031] + rev_services[2031]
    print(f"   Sous-total 2026 : {sous_total_2026:>10,.0f} k€")
    print(f"   Sous-total 2031 : {sous_total_2031:>10,.0f} k€")
    print("─" * 55)


    # --- Les modules seront branchés ici au fil des étapes ---
    # M3 : HQ Standalone      → à venir
    # M4 : Financement        → à venir
    # M5 : Fiscalité          → à venir
    # M6 : Consolidation      → à venir

    print(f"\n{'=' * 55}\n")
    
    return {
        "scenario":     scenario_nom,
        "df_ipp":       df_ipp,
        "df_services":  df_services,
        "rev_ipp":      rev_ipp,
        "rev_services": rev_services,
    }


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