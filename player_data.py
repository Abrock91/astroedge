"""
player_data.py — NBA Player Birthdates, Rosters & Season Stats
Update TEAM_STATS each season; birthdates are permanent.
"""

from datetime import date

# ─────────────────────────────────────────────
# PLAYER BIRTHDATES  (add more players as needed)
# ─────────────────────────────────────────────

PLAYER_BIRTHDATES: dict[str, date] = {
    # ── Boston Celtics ──────────────────────
    "Jayson Tatum":        date(1998, 3, 3),
    "Jaylen Brown":        date(1996, 10, 24),
    "Jrue Holiday":        date(1990, 6, 12),
    "Al Horford":          date(1986, 6, 3),
    "Kristaps Porzingis":  date(1995, 8, 2),
    "Payton Pritchard":    date(1998, 1, 28),

    # ── Oklahoma City Thunder ───────────────
    "Shai Gilgeous-Alexander": date(1998, 7, 31),
    "Chet Holmgren":       date(2002, 5, 1),
    "Jalen Williams":      date(2001, 6, 6),
    "Lu Dort":             date(1999, 4, 16),
    "Isaiah Hartenstein":  date(1998, 5, 5),
    "Isaiah Joe":          date(1999, 9, 5),

    # ── Cleveland Cavaliers ─────────────────
    "Donovan Mitchell":    date(1996, 9, 7),
    "Darius Garland":      date(2000, 1, 26),
    "Evan Mobley":         date(2001, 6, 18),
    "Jarrett Allen":       date(1998, 4, 21),
    "Max Strus":           date(1996, 3, 28),
    "Caris LeVert":        date(1994, 2, 26),

    # ── Milwaukee Bucks ─────────────────────
    "Giannis Antetokounmpo": date(1994, 12, 6),
    "Damian Lillard":      date(1990, 7, 15),
    "Khris Middleton":     date(1991, 8, 12),
    "Brook Lopez":         date(1988, 4, 1),
    "Bobby Portis":        date(1995, 2, 10),

    # ── Denver Nuggets ──────────────────────
    "Nikola Jokic":        date(1995, 2, 19),
    "Jamal Murray":        date(1997, 2, 23),
    "Michael Porter Jr.":  date(1998, 6, 29),
    "Aaron Gordon":        date(1995, 9, 16),
    "Kentavious Caldwell-Pope": date(1993, 2, 18),

    # ── Minnesota Timberwolves ───────────────
    "Anthony Edwards":     date(2001, 8, 5),
    "Karl-Anthony Towns":  date(1995, 11, 15),
    "Rudy Gobert":         date(1992, 6, 26),
    "Mike Conley":         date(1987, 10, 11),
    "Nickeil Alexander-Walker": date(1998, 9, 2),

    # ── Golden State Warriors ────────────────
    "Stephen Curry":       date(1988, 3, 14),
    "Klay Thompson":       date(1990, 2, 8),
    "Draymond Green":      date(1990, 3, 4),
    "Andrew Wiggins":      date(1995, 2, 23),
    "Jonathan Kuminga":    date(2002, 10, 6),

    # ── Phoenix Suns ────────────────────────
    "Kevin Durant":        date(1988, 9, 29),
    "Devin Booker":        date(1996, 10, 30),
    "Bradley Beal":        date(1993, 6, 28),
    "Grayson Allen":       date(1995, 10, 8),
    "Jusuf Nurkic":        date(1994, 8, 23),

    # ── LA Lakers ───────────────────────────
    "LeBron James":        date(1984, 12, 30),
    "Anthony Davis":       date(1993, 3, 11),
    "Austin Reaves":       date(1998, 5, 29),
    "D'Angelo Russell":    date(1996, 2, 23),
    "Rui Hachimura":       date(1998, 2, 8),

    # ── Dallas Mavericks ────────────────────
    "Luka Doncic":         date(1999, 2, 28),
    "Kyrie Irving":        date(1992, 3, 23),
    "Tim Hardaway Jr.":    date(1992, 3, 16),
    "P.J. Washington":     date(1998, 8, 23),
    "Dereck Lively II":    date(2003, 2, 12),

    # ── Indiana Pacers ───────────────────────
    "Tyrese Haliburton":   date(2000, 2, 29),
    "Bennedict Mathurin":  date(2002, 6, 19),
    "Myles Turner":        date(1996, 3, 24),
    "Pascal Siakam":       date(1994, 4, 2),
    "T.J. McConnell":      date(1992, 3, 25),

    # ── New York Knicks ──────────────────────
    "Jalen Brunson":       date(1996, 8, 31),
    "Julius Randle":       date(1994, 11, 29),
    "RJ Barrett":          date(2000, 6, 14),
    "Josh Hart":           date(1995, 3, 6),
    "Mitchell Robinson":   date(1998, 4, 1),

    # ── Philadelphia 76ers ───────────────────
    "Joel Embiid":         date(1994, 3, 16),
    "Tyrese Maxey":        date(2000, 11, 4),
    "Paul George":         date(1990, 5, 1),
    "Tobias Harris":       date(1992, 7, 15),
    "Kelly Oubre Jr.":     date(1995, 12, 9),

    # ── Miami Heat ───────────────────────────
    "Jimmy Butler":        date(1989, 9, 14),
    "Bam Adebayo":         date(1997, 7, 18),
    "Tyler Herro":         date(2000, 1, 20),
    "Kyle Lowry":          date(1986, 3, 25),
    "Caleb Martin":        date(1995, 9, 28),

    # ── San Antonio Spurs ────────────────────
    "Victor Wembanyama":   date(2004, 1, 4),
    "Devin Vassell":       date(2000, 8, 23),
    "Jeremy Sochan":       date(2003, 5, 20),
    "Keldon Johnson":      date(1999, 10, 7),
    "Tre Jones":           date(1999, 1, 8),

    # ── Memphis Grizzlies ────────────────────
    "Ja Morant":           date(1999, 8, 10),
    "Jaren Jackson Jr.":   date(1999, 9, 15),
    "Desmond Bane":        date(1999, 6, 25),
    "Vince Williams Jr.":  date(2001, 9, 14),
    "Santi Aldama":        date(2001, 1, 20),

    # ── Sacramento Kings ─────────────────────
    "De'Aaron Fox":        date(1997, 12, 20),
    "Domantas Sabonis":    date(1996, 5, 3),
    "Malik Monk":          date(1998, 2, 4),
    "Kevin Huerter":       date(1998, 8, 27),
    "Keegan Murray":       date(2001, 8, 19),
}


# ─────────────────────────────────────────────
# TEAM ROSTERS  (starting 5: PG, SG, SF, PF, C)
# Only include players in PLAYER_BIRTHDATES above
# ─────────────────────────────────────────────

TEAM_ROSTERS: dict[str, list[str]] = {
    "Boston Celtics":        ["Jrue Holiday", "Jaylen Brown", "Jayson Tatum", "Al Horford", "Kristaps Porzingis"],
    "Oklahoma City Thunder": ["Shai Gilgeous-Alexander", "Lu Dort", "Jalen Williams", "Chet Holmgren", "Isaiah Hartenstein"],
    "Cleveland Cavaliers":   ["Darius Garland", "Donovan Mitchell", "Max Strus", "Evan Mobley", "Jarrett Allen"],
    "Milwaukee Bucks":       ["Damian Lillard", "Khris Middleton", "Giannis Antetokounmpo", "Bobby Portis", "Brook Lopez"],
    "Denver Nuggets":        ["Jamal Murray", "Kentavious Caldwell-Pope", "Michael Porter Jr.", "Aaron Gordon", "Nikola Jokic"],
    "Minnesota Timberwolves":["Mike Conley", "Nickeil Alexander-Walker", "Anthony Edwards", "Karl-Anthony Towns", "Rudy Gobert"],
    "Golden State Warriors": ["Stephen Curry", "Klay Thompson", "Andrew Wiggins", "Draymond Green", "Jonathan Kuminga"],
    "Phoenix Suns":          ["Devin Booker", "Bradley Beal", "Kevin Durant", "Grayson Allen", "Jusuf Nurkic"],
    "LA Lakers":             ["D'Angelo Russell", "Austin Reaves", "LeBron James", "Anthony Davis", "Rui Hachimura"],
    "Dallas Mavericks":      ["Luka Doncic", "Kyrie Irving", "Tim Hardaway Jr.", "P.J. Washington", "Dereck Lively II"],
    "Indiana Pacers":        ["Tyrese Haliburton", "Bennedict Mathurin", "Andrew Nembhard", "Pascal Siakam", "Myles Turner"],
    "New York Knicks":       ["Jalen Brunson", "Josh Hart", "RJ Barrett", "Julius Randle", "Mitchell Robinson"],
    "Philadelphia 76ers":    ["Tyrese Maxey", "Paul George", "Kelly Oubre Jr.", "Tobias Harris", "Joel Embiid"],
    "Miami Heat":            ["Kyle Lowry", "Tyler Herro", "Jimmy Butler", "Caleb Martin", "Bam Adebayo"],
    "San Antonio Spurs":     ["Tre Jones", "Devin Vassell", "Jeremy Sochan", "Keldon Johnson", "Victor Wembanyama"],
    "Memphis Grizzlies":     ["Ja Morant", "Desmond Bane", "Vince Williams Jr.", "Jaren Jackson Jr.", "Santi Aldama"],
    "Sacramento Kings":      ["De'Aaron Fox", "Malik Monk", "Kevin Huerter", "Domantas Sabonis", "Keegan Murray"],
}

# Replace any roster players not in PLAYER_BIRTHDATES with a dummy so we never KeyError
_ALL_KNOWN = set(PLAYER_BIRTHDATES.keys())
for _team, _roster in TEAM_ROSTERS.items():
    TEAM_ROSTERS[_team] = [p for p in _roster if p in _ALL_KNOWN]


# ─────────────────────────────────────────────
# TEAM SEASON STATS  (update each season)
# net_rating, off_rating, def_rating, pace, avg_pts, wins, losses
# ─────────────────────────────────────────────

TEAM_STATS: dict[str, dict] = {
    "Oklahoma City Thunder":  {"net_rating": 8.9,  "off_rating": 118.5, "def_rating": 109.6, "pace": 100.2, "avg_pts": 120.8, "wins": 58, "losses": 24},
    "Cleveland Cavaliers":    {"net_rating": 8.3,  "off_rating": 116.8, "def_rating": 108.5, "pace": 98.9,  "avg_pts": 115.4, "wins": 64, "losses": 18},
    "Boston Celtics":         {"net_rating": 8.1,  "off_rating": 122.3, "def_rating": 114.2, "pace": 102.5, "avg_pts": 123.0, "wins": 61, "losses": 21},
    "Denver Nuggets":         {"net_rating": 7.1,  "off_rating": 119.4, "def_rating": 112.3, "pace": 100.9, "avg_pts": 120.1, "wins": 55, "losses": 27},
    "Minnesota Timberwolves": {"net_rating": 5.7,  "off_rating": 115.9, "def_rating": 110.2, "pace": 99.4,  "avg_pts": 115.7, "wins": 52, "losses": 30},
    "Milwaukee Bucks":        {"net_rating": 5.5,  "off_rating": 117.5, "def_rating": 112.0, "pace": 101.3, "avg_pts": 118.6, "wins": 50, "losses": 32},
    "Dallas Mavericks":       {"net_rating": 4.8,  "off_rating": 118.4, "def_rating": 113.6, "pace": 101.6, "avg_pts": 119.7, "wins": 50, "losses": 32},
    "Indiana Pacers":         {"net_rating": 4.3,  "off_rating": 121.0, "def_rating": 116.7, "pace": 106.0, "avg_pts": 125.5, "wins": 48, "losses": 34},
    "New York Knicks":        {"net_rating": 3.9,  "off_rating": 115.4, "def_rating": 111.5, "pace": 99.6,  "avg_pts": 114.7, "wins": 47, "losses": 35},
    "Golden State Warriors":  {"net_rating": 3.6,  "off_rating": 117.7, "def_rating": 114.1, "pace": 103.6, "avg_pts": 120.4, "wins": 48, "losses": 34},
    "LA Lakers":              {"net_rating": 3.3,  "off_rating": 115.7, "def_rating": 112.4, "pace": 100.6, "avg_pts": 117.0, "wins": 45, "losses": 37},
    "Miami Heat":             {"net_rating": 3.2,  "off_rating": 113.9, "def_rating": 110.7, "pace": 98.3,  "avg_pts": 112.0, "wins": 46, "losses": 36},
    "Philadelphia 76ers":     {"net_rating": 3.0,  "off_rating": 117.0, "def_rating": 114.0, "pace": 102.0, "avg_pts": 117.4, "wins": 43, "losses": 39},
    "Phoenix Suns":           {"net_rating": 2.6,  "off_rating": 116.7, "def_rating": 114.1, "pace": 101.0, "avg_pts": 117.7, "wins": 43, "losses": 39},
    "Memphis Grizzlies":      {"net_rating": 2.2,  "off_rating": 115.4, "def_rating": 113.2, "pace": 102.4, "avg_pts": 118.4, "wins": 42, "losses": 40},
    "Sacramento Kings":       {"net_rating": 1.8,  "off_rating": 117.2, "def_rating": 115.4, "pace": 103.8, "avg_pts": 120.3, "wins": 41, "losses": 41},
    "San Antonio Spurs":      {"net_rating": -1.2, "off_rating": 113.7, "def_rating": 114.9, "pace": 101.1, "avg_pts": 115.2, "wins": 36, "losses": 46},
    "Cleveland Cavaliers":    {"net_rating": 8.3,  "off_rating": 116.8, "def_rating": 108.5, "pace": 98.9,  "avg_pts": 115.4, "wins": 64, "losses": 18},
}

TEAM_LIST = sorted(TEAM_STATS.keys())
