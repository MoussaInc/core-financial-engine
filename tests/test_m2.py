# tests/test_m2.py
# Tests unitaires du module M2 - Revenus Services

import pytest
import pandas as pd

from config.scenarios import get_scenario
from config.constants import ANNEES
from modules.m2_services import (
    CONTRATS,
    calculer_revenus_services,
    aggreger_par_type,
    aggreger_total,
)


# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def scenario_base():
    return get_scenario("Base")

@pytest.fixture
def df_base(scenario_base):
    return calculer_revenus_services(scenario_base)


# Tests des données contrats
# ---------------------------------------------------------------------------
def test_contrats_nombre():
    """Le portefeuille contient 8 contrats de services."""
    assert len(CONTRATS) == 8


def test_contrats_cles_presentes():
    """Chaque contrat contient les clés attendues."""
    cles_attendues = ["client", "type", "pays", "base_keur"]
    for contrat in CONTRATS:
        for cle in cles_attendues:
            assert cle in contrat, f"Clé '{cle}' manquante dans {contrat['client']}"


def test_contrats_base_positive():
    """Tous les revenus de base sont positifs."""
    for contrat in CONTRATS:
        assert contrat["base_keur"] > 0, f"Revenu base négatif : {contrat['client']}"


def test_contrats_types_valides():
    """Les types de contrats sont parmi les valeurs attendues."""
    types_valides = {"O&M", "Ingenierie", "Conseil"}
    for contrat in CONTRATS:
        assert contrat["type"] in types_valides, (
            f"Type inconnu : {contrat['type']}"
        )


# Tests du calcul des revenus
# ---------------------------------------------------------------------------
def test_calculer_revenus_shape(df_base):
    """Le DataFrame retourné a la bonne forme : 8 lignes, 9 colonnes."""
    assert df_base.shape == (8, 9)  # 3 colonnes info + 6 années


def test_calculer_revenus_colonnes(df_base):
    """Les colonnes années sont bien présentes."""
    for annee in ANNEES:
        assert annee in df_base.columns, f"Colonne {annee} manquante"


def test_revenus_croissants_base(df_base):
    """En scénario Base, les revenus de chaque contrat croissent chaque année."""
    for _, row in df_base.iterrows():
        for i in range(len(ANNEES) - 1):
            assert row[ANNEES[i + 1]] >= row[ANNEES[i]], (
                f"Revenu décroissant pour {row['client']} entre "
                f"{ANNEES[i]} et {ANNEES[i+1]}"
            )


def test_revenus_2026_egaux_base():
    """En 2026 (i=0), les revenus doivent égaler la base (croissance^0 = 1)."""
    df = calculer_revenus_services(get_scenario("Base"))
    for i, contrat in enumerate(CONTRATS):
        assert df.iloc[i][2026] == contrat["base_keur"], (
            f"Revenu 2026 incorrect pour {contrat['client']}"
        )


def test_scenario_high_superieur_base():
    """Les revenus en High doivent être supérieurs au scénario Base."""
    total_high = aggreger_total(calculer_revenus_services(get_scenario("High")))
    total_base = aggreger_total(calculer_revenus_services(get_scenario("Base")))
    for annee in ANNEES[1:]:  # dès 2027, la croissance diverge
        assert total_high[annee] > total_base[annee]


def test_scenario_stress_inferieur_base():
    """Les revenus en Stress doivent être inférieurs au scénario Base."""
    total_stress = aggreger_total(calculer_revenus_services(get_scenario("Stress")))
    total_base   = aggreger_total(calculer_revenus_services(get_scenario("Base")))
    for annee in ANNEES[1:]:
        assert total_stress[annee] < total_base[annee]


# Tests des agrégations
# ---------------------------------------------------------------------------
def test_aggreger_par_type_shape(df_base):
    """L'agrégation par type retourne 3 lignes (O&M, Ingénierie, Conseil)."""
    df_type = aggreger_par_type(df_base)
    assert len(df_type) == 3


def test_aggreger_par_type_total_coherent(df_base):
    """La somme par type doit égaler le total consolidé."""
    total_type = aggreger_par_type(df_base)[ANNEES].sum()
    total      = aggreger_total(df_base)
    pd.testing.assert_series_equal(total_type, total, check_names=False)


def test_aggreger_total_type(df_base):
    """aggreger_total() retourne bien une pd.Series indexée par les années."""
    total = aggreger_total(df_base)
    assert isinstance(total, pd.Series)
    assert list(total.index) == ANNEES