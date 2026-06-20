# config/constants.py
# Constantes globales

# --- Période de projection ---
ANNEES = list(range(2026, 2032))  # [2026, 2027, 2028, 2029, 2030, 2031]

# --- Pays de consolidation fiscale ---
PAYS = [
    "France",
    "Espagne",
    "Allemagne",
    "Italie",
    "Portugal",
    "Belgique",
    "Pologne",
]

# --- Taux d'imposition sur les sociétés par pays ---
TAUX_IS = {
    "France":    0.25,
    "Espagne":   0.25,
    "Allemagne": 0.30,
    "Italie":    0.24,
    "Portugal":  0.21,
    "Belgique":  0.25,
    "Pologne":   0.19,
}

# --- Paramètres du solveur itératif (circularité DSCR) ---
EPSILON_CONVERGENCE = 1.0   # tolérance en euros
MAX_ITERATIONS      = 100

# --- Nombre de projets IPP ---
NB_PROJETS_IPP = 35