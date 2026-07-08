# ============================================================
# DASHBOARD — EFFET DE L'ÉDUCATION SUR LE NIVEAU DE VIE DES MÉNAGES AU BÉNIN
# Auteur : AZONLEGBE Noël Junior Azonsou
# Spécialité : Ingénieur Statisticien Économiste — Data Science & Marketing
# Mémoire 2026
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
    page_title="Éducation & Niveau de Vie — Bénin",
    #page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS Personnalisé ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1b2a 50%, #0a1628 100%);
    min-height: 100vh;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2a 0%, #112240 100%) !important;
    border-right: 1px solid rgba(100,200,150,0.15);
}
section[data-testid="stSidebar"] * { color: #cdd9f0 !important; }

.hero-title {
    font-size: 2.4rem; font-weight: 800;
    background: linear-gradient(135deg, #4ade80, #22d3ee, #a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 0.2rem; line-height: 1.15;
}
.hero-sub { font-size: 1rem; color: #7090b0; margin-top: 0.3rem; }

.kpi-card {
    background: linear-gradient(135deg, rgba(30,60,100,0.55), rgba(20,40,70,0.55));
    border: 1px solid rgba(74,222,128,0.2); border-radius: 16px;
    padding: 20px 16px 16px 16px; text-align: center;
    backdrop-filter: blur(12px); box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    transition: transform 0.2s ease, box-shadow 0.2s ease; height: 100%;
}
.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 8px 32px rgba(74,222,128,0.18); }
.kpi-icon { font-size: 1.8rem; margin-bottom: 6px; }
.kpi-label { font-size: 0.75rem; color: #7090b0; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 6px; }
.kpi-value { font-size: 1.7rem; font-weight: 700; color: #e0eeff; line-height: 1; }
.kpi-delta { font-size: 0.75rem; color: #4ade80; margin-top: 4px; }

.section-title {
    font-size: 1.2rem; font-weight: 700; color: #c8e0ff;
    border-left: 4px solid #22d3ee; padding-left: 12px; margin: 24px 0 14px 0;
}
.insight-box {
    background: rgba(30,50,90,0.45); border: 1px solid rgba(74,222,128,0.15);
    border-radius: 12px; padding: 18px 22px; margin-top: 14px;
    color: #a8c4e0; font-size: 0.88rem; line-height: 1.75;
}
.insight-box strong { color: #4ade80; }

.badge {
    display: inline-block; background: rgba(34,211,238,0.2);
    border: 1px solid rgba(34,211,238,0.4); border-radius: 20px;
    padding: 2px 12px; font-size: 0.73rem; color: #7dd3fc;
    margin-right: 6px; margin-bottom: 6px;
}
div[data-testid="stTabs"] button { font-size: 0.85rem; font-weight: 600; color: #7090b0; border-radius: 8px 8px 0 0; }
div[data-testid="stTabs"] button[aria-selected="true"] { color: #4ade80; border-bottom: 2px solid #4ade80; background: rgba(74,222,128,0.08); }

.stSelectbox > div > div, .stMultiSelect > div > div {
    background: rgba(20,40,70,0.7) !important;
    border: 1px solid rgba(74,222,128,0.2) !important;
    border-radius: 10px !important; color: #c8e0ff !important;
}
.stDataFrame { border-radius: 12px; overflow: hidden; }
div[data-testid="stDataFrameContainer"] { border: 1px solid rgba(74,222,128,0.15); border-radius: 12px; }

.footer {
    background: rgba(10,20,40,0.8); border-top: 1px solid rgba(74,222,128,0.1);
    padding: 20px 30px; text-align: center; color: #506080; font-size: 0.8rem;
    margin-top: 40px; border-radius: 12px;
}
.sig-positive { color: #4ade80; font-weight: 700; }
.sig-negative { color: #ff6b6b; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ─── Chargement des données ───────────────────────────────────
@st.cache_data
def load_default_data():
    df = pd.read_csv("data/base_ehcvm_education_niveauvie_benin2021.csv")
    return df

@st.cache_data
def load_uploaded_data(file_bytes, file_name):
    """Charge un fichier uploadé (.xlsx ou .csv) et vérifie les colonnes obligatoires."""
    REQUIRED_COLS = [
        'hhid', 'log_dep_percapita', 'annees_scol_chef',
        'niveau_instruction_chef', 'departement_nom', 'milieu_urbain',
        'chef_instruit', 'chef_superieur'
    ]
    try:
        if file_name.lower().endswith(".csv"):
            df = pd.read_csv(file_bytes)
        else:
            df = pd.read_excel(file_bytes)
        # Vérification des colonnes obligatoires
        missing = [c for c in REQUIRED_COLS if c not in df.columns]
        if missing:
            return None, f"Colonnes manquantes : {', '.join(missing)}"
        return df, None
    except Exception as e:
        return None, str(e)

# ─── Initialisation : charge la base par défaut si pas encore en session ──
if "df" not in st.session_state:
    try:
        st.session_state["df"] = load_default_data()
        st.session_state["data_source"] = "default"
    except FileNotFoundError:
        st.error("❌ Fichier CSV introuvable. Vérifiez que `data/base_ehcvm_education_niveauvie_benin2021.csv` est présent.")
        st.stop()

df = st.session_state["df"]

# Variables et palettes
PALETTE = px.colors.qualitative.Set2
EDUCATION_ORDER = ['1_Aucun', '2_Primaire', '3_Secondaire1', '4_Secondaire2', '5_Superieur']
EDUCATION_LABELS = {
    '1_Aucun': 'Aucun', '2_Primaire': 'Primaire',
    '3_Secondaire1': 'Secondaire 1', '4_Secondaire2': 'Secondaire 2', '5_Superieur': 'Supérieur'
}
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15,30,55,0.5)",
    font=dict(family="Inter", color="#c8e0ff"),
    xaxis=dict(gridcolor="rgba(100,180,255,0.08)", showline=False),
    yaxis=dict(gridcolor="rgba(100,180,255,0.08)", showline=False),
    legend=dict(bgcolor="rgba(10,25,50,0.7)", bordercolor="rgba(100,180,255,0.2)", borderwidth=1),
    margin=dict(l=20, r=20, t=45, b=20),
    hoverlabel=dict(bgcolor="rgba(10,25,50,0.9)", font_color="#c8e0ff"),
)

def apply_layout(fig, title="", **kwargs):
    fig.update_layout(title=dict(text=title, font=dict(size=14, color="#c8e0ff")),
                      **PLOTLY_LAYOUT, **kwargs)
    return fig

# ─── Cartographie du Bénin — bulles proportionnelles ──────────
# Coordonnées normalisées (sur 1000) des 12 départements, reprises du
# script d'analyse (notebook) afin de garder la même localisation visuelle.
COORD_DEPTS = {
    "Alibori": (585, 248), "Atacora": (372, 359), "Borgou": (538, 489),
    "Donga": (410, 442), "Collines": (455, 690), "Zou": (456, 790),
    "Couffo": (425, 828), "Plateau": (536, 775), "Mono": (432, 883),
    "Atlantique": (476, 888), "Oueme": (523, 856), "Littoral": (516, 912),
}

import base64
from pathlib import Path

@st.cache_data
def _load_map_background():
    img_path = Path("data/carte_benin_fond.jpg")
    if not img_path.exists():
        return None, 0, 0
    from PIL import Image
    im = Image.open(img_path)
    w, h = im.size
    b64 = base64.b64encode(img_path.read_bytes()).decode()
    return f"data:image/jpeg;base64,{b64}", w, h

def carte_bulles_benin(dept_series, titre, colorscale="Viridis", suffixe="", decimales=2):
    """Carte du Bénin avec bulles proportionnelles par département (Plotly, interactive)."""
    img_src, w, h = _load_map_background()
    vals = dept_series.reindex(list(COORD_DEPTS.keys()))
    v_min, v_max = vals.min(), vals.max()
    r_min, r_max = 16, 34

    def rayon(v):
        if pd.isna(v):
            return r_min
        if v_max == v_min:
            return (r_min + r_max) / 2
        return r_min + (v - v_min) * (r_max - r_min) / (v_max - v_min)

    xs, ys, sizes, hover = [], [], [], []
    for dept, (nx, ny) in COORD_DEPTS.items():
        v = vals.get(dept, np.nan)
        xs.append(nx / 1000 * w)
        ys.append(ny / 1000 * h)
        sizes.append(rayon(v))
        hover.append(f"<b>{dept}</b><br>Valeur : {v:.{decimales}f}{suffixe}" if pd.notna(v) else dept)

    fig = go.Figure()
    if img_src:
        fig.add_layout_image(dict(
            source=img_src, xref="x", yref="y", x=0, y=0,
            sizex=w, sizey=h, sizing="stretch", layer="below", opacity=0.95
        ))
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode="markers+text",
        marker=dict(size=sizes, color=vals.values,
                    colorscale=colorscale, showscale=True,
                    line=dict(color="black", width=1.3), sizemode="diameter",
                    colorbar=dict(title=dict(text=suffixe or "Valeur", font=dict(color="#c8e0ff")),
                                  tickfont=dict(color="#c8e0ff"))),
        text=[f"{v:.{decimales}f}" if pd.notna(v) else "" for v in vals.values],
        textposition="middle center", textfont=dict(color="white", size=10, family="Inter"),
        hovertext=hover, hoverinfo="text"
    ))
    fig.update_xaxes(visible=False, range=[0, w])
    fig.update_yaxes(visible=False, range=[h, 0], scaleanchor="x", scaleratio=1)
    fig.update_layout(
        title=dict(text=titre, font=dict(size=14, color="#c8e0ff")),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#c8e0ff"),
        margin=dict(l=10, r=10, t=45, b=10), height=560,
    )
    return fig

# Variables quali / quanti par défaut
QUANTI_COLS = ['age_chef', 'annees_scol_chef', 'dep_totale_annuelle', 'dep_educ',
               'taille_menage', 'score_actifs', 'dep_percapita',
               'log_dep_totale', 'log_dep_percapita', 'hhweight']
QUALI_COLS_DEFAULT = ['sexe_chef_bin', 'educ_hi_chef', 'diplome_chef', 'activite_chef',
                      'branch_chef', 'csp_chef', 'departement', 'departement_nom',
                      'milieu', 'milieu_urbain', 'educ_hi_mere',
                      'niveau_instruction_chef', 'niveau_instruction_mere',
                      'choc_economique', 'choc_naturel', 'choc_quelconque',
                      'tv', 'frigo', 'cuisin', 'ordin', 'decod', 'car',
                      'acces_electricite', 'logem', 'toilet', 'eauboi_ss',
                      'chef_instruit', 'chef_superieur']

all_cols = [c for c in df.columns if c != 'hhid']

# ─── Barre latérale ──────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:10px 0 20px 0;'>
        <div style='font-size:2.8rem;'></div>
        <div style='font-size:0.95rem;font-weight:700;color:#4ade80;margin-top:4px;'>Éducation & Niveau de Vie</div>
        <div style='font-size:0.7rem;color:#506080;margin-top:2px;'>Bénin 2021 — EHCVM · Mémoire ISE</div>
    </div>
    <hr style='border-color:rgba(74,222,128,0.12);margin-bottom:18px;'>
    """, unsafe_allow_html=True)

    st.markdown("FILTRES GLOBAUX")
    # ── Section upload ────────────────────────────────────────

    st.markdown("<hr style='border-color:rgba(74,222,128,0.1);'>", unsafe_allow_html=True)

    st.markdown("Informations pour importer votre base de données")

    st.markdown("""

    <div style='font-size:0.71rem; color:#7090b0; line-height:1.65; margin-bottom:10px;'>

        
        Vous pouvez remplacer la base par défaut par la vôtre.
        La base importée doit avoir exactement la même structure que la base fournie par défaut ; avec les premieres colonnes suivantes :
        
            hhid, log_dep_percapita, 
            annees_scol_chef, niveau_instruction_chef,
            departement_nom, milieu_residence...
        
        Formats acceptés : .csv ou .xlsx
        

    </div>

    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(

        "Choisir un fichier",

        type=["csv", "xlsx"],

        key="uploader_base",

        help="Doit avoir la même structure que la base EHCVM Bénin 2021"

    )

    if uploaded_file is not None:

        df_up, err = load_uploaded_data(uploaded_file, uploaded_file.name)

        if err:

            st.error(f"❌ Erreur : {err}")

        else:

            st.success(f" Fichier valide — {len(df_up):,} lignes · {df_up.shape[1]} colonnes")

            if st.button(" Charger cette base", use_container_width=True):

                st.session_state["df"] = df_up

                st.session_state["data_source"] = "uploaded"

                st.cache_data.clear()

                st.rerun()

    if st.session_state.get("data_source") == "uploaded":

        st.success(" Base importée active")

        if st.button(" Revenir à la base par défaut", use_container_width=True):

            st.session_state["df"] = load_default_data()

            st.session_state["data_source"] = "default"

            st.cache_data.clear()

            st.rerun()

    else:

        st.info(" Base par défaut active (EHCVM 2021)")

    st.markdown("<hr style='border-color:rgba(74,222,128,0.1);'>", unsafe_allow_html=True)

    # ── fin section upload ────────────────────────────────────
    sel_dept = st.multiselect(
        "Département", sorted(df['departement_nom'].unique()),
        default=sorted(df['departement_nom'].unique()),
        help="Filtrer par département"
    )
    sel_milieu = st.multiselect(
        "Milieu de résidence", ["Rural (0)", "Urbain (1)"],
        default=["Rural (0)", "Urbain (1)"]
    )
    milieu_vals = []
    if "Rural (0)" in sel_milieu: milieu_vals.append(0)
    if "Urbain (1)" in sel_milieu: milieu_vals.append(1)

    st.markdown("<hr style='border-color:rgba(74,222,128,0.1);'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem;color:#506080;text-align:center;line-height:1.9;'>
        <b style='color:#7090b0;'>Auteur</b><br>AZONLEGBE Noël Junior Azonsou<br><br>
        <b style='color:#7090b0;'>Spécialité</b><br>Ingénieur Statisticien Économiste<br>Data Science & Marketing<br><br>
        <b style='color:#7090b0;'>© 2026</b>
    </div>
    """, unsafe_allow_html=True)

df_f = df[df['departement_nom'].isin(sel_dept) & df['milieu_urbain'].isin(milieu_vals)].copy()

# ─── Navigation ──────────────────────────────────────────────
tab_home, tab_explore, tab_eco, tab_ml, tab_about = st.tabs([
    " Accueil", " Exploration", " Analyse Économétrique", " Machine Learning", " À propos"
])

# ══════════════════════════════════════════════════════════════
# ONGLET 1 — ACCUEIL
# ══════════════════════════════════════════════════════════════
with tab_home:
    st.markdown("""
    <div style='padding:10px 0 24px 0;'>
        <div class='hero-title'>Effet de l'Éducation sur le Niveau de Vie<br>des Ménages au Bénin</div>
        <div class='hero-sub'>Tableau de bord interactif · Données EHCVM 2021 · Mémoire de fin d'études ISE 2026</div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    k1, k2, k3, k4, k5 = st.columns(5)
    n_obs = len(df_f)
    moy_dep = df_f['log_dep_percapita'].mean()
    moy_scol = df_f['annees_scol_chef'].mean()
    pct_instruit = (df_f['chef_instruit'].mean() * 100)
    pct_sup = (df_f['chef_superieur'].mean() * 100)

    for col, icon, label, value, delta in [
        (k1, "", "Ménages analysés", f"{n_obs:,}", "Observations EHCVM 2021"),
        (k2, "", "Log dép./tête moyen", f"{moy_dep:.3f}", "Variable dépendante"),
        (k3, "", "Années de scol. moy.", f"{moy_scol:.1f} ans", "Chef de ménage"),
        (k4, "", "Chefs instruits", f"{pct_instruit:.1f}%", "Au moins primaire"),
        (k5, "", "Chefs niveau supérieur", f"{pct_sup:.1f}%", "Universitaire ou +"),
    ]:
        col.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-icon'>{icon}</div>
            <div class='kpi-label'>{label}</div>
            <div class='kpi-value'>{value}</div>
            <div class='kpi-delta'>{delta}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class='insight-box'>
        <strong>Contexte du mémoire</strong><br>
        Ce tableau de bord explore empiriquement la relation entre le <strong>niveau d'instruction du chef de ménage</strong>
        et le <strong>niveau de vie des ménages béninois</strong>, mesuré par le logarithme de la dépense per capita annuelle.
        Les données proviennent de l'<strong>Enquête Harmonisée sur les Conditions de Vie des Ménages (EHCVM 2021)</strong>
        conduite au Bénin, couvrant <strong>8 032 ménages</strong> répartis dans les 12 départements du pays.
        La démarche combine <strong>statistiques descriptives</strong>, <strong>économétrie MCO</strong> avec tests de spécification,
        et <strong>algorithmes de Machine Learning</strong> pour une analyse complète et robuste.
    </div>
    """, unsafe_allow_html=True)

    # ── Graphique central : Log dép. par tête selon le niveau d'instruction ──
    st.markdown("<div class='section-title'> Évolution conjointe — Niveau de vie selon le niveau d'éducation</div>", unsafe_allow_html=True)

    df_home = df_f[df_f['niveau_instruction_chef'].isin(EDUCATION_ORDER)].copy()
    df_home['educ_label'] = df_home['niveau_instruction_chef'].map(EDUCATION_LABELS)

    fig_joint = make_subplots(rows=1, cols=2, subplot_titles=["Log dépense per capita par niveau d'instruction", "Part des ménages par niveau d'instruction"])
    stats_educ = df_home.groupby('niveau_instruction_chef')['log_dep_percapita'].mean().reindex(EDUCATION_ORDER).reset_index()
    stats_educ['label'] = stats_educ['niveau_instruction_chef'].map(EDUCATION_LABELS)
    counts_educ = df_home['niveau_instruction_chef'].value_counts().reindex(EDUCATION_ORDER).reset_index()
    counts_educ.columns = ['niveau', 'count']
    counts_educ['label'] = counts_educ['niveau'].map(EDUCATION_LABELS)
    counts_educ['pct'] = counts_educ['count'] / counts_educ['count'].sum() * 100

    colors_educ = ['#22d3ee', '#4ade80', '#fbbf24', '#f472b6', '#a78bfa']
    fig_joint.add_trace(go.Bar(x=stats_educ['label'], y=stats_educ['log_dep_percapita'],
                               marker_color=colors_educ, text=stats_educ['log_dep_percapita'].round(3),
                               textposition='outside', name="Moy. log dép."), row=1, col=1)
    fig_joint.add_trace(go.Bar(x=counts_educ['label'], y=counts_educ['pct'],
                               marker_color=colors_educ, text=counts_educ['pct'].round(1),
                               texttemplate='%{text:.1f}%', textposition='outside', name="Part (%)"), row=1, col=2)
    apply_layout(fig_joint, height=420, showlegend=False)
    fig_joint.update_layout(annotations=[
        dict(text="Log dépense per capita par niveau d'instruction", x=0.22, y=1.08, xref='paper', yref='paper', showarrow=False, font=dict(color="#c8e0ff", size=13)),
        dict(text="Part des ménages par niveau d'instruction", x=0.78, y=1.08, xref='paper', yref='paper', showarrow=False, font=dict(color="#c8e0ff", size=13)),
    ])
    st.plotly_chart(fig_joint, use_container_width=True)
    st.markdown("""
    <div class='insight-box'>
        <strong>Lecture du graphique</strong><br>
        Le panneau de gauche montre une progression <strong>monotone et marquée</strong> du log de la dépense per capita
        avec le niveau d'instruction : les ménages dont le chef a atteint le niveau supérieur affichent un niveau de vie
        significativement plus élevé que ceux sans instruction. Le panneau de droite révèle que la majorité des ménages
        béninois (plus de 56%) sont dirigés par un chef <strong>sans aucune instruction</strong>, ce qui souligne
        l'enjeu majeur de la politique éducative pour la réduction des inégalités de niveau de vie.
    </div>
    """, unsafe_allow_html=True)

    # ── Cartes du Bénin — bulles proportionnelles ──
    st.markdown("<div class='section-title'> Cartographie du niveau de vie et de la scolarisation</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='insight-box' style='margin-bottom:14px;'>
        Chaque bulle représente un département : sa <strong>couleur</strong> et sa <strong>taille</strong> sont proportionnelles
        à la valeur moyenne affichée. Cette lecture spatiale complète l'analyse statistique en révélant les
        <strong>disparités géographiques</strong> du niveau de vie et de l'accès à l'éducation au Bénin.
    </div>
    """, unsafe_allow_html=True)
    map1, map2 = st.columns(2)
    with map1:
        dep_dep_data = df_f.groupby('departement_nom')['log_dep_percapita'].mean()
        st.plotly_chart(
            carte_bulles_benin(dep_dep_data, "Log dépense moyenne par tête, par département",
                                colorscale="RdYlBu_r", suffixe="", decimales=3),
            use_container_width=True
        )
    with map2:
        dep_scol_data = df_f.groupby('departement_nom')['annees_scol_chef'].mean()
        st.plotly_chart(
            carte_bulles_benin(dep_scol_data, "Années moyennes de scolarisation du chef, par département",
                                colorscale="YlGnBu", suffixe=" ans", decimales=1),
            use_container_width=True
        )
    st.markdown("""
    <div class='insight-box'>
        <strong>Lecture des cartes</strong><br>
        La carte de gauche confirme que le <strong>Littoral</strong> (Cotonou) et l'<strong>Atlantique</strong> — départements les plus urbanisés —
        affichent les niveaux de vie les plus élevés, tandis que les départements du nord et du centre-ouest présentent des valeurs plus faibles.
        La carte de droite montre une géographie très proche pour la scolarisation du chef de ménage, ce qui illustre visuellement
        le lien spatial entre éducation et niveau de vie qui sera testé formellement dans l'onglet <strong>Analyse Économétrique</strong>
        (hétérogénéité spatiale, Test de Chow).
    </div>
    """, unsafe_allow_html=True)

    # ── Boxplot global par département ──
    st.markdown("<div class='section-title'> Niveau de vie moyen par département</div>", unsafe_allow_html=True)
    dept_stats = df_f.groupby('departement_nom')['log_dep_percapita'].mean().sort_values(ascending=False).reset_index()
    fig_dept = px.bar(
         dept_stats,
         x='departement_nom',
         y='log_dep_percapita',
         color='log_dep_percapita',
         color_continuous_scale='Viridis',
         text=dept_stats['log_dep_percapita'].round(3)
    )
    fig_dept.update_traces(textposition='outside')
    fig_dept.update_layout(coloraxis_colorbar=dict(
             title="Log dép.",
             tickfont=dict(color="#c8e0ff"),
             title_font=dict(color="#c8e0ff")
    ))

    

    apply_layout(fig_dept, "Log dépense per capita moyenne par département (EHCVM 2021)", height=380)
    st.plotly_chart(fig_dept, use_container_width=True)

    # ── Heatmap Éducation × Milieu ──
    st.markdown("<div class='section-title'> Heatmap — Niveau de vie selon éducation et milieu de résidence</div>", unsafe_allow_html=True)
    df_hm = df_home.copy()
    df_hm['Milieu'] = df_hm['milieu_urbain'].map({0: 'Rural', 1: 'Urbain'})
    pivot_hm = df_hm.groupby(['niveau_instruction_chef', 'Milieu'])['log_dep_percapita'].mean().unstack().reindex(EDUCATION_ORDER)
    pivot_hm.index = [EDUCATION_LABELS[k] for k in pivot_hm.index]
    fig_hm = go.Figure(go.Heatmap(
        z=pivot_hm.values, 
        x=pivot_hm.columns.tolist(), 
        y=pivot_hm.index.tolist(),
        colorscale='Cividis',
        colorbar=dict(
            title="Log dép.", 
            tickfont=dict(color="#c8e0ff"), 
            title_font=dict(color="#c8e0ff")  # Correction ici
        )
    ))

    apply_layout(fig_hm, "Niveau de vie moyen (log dép./tête) selon l'instruction et le milieu", height=380)
    st.plotly_chart(fig_hm, use_container_width=True)
    st.markdown("""
    <div class='insight-box'>
        <strong>Comment lire ce tableau de bord ?</strong><br>
        • <strong>Accueil</strong> : indicateurs clés, cartographie et visualisation du lien éducation–niveau de vie.<br>
        • <strong>Exploration</strong> : statistiques descriptives complètes par type de variable (qualitative ou quantitative), matrice de corrélation.<br>
        • <strong>Analyse Économétrique</strong> : tests préalables (VIF, Breusch-Pagan, Jarque-Bera, RESET), régressions MCO (3 modèles progressifs), diagnostic des résidus,
        traitement de l'endogénéité (2SLS &amp; Test de Hausman), hétérogénéité spatiale (MCO par département &amp; Test de Chow).<br>
        • <strong>Machine Learning</strong> : validation croisée, optimisation GridSearchCV, comparaison de 7 algorithmes, importance des variables, comparaison MCO vs ML.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ONGLET 2 — EXPLORATION
# ══════════════════════════════════════════════════════════════
with tab_explore:
    st.markdown("<div class='hero-title' style='font-size:1.8rem;'> Exploration des données</div>", unsafe_allow_html=True)

    subtab_var, subtab_corr = st.tabs([" Statistiques par variable", " Matrice de corrélation & Heatmap"])

    # ── Sous-onglet : statistiques par variable ──
    with subtab_var:
        st.markdown("<div class='section-title'> Paramétrage de l'analyse</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='insight-box' style='margin-bottom:16px;'>
            <strong>Instructions</strong> — Sélectionnez d'abord la variable à analyser, puis indiquez son type
            (<strong>Quantitative</strong> = valeurs numériques continues, <strong>Qualitative</strong> = catégories ou codes).
            Les statistiques et graphiques s'adapteront automatiquement au type choisi.
        </div>
        """, unsafe_allow_html=True)

        col_sel, col_type = st.columns([2, 1])
        with col_sel:
            selected_var = st.selectbox("Variable à analyser", all_cols, index=all_cols.index('log_dep_percapita'))
        with col_type:
            default_type = "Quantitative" if selected_var in QUANTI_COLS else "Qualitative"
            var_type = st.radio("Type de variable", ["Quantitative", "Qualitative"],
                                index=0 if default_type == "Quantitative" else 1, horizontal=True)

        st.markdown("<hr style='border-color:rgba(74,222,128,0.1);'>", unsafe_allow_html=True)

        if var_type == "Qualitative":
            serie = df_f[selected_var].astype(str)
            freq = serie.value_counts().reset_index()
            freq.columns = ["Modalité", "Effectif"]
            freq["Fréquence (%)"] = (freq["Effectif"] / len(serie) * 100).round(2)
            freq["Fréquence cumulée (%)"] = freq["Fréquence (%)"].cumsum().round(2)
            mode_val = freq.iloc[0]["Modalité"]
            n_unique = serie.nunique()

            st.markdown("<div class='section-title'> Statistiques descriptives — Variable qualitative</div>", unsafe_allow_html=True)
            m1, m2, m3 = st.columns(3)
            for col_m, icon, lab, val in [
                (m1, "", "Mode (valeur la + fréquente)", mode_val),
                (m2, "🔢", "Nombre de modalités uniques", str(n_unique)),
                (m3, "", "Nb. total d'observations", f"{len(serie):,}"),
            ]:
                col_m.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-icon'>{icon}</div>
                    <div class='kpi-label'>{lab}</div>
                    <div class='kpi-value' style='font-size:1.2rem;'>{val}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'> Tableau de fréquences (Tri à plat)</div>", unsafe_allow_html=True)
            st.dataframe(freq.style.format({"Fréquence (%)": "{:.2f}%", "Fréquence cumulée (%)": "{:.2f}%"}), use_container_width=True, height=300)

            gc1, gc2 = st.columns(2)
            with gc1:
                fig_bar = px.bar(freq.head(20), x="Modalité", y="Effectif",
                                 color="Modalité", color_discrete_sequence=PALETTE,
                                 text="Effectif")
                fig_bar.update_traces(textposition="outside")
                apply_layout(fig_bar, f"Effectifs par modalité — {selected_var}")
                st.plotly_chart(fig_bar, use_container_width=True)
            with gc2:
                if n_unique <= 8:
                    fig_pie = px.pie(freq, names="Modalité", values="Effectif",
                                     color_discrete_sequence=PALETTE)
                    fig_pie.update_traces(textinfo="percent+label")
                    apply_layout(fig_pie, f"Répartition — {selected_var}")
                else:
                    fig_bar2 = px.bar(freq.head(20), x="Modalité", y="Fréquence (%)",
                                      color="Modalité", color_discrete_sequence=px.colors.qualitative.Pastel,
                                      text="Fréquence (%)")
                    fig_bar2.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
                    apply_layout(fig_bar2, f"Fréquences relatives (%) — {selected_var}")
                    fig_pie = fig_bar2
                st.plotly_chart(fig_pie, use_container_width=True)

            # Courbe de Lorenz approximative des fréquences
            if n_unique >= 3:
                st.markdown("<div class='section-title'> Courbe de concentration des modalités</div>", unsafe_allow_html=True)
                freq_sorted = freq.sort_values('Effectif', ascending=False).reset_index(drop=True)
                freq_sorted['cum_pct'] = freq_sorted['Effectif'].cumsum() / freq_sorted['Effectif'].sum() * 100
                freq_sorted['rank_pct'] = (freq_sorted.index + 1) / len(freq_sorted) * 100
                fig_lorenz = go.Figure()
                fig_lorenz.add_trace(go.Scatter(x=freq_sorted['rank_pct'], y=freq_sorted['cum_pct'],
                                                 mode='lines+markers', name='Concentration',
                                                 line=dict(color='#4ade80', width=2)))
                fig_lorenz.add_trace(go.Scatter(x=[0, 100], y=[0, 100], mode='lines',
                                                 name='Équirépartition', line=dict(color='#ff6b6b', dash='dash')))
                apply_layout(fig_lorenz, "Courbe de concentration des modalités (% cumulé d'effectif)", height=340)
                fig_lorenz.update_xaxes(title="% des modalités (classées par effectif décroissant)")
                fig_lorenz.update_yaxes(title="% cumulé de l'effectif total")
                st.plotly_chart(fig_lorenz, use_container_width=True)

            st.markdown(f"""
            <div class='insight-box'>
                <strong>Interprétation — Variable qualitative : {selected_var}</strong><br>
                Cette variable présente <strong>{n_unique} modalités distinctes</strong> sur un total de {len(serie):,} observations.
                La <strong>modalité la plus fréquente (mode)</strong> est <strong>« {mode_val} »</strong>,
                qui représente <strong>{freq.iloc[0]['Fréquence (%)']:.1f}%</strong> des observations.
                Le <strong>tableau de fréquences (tri à plat)</strong> permet de lire l'effectif et la proportion de chaque catégorie,
                ainsi que la fréquence cumulée qui indique, par exemple, combien de modalités couvrent 80% des observations.
                Le <strong>graphique en barres</strong> est idéal pour comparer les tailles des catégories,
                tandis que le <strong>camembert</strong> (affiché si ≤ 8 catégories) offre une vision globale des proportions relatives.
                La <strong>courbe de concentration</strong> montre si les effectifs sont uniformément répartis entre modalités
                (proche de la diagonale = équirépartition) ou très concentrés sur peu de modalités.
            </div>
            """, unsafe_allow_html=True)

        else:
            # ── STATS QUANTITATIVES ──
            serie = df_f[selected_var].dropna()
            st.markdown("<div class='section-title'> Statistiques descriptives — Variable quantitative</div>", unsafe_allow_html=True)

            s1, s2, s3, s4 = st.columns(4)
            for col_s, icon, lab, val in [
                (s1, "∑", "Somme totale", f"{serie.sum():,.2f}"),
                (s2, "μ", "Moyenne", f"{serie.mean():,.4f}"),
                (s3, "M", "Médiane", f"{serie.median():,.4f}"),
                (s4, "σ", "Écart-type", f"{serie.std():,.4f}"),
            ]:
                col_s.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-icon'>{icon}</div>
                    <div class='kpi-label'>{lab}</div>
                    <div class='kpi-value' style='font-size:1.2rem;'>{val}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            s5, s6, s7, s8 = st.columns(4)
            for col_s, icon, lab, val in [
                (s5, "⬇️", "Minimum", f"{serie.min():,.4f}"),
                (s6, "⬆️", "Maximum", f"{serie.max():,.4f}"),
                (s7, "Q1", "1er quartile (25%)", f"{serie.quantile(0.25):,.4f}"),
                (s8, "Q3", "3e quartile (75%)", f"{serie.quantile(0.75):,.4f}"),
            ]:
                col_s.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-icon'>{icon}</div>
                    <div class='kpi-label'>{lab}</div>
                    <div class='kpi-value' style='font-size:1.2rem;'>{val}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'> Table descriptive complète</div>", unsafe_allow_html=True)
            desc = serie.describe()
            skew = serie.skew()
            kurt = serie.kurtosis()
            desc_ext = pd.DataFrame({
                "Statistique": ["Effectif", "Moyenne", "Écart-type", "Minimum", "Q1 (25e pct)", "Médiane", "Q3 (75e pct)", "Maximum", "Asymétrie (skewness)", "Aplatissement (kurtosis)", "Coeff. variation (%)"],
                "Valeur": [
                    f"{int(desc['count']):,}", f"{desc['mean']:.6f}", f"{desc['std']:.6f}",
                    f"{desc['min']:.6f}", f"{desc['25%']:.6f}", f"{desc['50%']:.6f}",
                    f"{desc['75%']:.6f}", f"{desc['max']:.6f}",
                    f"{skew:.4f}", f"{kurt:.4f}", f"{(serie.std()/serie.mean()*100):.2f}%"
                ]
            })
            st.dataframe(desc_ext, use_container_width=True, hide_index=True)

            st.markdown("<div class='section-title'> Graphiques</div>", unsafe_allow_html=True)
            g1, g2 = st.columns(2)
            with g1:
                fig_hist = px.histogram(df_f, x=selected_var, nbins=40, color_discrete_sequence=["#4ade80"])
                fig_hist.update_traces(opacity=0.8)
                fig_hist.add_vline(x=float(serie.mean()), line_dash="dash", line_color="#fbbf24",
                                   annotation_text=f"Moy={serie.mean():.3f}", annotation_font_color="#fbbf24")
                fig_hist.add_vline(x=float(serie.median()), line_dash="dot", line_color="#f472b6",
                                   annotation_text=f"Med={serie.median():.3f}", annotation_font_color="#f472b6")
                apply_layout(fig_hist, f"Histogramme de distribution — {selected_var}")
                st.plotly_chart(fig_hist, use_container_width=True)
            with g2:
                fig_box_g = px.box(df_f, y=selected_var, color_discrete_sequence=["#22d3ee"],
                                   points="outliers")
                apply_layout(fig_box_g, f"Boîte à moustaches (détection outliers) — {selected_var}")
                st.plotly_chart(fig_box_g, use_container_width=True)

            g3, g4 = st.columns(2)
            with g3:
                # Boxplot par niveau d'instruction
                df_box2 = df_f[df_f['niveau_instruction_chef'].isin(EDUCATION_ORDER)].copy()
                df_box2['educ_label'] = df_box2['niveau_instruction_chef'].map(EDUCATION_LABELS)
                fig_box2 = px.box(df_box2, x='educ_label', y=selected_var,
                                  color='educ_label', color_discrete_sequence=PALETTE,
                                  category_orders={'educ_label': list(EDUCATION_LABELS.values())})
                apply_layout(fig_box2, f"Boxplot par niveau d'instruction — {selected_var}")
                st.plotly_chart(fig_box2, use_container_width=True)
            with g4:
                # Boxplot par milieu
                df_box3 = df_f.copy()
                df_box3['Milieu'] = df_box3['milieu_urbain'].map({0: 'Rural', 1: 'Urbain'})
                fig_box3 = px.violin(df_box3, x='Milieu', y=selected_var,
                                     color='Milieu', color_discrete_sequence=['#22d3ee', '#f472b6'],
                                     box=True, points='outliers')
                apply_layout(fig_box3, f"Distribution par milieu (violon + boxplot) — {selected_var}")
                st.plotly_chart(fig_box3, use_container_width=True)

            # Densité par département
            st.markdown("<div class='section-title'> Distribution par département</div>", unsafe_allow_html=True)
            fig_box_dept = px.box(df_f, x='departement_nom', y=selected_var,
                                  color='departement_nom', color_discrete_sequence=px.colors.qualitative.Set3,
                                  points=False)
            fig_box_dept.update_xaxes(tickangle=35)
            apply_layout(fig_box_dept, f"Distribution de {selected_var} par département", height=400)
            st.plotly_chart(fig_box_dept, use_container_width=True)

            st.markdown(f"""
            <div class='insight-box'>
                <strong>Interprétation — Variable quantitative : {selected_var}</strong><br>
                • <strong>Moyenne ({serie.mean():,.4f})</strong> : valeur centrale arithmétique, sensible aux valeurs extrêmes (outliers).<br>
                • <strong>Médiane ({serie.median():,.4f})</strong> : valeur coupant les données en deux parties égales ;
                {'la médiane est <strong>inférieure</strong> à la moyenne → distribution <strong>asymétrique à droite</strong> (valeurs élevées tirent la moyenne vers le haut).' if serie.median() < serie.mean() else 'médiane proche de la moyenne → distribution <strong>relativement symétrique</strong>.'}<br>
                • <strong>Écart-type ({serie.std():,.4f})</strong> : mesure de dispersion autour de la moyenne. Le
                <strong>coefficient de variation ({serie.std()/serie.mean()*100:.1f}%)</strong> indique une dispersion
                {'forte' if serie.std()/serie.mean() > 0.5 else 'modérée' if serie.std()/serie.mean() > 0.2 else 'faible'} de la variable.<br>
                • <strong>L'histogramme</strong> révèle la forme globale de la distribution ; la <strong>boîte à moustaches</strong> identifie les valeurs atypiques (outliers au-delà de 1,5 × IQR).
                Les graphiques par <strong>niveau d'instruction</strong> et <strong>milieu</strong> permettent une analyse différenciée des sous-groupes.
            </div>
            """, unsafe_allow_html=True)

    # ── Sous-onglet : Matrice de corrélation ──
    with subtab_corr:
        st.markdown("<div class='section-title'> Matrice de corrélation & Heatmap</div>", unsafe_allow_html=True)
        num_cols_corr = [c for c in QUANTI_COLS if c in df_f.columns]
        default_corr = ['log_dep_percapita', 'annees_scol_chef', 'age_chef', 'taille_menage',
                        'score_actifs', 'dep_educ', 'log_dep_totale']
        corr_vars = st.multiselect("Variables pour la matrice de corrélation", num_cols_corr, default=default_corr)

        if len(corr_vars) >= 2:
            corr_matrix = df_f[corr_vars].corr().round(3)
            fig_corr = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns.tolist(),
                y=corr_matrix.index.tolist(),
                colorscale='RdBu', zmin=-1, zmax=1,
                colorbar=dict(
                    title="r", 
                    tickfont=dict(color="#c8e0ff"), 
                    title_font=dict(color="#c8e0ff")  # Correction ici
                ),
                hovertemplate="%{y} × %{x}<br>r = %{z:.3f}<extra></extra>"
            ))

            apply_layout(fig_corr, "Matrice de corrélation de Pearson — Variables quantitatives clés", height=550)
            fig_corr.update_xaxes(tickangle=35)
            st.plotly_chart(fig_corr, use_container_width=True)

            # Corrélation avec log_dep_percapita
            if 'log_dep_percapita' in corr_vars:
                st.markdown("<div class='section-title'> Corrélations avec le niveau de vie (log dép. per capita)</div>", unsafe_allow_html=True)
                corr_dep = corr_matrix['log_dep_percapita'].drop('log_dep_percapita').sort_values()
                colors_bar = ["#ff6b6b" if v < 0 else "#4ade80" for v in corr_dep.values]
                fig_cbar = go.Figure(go.Bar(
                    x=corr_dep.values, y=corr_dep.index, orientation="h",
                    marker_color=colors_bar, text=[f"{v:.3f}" for v in corr_dep.values], textposition="outside"
                ))
                fig_cbar.add_vline(x=0, line_color="white", line_width=1)
                apply_layout(fig_cbar, "Corrélation de chaque variable avec le log de la dépense per capita", height=380)
                st.plotly_chart(fig_cbar, use_container_width=True)

            st.markdown("""
            <div class='insight-box'>
                <strong>Comment lire la matrice de corrélation ?</strong><br>
                La <strong>heatmap de corrélation de Pearson</strong> présente les coefficients de corrélation linéaire entre chaque paire de variables numériques.
                Les valeurs varient entre <strong>-1</strong> (corrélation négative parfaite : quand l'une augmente, l'autre diminue) et <strong>+1</strong> (corrélation positive parfaite).
                Les cases en <strong>rouge foncé</strong> indiquent une forte corrélation négative, celles en <strong>bleu foncé</strong> une forte corrélation positive,
                et les cases proches du blanc indiquent l'absence de liaison linéaire.<br><br>
                Le <strong>graphique en barres horizontales</strong> synthétise, pour chaque variable, sa corrélation avec le <em>log de la dépense per capita</em> (notre variable dépendante) :
                une barre <strong>verte</strong> signifie qu'une hausse de cette variable est associée à un niveau de vie plus élevé,
                une barre <strong>rouge</strong> indique l'inverse.
                Les <strong>corrélations > 0,7 en valeur absolue</strong> entre deux variables explicatives signalent un risque de <strong>multicolinéarité</strong>, qui sera formellement testé dans l'onglet Économétrique via le VIF.<br>
                <strong>Attention</strong> : la corrélation mesure uniquement la liaison <em>linéaire</em> et ne signifie pas causalité.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Sélectionnez au moins 2 variables pour afficher la matrice.")

# ══════════════════════════════════════════════════════════════
# ONGLET 3 — ANALYSE ÉCONOMÉTRIQUE
# ══════════════════════════════════════════════════════════════
with tab_eco:
    st.markdown("<div class='hero-title' style='font-size:1.8rem;'> Analyse Économétrique — MCO</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='insight-box' style='margin-bottom:20px;'>
        Cette section reproduit intégralement la méthodologie du notebook d'analyse.
        La démarche suit les étapes canoniques de l'économétrie MCO puis leurs extensions causales et spatiales :
        <strong>Statistiques descriptives → Tests préalables (VIF, Breusch-Pagan, Jarque-Bera) →
        Estimations MCO progressives (3 modèles) → Test RESET de Ramsey → Diagnostic des résidus →
        Traitement de l'endogénéité (2SLS &amp; Test de Hausman) → Hétérogénéité spatiale (MCO par département &amp; Test de Chow)</strong>.
    </div>
    """, unsafe_allow_html=True)

    try:
        import statsmodels.api as sm
        import statsmodels.formula.api as smf
        from statsmodels.stats.outliers_influence import variance_inflation_factor
        from statsmodels.stats.diagnostic import het_breuschpagan, linear_reset
        from statsmodels.stats.stattools import durbin_watson
        from scipy.stats import jarque_bera, shapiro
        from scipy.stats import chi2 as sp_chi2, f as sp_f
        eco_ok = True
    except ImportError:
        eco_ok = False
        st.error("statsmodels non installé. Ajoutez statsmodels au requirements.txt.")

    if eco_ok:
        variables_modele = ['annees_scol_chef', 'age_chef', 'taille_menage',
                            'score_actifs', 'acces_electricite', 'choc_economique', 'milieu_urbain']
        target_eco = 'log_dep_percapita'
        base_modele = df_f[variables_modele + [target_eco]].dropna().copy()
        base_modele['age_chef_carre'] = base_modele['age_chef'] ** 2
        base_modele['education_carre'] = base_modele['annees_scol_chef'] ** 2

        # ── Stats descriptives ──
        st.markdown("<div class='section-title'> Statistiques descriptives — Variables du modèle</div>", unsafe_allow_html=True)
        desc_eco = base_modele[variables_modele + [target_eco]].describe().T.round(4)
        st.dataframe(desc_eco.style.format("{:.4f}"), use_container_width=True)

        # Scatter éducation vs niveau de vie
        st.markdown("<div class='section-title'> Relation Éducation – Niveau de vie</div>", unsafe_allow_html=True)
        sc1, sc2 = st.columns(2)
        with sc1:
            fig_scat = px.scatter(base_modele, x='annees_scol_chef', y=target_eco,
                                  opacity=0.3, color_discrete_sequence=['#22d3ee'],
                                  trendline='ols', trendline_color_override='#fbbf24')
            apply_layout(fig_scat, "Années de scolarité vs Log dépense per capita (avec droite MCO)", height=380)
            fig_scat.update_xaxes(title="Années de scolarité du chef")
            fig_scat.update_yaxes(title="Log dépense per capita")
            st.plotly_chart(fig_scat, use_container_width=True)
        with sc2:
            df_box_educ = df_f[df_f['niveau_instruction_chef'].isin(EDUCATION_ORDER)].copy()
            df_box_educ['educ_label'] = df_box_educ['niveau_instruction_chef'].map(EDUCATION_LABELS)
            fig_bx_eco = px.box(df_box_educ, x='educ_label', y=target_eco, color='educ_label',
                                color_discrete_sequence=PALETTE,
                                category_orders={'educ_label': list(EDUCATION_LABELS.values())})
            apply_layout(fig_bx_eco, "Log dép. per capita par niveau d'instruction", height=380)
            st.plotly_chart(fig_bx_eco, use_container_width=True)

        # ── Test VIF ──
        st.markdown("<div class='section-title'> Test 1 — Multicolinéarité (VIF)</div>", unsafe_allow_html=True)
        X_vif = base_modele[variables_modele].copy()
        X_vif_const = sm.add_constant(X_vif)
        vif_data = pd.DataFrame()
        vif_data['Variable'] = X_vif_const.columns
        vif_data['VIF'] = [variance_inflation_factor(X_vif_const.values, i) for i in range(X_vif_const.shape[1])]
        vif_data['Diagnostic'] = vif_data['VIF'].apply(lambda v: "✅ OK" if v < 5 else ("⚠️ Alerte" if v < 10 else "❌ Sévère"))
        st.dataframe(vif_data.round(4), use_container_width=True, hide_index=True)

        fig_vif = go.Figure(go.Bar(
            x=vif_data['VIF'][1:], y=vif_data['Variable'][1:], orientation='h',
            marker_color=['#4ade80' if v < 5 else '#fbbf24' if v < 10 else '#ff6b6b' for v in vif_data['VIF'][1:]],
            text=vif_data['VIF'][1:].round(3), textposition='outside'
        ))
        fig_vif.add_vline(x=5, line_dash='dash', line_color='#fbbf24', annotation_text='Seuil 5', annotation_font_color='#fbbf24')
        fig_vif.add_vline(x=10, line_dash='dash', line_color='#ff6b6b', annotation_text='Seuil 10', annotation_font_color='#ff6b6b')
        apply_layout(fig_vif, "Facteurs d'Inflation de la Variance (VIF) par variable", height=370)
        st.plotly_chart(fig_vif, use_container_width=True)
        st.markdown("""
        <div class='insight-box'>
            <strong>Test de multicolinéarité — VIF (Variance Inflation Factor)</strong><br>
            Le VIF mesure à quel point la variance d'un coefficient estimé est « gonflée » en raison de la corrélation avec les autres variables.
            <strong>VIF = 1</strong> : aucune corrélation. <strong>VIF entre 1 et 5</strong> : acceptable. <strong>VIF > 5</strong> : alerte multicolinéarité.
            <strong>VIF > 10</strong> : multicolinéarité sévère, les coefficients MCO sont instables et peu fiables.
            En l'absence de multicolinéarité sévère, les estimations MCO restent BLUE (Best Linear Unbiased Estimators) selon le théorème de Gauss-Markov.
        </div>
        """, unsafe_allow_html=True)

        # Estimation du modèle 3 pour les tests suivants
        y_eco = base_modele[target_eco]
        X_eco = sm.add_constant(base_modele[variables_modele])
        modele3_sm = sm.OLS(y_eco, X_eco).fit(cov_type='HC3')

        # ── Test Breusch-Pagan ──
        st.markdown("<div class='section-title'> Test 2 — Hétéroscédasticité (Breusch-Pagan)</div>", unsafe_allow_html=True)
        bp_test = het_breuschpagan(modele3_sm.resid, X_eco)
        bp_labels = ['Lagrange Multiplier', 'p-value LM', 'F-statistique', 'p-value F']
        bp_df = pd.DataFrame({'Statistique': bp_labels, 'Valeur': [round(v, 4) for v in bp_test]})
        st.dataframe(bp_df, use_container_width=True, hide_index=True)
        bp_pval = bp_test[1]
        if bp_pval < 0.05:
            st.markdown(f"""<div class='insight-box'>
                <strong>⚠️ Hétéroscédasticité détectée (p-value = {bp_pval:.4f} &lt; 0,05)</strong><br>
                H₀ (homoscédasticité) est rejetée. La variance des résidus n'est pas constante.
                Les écarts-types OLS classiques sont biaisés → nous utilisons des <strong>erreurs standards robustes HC3 (Huber-White)</strong>
                pour garantir une inférence valide malgré l'hétéroscédasticité.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class='insight-box'>
                <strong>✅ Homoscédasticité non rejetée (p-value = {bp_pval:.4f} ≥ 0,05)</strong><br>
                La variance des résidus est homogène. Les écarts-types MCO classiques sont valides.
            </div>""", unsafe_allow_html=True)

        # ── Test Jarque-Bera ──
        st.markdown("<div class='section-title'> Test 3 — Normalité des résidus (Jarque-Bera)</div>", unsafe_allow_html=True)
        jb_stat, jb_pval = jarque_bera(modele3_sm.resid)
        jb_df = pd.DataFrame({'Statistique': ['JB Statistique', 'p-value', 'Asymétrie (skewness)', 'Aplatissement (kurtosis)'],
                              'Valeur': [round(jb_stat, 4), round(jb_pval, 4),
                                         round(pd.Series(modele3_sm.resid).skew(), 4),
                                         round(pd.Series(modele3_sm.resid).kurtosis(), 4)]})
        st.dataframe(jb_df, use_container_width=True, hide_index=True)
        if jb_pval < 0.05:
            st.markdown(f"""<div class='insight-box'>
                <strong>⚠️ Résidus non normaux (p = {jb_pval:.4f} &lt; 0,05)</strong><br>
                Mais avec <strong>N = {len(base_modele):,} >> 100</strong>, on invoque le
                <strong>Théorème Central Limite (TCL)</strong> : les tests asymptotiques (t, F) restent valides.
                La non-normalité ne compromet pas l'inférence pour de grands échantillons.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class='insight-box'>
                <strong>✅ Résidus normalement distribués (p = {jb_pval:.4f} ≥ 0,05)</strong><br>
                L'hypothèse de normalité des résidus est vérifiée. Les tests de Student et de Fisher sont exacts.
            </div>""", unsafe_allow_html=True)

        # ── MCO — 3 modèles ──
        st.markdown("<div class='section-title'> Estimations MCO — 3 modèles progressifs</div>", unsafe_allow_html=True)
        modele1 = smf.ols("log_dep_percapita ~ annees_scol_chef", data=base_modele).fit(cov_type='HC3')
        modele2 = smf.ols("log_dep_percapita ~ annees_scol_chef + age_chef + taille_menage", data=base_modele).fit(cov_type='HC3')
        modele3 = smf.ols("log_dep_percapita ~ annees_scol_chef + age_chef + taille_menage + score_actifs + acces_electricite + choc_economique + milieu_urbain", data=base_modele).fit(cov_type='HC3')

        # Tableau comparatif
        variables_disp = ['Intercept', 'annees_scol_chef', 'age_chef', 'taille_menage',
                          'score_actifs', 'acces_electricite', 'choc_economique', 'milieu_urbain']
        labels_disp = {
            'Intercept': 'Constante', 'annees_scol_chef': 'Années scol. chef',
            'age_chef': 'Âge chef', 'taille_menage': 'Taille ménage',
            'score_actifs': 'Score actifs', 'acces_electricite': 'Accès électricité',
            'choc_economique': 'Choc économique', 'milieu_urbain': 'Milieu urbain'
        }
        comp_rows = []
        for v in variables_disp:
            row = {'Variable': labels_disp.get(v, v)}
            for m_label, m in [('Modèle 1', modele1), ('Modèle 2', modele2), ('Modèle 3', modele3)]:
                try:
                    c = m.params[v]; p = m.pvalues[v]
                    stars = '***' if p < 0.01 else '**' if p < 0.05 else '*' if p < 0.1 else ''
                    row[m_label] = f"{c:.4f}{stars}\n({m.bse[v]:.4f})"
                except: row[m_label] = '—'
            comp_rows.append(row)
        comp_rows.append({'Variable': 'R²', 'Modèle 1': f"{modele1.rsquared:.4f}",
                          'Modèle 2': f"{modele2.rsquared:.4f}", 'Modèle 3': f"{modele3.rsquared:.4f}"})
        comp_rows.append({'Variable': 'R² ajusté', 'Modèle 1': f"{modele1.rsquared_adj:.4f}",
                          'Modèle 2': f"{modele2.rsquared_adj:.4f}", 'Modèle 3': f"{modele3.rsquared_adj:.4f}"})
        comp_rows.append({'Variable': 'AIC', 'Modèle 1': f"{modele1.aic:.1f}",
                          'Modèle 2': f"{modele2.aic:.1f}", 'Modèle 3': f"{modele3.aic:.1f}"})
        comp_rows.append({'Variable': 'N', 'Modèle 1': str(int(modele1.nobs)),
                          'Modèle 2': str(int(modele2.nobs)), 'Modèle 3': str(int(modele3.nobs))})
        comp_df = pd.DataFrame(comp_rows)
        st.dataframe(comp_df, use_container_width=True, hide_index=True)
        st.caption("*p<0.1  **p<0.05  ***p<0.01 · Erreurs standards HC3 (robustes) entre parenthèses")

        # Métriques Modèle 3
        m1c, m2c, m3c, m4c = st.columns(4)
        m1c.metric("R² (Modèle 3)", f"{modele3.rsquared:.4f}")
        m2c.metric("R² ajusté", f"{modele3.rsquared_adj:.4f}")
        m3c.metric("F-stat", f"{modele3.fvalue:.2f}")
        m4c.metric("p-value (F)", f"{modele3.f_pvalue:.4f}")

        # Graphique des coefficients du modèle 3
        st.markdown("<div class='section-title'> Coefficients du modèle complet (Modèle 3 — HC3)</div>", unsafe_allow_html=True)
        params3 = modele3.params.drop('Intercept')
        pvals3 = modele3.pvalues.drop('Intercept')
        ci3 = modele3.conf_int().drop('Intercept')
        coef_df = pd.DataFrame({
            'Variable': [labels_disp.get(v, v) for v in params3.index],
            'Coefficient': params3.values,
            'p-value': pvals3.values,
            'CI_low': ci3[0].values,
            'CI_high': ci3[1].values,
        })
        fig_coef3 = go.Figure()
        for _, row in coef_df.iterrows():
            color = '#4ade80' if row['Coefficient'] > 0 else '#ff6b6b'
            sig = row['p-value'] < 0.05
            fig_coef3.add_trace(go.Scatter(
                x=[row['CI_low'], row['CI_high']], y=[row['Variable'], row['Variable']],
                mode='lines', line=dict(color=color, width=3 if sig else 1.5, dash='solid' if sig else 'dot'),
                showlegend=False
            ))
            fig_coef3.add_trace(go.Scatter(
                x=[row['Coefficient']], y=[row['Variable']], mode='markers+text',
                marker=dict(color=color, size=12 if sig else 8, symbol='circle'),
                text=[f"{row['Coefficient']:.4f}{'✅' if sig else ''}"],
                textposition='middle right', showlegend=False
            ))
        fig_coef3.add_vline(x=0, line_color='white', line_width=1.5, line_dash='dash')
        apply_layout(fig_coef3, "Coefficients MCO avec intervalles de confiance (IC 95%) — Modèle 3 HC3", height=400)
        st.plotly_chart(fig_coef3, use_container_width=True)

        st.markdown(f"""
        <div class='insight-box'>
            <strong>Lecture des modèles MCO (Moindres Carrés Ordinaires)</strong><br>
            • <strong>Modèle 1</strong> (éducation seule, R²={modele1.rsquared:.4f}) : l'effet brut de l'éducation sur le niveau de vie.<br>
            • <strong>Modèle 2</strong> (+ âge, taille ménage, R²={modele2.rsquared:.4f}) : on contrôle les caractéristiques démographiques de base.<br>
            • <strong>Modèle 3</strong> (complet, R²={modele3.rsquared:.4f}) : toutes les variables de contrôle. Ce modèle explique
            <strong>{modele3.rsquared*100:.1f}%</strong> de la variance du log de la dépense per capita.<br>
            Les coefficients indiquent l'<strong>effet marginal toutes choses égales par ailleurs (ceteris paribus)</strong>.
            Une augmentation d'une unité des années de scolarité est associée à une variation de
            <strong>{modele3.params['annees_scol_chef']:.4f}</strong> du log de la dépense per capita, soit environ
            <strong>{modele3.params['annees_scol_chef']*100:.2f}%</strong> de variation de la dépense réelle.
            Les erreurs standards <strong>HC3 (Huber-White)</strong> corrigent l'hétéroscédasticité.
        </div>
        """, unsafe_allow_html=True)

        # ── Test RESET ──
        st.markdown("<div class='section-title'> Test 4 — Spécification (Ramsey RESET)</div>", unsafe_allow_html=True)
        try:
            reset_test = linear_reset(modele3, power=2, use_f=True)
            reset_df = pd.DataFrame({'Statistique': ['F-stat', 'p-value'],
                                     'Valeur': [round(reset_test.fvalue, 4), round(reset_test.pvalue, 4)]})
            st.dataframe(reset_df, use_container_width=True, hide_index=True)
            if reset_test.pvalue < 0.05:
                st.markdown(f"""<div class='insight-box'>
                    <strong>⚠️ Test RESET : rejet de la spécification linéaire (p = {reset_test.pvalue:.4f})</strong><br>
                    Des termes non-linéaires (carrés, interactions) pourraient améliorer le modèle.
                    On teste ci-dessous un modèle enrichi avec age² et education².
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class='insight-box'>
                    <strong>✅ Spécification linéaire acceptée (p = {reset_test.pvalue:.4f})</strong><br>
                    Le modèle linéaire est correctement spécifié.
                </div>""", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Test RESET : {e}")

        # ── Modèle non linéaire ──
        st.markdown("<div class='section-title'> Modèle enrichi — Termes non-linéaires (age², education²)</div>", unsafe_allow_html=True)
        modele3_nl = smf.ols("log_dep_percapita ~ annees_scol_chef + education_carre + age_chef + age_chef_carre + taille_menage + score_actifs + acces_electricite + choc_economique + milieu_urbain",
                              data=base_modele).fit(cov_type='HC3')
        nl_table = pd.DataFrame({
            'Variable': modele3_nl.params.index,
            'Coeff.': modele3_nl.params.values.round(5),
            'Std Err (HC3)': modele3_nl.bse.values.round(5),
            't-stat': modele3_nl.tvalues.values.round(3),
            'p-value': modele3_nl.pvalues.values.round(4),
            'Sig.': ['***' if p < 0.01 else '**' if p < 0.05 else '*' if p < 0.1 else '' for p in modele3_nl.pvalues]
        })
        st.dataframe(nl_table, use_container_width=True, hide_index=True)
        m_nl1, m_nl2, m_nl3 = st.columns(3)
        m_nl1.metric("R² (modèle non-lin.)", f"{modele3_nl.rsquared:.4f}")
        m_nl2.metric("R² ajusté", f"{modele3_nl.rsquared_adj:.4f}")
        m_nl3.metric("AIC", f"{modele3_nl.aic:.1f}")

        # ── Diagnostic résidus ──
        st.markdown("<div class='section-title'> Diagnostic des résidus (Modèle 3)</div>", unsafe_allow_html=True)
        residus = modele3.resid
        fitted = modele3.fittedvalues

        r1, r2 = st.columns(2)
        with r1:
            fig_res1 = go.Figure()
            fig_res1.add_trace(go.Scatter(x=fitted, y=residus, mode='markers',
                                          marker=dict(color='#22d3ee', size=4, opacity=0.4)))
            fig_res1.add_hline(y=0, line_color='#ff6b6b', line_dash='dash', line_width=2)
            apply_layout(fig_res1, "Résidus vs Valeurs ajustées", height=360)
            fig_res1.update_xaxes(title="Valeurs prédites")
            fig_res1.update_yaxes(title="Résidus")
            st.plotly_chart(fig_res1, use_container_width=True)
        with r2:
            fig_res2 = px.histogram(x=residus, nbins=40, color_discrete_sequence=['#4ade80'])
            fig_res2.update_traces(opacity=0.8)
            fig_res2.add_vline(x=0, line_color='#ff6b6b', line_dash='dash')
            apply_layout(fig_res2, "Distribution des résidus", height=360)
            st.plotly_chart(fig_res2, use_container_width=True)

        r3, r4 = st.columns(2)
        with r3:
            # Q-Q plot
            from scipy import stats as sp_stats
            (osm, osr), (slope, intercept, r) = sp_stats.probplot(residus, dist="norm")
            fig_qq = go.Figure()
            fig_qq.add_trace(go.Scatter(x=osm, y=osr, mode='markers',
                                         marker=dict(color='#a78bfa', size=5, opacity=0.6), name='Données'))
            fig_qq.add_trace(go.Scatter(x=[min(osm), max(osm)],
                                         y=[slope*min(osm)+intercept, slope*max(osm)+intercept],
                                         mode='lines', line=dict(color='#ff6b6b', dash='dash'), name='Référence normale'))
            apply_layout(fig_qq, "Q-Q plot des résidus (test de normalité visuel)", height=360)
            fig_qq.update_xaxes(title="Quantiles théoriques normaux")
            fig_qq.update_yaxes(title="Quantiles empiriques")
            st.plotly_chart(fig_qq, use_container_width=True)
        with r4:
            # Résidus vs éducation
            fig_res4 = go.Figure()
            fig_res4.add_trace(go.Scatter(x=base_modele['annees_scol_chef'], y=residus,
                                           mode='markers', marker=dict(color='#fbbf24', size=4, opacity=0.3)))
            fig_res4.add_hline(y=0, line_color='#ff6b6b', line_dash='dash')
            apply_layout(fig_res4, "Résidus vs Années de scolarité", height=360)
            fig_res4.update_xaxes(title="Années de scolarité du chef")
            fig_res4.update_yaxes(title="Résidus")
            st.plotly_chart(fig_res4, use_container_width=True)

        # Durbin-Watson
        dw = durbin_watson(residus)
        dw_col1, dw_col2 = st.columns(2)
        dw_col1.metric("Durbin-Watson", f"{dw:.4f}")
        dw_col2.metric("Diagnostic", "✅ Pas d'autocorrélation" if 1.5 < dw < 2.5 else "⚠️ Autocorrélation possible")

        st.markdown(f"""
        <div class='insight-box'>
            <strong>Diagnostic des résidus du Modèle 3</strong><br>
            • <strong>Résidus vs Valeurs ajustées</strong> : un nuage de points aléatoire autour de zéro confirme l'absence de structure systématique dans les erreurs (bonne spécification). Un motif en éventail signalerait de l'hétéroscédasticité.<br>
            • <strong>Histogramme des résidus</strong> : la distribution doit être approximativement en cloche centrée sur 0. Une asymétrie marquée indiquerait une non-normalité.<br>
            • <strong>Q-Q plot</strong> : si les points suivent la droite diagonale rouge, les résidus sont normalement distribués. Les déviations aux extrémités sont fréquentes et généralement acceptables.<br>
            • <strong>Durbin-Watson ({dw:.4f})</strong> : {'✅ entre 1.5 et 2.5, pas d\'autocorrélation problématique des résidus.' if 1.5 < dw < 2.5 else '⚠️ hors de la plage 1.5–2.5, possible autocorrélation à investiguer.'}<br>
            • <strong>Moyenne des résidus</strong> : {residus.mean():.2e} ≈ 0 ✅ (propriété fondamentale du MCO).
        </div>
        """, unsafe_allow_html=True)

        # ══════════════════════════════════════════════════════
        # PARTIE 4 — TRAITEMENT DE L'ENDOGÉNÉITÉ (2SLS + HAUSMAN)
        # ══════════════════════════════════════════════════════
        st.markdown("<hr style='border-color:rgba(74,222,128,0.15);margin:34px 0 18px 0;'>", unsafe_allow_html=True)
        st.markdown("<div class='hero-title' style='font-size:1.5rem;'> Traitement de l'endogénéité — 2SLS & Test de Hausman</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='insight-box' style='margin-bottom:16px;'>
            Le nombre d'années de scolarité du chef de ménage est potentiellement <strong>endogène</strong>
            (biais de causalité inverse, variables omises comme la capacité innée ou le milieu familial).
            Pour corriger ce biais, on estime un modèle par <strong>doubles moindres carrés (2SLS)</strong> en utilisant
            l'<strong>accès à une source d'eau potable améliorée du ménage</strong> (<code>eauboi_ss</code>) comme
            <strong>variable instrumentale</strong> : elle est corrélée aux conditions de vie du ménage durant l'enfance du chef
            (pertinence) sans affecter directement le niveau de vie actuel autrement que via l'éducation (exclusion).
        </div>
        """, unsafe_allow_html=True)

        try:
            instrument_col = 'eauboi_ss'
            base_iv = df_f[[target_eco, 'annees_scol_chef', instrument_col] + [c for c in variables_modele if c != 'annees_scol_chef']].dropna().copy()
            y_iv = base_iv[target_eco]
            educ_iv = base_iv['annees_scol_chef']
            controls_iv = base_iv[[c for c in variables_modele if c != 'annees_scol_chef']]
            instrument_iv = base_iv[instrument_col]

            # 1ère étape
            X_first = sm.add_constant(pd.concat([instrument_iv, controls_iv], axis=1))
            first_stage = sm.OLS(educ_iv, X_first).fit(cov_type='HC3')
            educ_hat = first_stage.predict(X_first)

            f_instr = first_stage.tvalues[instrument_col] ** 2
            st.markdown("<div class='section-title'> Étape 1 — Pertinence de l'instrument</div>", unsafe_allow_html=True)
            fs1, fs2, fs3 = st.columns(3)
            fs1.metric("Coeff. instrument (eauboi_ss)", f"{first_stage.params[instrument_col]:.4f}")
            fs2.metric("p-value instrument", f"{first_stage.pvalues[instrument_col]:.4f}")
            fs3.metric("F-stat (instrument faible si <10)", f"{f_instr:.1f}")
            if f_instr >= 10:
                st.markdown("<div class='insight-box'>✅ <strong>Instrument pertinent</strong> : F-stat ≥ 10, pas de problème d'instrument faible.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='insight-box'>⚠️ <strong>Instrument potentiellement faible</strong> (F-stat &lt; 10) : les résultats du 2SLS doivent être interprétés avec prudence.</div>", unsafe_allow_html=True)

            # 2e étape
            X_second = sm.add_constant(pd.concat([educ_hat.rename('education_hat'), controls_iv], axis=1))
            iv_model = sm.OLS(y_iv, X_second).fit(cov_type='HC3')

            # MCO simple pour comparaison (mêmes observations)
            X_ols_cmp = sm.add_constant(pd.concat([educ_iv, controls_iv], axis=1))
            ols_model_cmp = sm.OLS(y_iv, X_ols_cmp).fit(cov_type='HC3')

            coef_ols_h = ols_model_cmp.params['annees_scol_chef']
            coef_iv_h = iv_model.params['education_hat']
            se_ols_h = ols_model_cmp.bse['annees_scol_chef']
            se_iv_h = iv_model.bse['education_hat']

            st.markdown("<div class='section-title'> Étape 2 — Comparaison MCO vs 2SLS</div>", unsafe_allow_html=True)
            comp_iv_df = pd.DataFrame({
                'Modèle': ['MCO (potentiellement biaisé)', '2SLS (corrigé de l\'endogénéité)'],
                'Coefficient Éducation': [round(coef_ols_h, 4), round(coef_iv_h, 4)],
                'Erreur-type (HC3)': [round(se_ols_h, 4), round(se_iv_h, 4)],
                'p-value': [round(ols_model_cmp.pvalues['annees_scol_chef'], 4), round(iv_model.pvalues['education_hat'], 4)],
                'R²': [round(ols_model_cmp.rsquared, 4), round(iv_model.rsquared, 4)],
            })
            st.dataframe(comp_iv_df, use_container_width=True, hide_index=True)

            # Test de Hausman (forme simplifiée)
            hausman_stat = ((coef_ols_h - coef_iv_h) ** 2) / max(se_iv_h ** 2 - se_ols_h ** 2, 1e-10)
            p_value_hausman = 1 - sp_chi2.cdf(hausman_stat, 1)

            st.markdown("<div class='section-title'> Test de Hausman — Éducation est-elle endogène ?</div>", unsafe_allow_html=True)
            h1, h2 = st.columns(2)
            h1.metric("Statistique de Hausman", f"{hausman_stat:.4f}")
            h2.metric("p-value", f"{p_value_hausman:.4f}")

            if p_value_hausman < 0.05:
                st.markdown(f"""
                <div class='insight-box'>
                    <strong>⚠️ H₀ (exogénéité) rejetée (p = {p_value_hausman:.4f} &lt; 0,05)</strong><br>
                    L'éducation est statistiquement <strong>endogène</strong> : le modèle <strong>2SLS est préférable</strong> au MCO simple.
                    Le rendement <strong>causal</strong> corrigé d'une année d'étude supplémentaire est estimé à
                    <strong>+{coef_iv_h*100:.2f}%</strong> du niveau de vie (log dépense per capita), contre
                    +{coef_ols_h*100:.2f}% en MCO — l'écart traduit le biais que le 2SLS permet de corriger.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='insight-box'>
                    <strong>✅ H₀ (exogénéité) non rejetée (p = {p_value_hausman:.4f} ≥ 0,05)</strong><br>
                    Rien n'indique que l'éducation soit endogène sur cet échantillon : les estimations <strong>MCO restent valides et efficaces</strong>.
                </div>
                """, unsafe_allow_html=True)

            fig_iv = go.Figure(go.Bar(
                x=['MCO', '2SLS'], y=[coef_ols_h, coef_iv_h],
                marker_color=['#22d3ee', '#4ade80'],
                text=[f"{coef_ols_h:.4f}", f"{coef_iv_h:.4f}"], textposition='outside',
                error_y=dict(type='data', array=[se_ols_h * 1.96, se_iv_h * 1.96], visible=True)
            ))
            apply_layout(fig_iv, "Coefficient de l'éducation — MCO vs 2SLS (IC 95%)", height=380)
            st.plotly_chart(fig_iv, use_container_width=True)

        except Exception as e:
            st.warning(f"Analyse 2SLS indisponible : {e}")

        # ══════════════════════════════════════════════════════
        # PARTIE 5 — HÉTÉROGÉNÉITÉ SPATIALE (MCO PAR DÉPARTEMENT + CHOW)
        # ══════════════════════════════════════════════════════
        st.markdown("<hr style='border-color:rgba(74,222,128,0.15);margin:34px 0 18px 0;'>", unsafe_allow_html=True)
        st.markdown("<div class='hero-title' style='font-size:1.5rem;'> Hétérogénéité spatiale — MCO par département & Test de Chow</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='insight-box' style='margin-bottom:16px;'>
            L'effet de l'éducation sur le niveau de vie est-il le même partout au Bénin ? On ré-estime le
            <strong>modèle complet séparément dans chacun des 12 départements</strong>, puis on teste formellement
            l'homogénéité des coefficients avec le <strong>Test de Chow</strong>.
        </div>
        """, unsafe_allow_html=True)

        try:
            liste_depts = sorted(df_f['departement_nom'].unique())
            dict_mco_dept = {}
            modele_global_chow = smf.ols(
                "log_dep_percapita ~ annees_scol_chef + age_chef + taille_menage + score_actifs + acces_electricite + choc_economique + milieu_urbain",
                data=base_modele
            ).fit()
            scr_global = modele_global_chow.ssr
            n_total = len(base_modele)
            k_param = len(modele_global_chow.params)
            scr_non_global = 0

            for dept in liste_depts:
                base_dept = df_f[df_f['departement_nom'] == dept][variables_modele + [target_eco]].dropna()
                if len(base_dept) < k_param + 5:
                    continue
                res_dept = smf.ols(
                    "log_dep_percapita ~ annees_scol_chef + age_chef + taille_menage + score_actifs + acces_electricite + choc_economique + milieu_urbain",
                    data=base_dept
                ).fit(cov_type='HC3')
                dict_mco_dept[dept] = {
                    'Observations': len(base_dept),
                    'Coefficient (Éducation)': round(res_dept.params['annees_scol_chef'], 5),
                    'Erreur-Type': round(res_dept.bse['annees_scol_chef'], 5),
                    'P-value': round(res_dept.pvalues['annees_scol_chef'], 4),
                    'R²': round(res_dept.rsquared, 3),
                }
                scr_non_global += res_dept.ssr

            G = len(dict_mco_dept)
            ddl_num = (G - 1) * k_param
            ddl_den = n_total - (G * k_param)
            stat_chow = ((scr_global - scr_non_global) / ddl_num) / (scr_non_global / ddl_den)
            p_value_chow = 1 - sp_f.cdf(stat_chow, ddl_num, ddl_den)

            df_mco_dept = pd.DataFrame(dict_mco_dept).T.sort_values('Coefficient (Éducation)', ascending=False)

            st.markdown("<div class='section-title'> Estimations MCO par département</div>", unsafe_allow_html=True)
            st.dataframe(df_mco_dept, use_container_width=True)

            fig_dept_coef = go.Figure(go.Bar(
                x=df_mco_dept.index, y=df_mco_dept['Coefficient (Éducation)'] * 100,
                marker_color=['#4ade80' if p < 0.05 else '#7090b0' for p in df_mco_dept['P-value']],
                text=[f"{v:.2f}%" for v in df_mco_dept['Coefficient (Éducation)'] * 100], textposition='outside'
            ))
            apply_layout(fig_dept_coef, "Rendement marginal d'une année de scolarité en plus, par département (vert = significatif à 5%)", height=400)
            fig_dept_coef.update_yaxes(title="Effet sur le log dép. per capita (%)")
            fig_dept_coef.update_xaxes(tickangle=35)
            st.plotly_chart(fig_dept_coef, use_container_width=True)

            st.markdown("<div class='section-title'> Test de Chow — Stabilité structurelle des coefficients</div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            c1.metric("Statistique F (Chow)", f"{stat_chow:.3f}")
            c2.metric("Degrés de liberté", f"({ddl_num}, {ddl_den})")
            c3.metric("p-value", f"{p_value_chow:.2e}")

            top_dept = df_mco_dept.index[0]
            bottom_dept = df_mco_dept.index[-1]
            if p_value_chow < 0.05:
                st.markdown(f"""
                <div class='insight-box'>
                    <strong>⚠️ H₀ (coefficients identiques entre départements) rejetée (p = {p_value_chow:.2e} &lt; 0,05)</strong><br>
                    Il existe une <strong>hétérogénéité structurelle significative</strong> : le rendement de l'éducation
                    n'est pas homogène sur le territoire. Il est maximal à <strong>{top_dept}</strong>
                    (+{df_mco_dept.loc[top_dept, 'Coefficient (Éducation)']*100:.2f}% par année d'étude) et minimal à
                    <strong>{bottom_dept}</strong> (+{df_mco_dept.loc[bottom_dept, 'Coefficient (Éducation)']*100:.2f}%).
                    Cela plaide pour des <strong>politiques éducatives différenciées selon les départements</strong>.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='insight-box'>
                    <strong>✅ H₀ non rejetée (p = {p_value_chow:.2e} ≥ 0,05)</strong><br>
                    Les coefficients sont statistiquement stables sur l'ensemble du territoire : l'effet de l'éducation
                    ne varie pas significativement d'un département à l'autre.
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.warning(f"Analyse de l'hétérogénéité spatiale indisponible : {e}")

# ══════════════════════════════════════════════════════════════
# ONGLET 4 — MACHINE LEARNING
# ══════════════════════════════════════════════════════════════
with tab_ml:
    st.markdown("<div class='hero-title' style='font-size:1.8rem;'> Machine Learning</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='insight-box' style='margin-bottom:20px;'>
        Cette section compare <strong>7 algorithmes ML</strong> pour prédire le niveau de vie des ménages béninois.
        Démarche : préparation → validation croisée (5-fold) → optimisation GridSearchCV →
        évaluation sur jeu de test → importance des variables → comparaison MCO vs ML.
    </div>
    """, unsafe_allow_html=True)

    try:
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import train_test_split, cross_val_score, KFold, GridSearchCV
        from sklearn.linear_model import Ridge, Lasso, ElasticNet
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
        from sklearn.svm import SVR
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
        from sklearn.base import clone
        import time

        # Variables reprises telles quelles du notebook d'analyse (Partie Machine Learning)
        variables_ml = ['annees_scol_chef', 'age_chef', 'taille_menage', 'score_actifs',
                        'eauboi_ss', 'sexe_chef_bin', 'acces_electricite', 'choc_economique', 'milieu_urbain']
        var_multiclasse_ml = 'niveau_instruction_chef'
        target_ml = 'log_dep_percapita'

        data_ml_raw = df_f[[target_ml] + variables_ml + [var_multiclasse_ml]].dropna().copy()
        # Encodage one-hot du niveau d'instruction (drop_first pour éviter le piège de la colinéarité)
        data_ml = pd.get_dummies(data_ml_raw, columns=[var_multiclasse_ml], drop_first=True)
        dummy_cols_ml = [c for c in data_ml.columns if c.startswith(var_multiclasse_ml + '_')]
        feature_cols_ml = variables_ml + dummy_cols_ml

        X_ml = data_ml[feature_cols_ml].astype(float)
        y_ml = data_ml[target_ml]

        X_train, X_test, y_train, y_test = train_test_split(X_ml, y_ml, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train_sc = pd.DataFrame(scaler.fit_transform(X_train), columns=feature_cols_ml)
        X_test_sc = pd.DataFrame(scaler.transform(X_test), columns=feature_cols_ml)

        labels_ml = {
            'annees_scol_chef': 'Années scol. chef', 'age_chef': 'Âge chef',
            'taille_menage': 'Taille ménage', 'score_actifs': 'Score actifs',
            'eauboi_ss': 'Eau boisson saine', 'sexe_chef_bin': 'Sexe chef (masc.)',
            'acces_electricite': 'Accès électricité',
            'choc_economique': 'Choc économique', 'milieu_urbain': 'Milieu urbain',
        }
        for k in dummy_cols_ml:
            suffix = k.replace(var_multiclasse_ml + '_', '')
            labels_ml[k] = f"Instruction : {EDUCATION_LABELS.get(suffix, suffix)}"

        # On garde variables_ml pour les comparaisons MCO vs ML (variables continues/binaires du modèle économétrique)
        variables_ml = feature_cols_ml

        # Métriques de préparation
        pm1, pm2, pm3, pm4 = st.columns(4)
        pm1.markdown(f"<div class='kpi-card'><div class='kpi-icon'></div><div class='kpi-label'>Observations totales</div><div class='kpi-value'>{len(data_ml):,}</div></div>", unsafe_allow_html=True)
        pm2.markdown(f"<div class='kpi-card'><div class='kpi-icon'></div><div class='kpi-label'>Train (80%)</div><div class='kpi-value'>{len(X_train)}</div></div>", unsafe_allow_html=True)
        pm3.markdown(f"<div class='kpi-card'><div class='kpi-icon'></div><div class='kpi-label'>Test (20%)</div><div class='kpi-value'>{len(X_test)}</div></div>", unsafe_allow_html=True)
        pm4.markdown(f"<div class='kpi-card'><div class='kpi-icon'></div><div class='kpi-label'>Variables (après encodage)</div><div class='kpi-value'>{len(feature_cols_ml)}</div></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Modèles
        modeles_scaled = ['Ridge', 'Lasso', 'Elastic Net', 'SVM RBF']
        modeles_ml = {
            'Ridge': Ridge(alpha=1.0),
            'Lasso': Lasso(alpha=0.01, max_iter=10000),
            'Elastic Net': ElasticNet(alpha=0.01, l1_ratio=0.5, max_iter=10000),
            'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1),
            'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42),
            'SVM RBF': SVR(kernel='rbf', C=1.0, epsilon=0.1),
        }
        try:
            from xgboost import XGBRegressor
            modeles_ml['XGBoost'] = XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42, n_jobs=-1, verbosity=0)
        except ImportError:
            pass

        # ── Validation croisée ──
        st.markdown("<div class='section-title'> Validation croisée (5-fold)</div>", unsafe_allow_html=True)
        kfold = KFold(n_splits=5, shuffle=True, random_state=42)
        cv_rows = []
        for nom, modele in modeles_ml.items():
            X_cv = X_train_sc if nom in modeles_scaled else X_train
            r2_cv = cross_val_score(modele, X_cv, y_train, cv=kfold, scoring='r2')
            rmse_cv = np.sqrt(-cross_val_score(modele, X_cv, y_train, cv=kfold, scoring='neg_mean_squared_error'))
            cv_rows.append({'Modèle': nom, 'R² moyen': round(r2_cv.mean(), 4),
                            'R² std': round(r2_cv.std(), 4), 'RMSE moyen': round(rmse_cv.mean(), 4),
                            'RMSE std': round(rmse_cv.std(), 4)})
        cv_df = pd.DataFrame(cv_rows).sort_values('R² moyen', ascending=False).reset_index(drop=True)
        st.dataframe(cv_df, use_container_width=True, hide_index=True)

        fig_cv = go.Figure(go.Bar(
            x=cv_df['Modèle'], y=cv_df['R² moyen'],
            error_y=dict(type='data', array=cv_df['R² std'].tolist(), visible=True),
            marker_color=PALETTE[:len(cv_df)],
            text=[f"{v:.3f}" for v in cv_df['R² moyen']], textposition='outside'
        ))
        apply_layout(fig_cv, "R² moyen en validation croisée (5-fold) ± écart-type", height=400)
        st.plotly_chart(fig_cv, use_container_width=True)

        best_cv = cv_df.iloc[0]['Modèle']
        st.markdown(f"""
        <div class='insight-box'>
            <strong>Validation croisée (5-fold CV)</strong><br>
            La validation croisée divise le jeu d'entraînement en 5 sous-ensembles égaux. Chaque modèle est entraîné sur 4 sous-ensembles et évalué sur le 5e, répété 5 fois.
            Le <strong>R² moyen</strong> mesure la capacité explicative moyenne, et l'<strong>écart-type</strong> mesure la stabilité du modèle.
            Un faible écart-type indique que le modèle est robuste aux variations des données d'entraînement.
            Le meilleur modèle en validation croisée est <strong>{best_cv}</strong> (R² = {cv_df.iloc[0]['R² moyen']:.4f}).
        </div>
        """, unsafe_allow_html=True)

        # ── Optimisation des hyperparamètres du meilleur modèle (GridSearchCV) ──
        st.markdown("<div class='section-title'> Optimisation des hyperparamètres — GridSearchCV</div>", unsafe_allow_html=True)
        param_grids_ml = {
            'Ridge': {'alpha': [0.01, 0.1, 1.0, 10.0, 100.0]},
            'Lasso': {'alpha': [0.001, 0.01, 0.1, 1.0]},
            'Elastic Net': {'alpha': [0.001, 0.01, 0.1], 'l1_ratio': [0.2, 0.5, 0.8]},
            'SVM RBF': {'C': [0.1, 1.0, 10.0], 'epsilon': [0.01, 0.1, 0.2]},
            'Random Forest': {'n_estimators': [100, 200], 'max_depth': [10, 15], 'min_samples_split': [2, 5]},
            'Gradient Boosting': {'n_estimators': [100, 200], 'max_depth': [3, 5], 'learning_rate': [0.05, 0.1]},
            'XGBoost': {'n_estimators': [100, 200], 'max_depth': [3, 5], 'learning_rate': [0.05, 0.1], 'subsample': [0.8, 1.0]},
        }
        if best_cv in param_grids_ml:
            X_opt = X_train_sc if best_cv in modeles_scaled else X_train
            with st.spinner(f"Recherche des meilleurs hyperparamètres pour {best_cv}..."):
                grid_search = GridSearchCV(
                    estimator=clone(modeles_ml[best_cv]),
                    param_grid=param_grids_ml[best_cv], cv=5, scoring='r2', n_jobs=-1
                )
                grid_search.fit(X_opt, y_train)
            modeles_ml[best_cv] = grid_search.best_estimator_
            g1, g2 = st.columns(2)
            g1.metric("Meilleurs hyperparamètres", str(grid_search.best_params_))
            g2.metric("R² optimisé (validation croisée)", f"{grid_search.best_score_:.4f}")
            st.markdown(f"""
            <div class='insight-box'>
                Le <strong>GridSearchCV</strong> teste systématiquement toutes les combinaisons d'hyperparamètres définies pour
                <strong>{best_cv}</strong> et retient celle qui maximise le R² moyen en validation croisée. Le modèle
                ainsi optimisé remplace la version par défaut pour l'évaluation finale sur le jeu de test ci-dessous.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Pas de grille d'hyperparamètres définie pour ce modèle — évaluation avec les paramètres par défaut.")

        # ── Entraînement final ──
        st.markdown("<div class='section-title'> Évaluation finale sur le jeu de test</div>", unsafe_allow_html=True)
        final_results = []
        trained_models = {}
        for nom, modele in modeles_ml.items():
            m = clone(modele)
            X_tr = X_train_sc if nom in modeles_scaled else X_train
            X_te = X_test_sc if nom in modeles_scaled else X_test
            m.fit(X_tr, y_train)
            trained_models[nom] = (m, X_te)
            y_tr_pred = m.predict(X_tr)
            y_te_pred = m.predict(X_te)
            r2_tr = r2_score(y_train, y_tr_pred)
            r2_te = r2_score(y_test, y_te_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_te_pred))
            mae = mean_absolute_error(y_test, y_te_pred)
            final_results.append({
                'Modèle': nom, 'R² Train': round(r2_tr, 4), 'R² Test': round(r2_te, 4),
                'RMSE Test': round(rmse, 4), 'MAE Test': round(mae, 4),
                'Surapprentissage': round(r2_tr - r2_te, 4),
                'Statut': '⚠️ Surapprentissage' if (r2_tr - r2_te) > 0.15 else '✅ OK'
            })
        results_df = pd.DataFrame(final_results).sort_values('R² Test', ascending=False).reset_index(drop=True)
        st.dataframe(results_df, use_container_width=True, hide_index=True)

        best_name = results_df.iloc[0]['Modèle']
        best_model_obj, best_X_test = trained_models[best_name]

        fig_podium = go.Figure(go.Bar(
            x=results_df['Modèle'], y=results_df['R² Test'],
            marker=dict(color=results_df['R² Test'], colorscale='Viridis', showscale=True,
                        colorbar=dict(title="Importance", tickfont=dict(color="#c8e0ff"), title_font=dict(color="#c8e0ff"))),
            text=[f"{v:.4f}" for v in results_df['R² Test']], textposition='outside'
        ))
        apply_layout(fig_podium, "Classement des modèles ML — R² sur le jeu de test", height=380)
        st.plotly_chart(fig_podium, use_container_width=True)

        st.markdown(f"""
        <div class='kpi-card' style='margin:12px 0;'>
            <div class='kpi-icon'>🥇</div>
            <div class='kpi-label'>Meilleur modèle (jeu de test)</div>
            <div class='kpi-value' style='font-size:1.5rem;'>{best_name}</div>
            <div class='kpi-delta'>R² Test = {results_df.iloc[0]['R² Test']:.4f} · RMSE = {results_df.iloc[0]['RMSE Test']:.4f} · MAE = {results_df.iloc[0]['MAE Test']:.4f}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Importance des variables ──
        st.markdown("<div class='section-title'> Importance des variables — Meilleur modèle</div>", unsafe_allow_html=True)
        if hasattr(best_model_obj, 'feature_importances_'):
            imp = best_model_obj.feature_importances_
            imp_df = pd.DataFrame({'Variable': [labels_ml.get(v, v) for v in variables_ml], 'Importance': imp}).sort_values('Importance', ascending=True)
            fig_imp = go.Figure(go.Bar(
                x=imp_df['Importance'], y=imp_df['Variable'], orientation='h',
                marker_color=px.colors.sequential.Viridis[-1::-1][:len(imp_df)],
                text=[f"{v:.4f}" for v in imp_df['Importance']], textposition='outside'
            ))
            apply_layout(fig_imp, f"Importance des variables — {best_name}", height=380)
            st.plotly_chart(fig_imp, use_container_width=True)
        elif hasattr(best_model_obj, 'coef_'):
            coefs = best_model_obj.coef_.flatten()
            coef_df2 = pd.DataFrame({'Variable': [labels_ml.get(v, v) for v in variables_ml], 'Coef. absolu': np.abs(coefs)}).sort_values('Coef. absolu', ascending=True)
            fig_coef2 = go.Figure(go.Bar(
                x=coef_df2['Coef. absolu'], y=coef_df2['Variable'], orientation='h',
                marker_color=px.colors.sequential.Teal[::-1][:len(coef_df2)],
                text=[f"{v:.4f}" for v in coef_df2['Coef. absolu']], textposition='outside'
            ))
            apply_layout(fig_coef2, f"Importance (coeff. absolus) — {best_name}", height=380)
            st.plotly_chart(fig_coef2, use_container_width=True)
        else:
            from sklearn.inspection import permutation_importance
            perm = permutation_importance(best_model_obj, best_X_test, y_test, n_repeats=10, random_state=42)
            perm_df = pd.DataFrame({'Variable': [labels_ml.get(v, v) for v in variables_ml],
                                    'Importance': perm.importances_mean}).sort_values('Importance', ascending=True)
            fig_perm = go.Figure(go.Bar(
                x=perm_df['Importance'], y=perm_df['Variable'], orientation='h',
                marker_color=PALETTE[:len(perm_df)],
                text=[f"{v:.4f}" for v in perm_df['Importance']], textposition='outside'
            ))
            apply_layout(fig_perm, f"Importance par permutation — {best_name}", height=380)
            st.plotly_chart(fig_perm, use_container_width=True)

        st.markdown(f"""
        <div class='insight-box'>
            <strong>Interprétation de l'importance des variables</strong><br>
            Pour les modèles d'ensemble (Random Forest, Gradient Boosting, XGBoost), l'<strong>importance des variables</strong>
            mesure la contribution de chaque prédicteur à la réduction de l'erreur de prédiction (impureté de Gini ou MSE).
            Une variable avec une importance élevée est un <strong>déterminant clé</strong> du niveau de vie.
            Pour les modèles linéaires (Ridge, Lasso, Elastic Net), ce sont les <strong>coefficients absolus standardisés</strong>
            qui indiquent l'influence relative. Cette analyse permet de valider économétriquement quelles variables
            — et notamment le rôle de l'éducation — sont les plus prédictives du bien-être des ménages.
        </div>
        """, unsafe_allow_html=True)

        # ── Prédictions vs Réel ──
        st.markdown("<div class='section-title'> Prédictions vs Valeurs réelles</div>", unsafe_allow_html=True)
        y_pred_best = best_model_obj.predict(best_X_test)
        pr1, pr2 = st.columns(2)
        with pr1:
            fig_pred = go.Figure()
            fig_pred.add_trace(go.Scatter(x=y_test.values, y=y_pred_best, mode='markers',
                                          marker=dict(color='#22d3ee', size=7, opacity=0.5,
                                                       line=dict(color='white', width=0.5))))
            lmin = min(y_test.min(), y_pred_best.min())
            lmax = max(y_test.max(), y_pred_best.max())
            fig_pred.add_trace(go.Scatter(x=[lmin, lmax], y=[lmin, lmax], mode='lines',
                                           line=dict(color='#ff6b6b', dash='dash', width=2), name='Prédiction parfaite'))
            apply_layout(fig_pred, f"Réel vs Prédit — {best_name} (R²={results_df.iloc[0]['R² Test']:.4f})", height=380)
            fig_pred.update_xaxes(title="Log dépense per capita réelle")
            fig_pred.update_yaxes(title="Log dépense per capita prédite")
            st.plotly_chart(fig_pred, use_container_width=True)
        with pr2:
            residuals_ml = y_test.values - y_pred_best
            fig_res_ml = px.histogram(x=residuals_ml, nbins=35, color_discrete_sequence=['#a78bfa'])
            fig_res_ml.update_traces(opacity=0.8)
            fig_res_ml.add_vline(x=0, line_color='#ff6b6b', line_dash='dash')
            apply_layout(fig_res_ml, f"Distribution des erreurs (moy={residuals_ml.mean():.3f}, σ={residuals_ml.std():.3f})", height=380)
            fig_res_ml.update_xaxes(title="Erreur de prédiction")
            st.plotly_chart(fig_res_ml, use_container_width=True)

        # ── Comparaison MCO vs ML ──
        st.markdown("<div class='section-title'> Comparaison Économétrie MCO vs Machine Learning</div>", unsafe_allow_html=True)
        import statsmodels.formula.api as smf2
        vars_mco_comp = ['annees_scol_chef', 'age_chef', 'taille_menage', 'score_actifs',
                         'acces_electricite', 'choc_economique', 'milieu_urbain']
        base_modele_ml = df_f[vars_mco_comp + [target_ml]].dropna().copy()
        m3_comp = smf2.ols("log_dep_percapita ~ annees_scol_chef + age_chef + taille_menage + score_actifs + acces_electricite + choc_economique + milieu_urbain",
                           data=base_modele_ml).fit(cov_type='HC3')
        y_pred_mco = m3_comp.predict(base_modele_ml)
        y_true_mco = base_modele_ml[target_ml]
        r2_mco = r2_score(y_true_mco, y_pred_mco)
        rmse_mco = np.sqrt(mean_squared_error(y_true_mco, y_pred_mco))
        mae_mco = mean_absolute_error(y_true_mco, y_pred_mco)

        comp_fig = make_subplots(rows=1, cols=3, subplot_titles=["R²", "RMSE", "MAE"])
        for i, (metric, val_mco, val_ml) in enumerate([
            ("R²", r2_mco, results_df.iloc[0]['R² Test']),
            ("RMSE", rmse_mco, results_df.iloc[0]['RMSE Test']),
            ("MAE", mae_mco, results_df.iloc[0]['MAE Test']),
        ], 1):
            comp_fig.add_trace(go.Bar(x=["MCO", f"ML ({best_name})"], y=[val_mco, val_ml],
                                       marker_color=['#22d3ee', '#4ade80'], showlegend=False,
                                       text=[f"{val_mco:.4f}", f"{val_ml:.4f}"], textposition='outside'), row=1, col=i)
        apply_layout(comp_fig, "Comparaison des performances : MCO vs Meilleur modèle ML", height=380)
        st.plotly_chart(comp_fig, use_container_width=True)

        st.markdown(f"""
        <div class='insight-box'>
            <strong>Économétrie MCO vs Machine Learning — Synthèse</strong><br>
            • <strong>MCO (Moindres Carrés Ordinaires)</strong> — R² = {r2_mco:.4f} : privilégie l'<em>inférence causale</em> et l'interprétabilité.
            Chaque coefficient est économiquement interprétable et testable statistiquement. L'objectif est de quantifier <strong>l'effet de l'éducation</strong> toutes choses égales par ailleurs.<br><br>
            • <strong>{best_name} (ML)</strong> — R² Test = {results_df.iloc[0]['R² Test']:.4f} : privilégie la <em>précision prédictive</em>.
            Capture les relations non-linéaires et interactions complexes que le modèle linéaire ne peut détecter.
            RMSE = {results_df.iloc[0]['RMSE Test']:.4f}, MAE = {results_df.iloc[0]['MAE Test']:.4f}.<br><br>
            • Les deux approches sont <strong>complémentaires</strong> : l'économétrie <em>explique et teste</em>, le ML <em>prédit et classe</em>.
            La variable <strong>éducation (années de scolarité)</strong> ressort comme déterminant majeur du niveau de vie dans les deux cadres,
            ce qui renforce la robustesse des conclusions du mémoire.
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Erreur ML : {e}")
        import traceback
        st.code(traceback.format_exc())

# ══════════════════════════════════════════════════════════════
# ONGLET 5 — À PROPOS
# ══════════════════════════════════════════════════════════════
with tab_about:
    st.markdown("<div class='hero-title' style='font-size:1.8rem;'> À propos du projet</div>", unsafe_allow_html=True)

    a1, a2 = st.columns([1.3, 1])
    with a1:
        st.markdown("""
        <div class='insight-box'>
            <strong style='font-size:1.1rem;'>AZONLEGBE Noël Junior Azonsou</strong><br><br>
            <span class='badge'>Ingénieur Statisticien Économiste</span>
            <span class='badge'>Data Science</span>
            <span class='badge'>Marketing Quantitatif</span><br><br>
            <strong>Mémoire de fin d'études — Promotion 2026</strong><br><br>
            <strong>Titre :</strong> Effet de l'Éducation sur le Niveau de Vie des Ménages au Bénin<br><br>
            <strong>Thème central :</strong> Ce mémoire explore empiriquement si le niveau d'instruction du chef de ménage
            — mesuré par les années de scolarité et le niveau d'éducation atteint — contribue à améliorer
            le niveau de vie des ménages béninois, mesuré par le logarithme de la dépense per capita annuelle.<br><br>
            <strong>Méthodologie :</strong> Économétrie MCO avec 3 spécifications progressives, tests de spécification
            (VIF, Breusch-Pagan, Jarque-Bera, RESET de Ramsey), diagnostics des résidus, <strong>traitement de
            l'endogénéité de l'éducation par doubles moindres carrés (2SLS)</strong> avec test de Hausman, et
            <strong>analyse de l'hétérogénéité spatiale</strong> (MCO par département, Test de Chow) — le tout combiné
            à 7 algorithmes de Machine Learning (Ridge, Lasso, Elastic Net, Random Forest, Gradient Boosting,
            XGBoost, SVM) avec validation croisée et optimisation des hyperparamètres (GridSearchCV).<br><br>
            <strong>Données :</strong> Enquête Harmonisée sur les Conditions de Vie des Ménages (EHCVM 2021),
            conduite au Bénin sous l'égide de la Banque Mondiale et de l'UEMOA, couvrant <strong>8 032 ménages</strong>
            dans les 12 départements du Bénin, sur une base enrichie de <strong>77 variables</strong>.
        </div>
        """, unsafe_allow_html=True)

    with a2:
        st.markdown("""
        <div class='insight-box'>
            <strong> Zones géographiques couvertes</strong><br><br>
            🇧🇯 Alibori · Atacora · Atlantique<br>
            🇧🇯 Borgou · Collines · Couffo<br>
            🇧🇯 Donga · Littoral · Mono<br>
            🇧🇯 Ouémé · Plateau · Zou<br><br>
            <strong> Année d'enquête :</strong> 2021<br>
            <strong> Ménages :</strong> 8 032<br>
            <strong> Variables :</strong> 77 indicateurs (base enrichie)<br>
            <strong>🏙️ Milieux :</strong> Rural + Urbain<br><br>
            <strong> Variable dépendante :</strong><br>
            Log de la dépense per capita annuelle<br><br>
            <strong> Variable d'intérêt :</strong><br>
            Années de scolarité du chef de ménage
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class='insight-box' style='margin-top:12px;'>
        <strong>📖 Références clés</strong><br><br>
        • Mincer, J. (1974). <em>Schooling, Experience, and Earnings.</em> NBER.<br>
        • Becker, G. S. (1964). <em>Human Capital: A Theoretical and Empirical Analysis.</em> University of Chicago Press.<br>
        • Schultz, T. W. (1961). <em>Investment in Human Capital.</em> American Economic Review.<br>
        • Banque Mondiale (2021). <em>Enquête Harmonisée sur les Conditions de Vie des Ménages — EHCVM Bénin.</em><br>
        • INSEE / INSAE (2021). <em>Méthodologie EHCVM.</em> Rapport technique UEMOA.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='footer'>
        <strong style='color:#c8e0ff;'>AZONLEGBE Noël Junior Azonsou</strong><br>
        Ingénieur Statisticien Économiste — Data Science & Marketing<br>
        <em>Mémoire : Effet de l'Éducation sur le Niveau de Vie des Ménages au Bénin</em><br><br>
        © 2026 — Mémoire Éducation Et Niveau de Vie · Bénin · Tous droits réservés
    </div>
    """, unsafe_allow_html=True)
