# modules/m1_revenus_ipp.py
# Module M1 - Revenus IPP (Independent Power Producer)
# 35 projets en régime project finance
# Technologies : PV solaire, éolien terrestre, éolien offshore, stockage BESS

import numpy as np
import pandas as pd

from config.constants import ANNEES, NB_PROJETS_IPP


# ---------------------------------------------------------------------------
# Bloc 1 : Données des 35 projets
# ---------------------------------------------------------------------------

def _generer_projets() -> pd.DataFrame:
    """
    Génère un portefeuille fictif mais réaliste de 35 projets EnR.
    Le préfixe _ indique que cette fonction est privée au module.
    """
    np.random.seed(42)  # graine fixe : résultats reproductibles à chaque run

    technologies = (
        ["Solaire PV"]      * 15
        + ["Eolien terrestre"] * 12
        + ["Eolien offshore"]  * 5
        + ["Stockage BESS"]    * 3
    )

    pays = (
        ["France"]    * 10
        + ["Espagne"]   * 7
        + ["Allemagne"] * 5
        + ["Italie"]    * 5
        + ["Portugal"]  * 4
        + ["Belgique"]  * 2
        + ["Pologne"]   * 2
    )

    return pd.DataFrame({
        "id_projet":      [f"PRJ-{i:03d}" for i in range(1, NB_PROJETS_IPP + 1)],
        "nom":            [f"Projet_{i:03d}" for i in range(1, NB_PROJETS_IPP + 1)],
        "technologie":    technologies,
        "pays":           pays,
        # Capacité installée en MW
        "capacite_mw":    np.round(np.random.uniform(10, 250, NB_PROJETS_IPP), 1),
        # Tarif de rachat en €/MWh
        "tarif_eur_mwh":  np.round(np.random.uniform(45, 110, NB_PROJETS_IPP), 2),
        # Facteur de charge annuel
        "facteur_charge": np.round(np.random.uniform(0.18, 0.42, NB_PROJETS_IPP), 3),
        # Disponibilité technique
        "disponibilite":  np.round(np.random.uniform(0.93, 0.99, NB_PROJETS_IPP), 3),
        # Année de mise en service
        "annee_cod":      np.random.choice([2021, 2022, 2023, 2024, 2025], NB_PROJETS_IPP),
        # Durée du contrat de vente en années
        "duree_contrat":  np.random.choice([15, 20, 25], NB_PROJETS_IPP),
        # OPEX annuel en €/MW/an
        "opex_eur_mw":    np.round(np.random.uniform(12_000, 35_000, NB_PROJETS_IPP), 0),
    })


# Instance unique chargée au démarrage du module
PROJETS = _generer_projets()



# ---------------------------------------------------------------------------
# Bloc 2 : Calcul de l'EBITDA annuel par projet
# ---------------------------------------------------------------------------

def calculer_revenus_ipp(scenario: dict) -> pd.DataFrame:
    """
    Calcule l'EBITDA de chaque projet IPP sur 2026-2031.

    Paramètres
    ----------
    scenario : dict
        Dictionnaire issu de config.scenarios.get_scenario()

    Retourne
    --------
    pd.DataFrame
        Colonnes : id_projet, nom, pays, technologie, 2026, 2027, ..., 2031
        Valeurs en k€.
    """
    # Paramètres du scénario
    fp  = scenario["facteur_production"]
    fpe = scenario["facteur_prix_elec"]
    fo  = scenario["facteur_opex"]
    inf = scenario["taux_inflation"]

    resultats = []

    for _, projet in PROJETS.iterrows():
        revenus_par_annee = {}

        for i, annee in enumerate(ANNEES):

            # --- Conditions d'activation ---
            annees_exploitation = annee - projet["annee_cod"]
            en_service          = annees_exploitation >= 0
            contrat_actif       = annees_exploitation < projet["duree_contrat"]

            if not en_service or not contrat_actif:
                revenus_par_annee[annee] = 0.0
                continue

            # --- Production annuelle (MWh) ---
            production_mwh = (
                projet["capacite_mw"]
                * projet["facteur_charge"]
                * projet["disponibilite"]
                * fp
                * 8_760
            )

            # --- Tarif indexé (€/MWh) ---
            tarif_indexe = (
                projet["tarif_eur_mwh"]
                * fpe
                * (1 + 0.7 * inf) ** i
            )

            # --- Revenus bruts (€) ---
            revenus_bruts = production_mwh * tarif_indexe

            # --- OPEX (€) ---
            opex = (
                projet["opex_eur_mw"]
                * projet["capacite_mw"]
                * fo
                * (1 + inf) ** i
            )

            # --- EBITDA projet (k€) ---
            revenus_par_annee[annee] = round((revenus_bruts - opex) / 1_000, 1)

        resultats.append({
            "id_projet":   projet["id_projet"],
            "nom":         projet["nom"],
            "pays":        projet["pays"],
            "technologie": projet["technologie"],
            **revenus_par_annee,
        })

    return pd.DataFrame(resultats)



# ---------------------------------------------------------------------------
# Bloc 3 : Agrégations
# ---------------------------------------------------------------------------

def aggreger_par_pays(df_ipp: pd.DataFrame) -> pd.DataFrame:
    """
    Agrège l'EBITDA IPP par pays sur 2026-2031.

    Retourne
    --------
    pd.DataFrame
        Colonnes : pays, 2026, 2027, ..., 2031
        Valeurs en k€.
    """
    return (
        df_ipp
        .groupby("pays")[ANNEES]
        .sum()
        .reset_index()
    )


def aggreger_par_technologie(df_ipp: pd.DataFrame) -> pd.DataFrame:
    """
    Agrège l'EBITDA IPP par technologie sur 2026-2031.

    Retourne
    --------
    pd.DataFrame
        Colonnes : technologie, 2026, 2027, ..., 2031
        Valeurs en k€.
    """
    return (
        df_ipp
        .groupby("technologie")[ANNEES]
        .sum()
        .reset_index()
    )


def aggreger_total(df_ipp: pd.DataFrame) -> pd.Series:
    """
    EBITDA total consolidé de tous les projets IPP par année.

    Retourne
    --------
    pd.Series
        Index : années (2026, ..., 2031)
        Valeurs en k€.
    """
    return df_ipp[ANNEES].sum()



