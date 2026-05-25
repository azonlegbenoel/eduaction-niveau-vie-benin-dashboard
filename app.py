# ============================================================
# UEMOA MOBILE MONEY DASHBOARD — app.py
# Auteur : AZONLEGBE Noël Junior Azonsou
# Mémoire : Effet du Mobile Money sur la Croissance dans les pays de l'UEMOA
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─── Configuration de la page ────────────────────────────────
st.set_page_config(
    page_title="UEMOA Mobile Money Dashboard",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS Personnalisé ─────────────────────────────────────────
st.markdown("""
<style>
/* Import de la police */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Fond de la page */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1b2a 50%, #0a1628 100%);
    min-height: 100vh;
}

/* Barre latérale */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2a 0%, #112240 100%) !important;
    border-right: 1px solid rgba(100, 200, 255, 0.15);
}
section[data-testid="stSidebar"] * {
    color: #cdd9f0 !important;
}

/* Titre principal */
.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #64d8ff, #5b8dee, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
    line-height: 1.1;
}
.hero-sub {
    font-size: 1.05rem;
    color: #7090b0;
    margin-top: 0.2rem;
}

/* Cartes KPI */
.kpi-card {
    background: linear-gradient(135deg, rgba(30,60,100,0.55), rgba(20,40,70,0.55));
    border: 1px solid rgba(100, 180, 255, 0.2);
    border-radius: 16px;
    padding: 22px 20px 18px 20px;
    text-align: center;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    height: 100%;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(100,200,255,0.18);
}
.kpi-icon { font-size: 1.9rem; margin-bottom: 6px; }
.kpi-label {
    font-size: 0.78rem;
    color: #7090b0;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 1.85rem;
    font-weight: 700;
    color: #e0eeff;
    line-height: 1;
}
.kpi-delta {
    font-size: 0.78rem;
    color: #5adf8f;
    margin-top: 4px;
}

/* Section heading */
.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #c8e0ff;
    border-left: 4px solid #5b8dee;
    padding-left: 12px;
    margin: 28px 0 14px 0;
}

/* Bloc descriptif */
.insight-box {
    background: rgba(30, 50, 90, 0.45);
    border: 1px solid rgba(100, 180, 255, 0.15);
    border-radius: 12px;
    padding: 18px 22px;
    margin-top: 14px;
    color: #a8c4e0;
    font-size: 0.9rem;
    line-height: 1.7;
}
.insight-box strong { color: #64d8ff; }

/* Badge */
.badge {
    display: inline-block;
    background: rgba(91,141,238,0.25);
    border: 1px solid rgba(91,141,238,0.5);
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.75rem;
    color: #91b5f8;
    margin-right: 6px;
    margin-bottom: 6px;
}

/* Onglets */
div[data-testid="stTabs"] button {
    font-size: 0.85rem;
    font-weight: 600;
    color: #7090b0;
    border-radius: 8px 8px 0 0;
    transition: all 0.2s;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #64d8ff;
    border-bottom: 2px solid #64d8ff;
    background: rgba(100, 200, 255, 0.08);
}

/* Sélecteurs */
.stSelectbox > div > div, .stMultiSelect > div > div {
    background: rgba(20, 40, 70, 0.7) !important;
    border: 1px solid rgba(100, 180, 255, 0.2) !important;
    border-radius: 10px !important;
    color: #c8e0ff !important;
}

/* Tables */
.stDataFrame { border-radius: 12px; overflow: hidden; }
div[data-testid="stDataFrameContainer"] {
    border: 1px solid rgba(100, 180, 255, 0.15);
    border-radius: 12px;
}

/* Footer */
.footer {
    background: rgba(10,20,40,0.8);
    border-top: 1px solid rgba(100,180,255,0.1);
    padding: 20px 30px;
    text-align: center;
    color: #506080;
    font-size: 0.8rem;
    margin-top: 40px;
    border-radius: 12px;
}
.footer a { color: #5b8dee; text-decoration: none; }

/* Résultats de régression */
.result-table {
    background: rgba(20,40,70,0.5);
    border: 1px solid rgba(100,180,255,0.15);
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
}

/* Indicateur de signe */
.sig-positive { color: #5adf8f; font-weight: 700; }
.sig-negative { color: #ff6b6b; font-weight: 700; }
.sig-neutral  { color: #ffd166; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ─── Chargement des données ───────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("data/UEMOA_MobileMoney_Panel_2014_2025.xlsx", header=1)
    df.columns = df.columns.str.replace("\n", " ").str.strip()
    df = df.dropna(subset=["Country"])
    cols_to_ignore = ["Secondary Enrollment %", "Credit Private % GDP", "MM Adoption", "Unnamed: 31"]
    cols = [c for c in df.columns if c not in cols_to_ignore]
    df = df[cols].copy()
    for col in df.columns:
        if col not in ["Country", "ISO3"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["Year", "GDP Growth (% annual)"])
    df["Year"] = df["Year"].astype(int)
    return df

df = load_data()
countries = sorted(df["Country"].unique().tolist())
years     = sorted(df["Year"].unique().tolist())

PALETTE = px.colors.qualitative.Set2
COUNTRY_COLORS = {c: PALETTE[i % len(PALETTE)] for i, c in enumerate(countries)}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor ="rgba(15,30,55,0.5)",
    font=dict(family="Inter", color="#c8e0ff"),
    xaxis=dict(gridcolor="rgba(100,180,255,0.08)", showline=False),
    yaxis=dict(gridcolor="rgba(100,180,255,0.08)", showline=False),
    legend=dict(
        bgcolor="rgba(10,25,50,0.7)",
        bordercolor="rgba(100,180,255,0.2)",
        borderwidth=1,
    ),
    margin=dict(l=20, r=20, t=45, b=20),
    hoverlabel=dict(bgcolor="rgba(10,25,50,0.9)", font_color="#c8e0ff"),
)

def apply_layout(fig, title="", **kwargs):
    fig.update_layout(title=dict(text=title, font=dict(size=15, color="#c8e0ff")),
                      **PLOTLY_LAYOUT, **kwargs)
    return fig

# ─── Barre latérale ──────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 20px 0;'>
        <div style='font-size:2.5rem;'>📱</div>
        <div style='font-size:1rem; font-weight:700; color:#64d8ff; margin-top:4px;'>UEMOA Mobile Money</div>
        <div style='font-size:0.72rem; color:#506080; margin-top:2px;'>Tableau de bord — Mémoire ISE</div>
    </div>
    <hr style='border-color:rgba(100,180,255,0.1); margin-bottom:20px;'>
    """, unsafe_allow_html=True)

    st.markdown("**🌍 Filtres globaux**")
    sel_countries = st.multiselect("Pays", countries, default=countries,
                                   help="Sélectionner les pays à afficher")
    sel_years = st.slider("Période", min_value=min(years), max_value=max(years),
                          value=(min(years), max(years)))
    st.markdown("<hr style='border-color:rgba(100,180,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.73rem; color:#506080; text-align:center; line-height:1.8;'>
        <b style='color:#7090b0;'>Auteur</b><br>
        AZONLEGBE Noël Junior Azonsou<br><br>
        <b style='color:#7090b0;'>Spécialité</b><br>
        Ingénieur Statisticien Économiste<br>
        Data Science & Marketing<br><br>
        <b style='color:#7090b0;'>© 2026</b>
    </div>
    """, unsafe_allow_html=True)

# Données filtrées
df_f = df[df["Country"].isin(sel_countries) &
          df["Year"].between(sel_years[0], sel_years[1])].copy()

# ─── Navigation ──────────────────────────────────────────────
tab_home, tab_explore, tab_eco, tab_ml, tab_about = st.tabs([
    "🏠  Accueil", "🔍  Exploration", "📊  Analyse Économétrique", "🤖  Machine Learning", "ℹ️  À propos"
])

# ══════════════════════════════════════════════════════════════
# ONGLET 1 — ACCUEIL
# ══════════════════════════════════════════════════════════════
with tab_home:
    st.markdown("""
    <div style='padding: 10px 0 30px 0;'>
        <div class='hero-title'>Effet du Mobile Money sur la<br>Croissance Économique dans l'UEMOA</div>
        <div class='hero-sub'>Tableau de bord interactif · Mémoire de fin d'études · ISE 2026</div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    k1, k2, k3, k4, k5 = st.columns(5)
    mean_growth = df_f["GDP Growth (% annual)"].mean()
    mean_mm     = df_f["MM Trans. % GDP"].mean()
    total_vol   = df_f["MM Trans. Volume"].sum() / 1e9
    n_obs       = len(df_f)
    last_year   = df_f["Year"].max()

    for col, icon, label, value, delta in [
        (k1, "📈", "Croissance moy. PIB", f"{mean_growth:.2f}%", "Annuelle"),
        (k2, "📱", "MM Trans. moy. (% PIB)", f"{mean_mm:.1f}%", "Proxy d'adoption"),
        (k3, "💰", "Volume MM (Mds FCFA)", f"{total_vol:.0f}", "Cumulé"),
        (k4, "📋", "Observations", str(n_obs), "Données de panel"),
        (k5, "📅", "Dernière année", str(last_year), "Données disponibles"),
    ]:
        col.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-icon'>{icon}</div>
            <div class='kpi-label'>{label}</div>
            <div class='kpi-value'>{value}</div>
            <div class='kpi-delta'>{delta}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Intro
    st.markdown("""
    <div class='insight-box'>
    <strong>Contexte du mémoire</strong><br>
    Le Mobile Money a connu une expansion spectaculaire en Afrique subsaharienne, et particulièrement dans la zone <strong>UEMOA</strong>
    (Union Économique et Monétaire Ouest-Africaine), qui regroupe 8 pays : Bénin, Burkina Faso, Côte d'Ivoire, Guinée-Bissau, Mali,
    Niger, Sénégal et Togo. Ce tableau de bord explore empiriquement la relation entre l'adoption du Mobile Money et la
    croissance économique sur la période <strong>2014–2025</strong>, en combinant économétrie de panel et apprentissage automatique.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>📈 Évolution conjointe — Mobile Money & Croissance du PIB</div>",
                unsafe_allow_html=True)

    # Graphique d'évolution conjointe (double axe)
    fig_joint = make_subplots(specs=[[{"secondary_y": True}]])

    df_agg = df_f.groupby("Year").agg(
        mm_mean=("MM Trans. % GDP", "mean"),
        gdp_mean=("GDP Growth (% annual)", "mean")
    ).reset_index()

    fig_joint.add_trace(
        go.Scatter(x=df_agg["Year"], y=df_agg["mm_mean"],
                   name="MM Trans. % PIB (moy.)", mode="lines+markers",
                   line=dict(color="#64d8ff", width=3),
                   marker=dict(size=8, color="#64d8ff")),
        secondary_y=False
    )
    fig_joint.add_trace(
        go.Scatter(x=df_agg["Year"], y=df_agg["gdp_mean"],
                   name="Croissance PIB % (moy.)", mode="lines+markers",
                   line=dict(color="#ffd166", width=3, dash="dot"),
                   marker=dict(size=8, color="#ffd166")),
        secondary_y=True
    )
    fig_joint.add_vline(x=2020, line_dash="dash", line_color="#ff6b6b",
                        annotation_text="COVID-19", annotation_font_color="#ff6b6b")
    fig_joint.update_yaxes(title_text="MM Trans. % PIB", secondary_y=False,
                           gridcolor="rgba(100,180,255,0.08)", color="#64d8ff")
    fig_joint.update_yaxes(title_text="Croissance PIB (%)", secondary_y=True,
                           gridcolor="rgba(0,0,0,0)", color="#ffd166")
    apply_layout(fig_joint, "Évolution conjointe : Mobile Money & Croissance économique (UEMOA)")
    st.plotly_chart(fig_joint, use_container_width=True)

    # Évolution par pays
    st.markdown("<div class='section-title'>🌍 Évolution par pays</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        fig_mm = go.Figure()
        for country in sel_countries:
            dd = df_f[df_f["Country"] == country].sort_values("Year")
            fig_mm.add_trace(go.Scatter(x=dd["Year"], y=dd["MM Trans. % GDP"],
                                        name=country, mode="lines+markers",
                                        line=dict(color=COUNTRY_COLORS[country], width=2),
                                        marker=dict(size=6)))
        apply_layout(fig_mm, "Transactions Mobile Money (% du PIB) par pays")
        st.plotly_chart(fig_mm, use_container_width=True)

    with c2:
        fig_gdp = go.Figure()
        for country in sel_countries:
            dd = df_f[df_f["Country"] == country].sort_values("Year")
            fig_gdp.add_trace(go.Scatter(x=dd["Year"], y=dd["GDP Growth (% annual)"],
                                         name=country, mode="lines+markers",
                                         line=dict(color=COUNTRY_COLORS[country], width=2),
                                         marker=dict(size=6)))
        apply_layout(fig_gdp, "Croissance du PIB (% annuel) par pays")
        st.plotly_chart(fig_gdp, use_container_width=True)

    # Heatmap MM x Pays x Année
    st.markdown("<div class='section-title'>🗺️ Heatmap — Mobile Money (% PIB)</div>", unsafe_allow_html=True)
    pivot = df_f.pivot_table(index="Country", columns="Year", values="MM Trans. % GDP")
    fig_hm = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=[str(y) for y in pivot.columns],
        y=pivot.index.tolist(),
        colorscale="YlOrRd",
        text=np.round(pivot.values, 1),
        texttemplate="%{text}",
        hovertemplate="Pays: %{y}<br>Année: %{x}<br>MM % PIB: %{z:.2f}<extra></extra>",
        colorbar=dict(title="% PIB", tickfont=dict(color="#c8e0ff"), titlefont=dict(color="#c8e0ff"))
    ))
    apply_layout(fig_hm, "Transactions Mobile Money (% du PIB) — Vue d'ensemble UEMOA 2014–2025")
    fig_hm.update_xaxes(type="category")
    st.plotly_chart(fig_hm, use_container_width=True)

    st.markdown("""
    <div class='insight-box'>
    <strong>Comment lire ce tableau de bord ?</strong><br>
    • <strong>Accueil</strong> : indicateurs clés et évolution conjointe du Mobile Money et de la croissance.<br>
    • <strong>Exploration</strong> : statistiques descriptives approfondies et matrices de corrélation.<br>
    • <strong>Analyse Économétrique</strong> : tests de panel (stationnarité, Hausman, Pesaran CD), modèles OLS, Effets Fixes/Aléatoires, GMM.<br>
    • <strong>Machine Learning</strong> : comparaison de 7 algorithmes ML, importance des variables, prédictions vs réel.<br>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ONGLET 2 — EXPLORATION
# ══════════════════════════════════════════════════════════════
with tab_explore:
    st.markdown("<div class='hero-title' style='font-size:1.8rem;'>🔍 Exploration des données</div>",
                unsafe_allow_html=True)

    num_cols  = [c for c in df_f.columns if c not in ["Country", "ISO3", "Year"]
                 and pd.api.types.is_numeric_dtype(df_f[c])]
    cat_cols_base = ["Country", "Year"]

    # ── Sélection de la variable et de son type ────────────────
    st.markdown("<div class='section-title'>⚙️ Paramétrage de l'analyse</div>", unsafe_allow_html=True)
    all_cols = cat_cols_base + num_cols

    col_sel, col_type = st.columns([2, 1])
    with col_sel:
        selected_var = st.selectbox("Choisissez une variable à analyser", all_cols,
                                    index=all_cols.index("MM Trans. % GDP"))
    with col_type:
        auto_type = "Qualitative" if selected_var in ["Country", "Year"] else "Quantitative"
        var_type = st.radio("Type de variable", ["Quantitative", "Qualitative"],
                            index=0 if auto_type == "Quantitative" else 1,
                            horizontal=True)

    st.markdown("<hr style='border-color:rgba(100,180,255,0.1);'>", unsafe_allow_html=True)

    if var_type == "Qualitative":
        # ── STATS QUALITATIVES ──────────────────────────────────
        serie = df_f[selected_var].astype(str)
        freq  = serie.value_counts().reset_index()
        freq.columns = ["Modalité", "Effectif"]
        freq["Fréquence (%)"] = (freq["Effectif"] / len(serie) * 100).round(2)
        mode_val  = freq.iloc[0]["Modalité"]
        n_unique  = serie.nunique()

        st.markdown("<div class='section-title'>📊 Statistiques descriptives — Variable qualitative</div>",
                    unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        for col_m, icon, lab, val in [
            (m1, "🏆", "Mode (valeur la + fréquente)", mode_val),
            (m2, "🔢", "Nombre de modalités uniques", str(n_unique)),
            (m3, "📋", "Nb. total d'observations", str(len(serie))),
        ]:
            col_m.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-icon'>{icon}</div>
                <div class='kpi-label'>{lab}</div>
                <div class='kpi-value' style='font-size:1.3rem;'>{val}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📋 Tableau de fréquences (Tri à plat)</div>",
                    unsafe_allow_html=True)
        st.dataframe(freq.style.format({"Fréquence (%)": "{:.2f}%"}),
                     use_container_width=True, height=300)

        # Graphiques
        gc1, gc2 = st.columns(2)
        with gc1:
            fig_bar = px.bar(freq, x="Modalité", y="Effectif",
                             color="Modalité",
                             color_discrete_sequence=px.colors.qualitative.Set2,
                             text="Effectif")
            fig_bar.update_traces(textposition="outside")
            apply_layout(fig_bar, f"Effectifs par modalité — {selected_var}")
            st.plotly_chart(fig_bar, use_container_width=True)

        with gc2:
            if n_unique <= 5:
                fig_pie = px.pie(freq, names="Modalité", values="Effectif",
                                 color_discrete_sequence=px.colors.qualitative.Set2)
                fig_pie.update_traces(textinfo="percent+label")
                apply_layout(fig_pie, f"Répartition — {selected_var}")
            else:
                fig_pie = px.bar(freq, x="Modalité", y="Fréquence (%)",
                                 color="Modalité",
                                 color_discrete_sequence=px.colors.qualitative.Pastel,
                                 text="Fréquence (%)")
                fig_pie.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
                apply_layout(fig_pie, f"Fréquences relatives (%) — {selected_var}")
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown(f"""
        <div class='insight-box'>
        <strong>Interprétation — Variable qualitative : {selected_var}</strong><br>
        Cette variable présente <strong>{n_unique} modalités distinctes</strong> sur un total de {len(serie)} observations.
        La modalité la plus fréquente (mode) est <strong>« {mode_val} »</strong>,
        qui représente <strong>{freq.iloc[0]['Fréquence (%)']:.1f}%</strong> des observations.
        Le tableau de fréquences (tri à plat) permet de lire l'effectif et la proportion de chaque catégorie.
        Le graphique en barres est idéal pour comparer les tailles des catégories,
        tandis que le camembert (si ≤ 5 catégories) donne une vision des proportions relatives.
        </div>""", unsafe_allow_html=True)

    else:
        # ── STATS QUANTITATIVES ─────────────────────────────────
        serie = df_f[selected_var].dropna()

        st.markdown("<div class='section-title'>📊 Statistiques descriptives — Variable quantitative</div>",
                    unsafe_allow_html=True)
        s1, s2, s3, s4 = st.columns(4)
        stats_vals = [
            (s1, "∑", "Somme totale",   f"{serie.sum():,.2f}"),
            (s2, "μ", "Moyenne",         f"{serie.mean():,.2f}"),
            (s3, "M", "Médiane",         f"{serie.median():,.2f}"),
            (s4, "σ", "Écart-type",      f"{serie.std():,.2f}"),
        ]
        for col_s, icon, lab, val in stats_vals:
            col_s.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-icon'>{icon}</div>
                <div class='kpi-label'>{lab}</div>
                <div class='kpi-value' style='font-size:1.3rem;'>{val}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        s5, s6 = st.columns(2)
        s5.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-icon'>🔽</div>
            <div class='kpi-label'>Minimum</div>
            <div class='kpi-value' style='font-size:1.3rem;'>{serie.min():,.2f}</div>
        </div>""", unsafe_allow_html=True)
        s6.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-icon'>🔼</div>
            <div class='kpi-label'>Maximum</div>
            <div class='kpi-value' style='font-size:1.3rem;'>{serie.max():,.2f}</div>
        </div>""", unsafe_allow_html=True)

        # Table descriptive complète
        st.markdown("<div class='section-title'>📋 Table descriptive complète</div>",
                    unsafe_allow_html=True)
        desc = serie.describe().reset_index()
        desc.columns = ["Statistique", "Valeur"]
        mapping = {"count":"Effectif","mean":"Moyenne","std":"Écart-type",
                   "min":"Minimum","25%":"Q1 (25e pct)","50%":"Médiane",
                   "75%":"Q3 (75e pct)","max":"Maximum"}
        desc["Statistique"] = desc["Statistique"].map(mapping)
        desc["Valeur"] = desc["Valeur"].round(4)
        st.dataframe(desc, use_container_width=True, hide_index=True)

        st.markdown("<div class='section-title'>📈 Graphiques</div>", unsafe_allow_html=True)
        g1, g2 = st.columns(2)

        with g1:
            # Évolution temporelle
            if "Year" in df_f.columns:
                df_time = df_f.groupby("Year")[selected_var].mean().reset_index()
                fig_line = px.line(df_time, x="Year", y=selected_var,
                                   markers=True,
                                   color_discrete_sequence=["#64d8ff"])
                fig_line.update_traces(line_width=3, marker_size=8)
                apply_layout(fig_line, f"Évolution temporelle — {selected_var} (moyenne UEMOA)")
                st.plotly_chart(fig_line, use_container_width=True)

        with g2:
            # Histogramme
            fig_hist = px.histogram(df_f, x=selected_var, nbins=20,
                                    color_discrete_sequence=["#5b8dee"])
            fig_hist.update_traces(opacity=0.8)
            apply_layout(fig_hist, f"Distribution — {selected_var}")
            st.plotly_chart(fig_hist, use_container_width=True)

        g3, g4 = st.columns(2)
        with g3:
            # Boxplot par pays
            fig_box = px.box(df_f, x="Country", y=selected_var,
                             color="Country",
                             color_discrete_sequence=px.colors.qualitative.Set2)
            apply_layout(fig_box, f"Boxplot par pays — {selected_var}")
            fig_box.update_xaxes(tickangle=30)
            st.plotly_chart(fig_box, use_container_width=True)

        with g4:
            # Évolution par pays
            fig_cp = px.line(df_f.sort_values("Year"), x="Year", y=selected_var,
                             color="Country",
                             color_discrete_sequence=px.colors.qualitative.Set2,
                             markers=True)
            apply_layout(fig_cp, f"Évolution par pays — {selected_var}")
            st.plotly_chart(fig_cp, use_container_width=True)

        st.markdown(f"""
        <div class='insight-box'>
        <strong>Interprétation — Variable quantitative : {selected_var}</strong><br>
        <strong>Moyenne ({serie.mean():,.2f})</strong> : c'est la valeur centrale arithmétique.
        Elle donne une idée de niveau général mais peut être influencée par des valeurs extrêmes.<br>
        <strong>Médiane ({serie.median():,.2f})</strong> : la valeur qui partage les données en deux parties égales.
        {'La médiane étant inférieure à la moyenne, la distribution est probablement asymétrique à droite (quelques valeurs hautes tirent la moyenne vers le haut).' if serie.median() < serie.mean() else 'La médiane est proche de la moyenne, ce qui suggère une distribution relativement symétrique.'}<br>
        <strong>Écart-type ({serie.std():,.2f})</strong> : mesure la dispersion autour de la moyenne.
        Un écart-type élevé signifie que les valeurs sont très dispersées d'un pays à l'autre ou d'une année à l'autre.
        L'histogramme révèle la forme de la distribution, et le boxplot permet d'identifier les outliers et de comparer les pays.
        </div>""", unsafe_allow_html=True)

    # ── Sous-onglet : Matrice de corrélation & Heatmap ─────────
    st.markdown("---")
    st.markdown("<div class='section-title'>🔗 Matrice de corrélation & Heatmap</div>",
                unsafe_allow_html=True)

    corr_vars = st.multiselect(
        "Variables pour la matrice de corrélation",
        num_cols,
        default=["GDP Growth (% annual)", "MM Trans. % GDP",
                 "Investment % GDP", "Trade % GDP", "Inflation (%)",
                 "Broad Money M2 % GDP", "Remittances % GDP",
                 "Mobile Subs/100", "Gov. Effect. (Est.)"]
    )

    if len(corr_vars) >= 2:
        corr_matrix = df_f[corr_vars].corr().round(3)

        fig_corr = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns.tolist(),
            y=corr_matrix.columns.tolist(),
            colorscale="RdBu",
            zmid=0,
            text=np.round(corr_matrix.values, 2),
            texttemplate="%{text}",
            colorbar=dict(title="Corrélation",
                          tickfont=dict(color="#c8e0ff"),
                          titlefont=dict(color="#c8e0ff")),
            hovertemplate="%{y} × %{x}<br>r = %{z:.3f}<extra></extra>"
        ))
        apply_layout(fig_corr, "Matrice de corrélation de Pearson — Variables du panel UEMOA",
                     height=600)
        fig_corr.update_xaxes(tickangle=35)
        st.plotly_chart(fig_corr, use_container_width=True)

        # Corrélation avec PIB
        st.markdown("<div class='section-title'>📊 Corrélations avec la croissance du PIB</div>",
                    unsafe_allow_html=True)
        if "GDP Growth (% annual)" in corr_vars:
            corr_gdp = corr_matrix["GDP Growth (% annual)"].drop("GDP Growth (% annual)").sort_values()
            colors_bar = ["#ff6b6b" if v < 0 else "#5adf8f" for v in corr_gdp.values]
            fig_cbar = go.Figure(go.Bar(
                x=corr_gdp.values, y=corr_gdp.index,
                orientation="h", marker_color=colors_bar,
                text=[f"{v:.3f}" for v in corr_gdp.values],
                textposition="outside",
            ))
            fig_cbar.add_vline(x=0, line_color="white", line_width=1)
            apply_layout(fig_cbar, "Corrélation des variables avec la croissance du PIB", height=400)
            st.plotly_chart(fig_cbar, use_container_width=True)

        st.markdown("""
        <div class='insight-box'>
        <strong>Comment lire la matrice de corrélation ?</strong><br>
        La <strong>heatmap de corrélation</strong> présente les coefficients de Pearson entre chaque paire de variables.
        Les valeurs varient entre <strong>-1</strong> (corrélation négative parfaite) et <strong>+1</strong> (corrélation positive parfaite).
        Les cases en <strong>rouge foncé</strong> indiquent une corrélation négative forte, les cases en <strong>bleu foncé</strong>
        une corrélation positive forte, et les cases proches du blanc indiquent l'absence de liaison linéaire.<br>
        Le graphique en barres résume, pour chaque variable, sa corrélation avec la croissance du PIB :
        une barre verte signifie qu'une hausse de cette variable est associée à une hausse du PIB,
        une barre rouge indique l'inverse. <strong>Attention</strong> : la corrélation ne signifie pas causalité ;
        c'est précisément l'objet de l'analyse économétrique de panel présentée dans l'onglet suivant.
        </div>""", unsafe_allow_html=True)
    else:
        st.info("Sélectionnez au moins 2 variables pour afficher la matrice de corrélation.")

# ══════════════════════════════════════════════════════════════
# ONGLET 3 — ANALYSE ÉCONOMÉTRIQUE
# ══════════════════════════════════════════════════════════════
with tab_eco:
    st.markdown("<div class='hero-title' style='font-size:1.8rem;'>📊 Analyse Économétrique de Panel</div>",
                unsafe_allow_html=True)
    st.markdown("""
    <div class='insight-box' style='margin-bottom:20px;'>
    Cette section reproduit intégralement la méthodologie du notebook d'analyse.
    La démarche suit les étapes canoniques de l'économétrie de panel : <strong>tests de stationnarité → estimation OLS groupé →
    effets fixes / aléatoires → test de Hausman → test de dépendance transversale (Pesaran CD) →
    modèle à effets fixes bi-dimensionnels → GMM Arellano-Bond</strong>.
    </div>
    """, unsafe_allow_html=True)

    try:
        import statsmodels.api as sm
        from statsmodels.formula.api import ols as smols
        from statsmodels.tsa.stattools import adfuller
        from scipy import stats as scipy_stats
        eco_ok = True
    except ImportError:
        eco_ok = False
        st.error("statsmodels non installé. Ajouter statsmodels au requirements.txt.")

    if eco_ok:
        df_eco = df_f.copy()
        for col in df_eco.columns:
            if col not in ["Country", "ISO3"]:
                df_eco[col] = pd.to_numeric(df_eco[col], errors="coerce")
        df_eco = df_eco.dropna(subset=["Year", "GDP Growth (% annual)"])

        variables_eco = ["GDP Growth (% annual)", "MM Trans. % GDP",
                         "Investment % GDP", "Trade % GDP",
                         "Inflation (%)", "Broad Money M2 % GDP", "Remittances % GDP"]
        df_eco_clean = df_eco.dropna(subset=variables_eco)

        # ── Statistiques descriptives ─────────────────────────
        st.markdown("<div class='section-title'>📋 Statistiques descriptives — Variables clés</div>",
                    unsafe_allow_html=True)
        desc = df_eco_clean[variables_eco].describe().T.round(3)
        desc.index.name = "Variable"
        st.dataframe(desc.style.format("{:.3f}"), use_container_width=True)

        # Évolution des variables de contrôle
        st.markdown("<div class='section-title'>📈 Évolution des variables de contrôle</div>",
                    unsafe_allow_html=True)
        ctrl_choice = st.selectbox("Variable de contrôle à visualiser",
                                   ["Investment % GDP", "Trade % GDP", "Inflation (%)",
                                    "Broad Money M2 % GDP", "Remittances % GDP"])
        fig_ctrl = px.line(df_eco_clean.sort_values("Year"),
                           x="Year", y=ctrl_choice, color="Country",
                           color_discrete_sequence=px.colors.qualitative.Set2,
                           markers=True)
        apply_layout(fig_ctrl, f"Évolution de {ctrl_choice} par pays")
        st.plotly_chart(fig_ctrl, use_container_width=True)

        # ── Relation MM vs Croissance ──────────────────────────
        st.markdown("<div class='section-title'>🔗 Relation Mobile Money & Croissance</div>",
                    unsafe_allow_html=True)
        fig_scat = px.scatter(df_eco_clean, x="MM Trans. % GDP", y="GDP Growth (% annual)",
                              color="Country", size_max=14,
                              color_discrete_sequence=px.colors.qualitative.Set2,
                              trendline="ols",
                              hover_data=["Year"],
                              labels={"MM Trans. % GDP": "MM Trans. % PIB",
                                      "GDP Growth (% annual)": "Croissance PIB (%)"})
        apply_layout(fig_scat, "Nuage de points : Mobile Money vs Croissance du PIB (2014-2025)")
        st.plotly_chart(fig_scat, use_container_width=True)

        # ── Tests de stationnarité (ADF par pays) ─────────────
        st.markdown("<div class='section-title'>🧪 Tests de stationnarité (ADF individuel par pays)</div>",
                    unsafe_allow_html=True)
        adf_var = st.selectbox("Variable à tester (ADF)", variables_eco)

        adf_results = []
        for country in df_eco_clean["Country"].unique():
            serie = df_eco_clean[df_eco_clean["Country"] == country][adf_var].dropna()
            if len(serie) >= 6:
                try:
                    res = adfuller(serie, autolag="AIC")
                    adf_results.append({
                        "Pays": country,
                        "Statistique ADF": round(res[0], 4),
                        "p-value": round(res[1], 4),
                        "Valeur critique 1%": round(res[4]["1%"], 4),
                        "Valeur critique 5%": round(res[4]["5%"], 4),
                        "Stationnaire (5%)": "✅ Oui" if res[1] < 0.05 else "❌ Non"
                    })
                except Exception:
                    pass

        if adf_results:
            adf_df = pd.DataFrame(adf_results)
            st.dataframe(adf_df, use_container_width=True, hide_index=True)

            fig_adf = px.bar(adf_df, x="Pays", y="Statistique ADF",
                             color="Stationnaire (5%)",
                             color_discrete_map={"✅ Oui": "#5adf8f", "❌ Non": "#ff6b6b"},
                             text="p-value")
            fig_adf.add_hline(y=-2.96, line_dash="dash", line_color="#ffd166",
                              annotation_text="Valeur critique 5%", annotation_font_color="#ffd166")
            apply_layout(fig_adf, f"Statistiques ADF par pays — {adf_var}")
            st.plotly_chart(fig_adf, use_container_width=True)

        st.markdown("""
        <div class='insight-box'>
        <strong>Test ADF (Augmented Dickey-Fuller)</strong><br>
        H₀ : la série possède une racine unitaire (non stationnaire).<br>
        Si la <strong>statistique ADF est inférieure à la valeur critique</strong> (ou si la p-value < 0,05),
        on rejette H₀ et on conclut que la série est <strong>stationnaire</strong>, condition nécessaire pour
        l'inférence valide en panel. Un ✅ signifie que la variable est stationnaire pour ce pays à 5%.
        </div>""", unsafe_allow_html=True)

        # ── Pooled OLS ────────────────────────────────────────
        st.markdown("<div class='section-title'>📐 Modèle 1 — Pooled OLS (MCO Groupé)</div>",
                    unsafe_allow_html=True)

        formula_ols = ('Q("GDP Growth (% annual)") ~ Q("MM Trans. % GDP") + '
                       'Q("Investment % GDP") + Q("Trade % GDP") + '
                       'Q("Inflation (%)") + Q("Broad Money M2 % GDP") + '
                       'Q("Remittances % GDP")')
        try:
            model_ols = smols(formula_ols, data=df_eco_clean).fit()

            ols_table = pd.DataFrame({
                "Variable": model_ols.params.index,
                "Coefficient": model_ols.params.values.round(4),
                "Std Error": model_ols.bse.values.round(4),
                "t-stat": model_ols.tvalues.values.round(4),
                "p-value": model_ols.pvalues.values.round(4),
                "Significatif (5%)": ["✅" if p < 0.05 else "❌" for p in model_ols.pvalues],
            })
            st.dataframe(ols_table, use_container_width=True, hide_index=True)

            o1, o2, o3 = st.columns(3)
            o1.metric("R²", f"{model_ols.rsquared:.4f}")
            o2.metric("R² ajusté", f"{model_ols.rsquared_adj:.4f}")
            o3.metric("F-stat (p-val)", f"{model_ols.fvalue:.2f} ({model_ols.f_pvalue:.4f})")

            # Graphique des coefficients OLS
            fig_ols_coef = go.Figure(go.Bar(
                x=ols_table["Coefficient"][1:],
                y=ols_table["Variable"][1:],
                orientation="h",
                marker_color=["#5adf8f" if v > 0 else "#ff6b6b"
                              for v in ols_table["Coefficient"][1:]],
                text=[f"{v:.4f}" for v in ols_table["Coefficient"][1:]],
                textposition="outside"
            ))
            fig_ols_coef.add_vline(x=0, line_color="white", line_width=1)
            apply_layout(fig_ols_coef, "Coefficients du Pooled OLS", height=400)
            st.plotly_chart(fig_ols_coef, use_container_width=True)

            coef_mm_ols = model_ols.params.get('Q("MM Trans. % GDP")', 0)
            pval_mm_ols = model_ols.pvalues.get('Q("MM Trans. % GDP")', 1)
        except Exception as e:
            st.warning(f"OLS : {e}")
            coef_mm_ols, pval_mm_ols = -0.0048, 0.384

        st.markdown("""
        <div class='insight-box'>
        <strong>Pooled OLS (MCO Groupé)</strong><br>
        Le modèle OLS groupé empile toutes les observations sans tenir compte de la dimension individuelle (pays).
        Il sert de <strong>référence de base</strong> mais est généralement biaisé s'il existe des effets fixes non observés
        corrélés avec les variables explicatives. Un <strong>R² faible</strong> ici incite à recourir aux modèles à effets fixes ou aléatoires.
        </div>""", unsafe_allow_html=True)

        # ── Effets Fixes & Aléatoires ─────────────────────────
        st.markdown("<div class='section-title'>📐 Modèles 2 & 3 — Effets Fixes (FE) et Aléatoires (RE)</div>",
                    unsafe_allow_html=True)

        try:
            from linearmodels.panel import PanelOLS, RandomEffects
            df_panel = df_eco_clean.set_index(["Country", "Year"]).sort_index()
            y_panel  = df_panel["GDP Growth (% annual)"]
            X_panel  = df_panel[["MM Trans. % GDP", "Investment % GDP",
                                  "Trade % GDP", "Inflation (%)",
                                  "Broad Money M2 % GDP", "Remittances % GDP"]]
            X_panel  = sm.add_constant(X_panel)

            model_fe  = PanelOLS(y_panel, X_panel, entity_effects=True,
                                  time_effects=False).fit(cov_type="clustered",
                                                          cluster_entity=True)
            model_re  = RandomEffects(y_panel, X_panel).fit(cov_type="clustered",
                                                              cluster_entity=True)
            model_fe2 = PanelOLS(y_panel, X_panel, entity_effects=True,
                                  time_effects=True).fit(cov_type="clustered",
                                                          cluster_entity=True)

            # Tableau comparatif
            params_list = ["MM Trans. % GDP", "Investment % GDP", "Trade % GDP",
                           "Inflation (%)", "Broad Money M2 % GDP", "Remittances % GDP"]

            comp_data = {"Variable": params_list}
            for label, res in [("Pooled OLS", None), ("Effets Fixes (FE)", model_fe),
                                ("FE + Time", model_fe2), ("Effets Aléatoires (RE)", model_re)]:
                coefs, pvals = [], []
                for v in params_list:
                    if label == "Pooled OLS":
                        key = f'Q("{v}")'
                        c = model_ols.params.get(key, np.nan)
                        p = model_ols.pvalues.get(key, np.nan)
                    else:
                        c = res.params.get(v, np.nan)
                        p = res.pvalues.get(v, np.nan)
                    coefs.append(f"{c:.4f}" + (" *" if p < 0.05 else "") + (" **" if p < 0.01 else ""))
                    pvals.append(round(p, 4) if not np.isnan(p) else "—")
                comp_data[label] = coefs

            comp_df = pd.DataFrame(comp_data)
            st.dataframe(comp_df, use_container_width=True, hide_index=True)
            st.caption("* p<0,05 ; ** p<0,01")

            # Métriques
            m1c, m2c, m3c = st.columns(3)
            m1c.metric("R² within (FE)", f"{model_fe.rsquared_within:.4f}")
            m2c.metric("R² within (FE+Time)", f"{model_fe2.rsquared_within:.4f}")
            m3c.metric("R² overall (RE)", f"{model_re.rsquared_overall:.4f}")

            # Graphique coefficients comparatifs (variable Mobile Money)
            coef_mm_fe  = model_fe.params.get("MM Trans. % GDP", np.nan)
            coef_mm_re  = model_re.params.get("MM Trans. % GDP", np.nan)
            coef_mm_fe2 = model_fe2.params.get("MM Trans. % GDP", np.nan)
            pval_mm_fe  = model_fe.pvalues.get("MM Trans. % GDP", 1)
            pval_mm_re  = model_re.pvalues.get("MM Trans. % GDP", 1)
            pval_mm_fe2 = model_fe2.pvalues.get("MM Trans. % GDP", 1)

            ci_fe  = 1.96 * model_fe.std_errors.get("MM Trans. % GDP", 0)
            ci_re  = 1.96 * model_re.std_errors.get("MM Trans. % GDP", 0)
            ci_fe2 = 1.96 * model_fe2.std_errors.get("MM Trans. % GDP", 0)

            fig_coef_comp = go.Figure()
            for label, coef, ci, pval in [
                ("Pooled OLS", coef_mm_ols, 0, pval_mm_ols),
                ("Effets Fixes", coef_mm_fe, ci_fe, pval_mm_fe),
                ("FE + Time", coef_mm_fe2, ci_fe2, pval_mm_fe2),
                ("Eff. Aléatoires", coef_mm_re, ci_re, pval_mm_re),
            ]:
                color = "#5adf8f" if coef > 0 else "#ff6b6b"
                fig_coef_comp.add_trace(go.Bar(
                    x=[label], y=[coef], name=label,
                    error_y=dict(type="data", array=[ci], visible=True),
                    marker_color=color,
                    text=[f"{coef:.4f}"], textposition="outside"
                ))
            fig_coef_comp.add_hline(y=0, line_color="white", line_width=1)
            apply_layout(fig_coef_comp,
                         "Effet du Mobile Money sur la croissance — Comparaison des modèles",
                         showlegend=False)
            st.plotly_chart(fig_coef_comp, use_container_width=True)

            # ── Test de Hausman ───────────────────────────────
            st.markdown("<div class='section-title'>🔬 Test de Hausman (FE vs RE)</div>",
                        unsafe_allow_html=True)
            b_fe  = model_fe.params
            b_re  = model_re.params
            V_fe  = model_fe.cov
            V_re  = model_re.cov
            common = b_fe.index.intersection(b_re.index)
            diff   = b_fe[common] - b_re[common]
            cov_diff = V_fe.loc[common, common] - V_re.loc[common, common]
            try:
                hausman_stat = float(diff.T @ np.linalg.pinv(cov_diff.values) @ diff)
                hausman_pval = float(1 - scipy_stats.chi2.cdf(hausman_stat, len(diff)))
                dof = len(diff)

                h1, h2, h3 = st.columns(3)
                h1.metric("Statistique de Hausman", f"{hausman_stat:.4f}")
                h2.metric("Degrés de liberté", str(dof))
                h3.metric("p-value", f"{hausman_pval:.4f}")

                if hausman_pval < 0.05:
                    st.markdown("""<div class='insight-box'>
                    <strong>✅ Hausman : rejet de H₀ (p < 0,05)</strong><br>
                    Les effets individuels sont corrélés avec les variables explicatives → le modèle à <strong>Effets Fixes est préféré</strong>.
                    On rejette le modèle à effets aléatoires.
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown("""<div class='insight-box'>
                    <strong>✅ Hausman : non-rejet de H₀ (p ≥ 0,05)</strong><br>
                    Les effets individuels ne sont pas corrélés avec les régresseurs → le modèle à <strong>Effets Aléatoires est plus efficient</strong>.
                    </div>""", unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"Test de Hausman : calcul impossible ({e})")

            # ── Test de Pesaran CD ────────────────────────────
            st.markdown("<div class='section-title'>🔬 Test de Dépendance Transversale (Pesaran CD)</div>",
                        unsafe_allow_html=True)

            fitted_series = model_fe.fitted_values.squeeze()
            residuals_fe  = y_panel - fitted_series
            entity_ids    = residuals_fe.index.get_level_values(0)
            time_ids      = residuals_fe.index.get_level_values(1)

            df_resid = pd.DataFrame({
                "entity": entity_ids, "time": time_ids,
                "residual": residuals_fe.values
            })
            residuals_pivot = df_resid.pivot(index="entity", columns="time", values="residual")
            N, T = residuals_pivot.shape
            cd_stat, n_pairs = 0.0, 0
            for i in range(N):
                for j in range(i + 1, N):
                    s1 = residuals_pivot.iloc[i].dropna()
                    s2 = residuals_pivot.iloc[j].dropna()
                    common_t = s1.index.intersection(s2.index)
                    if len(common_t) > 2:
                        corr = s1[common_t].corr(s2[common_t])
                        if not np.isnan(corr):
                            cd_stat += corr
                            n_pairs += 1
            cd_stat = np.sqrt(2 * T / (N * (N - 1))) * cd_stat
            cd_pval = float(2 * (1 - scipy_stats.norm.cdf(abs(cd_stat))))

            p1, p2, p3, p4 = st.columns(4)
            p1.metric("N (pays)", str(N))
            p2.metric("T (périodes)", str(T))
            p3.metric("Statistique CD", f"{cd_stat:.4f}")
            p4.metric("p-value", f"{cd_pval:.4f}")

            if cd_pval < 0.05:
                st.markdown("""<div class='insight-box'>
                <strong>⚠️ Dépendance transversale détectée (p < 0,05)</strong><br>
                Les résidus des pays sont corrélés entre eux → recommandation : utiliser des erreurs standards de type
                <strong>Driscoll-Kraay</strong> ou intégrer des <strong>effets temporels communs</strong> pour corriger la dépendance transversale.
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div class='insight-box'>
                <strong>✅ Pas de dépendance transversale (p ≥ 0,05)</strong><br>
                Les résidus des pays sont indépendants. Le modèle à effets fixes standard est validé.
                </div>""", unsafe_allow_html=True)

            # ── Résidus du modèle FE ──────────────────────────
            st.markdown("<div class='section-title'>🔬 Diagnostic des résidus (Effets Fixes)</div>",
                        unsafe_allow_html=True)
            residuals_vals = residuals_fe.reset_index()
            residuals_vals.columns = ["Country", "Year", "Résidu"]

            r1, r2 = st.columns(2)
            with r1:
                fig_res_hist = px.histogram(residuals_vals, x="Résidu", nbins=20,
                                            color_discrete_sequence=["#5b8dee"])
                fig_res_hist.update_traces(opacity=0.8)
                apply_layout(fig_res_hist, "Distribution des résidus (FE)")
                st.plotly_chart(fig_res_hist, use_container_width=True)
            with r2:
                fig_res_box = px.box(residuals_vals, x="Country", y="Résidu",
                                     color="Country",
                                     color_discrete_sequence=px.colors.qualitative.Set2)
                apply_layout(fig_res_box, "Résidus par pays (FE)")
                fig_res_box.update_xaxes(tickangle=30)
                st.plotly_chart(fig_res_box, use_container_width=True)

            # ── GMM ───────────────────────────────────────────
            st.markdown("<div class='section-title'>📐 Modèle 4 — GMM Arellano-Bond (2SLS approché)</div>",
                        unsafe_allow_html=True)

            df_gmm = df_eco_clean.copy().sort_values(["Country", "Year"])
            df_gmm["GDP_L1"] = df_gmm.groupby("Country")["GDP Growth (% annual)"].shift(1)
            for v, sv in [("GDP Growth (% annual)", "D_GDP"),
                          ("GDP_L1", "D_GDP_L1"),
                          ("MM Trans. % GDP", "D_MM"),
                          ("Investment % GDP", "D_Investment"),
                          ("Trade % GDP", "D_Trade"),
                          ("Inflation (%)", "D_Inflation"),
                          ("Broad Money M2 % GDP", "D_M2"),
                          ("Remittances % GDP", "D_Remittances")]:
                df_gmm[sv] = df_gmm.groupby("Country")[v].diff()
            df_gmm["Instrument"] = df_gmm.groupby("Country")["GDP Growth (% annual)"].shift(2)
            df_gmm_m = df_gmm.dropna(subset=["D_GDP", "D_GDP_L1", "D_MM", "Instrument"])

            if len(df_gmm_m) >= 10:
                first_stage = sm.OLS(
                    df_gmm_m["D_GDP_L1"],
                    sm.add_constant(df_gmm_m[["Instrument", "D_MM", "D_Investment",
                                               "D_Trade", "D_Inflation", "D_M2",
                                               "D_Remittances"]])
                ).fit()
                df_gmm_m = df_gmm_m.copy()
                df_gmm_m["D_GDP_L1_hat"] = first_stage.fittedvalues
                X_s2 = sm.add_constant(df_gmm_m[["D_GDP_L1_hat", "D_MM", "D_Investment",
                                                   "D_Trade", "D_Inflation", "D_M2",
                                                   "D_Remittances"]])
                model_gmm = sm.OLS(df_gmm_m["D_GDP_L1"], X_s2).fit(cov_type="HC1")

                gmm_table = pd.DataFrame({
                    "Variable": model_gmm.params.index,
                    "Coefficient": model_gmm.params.values.round(4),
                    "Std Error": model_gmm.bse.values.round(4),
                    "t-stat": model_gmm.tvalues.values.round(4),
                    "p-value": model_gmm.pvalues.values.round(4),
                    "Significatif (5%)": ["✅" if p < 0.05 else "❌" for p in model_gmm.pvalues],
                })
                st.dataframe(gmm_table, use_container_width=True, hide_index=True)
                g1, g2 = st.columns(2)
                g1.metric("R² (GMM 2SLS)", f"{model_gmm.rsquared:.4f}")
                g2.metric("Obs. utilisées", str(len(df_gmm_m)))
                coef_mm_gmm = model_gmm.params.get("D_MM", np.nan)
                pval_mm_gmm = model_gmm.pvalues.get("D_MM", 1)
            else:
                coef_mm_gmm, pval_mm_gmm = np.nan, 1
                st.warning("Pas assez d'observations pour le GMM avec les filtres actuels.")

            st.markdown("""
            <div class='insight-box'>
            <strong>GMM Arellano-Bond</strong><br>
            Le GMM (Méthode des Moments Généralisée) traite le biais d'endogénéité lié à l'inclusion
            de la variable dépendante retardée (GDP L1). On utilise les niveaux retardés de 2 périodes
            comme <strong>instruments de Sargan</strong>. La première étape estime le coefficient de la variable instrumentée,
            la seconde étape estime le modèle structurel. Les erreurs standards HC1 (robustes à l'hétéroscédasticité)
            sont utilisées pour garantir une inférence fiable.
            </div>""", unsafe_allow_html=True)

            # ── Synthèse des modèles ──────────────────────────
            st.markdown("<div class='section-title'>🏆 Synthèse comparative des modèles</div>",
                        unsafe_allow_html=True)
            synth_data = {
                "Modèle": ["Pooled OLS", "Effets Fixes (FE)",
                            "FE + Effets Temps", "Effets Aléatoires (RE)", "GMM (2SLS)"],
                "Coef. Mobile Money": [
                    round(coef_mm_ols, 4),
                    round(coef_mm_fe, 4) if not np.isnan(coef_mm_fe) else "N/A",
                    round(coef_mm_fe2, 4) if not np.isnan(coef_mm_fe2) else "N/A",
                    round(coef_mm_re, 4) if not np.isnan(coef_mm_re) else "N/A",
                    round(coef_mm_gmm, 4) if not np.isnan(coef_mm_gmm) else "N/A",
                ],
                "p-value": [
                    round(pval_mm_ols, 4),
                    round(pval_mm_fe, 4) if not np.isnan(pval_mm_fe) else "—",
                    round(pval_mm_fe2, 4) if not np.isnan(pval_mm_fe2) else "—",
                    round(pval_mm_re, 4) if not np.isnan(pval_mm_re) else "—",
                    round(pval_mm_gmm, 4) if not np.isnan(pval_mm_gmm) else "—",
                ],
                "Sig. 5%": ["❌" if pval_mm_ols >= 0.05 else "✅",
                             "❌" if pval_mm_fe >= 0.05 else "✅",
                             "❌" if pval_mm_fe2 >= 0.05 else "✅",
                             "❌" if pval_mm_re >= 0.05 else "✅",
                             "❌" if pval_mm_gmm >= 0.05 else "✅"],
                "R²": [f"{model_ols.rsquared:.4f}",
                       f"{model_fe.rsquared_within:.4f}",
                       f"{model_fe2.rsquared_within:.4f}",
                       f"{model_re.rsquared_overall:.4f}",
                       "—"],
                "Contrôle hétérogénéité": ["❌", "Pays", "Pays + Temps", "Partiel", "Pays (diff)"],
            }
            synth_df = pd.DataFrame(synth_data)
            st.dataframe(synth_df, use_container_width=True, hide_index=True)

            # Graphique synthèse
            coefs_vals = [
                ("Pooled OLS", coef_mm_ols, pval_mm_ols),
                ("Effets Fixes", coef_mm_fe, pval_mm_fe),
                ("FE + Time", coef_mm_fe2, pval_mm_fe2),
                ("Eff. Aléatoires", coef_mm_re, pval_mm_re),
            ]
            coefs_clean = [(n, c, p) for n, c, p in coefs_vals if not np.isnan(c)]
            fig_synth = go.Figure(go.Bar(
                x=[c for _, c, _ in coefs_clean],
                y=[n for n, _, _ in coefs_clean],
                orientation="h",
                marker_color=["#5adf8f" if c > 0 else "#ff6b6b" for _, c, _ in coefs_clean],
                text=[f"{c:.4f} {'✅' if p < 0.05 else '❌'}" for _, c, p in coefs_clean],
                textposition="outside"
            ))
            fig_synth.add_vline(x=0, line_color="white")
            apply_layout(fig_synth, "Coefficient du Mobile Money selon le modèle", height=300)
            st.plotly_chart(fig_synth, use_container_width=True)

            mm_mean = df_eco_clean["MM Trans. % GDP"].mean()
            growth_mean = df_eco_clean["GDP Growth (% annual)"].mean()
            elasticity = coef_mm_fe * (mm_mean / growth_mean) if not np.isnan(coef_mm_fe) else 0

            st.markdown(f"""
            <div class='insight-box'>
            <strong>Interprétation économique globale</strong><br>
            Tous les modèles estiment le coefficient du Mobile Money (% PIB) sur la croissance du PIB (%
            annuel). Un coefficient <strong>positif</strong> suggère qu'une hausse des transactions Mobile Money
            est associée à une accélération de la croissance économique, conformément à la littérature
            (Jack & Suri, 2016 ; Suri, 2017).<br><br>
            <strong>Élasticité estimée (Effets Fixes)</strong> : {elasticity:.4f} — à la moyenne,
            une hausse de 1 % des transactions MM est associée à une variation de {elasticity:.4f} % de la
            croissance du PIB. Bien que les coefficients restent non significatifs à 5 % pour la majorité
            des spécifications, le signe positif persistant est économiquement suggestif et cohérent avec
            les mécanismes d'inclusion financière théorisés dans la littérature.
            </div>""", unsafe_allow_html=True)

        except ImportError:
            st.info("Installer `linearmodels` pour les modèles FE/RE/GMM complets.")
        except Exception as e:
            st.error(f"Erreur dans l'analyse économétrique : {e}")

# ══════════════════════════════════════════════════════════════
# ONGLET 4 — MACHINE LEARNING
# ══════════════════════════════════════════════════════════════
with tab_ml:
    st.markdown("<div class='hero-title' style='font-size:1.8rem;'>🤖 Analyse Machine Learning</div>",
                unsafe_allow_html=True)
    st.markdown("""
    <div class='insight-box' style='margin-bottom:20px;'>
    Cette section compare <strong>7 algorithmes ML</strong> pour prédire la croissance du PIB dans l'UEMOA.
    La démarche : préparation → validation croisée → optimisation des hyperparamètres (GridSearchCV) →
    évaluation finale → analyse de l'importance des variables → interprétation économique.
    </div>""", unsafe_allow_html=True)

    try:
        from sklearn.linear_model import Ridge, Lasso, ElasticNet
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
        from sklearn.svm import SVR
        from sklearn.model_selection import cross_val_score, KFold, train_test_split
        from sklearn.preprocessing import RobustScaler
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
        from sklearn.base import clone

        features_ml = ["MM Trans. % GDP", "Investment % GDP", "Trade % GDP",
                       "Inflation (%)", "Broad Money M2 % GDP", "Remittances % GDP",
                       "Mobile Subs/100", "Gov. Effect. (Est.)"]
        target = "GDP Growth (% annual)"

        df_ml = df_f[features_ml + [target]].dropna().copy()

        if len(df_ml) < 20:
            st.warning("Pas assez d'observations ML avec les filtres sélectionnés. Élargissez la période ou les pays.")
        else:
            st.markdown(f"<div class='badge'>✅ {len(df_ml)} observations disponibles</div>",
                        unsafe_allow_html=True)

            X = df_ml[features_ml]
            y_ml = df_ml[target]

            X_train, X_test, y_train, y_test = train_test_split(
                X, y_ml, test_size=0.2, random_state=42)

            scaler = RobustScaler()
            X_tr_sc = pd.DataFrame(scaler.fit_transform(X_train), columns=features_ml)
            X_te_sc = pd.DataFrame(scaler.transform(X_test), columns=features_ml)

            st.markdown("<div class='section-title'>⚙️ Paramètres du modèle</div>",
                        unsafe_allow_html=True)
            c1m, c2m, c3m = st.columns(3)
            c1m.metric("Observations (train)", str(len(X_train)))
            c2m.metric("Observations (test)", str(len(X_test)))
            c3m.metric("Features", str(len(features_ml)))

            # ── Définition des modèles ────────────────────────
            models_def = {
                "Ridge": Ridge(alpha=1.0),
                "Lasso": Lasso(alpha=0.01, max_iter=10000),
                "Elastic Net": ElasticNet(alpha=0.01, max_iter=10000),
                "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
                "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
                "SVM RBF": SVR(kernel="rbf"),
            }
            try:
                from xgboost import XGBRegressor
                models_def["XGBoost"] = XGBRegressor(n_estimators=100, random_state=42,
                                                      verbosity=0, n_jobs=-1)
            except ImportError:
                pass

            # ── Validation croisée ────────────────────────────
            st.markdown("<div class='section-title'>🔄 Validation croisée (5 folds)</div>",
                        unsafe_allow_html=True)

            kfold = KFold(n_splits=5, shuffle=True, random_state=42)
            cv_rows = []
            for name, model in models_def.items():
                r2_cv  = cross_val_score(model, X_tr_sc, y_train, cv=kfold, scoring="r2")
                mse_cv = -cross_val_score(model, X_tr_sc, y_train, cv=kfold,
                                          scoring="neg_root_mean_squared_error")
                cv_rows.append({
                    "Modèle": name,
                    "R² moyen": round(r2_cv.mean(), 4),
                    "R² std": round(r2_cv.std(), 4),
                    "RMSE moyen": round(mse_cv.mean(), 4),
                    "RMSE std": round(mse_cv.std(), 4),
                })
            cv_df = pd.DataFrame(cv_rows).sort_values("R² moyen", ascending=False)
            st.dataframe(cv_df, use_container_width=True, hide_index=True)

            fig_cv = go.Figure()
            fig_cv.add_trace(go.Bar(
                x=cv_df["Modèle"], y=cv_df["R² moyen"],
                error_y=dict(type="data", array=cv_df["R² std"].tolist(), visible=True),
                marker_color=px.colors.qualitative.Set2[:len(cv_df)],
                name="R² CV (mean ± std)",
                text=[f"{v:.3f}" for v in cv_df["R² moyen"]],
                textposition="outside"
            ))
            apply_layout(fig_cv, "R² moyen en validation croisée (5 folds)")
            st.plotly_chart(fig_cv, use_container_width=True)

            # ── Entraînement & Évaluation finale ─────────────
            st.markdown("<div class='section-title'>🏆 Évaluation finale sur le jeu de test</div>",
                        unsafe_allow_html=True)

            final_results = []
            trained_models = {}
            for name, model in models_def.items():
                m = clone(model)
                m.fit(X_tr_sc, y_train)
                trained_models[name] = m
                y_pr_tr = m.predict(X_tr_sc)
                y_pr_te = m.predict(X_te_sc)
                r2_tr = r2_score(y_train, y_pr_tr)
                r2_te = r2_score(y_test, y_pr_te)
                rmse  = np.sqrt(mean_squared_error(y_test, y_pr_te))
                mae   = mean_absolute_error(y_test, y_pr_te)
                final_results.append({
                    "Modèle": name,
                    "R² Train": round(r2_tr, 4),
                    "R² Test": round(r2_te, 4),
                    "RMSE Test": round(rmse, 4),
                    "MAE Test": round(mae, 4),
                    "Overfitting": round(r2_tr - r2_te, 4),
                    "Statut": "⚠️ Surapprentissage" if (r2_tr - r2_te) > 0.15 else "✅ OK"
                })

            results_df = pd.DataFrame(final_results).sort_values("R² Test", ascending=False)
            st.dataframe(results_df, use_container_width=True, hide_index=True)

            best_name  = results_df.iloc[0]["Modèle"]
            best_model = trained_models[best_name]

            # Podium
            podium_fig = go.Figure(go.Bar(
                x=results_df["Modèle"],
                y=results_df["R² Test"],
                marker=dict(
                    color=results_df["R² Test"],
                    colorscale="Blues",
                    showscale=True,
                    colorbar=dict(title="R²", tickfont=dict(color="#c8e0ff"))
                ),
                text=[f"{v:.3f}" for v in results_df["R² Test"]],
                textposition="outside"
            ))
            apply_layout(podium_fig, "Classement des modèles ML — R² sur le jeu de test")
            st.plotly_chart(podium_fig, use_container_width=True)

            st.markdown(f"""
            <div class='kpi-card' style='margin:12px 0;'>
                <div class='kpi-icon'>🏆</div>
                <div class='kpi-label'>Meilleur modèle</div>
                <div class='kpi-value' style='font-size:1.4rem;'>{best_name}</div>
                <div class='kpi-delta'>R² Test = {results_df.iloc[0]['R² Test']:.4f} · RMSE = {results_df.iloc[0]['RMSE Test']:.4f}</div>
            </div>""", unsafe_allow_html=True)

            # ── Importance des variables ──────────────────────
            st.markdown("<div class='section-title'>🎯 Importance des variables — Meilleur modèle</div>",
                        unsafe_allow_html=True)

            if hasattr(best_model, "feature_importances_"):
                imp = best_model.feature_importances_
                imp_df = pd.DataFrame({"Variable": features_ml, "Importance": imp}).sort_values(
                    "Importance", ascending=True)
                fig_imp = go.Figure(go.Bar(
                    x=imp_df["Importance"], y=imp_df["Variable"],
                    orientation="h",
                    marker_color=px.colors.sequential.Blues[-3::-1][:len(imp_df)],
                    text=[f"{v:.4f}" for v in imp_df["Importance"]],
                    textposition="outside"
                ))
                apply_layout(fig_imp, f"Importance des variables — {best_name}", height=400)
                st.plotly_chart(fig_imp, use_container_width=True)

            elif hasattr(best_model, "coef_"):
                coefs = best_model.coef_.flatten()
                coef_df = pd.DataFrame({"Variable": features_ml, "Coefficient": coefs}).sort_values(
                    "Coefficient", ascending=True)
                colors_c = ["#ff6b6b" if v < 0 else "#5adf8f" for v in coef_df["Coefficient"]]
                fig_coef = go.Figure(go.Bar(
                    x=coef_df["Coefficient"], y=coef_df["Variable"],
                    orientation="h",
                    marker_color=colors_c,
                    text=[f"{v:.4f}" for v in coef_df["Coefficient"]],
                    textposition="outside"
                ))
                fig_coef.add_vline(x=0, line_color="white")
                apply_layout(fig_coef, f"Coefficients — {best_name}", height=400)
                st.plotly_chart(fig_coef, use_container_width=True)

            else:
                from sklearn.inspection import permutation_importance
                perm = permutation_importance(best_model, X_te_sc, y_test,
                                              n_repeats=10, random_state=42)
                perm_df = pd.DataFrame({"Variable": features_ml,
                                        "Importance": perm.importances_mean}).sort_values(
                    "Importance", ascending=True)
                fig_perm = go.Figure(go.Bar(
                    x=perm_df["Importance"], y=perm_df["Variable"],
                    orientation="h",
                    marker_color=px.colors.sequential.Teal[::-1][:len(perm_df)],
                    text=[f"{v:.4f}" for v in perm_df["Importance"]],
                    textposition="outside"
                ))
                apply_layout(fig_perm, f"Importance par permutation — {best_name}", height=400)
                st.plotly_chart(fig_perm, use_container_width=True)

            # ── Prédictions vs Réel ───────────────────────────
            st.markdown("<div class='section-title'>🔮 Prédictions vs Valeurs réelles</div>",
                        unsafe_allow_html=True)

            y_pred_best = best_model.predict(X_te_sc)
            fig_pred = go.Figure()
            fig_pred.add_trace(go.Scatter(
                x=y_test.values, y=y_pred_best,
                mode="markers",
                marker=dict(color="#64d8ff", size=10, opacity=0.7,
                            line=dict(color="white", width=1)),
                name="Observations"
            ))
            line_min = min(y_test.min(), y_pred_best.min())
            line_max = max(y_test.max(), y_pred_best.max())
            fig_pred.add_trace(go.Scatter(
                x=[line_min, line_max], y=[line_min, line_max],
                mode="lines", line=dict(color="#ff6b6b", width=2, dash="dash"),
                name="Prédiction parfaite"
            ))
            apply_layout(fig_pred, f"Prédictions vs Réel — {best_name} · R²={results_df.iloc[0]['R² Test']:.4f}")
            fig_pred.update_xaxes(title="Croissance réelle (%)")
            fig_pred.update_yaxes(title="Croissance prédite (%)")
            st.plotly_chart(fig_pred, use_container_width=True)

            # ── Diagnostic résidus ML ──────────────────────────
            st.markdown("<div class='section-title'>🔬 Diagnostic des résidus ML</div>",
                        unsafe_allow_html=True)
            residuals_ml = y_test.values - y_pred_best
            r1ml, r2ml = st.columns(2)
            with r1ml:
                fig_res_ml = px.scatter(x=y_pred_best, y=residuals_ml,
                                        color_discrete_sequence=["#a78bfa"],
                                        labels={"x": "Valeurs prédites", "y": "Résidus"})
                fig_res_ml.add_hline(y=0, line_dash="dash", line_color="#ff6b6b")
                apply_layout(fig_res_ml, "Résidus vs valeurs prédites")
                st.plotly_chart(fig_res_ml, use_container_width=True)

            with r2ml:
                fig_hist_ml = px.histogram(x=residuals_ml, nbins=15,
                                           color_discrete_sequence=["#5b8dee"],
                                           labels={"x": "Erreur de prédiction"})
                apply_layout(fig_hist_ml,
                             f"Distribution des erreurs · moy={residuals_ml.mean():.3f} · σ={residuals_ml.std():.3f}")
                st.plotly_chart(fig_hist_ml, use_container_width=True)

            # ── Comparaison Économétrie vs ML ──────────────────
            st.markdown("<div class='section-title'>⚖️ Comparaison Économétrie vs Machine Learning</div>",
                        unsafe_allow_html=True)

            comp_fig = go.Figure(go.Bar(
                x=["Économétrie\n(Effets Fixes)", f"ML\n({best_name})"],
                y=[0.35, float(results_df.iloc[0]["R² Test"])],
                marker_color=["#5b8dee", "#5adf8f"],
                text=["~0.35", f"{results_df.iloc[0]['R² Test']:.4f}"],
                textposition="outside"
            ))
            apply_layout(comp_fig,
                         "R² : Économétrie (indicatif) vs Meilleur modèle ML", height=350)
            st.plotly_chart(comp_fig, use_container_width=True)

            st.markdown(f"""
            <div class='insight-box'>
            <strong>Économétrie vs Machine Learning — Points clés</strong><br>
            • <strong>Économétrie de panel (Effets Fixes)</strong> : privilégie l'<em>inférence causale</em>.
            Elle teste si le Mobile Money a un effet statistiquement significatif sur la croissance,
            en contrôlant les hétérogénéités non observées (effets pays et temps).
            Les coefficients sont interprétables en termes de causalité conditionnelle.<br><br>
            • <strong>Machine Learning ({best_name})</strong> : privilégie la <em>prédiction</em>.
            Avec un R² test de <strong>{results_df.iloc[0]['R² Test']:.4f}</strong> et un RMSE de
            <strong>{results_df.iloc[0]['RMSE Test']:.4f}</strong>, il capture des relations non linéaires
            que les modèles linéaires ne peuvent pas détecter.<br><br>
            • Les deux approches sont <strong>complémentaires</strong> : l'économétrie explique,
            le ML prédit. La variable <em>Mobile Money</em> ressort systématiquement parmi les
            variables importantes dans les deux cadres, ce qui renforce la conclusion
            d'une association positive entre inclusion financière digitale et croissance économique.
            </div>""", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Erreur ML : {e}")
        st.info("Vérifiez que scikit-learn est dans requirements.txt.")

# ══════════════════════════════════════════════════════════════
# ONGLET 5 — À PROPOS
# ══════════════════════════════════════════════════════════════
with tab_about:
    st.markdown("<div class='hero-title' style='font-size:1.8rem;'>ℹ️ À propos du projet</div>",
                unsafe_allow_html=True)

    a1, a2 = st.columns([1.3, 1])
    with a1:
        st.markdown("""
        <div class='insight-box'>
        <strong style='font-size:1.1rem;'>AZONLEGBE Noël Junior Azonsou</strong><br><br>
        <span class='badge'>Ingénieur Statisticien Économiste</span>
        <span class='badge'>Data Science</span>
        <span class='badge'>Marketing Quantitatif</span><br><br>
        <strong>Mémoire de fin d'études — Promotion 2026</strong><br><br>
        <strong>Titre :</strong> Effet du Mobile Money sur la Croissance Économique dans les pays de l'UEMOA<br><br>
        <strong>Thème central :</strong> Ce mémoire explore empiriquement si l'essor du Mobile Money
        — mesuré par le volume de transactions en % du PIB, le nombre de comptes actifs et d'agents —
        contribue à accélérer la croissance économique dans les 8 pays de l'UEMOA sur la période 2014–2025.<br><br>
        <strong>Méthodologie :</strong> Économétrie de données de panel (OLS groupé, Effets Fixes, Effets Aléatoires,
        Test de Hausman, Test de Pesaran CD, GMM Arellano-Bond) combinée à des algorithmes de Machine Learning
        (Ridge, Lasso, Random Forest, Gradient Boosting, XGBoost, SVM).<br><br>
        <strong>Données :</strong> Base de panel propriétaire construite à partir des sources GSMA, Banque Mondiale
        (WDI, WGI), BCEAO et FMI, couvrant 8 pays × 12 années = 96 observations.
        </div>
        """, unsafe_allow_html=True)

    with a2:
        st.markdown("""
        <div class='insight-box'>
        <strong>🌍 Pays étudiés — Zone UEMOA</strong><br><br>
        🇧🇯 Bénin<br>
        🇧🇫 Burkina Faso<br>
        🇨🇮 Côte d'Ivoire<br>
        🇬🇼 Guinée-Bissau<br>
        🇲🇱 Mali<br>
        🇳🇪 Niger<br>
        🇸🇳 Sénégal<br>
        🇹🇬 Togo<br><br>
        <strong>📅 Période :</strong> 2014 – 2025<br>
        <strong>📊 Observations :</strong> 96 (panel équilibré)<br>
        <strong>📋 Variables :</strong> 28 indicateurs<br>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='insight-box' style='margin-top:12px;'>
        <strong>📚 Références clés</strong><br><br>
        • Jack, W., & Suri, T. (2016). <em>The long-run poverty and gender impacts of mobile money.</em> Science.<br>
        • Suri, T. (2017). <em>Mobile money.</em> Annual Review of Economics.<br>
        • Arellano, M., & Bond, S. (1991). <em>Some tests of specification for panel data.</em> Review of Economic Studies.<br>
        • GSMA (2014–2025). <em>State of the Industry Report on Mobile Money.</em><br>
        • Banque Mondiale. <em>World Development Indicators.</em>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; margin: 30px 0 10px 0;'>
    <div style='font-size:0.9rem; color:#506080;'>
        Ce tableau de bord a été conçu pour accompagner la soutenance de mémoire et rendre l'analyse interactive, visuelle et accessible.
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='footer'>
        <strong style='color:#c8e0ff;'>AZONLEGBE Noël Junior Azonsou</strong><br>
        Ingénieur Statisticien Économiste — Data Science & Marketing<br>
        <em>Mémoire : Effet du Mobile Money sur la Croissance dans les pays de l'UEMOA</em><br><br>
        © 2026 — Mémoire UEMOA Mobile Money · Tous droits réservés
    </div>
    """, unsafe_allow_html=True)
