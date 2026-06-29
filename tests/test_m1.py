# tests/test_m1.py
# Tests unitaires du module M1 - Revenus IPP

import pytest
import pandas as pd

from config.scenarios import get_scenario
from config.constants import ANNEES, PAYS
from modules.m1_revenus_ipp import (
    PROJETS,
    calculer_revenus_ipp,
    aggreger_par_pays,
    aggreger_par_technologie,
    aggreger_total,
)


# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def scenario_base():
    return get_scenario("Base")

@pytest.fixture
def df_base(scenario_base):
    return calculer_revenus_ipp(scenario_base)


# Tests des données projets
# ---------------------------------------------------------------------------
def test_projets_nombre():
    """Le portefeuille contient exactement 35 projets."""
    assert len(PROJETS) == 35


def test_projets_colonnes():
    """Toutes les colonnes attendues sont présentes."""
    colonnes_attendues = [
        "id_projet", "nom", "technologie", "pays",
        "capacite_mw", "tarif_eur_mwh", "facteur_charge",
        "disponibilite", "annee_cod", "duree_contrat", "opex_eur_mw",
    ]
    for col in colonnes_attendues:
        assert col in PROJETS.columns, f"Colonne manquante : {col}"


def test_projets_valeurs_coherentes():
    """Les valeurs des paramètres sont dans des plages réalistes."""
    assert PROJETS["capacite_mw"].between(1, 500).all()
    assert PROJETS["facteur_charge"].between(0.10, 0.60).all()
    assert PROJETS["disponibilite"].between(0.80, 1.00).all()
    assert PROJETS["tarif_eur_mwh"].between(10, 200).all()
    assert PROJETS["annee_cod"].between(2015, 2025).all()


def test_projets_reproductibles():
    """Les données générées sont identiques à chaque appel (seed fixe)."""
    from modules.m1_revenus_ipp import _generer_projets
    df1 = _generer_projets()
    df2 = _generer_projets()
    pd.testing.assert_frame_equal(df1, df2)


# Tests du calcul EBITDA
# ---------------------------------------------------------------------------
def test_calculer_revenus_shape(df_base):
    """Le DataFrame retourné a la bonne forme : 35 lignes, 10 colonnes."""
    assert df_base.shape == (35, 10)  # 4 colonnes info + 6 années


def test_calculer_revenus_colonnes(df_base):
    """Les colonnes années sont bien présentes."""
    for annee in ANNEES:
        assert annee in df_base.columns, f"Colonne {annee} manquante"


def test_ebitda_positif_majoritaire(df_base):
    """La majorité des EBITDA actifs sont positifs."""
    valeurs = df_base[ANNEES].values.flatten()
    valeurs_actives = valeurs[valeurs != 0.0]
    taux_positif = (valeurs_actives > 0).mean()
    assert taux_positif > 0.80, f"Trop d'EBITDA négatifs : {taux_positif:.0%}"


def test_ebitda_croissant_base(df_base):
    """L'EBITDA total doit croître de 2026 à 2031 en scénario Base."""
    total = aggreger_total(df_base)
    assert total[2031] > total[2026], "L'EBITDA total devrait croître sur la période"


def test_scenario_stress_inferieur_base():
    """L'EBITDA total en Stress doit être inférieur au scénario Base."""
    df_stress = calculer_revenus_ipp(get_scenario("Stress"))
    df_base   = calculer_revenus_ipp(get_scenario("Base"))
    assert aggreger_total(df_stress)[2026] < aggreger_total(df_base)[2026]


def test_scenario_high_superieur_base():
    """L'EBITDA total en High doit être supérieur au scénario Base."""
    df_high = calculer_revenus_ipp(get_scenario("High"))
    df_base = calculer_revenus_ipp(get_scenario("Base"))
    assert aggreger_total(df_high)[2026] > aggreger_total(df_base)[2026]


# Tests des agrégations
# ---------------------------------------------------------------------------

def test_aggreger_par_pays_shape(df_base):
    """L'agrégation par pays retourne autant de lignes que de pays."""
    df_pays = aggreger_par_pays(df_base)
    assert len(df_pays) == len(PROJETS["pays"].unique())


def test_aggreger_par_pays_total_coherent(df_base):
    """La somme par pays doit égaler le total consolidé."""
    total_pays = aggreger_par_pays(df_base)[ANNEES].sum()
    total       = aggreger_total(df_base)
    pd.testing.assert_series_equal(total_pays, total, check_names=False)


def test_aggreger_par_technologie(df_base):
    """L'agrégation par technologie retourne les 4 technologies."""
    df_tech = aggreger_par_technologie(df_base)
    assert len(df_tech) == 4


def test_aggreger_total_type(df_base):
    """aggreger_total() retourne bien une pd.Series."""
    total = aggreger_total(df_base)
    assert isinstance(total, pd.Series)
    assert list(total.index) == ANNEES