# config/scenarios.py
# Switch de scénarios : Base / High / Stress

SCENARIOS = {
    "Base": {
        "description":         "Scénario central - hypothèses de marché normalisées",
        "facteur_prix_elec":   1.00,  # prix spot électricité : base 100%
        "facteur_production":  1.00,  # P50 de production
        "facteur_opex":        1.00,  # OPEX normatifs
        "taux_interet_dette":  0.045, # 4,5% fixe
        "gearing_cible":       0.70,  # 70% dette / valeur actif
        "croissance_services": 0.03,  # +3%/an sur revenus services
        "taux_inflation":      0.02,
    },
    "High": {
        "description":         "Scénario optimiste - prix élevés et surproduction",
        "facteur_prix_elec":   1.15,
        "facteur_production":  1.05,  # P75 de production
        "facteur_opex":        0.95,  # OPEX réduits de 5%
        "taux_interet_dette":  0.040,
        "gearing_cible":       0.72,
        "croissance_services": 0.05,
        "taux_inflation":      0.025,
    },
    "Stress": {
        "description":         "Scénario pessimiste - choc de marché et sous-production",
        "facteur_prix_elec":   0.80,
        "facteur_production":  0.92,  # P25 de production
        "facteur_opex":        1.10,  # OPEX majorés de 10%
        "taux_interet_dette":  0.055,
        "gearing_cible":       0.65,
        "croissance_services": 0.01,
        "taux_inflation":      0.015,
    },
}


def get_scenario(nom: str) -> dict:
    """
    Retourne les paramètres du scénario demandé.
    Lève une ValueError si le nom est inconnu.
    """
    if nom not in SCENARIOS:
        raise ValueError(
            f"Scénario inconnu : '{nom}'. "
            f"Valeurs acceptées : {list(SCENARIOS.keys())}"
        )
    return SCENARIOS[nom]