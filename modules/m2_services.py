# modules/m2_services.py
# Module M2 - Revenus Services
# Contrats O&M, ingénierie et conseil EnR

import pandas as pd

from config.constants import ANNEES


# Bloc 1 : Données des contrats de services (revenus base 2026 en k€)
# ---------------------------------------------------------------------------
CONTRATS = [
    {"client": "TotalEnergies Renew",  "type": "O&M",        "pays": "France",    "base_keur": 1_850},
    {"client": "Iberdrola Renovables", "type": "O&M",        "pays": "Espagne",   "base_keur": 2_100},
    {"client": "RWE Renewables",       "type": "Ingenierie", "pays": "Allemagne", "base_keur":   750},
    {"client": "Enel Green Power",     "type": "Conseil",    "pays": "Italie",    "base_keur":   480},
    {"client": "EDP Renewables",       "type": "O&M",        "pays": "Portugal",  "base_keur": 1_200},
    {"client": "Engie",                "type": "O&M",        "pays": "France",    "base_keur":   920},
    {"client": "Orsted",               "type": "Ingenierie", "pays": "Belgique",  "base_keur": 1_050},
    {"client": "PGE Energia",          "type": "Conseil",    "pays": "Pologne",   "base_keur":   310},
]


# Bloc 2 : Calcul des revenus annuels
# ---------------------------------------------------------------------------
def calculer_revenus_services(scenario: dict) -> pd.DataFrame:
    """
    Projette les revenus de chaque contrat de services sur 2026-2031.

    Paramètres
    ----------
    scenario : dict
        Dictionnaire issu de config.scenarios.get_scenario()

    Retourne
    --------
    pd.DataFrame
        Colonnes : client, type, pays, 2026, 2027, ..., 2031
        Valeurs en k€.
    """
    g = scenario["croissance_services"]

    resultats = []

    for contrat in CONTRATS:
        revenus_par_annee = {
            annee: round(contrat["base_keur"] * (1 + g) ** i, 1)
            for i, annee in enumerate(ANNEES)
        }
        resultats.append({
            "client": contrat["client"],
            "type":   contrat["type"],
            "pays":   contrat["pays"],
            **revenus_par_annee,
        })

    return pd.DataFrame(resultats)


# Bloc 3 : Agrégations
# ---------------------------------------------------------------------------
def aggreger_par_type(df_services: pd.DataFrame) -> pd.DataFrame:
    """
    Agrège les revenus services par type (O&M, Ingénierie, Conseil).
    """
    return df_services.groupby("type")[ANNEES].sum().reset_index()


def aggreger_total(df_services: pd.DataFrame) -> pd.Series:
    """
    Revenus services totaux par année (k€).
    """
    return df_services[ANNEES].sum()