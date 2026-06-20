# tests/test_scenarios.py
# Tests unitaires du module config.scenarios

import pytest
from config.scenarios import get_scenario, SCENARIOS


# --- Tests des scénarios valides ---

def test_scenarios_existants():
    """Les 3 scénarios attendus sont bien définis."""
    assert "Base"   in SCENARIOS
    assert "High"   in SCENARIOS
    assert "Stress" in SCENARIOS


def test_get_scenario_retourne_un_dict():
    """get_scenario() retourne bien un dictionnaire."""
    resultat = get_scenario("Base")
    assert isinstance(resultat, dict)


def test_get_scenario_contient_les_cles_attendues():
    """Chaque scénario contient toutes les clés requises par les modules."""
    cles_requises = [
        "description",
        "facteur_prix_elec",
        "facteur_production",
        "facteur_opex",
        "taux_interet_dette",
        "gearing_cible",
        "croissance_services",
        "taux_inflation",
    ]
    for nom in SCENARIOS:
        scenario = get_scenario(nom)
        for cle in cles_requises:
            assert cle in scenario, (f"Clé '{cle}' manquante dans le scénario '{nom}'")


def test_get_scenario_valeurs_coherentes():
    """Les valeurs numériques sont dans des plages réalistes."""
    for nom in SCENARIOS:
        s = get_scenario(nom)
        assert 0 < s["facteur_prix_elec"]   <= 2.0,  f"{nom}: facteur_prix_elec hors plage"
        assert 0 < s["facteur_production"]  <= 2.0,  f"{nom}: facteur_production hors plage"
        assert 0 < s["facteur_opex"]        <= 2.0,  f"{nom}: facteur_opex hors plage"
        assert 0 < s["taux_interet_dette"]  <  0.20, f"{nom}: taux_interet_dette hors plage"
        assert 0 < s["taux_inflation"]      <  0.10, f"{nom}: taux_inflation hors plage"


def test_get_scenario_stress_plus_pessimiste_que_base():
    """Le scénario Stress doit être plus défavorable que le scénario Base."""
    base   = get_scenario("Base")
    stress = get_scenario("Stress")
    assert stress["facteur_prix_elec"]  < base["facteur_prix_elec"]
    assert stress["facteur_production"] < base["facteur_production"]
    assert stress["facteur_opex"]       > base["facteur_opex"]
    assert stress["taux_interet_dette"] > base["taux_interet_dette"]


def test_get_scenario_high_plus_optimiste_que_base():
    """Le scénario High doit être plus favorable que le scénario Base."""
    base = get_scenario("Base")
    high = get_scenario("High")
    assert high["facteur_prix_elec"]  > base["facteur_prix_elec"]
    assert high["facteur_production"] > base["facteur_production"]
    assert high["facteur_opex"]       < base["facteur_opex"]
    assert high["taux_interet_dette"] < base["taux_interet_dette"]


# --- Tests des cas d'erreur ---

def test_get_scenario_nom_inconnu():
    """Un nom de scénario inconnu doit lever une ValueError."""
    with pytest.raises(ValueError):
        get_scenario("Inconnu")


def test_get_scenario_casse_sensible():
    """Le nom du scénario est sensible à la casse."""
    with pytest.raises(ValueError):
        get_scenario("base")  # minuscule → doit échouer