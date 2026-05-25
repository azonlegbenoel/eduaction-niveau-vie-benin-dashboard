# 📊 Éducation et Niveau de Vie des Ménages au Bénin (EHCVM 2021)

## 📝 À propos du projet
Ce dépôt héberge un tableau de bord interactif développé avec **Streamlit**. Il s'agit de la composante pratique et visuelle d'un mémoire de recherche analysant l'impact des facteurs éducatifs (alphabétisation, niveau d'instruction du chef de ménage, scolarisation) sur les conditions et le niveau de vie des ménages au Bénin.

L'étude s'appuie sur les données de l'**Enquête Harmonisée sur les Conditions de Vie des Ménages (EHCVM)** réalisée en **2021**.

* **Zone d'étude :** Bénin (Analyses désagrégées par départements et milieu de résidence)
* **Objectif :** Fournir un outil palpable d'aide à la décision pour évaluer le rôle de l'éducation dans la réduction de la pauvreté.

---

## 📁 Structure du Dépôt
```eduaction-niveau-vie-benin-dashboard/
├── app.py                  # Code principal de l'interface Streamlit
├── requirements.txt        # Dépendances et bibliothèques Python requises
├── README.md               # Présentation du projet (ce fichier)
└── data/
    └── base_ehcvm_education_niveauvie_benin2021.csv  # Base de données EHCVM
```

---

## 🚀 Organisation du Tableau de Bord
L'interface web est structurée en plusieurs sections dynamiques :
1. **🏠 Vue d'Ensemble & Indicateurs clés** : Cartographie et KPIs du niveau de vie moyen (dépenses, taux de pauvreté) et profil éducatif global au Bénin.
2. **📈 Analyse Qualitative (Profils)** : Analyse des variables catégorielles (Milieu de résidence, sexe du chef de ménage, niveau d'étude maximum atteint) via des graphiques en barres et tris à plat.
3. **🔢 Analyse Quantitative (Dispersions)** : Étude du volume des dépenses de consommation, corrélations et boîtes à moustaches pour visualiser l'impact direct du diplôme sur le revenu/bien-être.
4. **🔬 Modélisation Économétrique** : Visualisation des résultats d'un modèle (ex: Régression linéaire ou Logistique de pauvreté) mesurant les déterminants du niveau de vie.

---

## 🛠️ Installation et Exécution Locale

Pour lancer ce tableau de bord sur votre machine :

1. **Clonez le dépôt :**
   ```bash
   git clone https://github.com
   cd eduaction-niveau-vie-benin-dashboard
   ```

2. **Installez les bibliothèques indispensables :**
   ```bash
   pip install -r requirements.txt
   ```

3. **Exécutez l'application :**
   ```bash
   streamlit run app.py
   ```
