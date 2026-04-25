"""
astrology.py — Chinese Astrology + Numerology Feature Engine
Computes zodiac animals, elements, compatibility scores, and numerology
numbers for NBA players. All outputs feed directly into the ML models.
"""

from datetime import date
from typing import Dict, List, Tuple


# ─────────────────────────────────────────────
# CHINESE ZODIAC TABLES
# ─────────────────────────────────────────────

ZODIAC_ANIMALS = [
    "Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake",
    "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"
]

# Five elements cycle through each zodiac animal
ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]

# Element associated with each animal (traditional system)
ANIMAL_ELEMENT = {
    "Rat": "Water", "Ox": "Earth", "Tiger": "Wood", "Rabbit": "Wood",
    "Dragon": "Earth", "Snake": "Fire", "Horse": "Fire", "Goat": "Earth",
    "Monkey": "Metal", "Rooster": "Metal", "Dog": "Earth", "Pig": "Water",
}

# Clashing pairs (opposite in the zodiac wheel)
ZODIAC_CLASHES = [
    {"Rat", "Horse"}, {"Ox", "Goat"}, {"Tiger", "Monkey"},
    {"Rabbit", "Rooster"}, {"Dragon", "Dog"}, {"Snake", "Pig"},
]

# Best match trios (san he / three harmonies)
ZODIAC_TRIOS = [
    {"Rat", "Dragon", "Monkey"},
    {"Ox", "Snake", "Rooster"},
    {"Tiger", "Horse", "Dog"},
    {"Rabbit", "Goat", "Pig"},
]

# Element interactions
ELEMENT_GENERATES = {  # generates → strong synergy
    "Wood": "Fire", "Fire": "Earth", "Earth": "Metal",
    "Metal": "Water", "Water": "Wood",
}
ELEMENT_CONTROLS = {  # controls → conflict
    "Wood": "Earth", "Earth": "Water", "Water": "Fire",
    "Fire": "Metal", "Metal": "Wood",
}

# 2026 is the Year of the Horse
CURRENT_YEAR = 2026
CURRENT_YEAR_ANIMAL = "Horse"


# ─────────────────────────────────────────────
# ZODIAC HELPERS
# ─────────────────────────────────────────────

def get_zodiac_animal(birth_year: int) -> str:
    return ZODIAC_ANIMALS[(birth_year - 4) % 12]


def get_birth_element(birth_year: int) -> str:
    """Returns element from birth year (pairs of years share an element)."""
    return ELEMENTS[((birth_year - 4) // 2) % 5]


def get_animal_element(animal: str) -> str:
    return ANIMAL_ELEMENT.get(animal, "Earth")


def zodiac_compatibility(animal1: str, animal2: str) -> int:
    """Returns compatibility score 0-100 between two zodiac animals."""
    pair = {animal1, animal2}

    # Clash = very low
    for clash in ZODIAC_CLASHES:
        if pair == clash:
            return 15

    # Trio match = excellent
    for trio in ZODIAC_TRIOS:
        if animal1 in trio and animal2 in trio:
            return 92

    # Same animal = good
    if animal1 == animal2:
        return 80

    # Element relationship
    elem1 = get_animal_element(animal1)
    elem2 = get_animal_element(animal2)

    if ELEMENT_GENERATES.get(elem1) == elem2:
        return 78  # elem1 generates elem2 — supportive
    if ELEMENT_GENERATES.get(elem2) == elem1:
        return 75  # elem2 generates elem1 — also good
    if ELEMENT_CONTROLS.get(elem1) == elem2:
        return 35  # elem1 controls elem2 — friction
    if ELEMENT_CONTROLS.get(elem2) == elem1:
        return 40  # elem2 controls elem1 — friction

    return 60  # neutral


def luck_modifier_for_year(animal: str, year: int = CURRENT_YEAR) -> float:
    """
    Returns a -0.12 to +0.12 modifier based on how well the player's
    zodiac animal interacts with the current year's animal.
    """
    year_animal = ZODIAC_ANIMALS[(year - 4) % 12]
    compat = zodiac_compatibility(animal, year_animal)
    return (compat - 60) / 350.0  # normalize around 0


# ─────────────────────────────────────────────
# NUMEROLOGY
# ─────────────────────────────────────────────

MASTER_NUMBERS = {11, 22, 33}
POWER_NUMBERS = {1, 3, 9, 11, 22, 33}


def _reduce(n: int) -> int:
    """Reduce a number to a single digit, preserving master numbers."""
    while n > 9 and n not in MASTER_NUMBERS:
        n = sum(int(d) for d in str(n))
    return n


def life_path_number(birthdate: date) -> int:
    """Classic numerology life path: reduce each component then sum."""
    m = _reduce(birthdate.month)
    d = _reduce(birthdate.day)
    y = _reduce(sum(int(c) for c in str(birthdate.year)))
    return _reduce(m + d + y)


def personal_year_number(birthdate: date, year: int = CURRENT_YEAR) -> int:
    """
    Personal Year = reduced(birth_month + birth_day + current_year_digits).
    Resets each birthday; indicates overall theme for that year.
    """
    m = _reduce(birthdate.month)
    d = _reduce(birthdate.day)
    y = _reduce(sum(int(c) for c in str(year)))
    return _reduce(m + d + y)


def personal_day_number(birthdate: date, game_date: date) -> int:
    """
    Personal Day = reduced(personal_year + game_month + game_day).
    Most granular numerology indicator — specific to each game.
    """
    py = personal_year_number(birthdate, game_date.year)
    m = _reduce(game_date.month)
    d = _reduce(game_date.day)
    return _reduce(py + m + d)


# ─────────────────────────────────────────────
# PLAYER ASTRO SCORE
# ─────────────────────────────────────────────

def player_astro_score(birthdate: date, game_date: date) -> Dict:
    """
    Compute a single player's full astrological profile for a given game date.
    Returns a dict with all raw values and a composite 0-100 score.
    """
    animal = get_zodiac_animal(birthdate.year)
    birth_elem = get_birth_element(birthdate.year)
    lp = life_path_number(birthdate)
    py = personal_year_number(birthdate, game_date.year)
    pd_ = personal_day_number(birthdate, game_date)
    luck = luck_modifier_for_year(animal)
    power_day = pd_ in POWER_NUMBERS

    # Build composite score around 50 baseline
    score = 50.0
    score += luck * 120                  # year luck: ±~14 pts
    score += (power_day * 12)            # power personal day: +12
    score += (_reduce(lp) / 33.0) * 8   # higher life path = slight boost
    score += (py / 33.0) * 5            # personal year energy
    score = round(min(100.0, max(0.0, score)), 1)

    return {
        "animal":       animal,
        "element":      birth_elem,
        "life_path":    lp,
        "personal_year": py,
        "personal_day": pd_,
        "power_day":    power_day,
        "luck_modifier": round(luck, 4),
        "astro_score":  score,
    }


# ─────────────────────────────────────────────
# TEAM ASTRO FEATURES  (what the model ingests)
# ─────────────────────────────────────────────

def _avg_pair_compat(animals: List[str]) -> float:
    """Average pairwise zodiac compatibility across a list of animals."""
    if len(animals) < 2:
        return 60.0
    scores = [
        zodiac_compatibility(animals[i], animals[j])
        for i in range(len(animals))
        for j in range(i + 1, len(animals))
    ]
    return round(sum(scores) / len(scores), 1)


def _are_clashing(a1: str, a2: str) -> bool:
    return {a1, a2} in ZODIAC_CLASHES


def team_astro_features(
    home_bdays: List[date],
    away_bdays: List[date],
    game_date: date,
) -> Dict:
    """
    Computes all astrology/numerology features for a matchup.
    home_bdays / away_bdays: list of player birth dates (starters first).
    """
    home_profiles = [player_astro_score(bd, game_date) for bd in home_bdays]
    away_profiles = [player_astro_score(bd, game_date) for bd in away_bdays]

    home_avg = sum(p["astro_score"] for p in home_profiles) / max(len(home_profiles), 1)
    away_avg = sum(p["astro_score"] for p in away_profiles) / max(len(away_profiles), 1)

    home_animals = [p["animal"] for p in home_profiles]
    away_animals = [p["animal"] for p in away_profiles]

    home_compat = _avg_pair_compat(home_animals)
    away_compat = _avg_pair_compat(away_animals)

    # Star player (index 0) clash
    star_clash = (
        _are_clashing(home_animals[0], away_animals[0])
        if home_animals and away_animals else False
    )

    # Cross-team compatibility: home star vs away team average
    cross_scores = [
        zodiac_compatibility(home_animals[0], a)
        for a in away_animals
    ] if home_animals and away_animals else [60]
    cross_compat = sum(cross_scores) / len(cross_scores)

    return {
        # Scalar features fed to the model
        "home_avg_astro":    round(home_avg, 2),
        "away_avg_astro":    round(away_avg, 2),
        "astro_differential": round(home_avg - away_avg, 2),
        "home_team_compat":  home_compat,
        "away_team_compat":  away_compat,
        "compat_differential": round(home_compat - away_compat, 2),
        "star_clash":        float(star_clash),
        "cross_compat":      round(cross_compat, 2),
        "home_power_players": sum(1 for p in home_profiles if p["power_day"]),
        "away_power_players": sum(1 for p in away_profiles if p["power_day"]),
        # Full profiles for UI display
        "home_profiles":     home_profiles,
        "away_profiles":     away_profiles,
    }
