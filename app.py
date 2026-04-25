"""
app.py — AstroEdge NBA Playoffs Predictor
Run with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, timedelta

from astrology import team_astro_features, player_astro_score
from player_data import PLAYER_BIRTHDATES, TEAM_ROSTERS, TEAM_STATS, TEAM_LIST
from models import PlayoffPredictor

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="AstroEdge NBA Playoffs",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────

st.markdown("""
<style>
    .stApp { background-color: #0d1117; }

    /* Cards */
    .card {
        background: linear-gradient(135deg, #161b27, #1e2535);
        border: 1px solid #2d3550;
        border-radius: 14px;
        padding: 22px 18px;
        text-align: center;
    }
    .card-sm {
        background: #161b27;
        border: 1px solid #2d3550;
        border-radius: 10px;
        padding: 14px 12px;
        margin: 5px 0;
    }

    /* Typography */
    .big-prob { font-size: 2.8rem; font-weight: 800; line-height: 1.1; }
    .home-clr { color: #38bdf8; }
    .away-clr { color: #f87171; }
    .gold     { color: #fbbf24; }
    .muted    { color: #64748b; font-size: 0.82rem; }

    /* Confidence badges */
    .badge-HIGH   { background:#14532d; color:#4ade80; border-radius:6px; padding:2px 10px; font-weight:700; }
    .badge-MEDIUM { background:#451a03; color:#fb923c; border-radius:6px; padding:2px 10px; font-weight:700; }
    .badge-LOW    { background:#3f1d1d; color:#f87171; border-radius:6px; padding:2px 10px; font-weight:700; }

    /* Astro cards */
    .astro-row {
        background: #0f172a;
        border-left: 3px solid #7c3aed;
        border-radius: 6px;
        padding: 8px 12px;
        margin: 4px 0;
        font-size: 0.88rem;
        color: #cbd5e1;
    }
    .power-day { border-left-color: #fbbf24 !important; }

    /* Divider */
    hr { border-color: #1e2535 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CACHED RESOURCES
# ─────────────────────────────────────────────

@st.cache_resource(show_spinner="🏋️ Training prediction models…")
def load_predictor():
    p = PlayoffPredictor()
    p.train()
    return p


predictor = load_predictor()


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🏀 AstroEdge")
    st.markdown("*NBA Playoffs Predictor*")
    st.divider()

    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "🔮 Game Predictor", "🎰 Parlay Builder", "📖 About"],
        label_visibility="collapsed",
    )

    st.divider()

    use_astro = st.toggle("🌟 Astrology Features", value=True)
    game_date = st.date_input("📅 Game Date", value=date.today())

    st.divider()

    st.markdown("**💰 Bankroll**")
    bankroll = st.number_input("Total bankroll ($)", min_value=50, value=1000, step=50)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def build_features(
    home: str, away: str, home_rest: int, away_rest: int,
    series_lead: int, use_astro: bool = True,
) -> tuple[dict, dict | None]:
    hs = TEAM_STATS.get(home, {})
    as_ = TEAM_STATS.get(away, {})

    astro_feats = None
    astro_diff = 0.0

    if use_astro:
        h_roster = TEAM_ROSTERS.get(home, [])
        a_roster = TEAM_ROSTERS.get(away, [])
        h_bdays = [PLAYER_BIRTHDATES[p] for p in h_roster if p in PLAYER_BIRTHDATES]
        a_bdays = [PLAYER_BIRTHDATES[p] for p in a_roster if p in PLAYER_BIRTHDATES]
        if h_bdays and a_bdays:
            astro_feats = team_astro_features(h_bdays, a_bdays, game_date)
            astro_diff = astro_feats["astro_differential"]

    feats = {
        "net_rating_diff":  hs.get("net_rating", 0) - as_.get("net_rating", 0),
        "home_court":       1.0,
        "rest_diff":        float(home_rest - away_rest),
        "series_momentum":  float(series_lead),
        "pace_diff":        hs.get("pace", 100) - as_.get("pace", 100),
        "astro_diff":       astro_diff,
    }
    return feats, astro_feats


def win_bar(home_prob: float, home_name: str, away_name: str) -> go.Figure:
    """Horizontal probability bar."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[home_prob * 100], y=[""],
        orientation="h",
        marker_color="#38bdf8",
        name=home_name, text=f"{home_name}  {home_prob*100:.1f}%",
        textposition="inside", insidetextanchor="start",
    ))
    fig.add_trace(go.Bar(
        x=[(1 - home_prob) * 100], y=[""],
        orientation="h",
        marker_color="#f87171",
        name=away_name, text=f"{away_name}  {(1-home_prob)*100:.1f}%",
        textposition="inside", insidetextanchor="end",
    ))
    fig.update_layout(
        barmode="stack", template="plotly_dark",
        height=80, margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        xaxis=dict(visible=False, range=[0, 100]),
        yaxis=dict(visible=False),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def confidence_badge(conf: str) -> str:
    return f'<span class="badge-{conf}">{conf}</span>'


# ─────────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────────

if "Dashboard" in page:
    st.markdown("# 🏀 AstroEdge — NBA Playoffs 2026")
    st.markdown(f"*{game_date.strftime('%A, %B %d, %Y')} · Predictions powered by ML + Chinese Astrology*")
    st.divider()

    # Featured matchups
    FEATURED = [
        ("Oklahoma City Thunder", "Denver Nuggets",          2, 1, 1),
        ("Boston Celtics",        "Cleveland Cavaliers",     2, 2, 0),
        ("Minnesota Timberwolves","Dallas Mavericks",        1, 2, -1),
        ("Indiana Pacers",        "Milwaukee Bucks",         2, 1, 0),
        ("LA Lakers",             "Golden State Warriors",   2, 1, 1),
        ("New York Knicks",       "Philadelphia 76ers",      3, 0, 2),
    ]

    cols = st.columns(3)
    for i, (home, away, hr, ar, lead) in enumerate(FEATURED):
        if home not in TEAM_STATS or away not in TEAM_STATS:
            continue
        feats, _ = build_features(home, away, hr, ar, lead, use_astro)
        res = predictor.predict(feats)
        p = res["home_win_prob"]
        conf = res["confidence"]
        sprd = res["predicted_spread"]
        tot  = res["predicted_total"]

        with cols[i % 3]:
            st.markdown(f"""
            <div class="card">
                <div class="muted">2026 PLAYOFFS</div>
                <div style="font-size:1rem;font-weight:700;color:#38bdf8;margin-top:6px">{home}</div>
                <div class="muted">vs</div>
                <div style="font-size:1rem;font-weight:700;color:#f87171">{away}</div>
                <hr style="margin:10px 0">
                <div class="big-prob home-clr">{p*100:.1f}%</div>
                <div class="muted">home win probability</div>
                <div style="margin-top:8px;color:#e2e8f0">
                    Spread <span class="gold">{"+" if sprd>0 else ""}{sprd:.1f}</span>
                    &nbsp;·&nbsp; O/U <span class="gold">{tot:.0f}</span>
                </div>
                <div style="margin-top:8px">{confidence_badge(conf)}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Quick stats table
    st.markdown("### 📊 All Matchup Predictions")
    rows = []
    for home, away, hr, ar, lead in FEATURED:
        if home not in TEAM_STATS or away not in TEAM_STATS:
            continue
        feats, _ = build_features(home, away, hr, ar, lead, use_astro)
        res = predictor.predict(feats)
        rows.append({
            "Home Team": home,
            "Away Team": away,
            "Home Win %": f"{res['home_win_prob']*100:.1f}%",
            "Away Win %": f"{res['away_win_prob']*100:.1f}%",
            "Spread": f"{'+'if res['predicted_spread']>0 else ''}{res['predicted_spread']:.1f}",
            "Total": f"{res['predicted_total']:.0f}",
            "Confidence": res["confidence"],
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
# PAGE: GAME PREDICTOR
# ─────────────────────────────────────────────

elif "Predictor" in page:
    st.markdown("# 🔮 Game Predictor")
    st.markdown("Configure a matchup and run the full model + astrology analysis.")
    st.divider()

    # ── Inputs ───────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🏠 Home Team")
        home = st.selectbox("Home", TEAM_LIST, label_visibility="collapsed",
                            index=TEAM_LIST.index("Oklahoma City Thunder"))
        home_rest = st.slider("Rest days", 0, 5, 2, key="h_rest")
        series_lead = st.slider(
            "Series lead (home)", -3, 3, 0,
            help="Positive = home team leads; negative = away team leads",
        )

    with c2:
        st.markdown("#### ✈️ Away Team")
        away_opts = [t for t in TEAM_LIST if t != home]
        away = st.selectbox("Away", away_opts, label_visibility="collapsed",
                            index=away_opts.index("Denver Nuggets") if "Denver Nuggets" in away_opts else 0)
        away_rest = st.slider("Rest days", 0, 5, 1, key="a_rest")
        vegas_line = st.number_input("Vegas moneyline (home, optional)", value=-115)

    if st.button("🚀 Generate Full Prediction", type="primary", use_container_width=True):

        with st.spinner("Running models + astrology engine…"):
            feats, astro = build_features(home, away, home_rest, away_rest, series_lead, use_astro)
            res = predictor.predict(feats)

        st.divider()

        # ── Win probability bar ───────────────
        st.plotly_chart(win_bar(res["home_win_prob"], home, away),
                        use_container_width=True, config={"displayModeBar": False})

        # ── Key metrics row ───────────────────
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Home Win Prob", f"{res['home_win_prob']*100:.1f}%")
        m2.metric("Predicted Spread", f"{'+'if res['predicted_spread']>0 else ''}{res['predicted_spread']:.1f}")
        m3.metric("Predicted Total", f"{res['predicted_total']:.0f}")
        edge_val = predictor.edge(res["home_win_prob"], vegas_line)
        m4.metric("Model Edge", f"{edge_val:+.1f}%")
        kelly = predictor.kelly_fraction(res["home_win_prob"], vegas_line)
        m5.metric("Kelly Bet", f"${kelly * bankroll:.0f}  ({kelly*100:.1f}%)")

        # Confidence
        conf = res["confidence"]
        st.markdown(f"**Confidence:** {confidence_badge(conf)} &nbsp; "
                    f"({res['confidence_pct']:.1f}% margin above 50/50)",
                    unsafe_allow_html=True)

        st.divider()

        # ── Model breakdown ───────────────────
        col_l, col_r = st.columns(2)

        with col_l:
            st.markdown("#### 📊 Model Breakdown")
            md = pd.DataFrame({
                "Model":     ["Logistic Regression", "Random Forest", "Gradient Boosting", "🏆 Ensemble"],
                "Win Prob":  [
                    f"{res['lr_prob']*100:.1f}%",
                    f"{res['rf_prob']*100:.1f}%",
                    f"{res['gb_prob']*100:.1f}%",
                    f"{res['home_win_prob']*100:.1f}%",
                ],
                "Weight": ["20%", "35%", "45%", "—"],
            })
            st.dataframe(md, hide_index=True, use_container_width=True)

            st.markdown("#### 🔍 Feature Importance")
            fi = res["feature_importance"]
            fig_fi = px.bar(
                x=list(fi.values()), y=list(fi.keys()),
                orientation="h",
                color=list(fi.values()),
                color_continuous_scale="Blues",
                template="plotly_dark",
            )
            fig_fi.update_layout(
                height=280, margin=dict(l=0, r=0, t=10, b=0),
                showlegend=False, coloraxis_showscale=False,
            )
            st.plotly_chart(fig_fi, use_container_width=True, config={"displayModeBar": False})

        with col_r:
            st.markdown("#### 🎲 Monte Carlo (10,000 simulations)")
            mc_x = res["mc_spread_dist"]
            fig_mc = go.Figure()
            fig_mc.add_trace(go.Histogram(
                x=mc_x, nbinsx=50,
                marker_color="#38bdf8", opacity=0.75,
                name="Simulations",
            ))
            fig_mc.add_vline(x=0, line_dash="dash", line_color="white",
                             annotation_text="Pick'em", annotation_font_color="white")
            fig_mc.add_vline(x=res["predicted_spread"], line_dash="dot",
                             line_color="#fbbf24",
                             annotation_text=f"Model: {res['predicted_spread']:+.1f}",
                             annotation_font_color="#fbbf24")
            fig_mc.update_layout(
                xaxis_title="Point Diff (Home − Away)",
                yaxis_title="Frequency",
                template="plotly_dark",
                height=280,
                margin=dict(l=0, r=0, t=10, b=40),
                showlegend=False,
            )
            st.plotly_chart(fig_mc, use_container_width=True, config={"displayModeBar": False})

            # Total distribution
            st.markdown("#### 📈 Total Points Distribution")
            fig_tot = go.Figure()
            fig_tot.add_trace(go.Histogram(
                x=res["mc_total_dist"], nbinsx=40,
                marker_color="#a78bfa", opacity=0.75,
            ))
            fig_tot.add_vline(x=res["predicted_total"], line_dash="dot",
                              line_color="#fbbf24",
                              annotation_text=f"O/U {res['predicted_total']:.0f}",
                              annotation_font_color="#fbbf24")
            fig_tot.update_layout(
                xaxis_title="Total Points",
                template="plotly_dark",
                height=200,
                margin=dict(l=0, r=0, t=10, b=40),
                showlegend=False,
            )
            st.plotly_chart(fig_tot, use_container_width=True, config={"displayModeBar": False})

        # ── Astrology section ─────────────────
        if use_astro and astro:
            st.divider()
            st.markdown("### 🌟 Astrology & Numerology")

            # Astro summary banner
            diff = astro["astro_differential"]
            favor = home if diff >= 0 else away
            col_a, col_b, col_c, col_d = st.columns(4)
            col_a.metric("Astro Edge", f"{abs(diff):.1f} pts → {favor}")
            col_b.metric("Home Team Compat.", f"{astro['home_team_compat']:.0f}/100")
            col_c.metric("Away Team Compat.", f"{astro['away_team_compat']:.0f}/100")
            col_d.metric(
                "Power Players Today",
                f"🏠 {astro['home_power_players']}  ✈️ {astro['away_power_players']}",
            )

            if astro["star_clash"]:
                st.warning("⚠️ **Zodiac Clash:** The two star players have clashing zodiac animals — expect heightened personal intensity and possible emotional swings.")

            # Player profiles
            pcol1, pcol2 = st.columns(2)
            h_roster = TEAM_ROSTERS.get(home, [])
            a_roster = TEAM_ROSTERS.get(away, [])

            with pcol1:
                avg = astro["home_avg_astro"]
                st.markdown(f"**{home}** · Team Astro Score: **{avg:.1f}/100**")
                for name, prof in zip(h_roster, astro["home_profiles"]):
                    power_cls = "power-day" if prof["power_day"] else ""
                    icon = "⚡" if prof["power_day"] else "·"
                    st.markdown(f"""
                    <div class="astro-row {power_cls}">
                        {icon} <b>{name}</b> &nbsp;—&nbsp;
                        🐉 {prof['animal']} · {prof['element']} &nbsp;|&nbsp;
                        LP <b>{prof['life_path']}</b> &nbsp;|&nbsp;
                        PD <b>{prof['personal_day']}</b> &nbsp;|&nbsp;
                        Score <b>{prof['astro_score']}</b>
                    </div>
                    """, unsafe_allow_html=True)

            with pcol2:
                avg = astro["away_avg_astro"]
                st.markdown(f"**{away}** · Team Astro Score: **{avg:.1f}/100**")
                for name, prof in zip(a_roster, astro["away_profiles"]):
                    power_cls = "power-day" if prof["power_day"] else ""
                    icon = "⚡" if prof["power_day"] else "·"
                    st.markdown(f"""
                    <div class="astro-row {power_cls}">
                        {icon} <b>{name}</b> &nbsp;—&nbsp;
                        🐉 {prof['animal']} · {prof['element']} &nbsp;|&nbsp;
                        LP <b>{prof['life_path']}</b> &nbsp;|&nbsp;
                        PD <b>{prof['personal_day']}</b> &nbsp;|&nbsp;
                        Score <b>{prof['astro_score']}</b>
                    </div>
                    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: PARLAY BUILDER
# ─────────────────────────────────────────────

elif "Parlay" in page:
    st.markdown("# 🎰 Parlay Builder")
    st.markdown("Build up to 6 legs. Each leg uses the ensemble model win probability.")
    st.divider()

    if "parlay_legs" not in st.session_state:
        st.session_state.parlay_legs = []

    # Add a leg
    with st.expander("➕ Add a Leg", expanded=len(st.session_state.parlay_legs) == 0):
        lc1, lc2, lc3 = st.columns(3)
        with lc1:
            ph = st.selectbox("Home Team", TEAM_LIST, key="ph")
        with lc2:
            pa_opts = [t for t in TEAM_LIST if t != ph]
            pa = st.selectbox("Away Team", pa_opts, key="pa")
        with lc3:
            pick = st.selectbox("Pick", [ph, pa], key="pick")

        lc4, lc5 = st.columns(2)
        with lc4:
            leg_odds = st.number_input("Moneyline odds", value=-110, key="leg_odds")
        with lc5:
            add_btn = st.button(
                "Add Leg",
                disabled=len(st.session_state.parlay_legs) >= 6,
                type="primary",
            )

        if add_btn:
            feats, _ = build_features(ph, pa, 2, 1, 0, use_astro)
            res = predictor.predict(feats)
            wp = res["home_win_prob"] if pick == ph else res["away_win_prob"]
            st.session_state.parlay_legs.append({
                "matchup": f"{ph} vs {pa}",
                "pick":    pick,
                "win_prob": wp,
                "odds":    leg_odds,
            })
            st.rerun()

    # Display legs
    if st.session_state.parlay_legs:
        st.markdown(f"### 📋 Your Parlay ({len(st.session_state.parlay_legs)} legs)")

        remove_idx = None
        for i, leg in enumerate(st.session_state.parlay_legs):
            dc, nc = st.columns([5, 1])
            with dc:
                st.markdown(f"""
                <div class="card-sm">
                    <b>{i+1}. {leg['pick']}</b>
                    <span class="muted"> ({leg['matchup']})</span>
                    &nbsp;·&nbsp; {leg['win_prob']*100:.1f}% model prob
                    &nbsp;·&nbsp; Odds: {leg['odds']}
                </div>
                """, unsafe_allow_html=True)
            with nc:
                if st.button("✕", key=f"rm_{i}"):
                    remove_idx = i

        if remove_idx is not None:
            st.session_state.parlay_legs.pop(remove_idx)
            st.rerun()

        st.divider()

        # Parlay math
        stake = st.number_input("Stake ($)", min_value=1, value=50)
        ev_data = predictor.parlay_ev(st.session_state.parlay_legs, stake)

        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Combined Win Prob", f"{ev_data['combined_prob']*100:.2f}%")
        r2.metric("Combined Odds",     f"+{ev_data['combined_american']:.0f}")
        r3.metric("Potential Payout",  f"${ev_data['payout']:.2f}")
        r4.metric("Expected Value",    f"${ev_data['ev']:.2f}",
                  delta=f"${ev_data['ev']:.2f}",
                  delta_color="normal" if ev_data["ev"] > 0 else "inverse")

        # Monte Carlo simulation for the parlay
        n_sim = 10_000
        rng = np.random.default_rng()
        wins = sum(
            1 for _ in range(n_sim)
            if all(rng.random() < leg["win_prob"] for leg in st.session_state.parlay_legs)
        )
        mc_hit = wins / n_sim

        st.info(
            f"🎲 **Monte Carlo** ({n_sim:,} sims): "
            f"Parlay hits **{mc_hit*100:.2f}%** of the time  ·  "
            f"EV per $100 wagered: **${ev_data['ev']/stake*100:.2f}**"
        )

        if st.button("🗑️ Clear Parlay", type="secondary"):
            st.session_state.parlay_legs = []
            st.rerun()

    else:
        st.info("Add at least one leg above to get started.")


# ─────────────────────────────────────────────
# PAGE: ABOUT
# ─────────────────────────────────────────────

elif "About" in page:
    st.markdown("# 📖 About AstroEdge")
    st.divider()

    st.markdown("""
    ### 🤖 Prediction Models

    | Model | Type | Ensemble Weight |
    |-------|------|----------------|
    | Logistic Regression | Linear classifier, calibrated | 20% |
    | Random Forest | 200-tree ensemble | 35% |
    | Gradient Boosting | 200-stage boosting | 45% |

    All classifiers are probability-calibrated with isotonic regression to avoid
    overconfidence. Regression heads (Ridge) predict point spread and game total.

    ---

    ### 📐 Input Features

    | Feature | What It Captures |
    |---------|-----------------|
    | Net Rating Differential | Efficiency advantage (strongest predictor) |
    | Home Court | ~2-3 point advantage in playoffs |
    | Rest Differential | Fatigue / back-to-back effects |
    | Series Momentum | Psychological edge in best-of-7 |
    | Pace Differential | Style mismatch (up-tempo vs. half-court) |
    | Astro Differential | Chinese astrology composite edge |

    ---

    ### 🌟 Astrology System (2026 = Year of the Horse 🐎)

    **Chinese Zodiac:**  
    Each player's birth year determines their animal and element. Animals are tested
    for clash pairs (e.g., Rat vs Horse), three-harmony trios, and element generation/
    control cycles. A 0-100 compatibility score is computed for each team's internal
    chemistry and cross-team matchup.

    **Numerology:**  
    - **Life Path**: birth date reduced to single digit (or master number 11/22/33)
    - **Personal Year**: birth month + birth day + current year, reduced
    - **Personal Day**: personal year + game month + game day, reduced
    - **Power Days**: days where personal day = 1, 3, 9, 11, 22, or 33

    All values feed into the ML models as numeric features. Toggle astrology off
    in the sidebar to see pure statistical predictions.

    ---

    ### 💰 Betting Tools

    - **Kelly Criterion** (Quarter-Kelly): conservative bet sizing based on model edge vs. implied odds
    - **Model Edge**: difference between model win probability and Vegas implied probability
    - **Monte Carlo**: 10,000 simulated game outcomes per prediction
    - **Parlay EV**: exact combined probability and expected value for multi-leg bets

    ---

    > ⚠️ *For research and entertainment purposes only. Past model performance does not
    > guarantee future results. Gamble responsibly.*
    """)
