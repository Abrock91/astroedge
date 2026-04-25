# 🏀 AstroEdge — NBA Playoffs Predictor

A personal-use NBA playoff prediction tool combining ML ensemble models
with Chinese astrology and numerology features.

---

## Quick Start (5 minutes)

### 1. Install Python 3.11+ if you don't have it
https://www.python.org/downloads/

### 2. Create a virtual environment (recommended)
```bash
cd astroedge
python -m venv venv

# Mac/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

The browser will open automatically at http://localhost:8501

---

## Pages

| Page | What it does |
|------|-------------|
| 🏠 Dashboard | Shows predictions for 6 featured playoff matchups at a glance |
| 🔮 Game Predictor | Full model breakdown for any matchup you choose |
| 🎰 Parlay Builder | Build up to 6-leg parlays with auto-calculated EV |
| 📖 About | Explains every model and feature in detail |

---

## Sidebar Controls

- **🌟 Astrology Features** — Toggle Chinese astrology/numerology on or off
- **📅 Game Date** — Change the date for accurate Personal Day calculations
- **💰 Bankroll** — Sets your total bankroll for Kelly Criterion bet sizing

---

## Updating Stats

Player birthdates are permanent and won't need updating.
Team stats in `player_data.py → TEAM_STATS` should be updated each season
with current net ratings, pace, and win totals.

---

## File Structure

```
astroedge/
├── app.py           # Streamlit UI (4 pages)
├── astrology.py     # Chinese zodiac + numerology engine
├── models.py        # ML ensemble + Monte Carlo + betting tools
├── player_data.py   # Player birthdates, rosters, team stats
├── requirements.txt
└── README.md
```

---

## Expanding Later

Planned additions:
- [ ] Live odds API integration (The Odds API — free tier available)
- [ ] nba_api real-time stats pull
- [ ] XGBoost / LightGBM models
- [ ] SHAP value explainability charts
- [ ] Historical backtesting module
- [ ] Series simulator (full 7-game series outcome probabilities)
- [ ] Export to PDF / CSV

---

> ⚠️ For personal research and entertainment only. Gamble responsibly.
