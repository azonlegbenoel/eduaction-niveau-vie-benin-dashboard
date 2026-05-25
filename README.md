# 📊 Éducation et Niveau de Vie des Ménages au Bénin (EHCVM 2021)

[![Streamlit App](https://streamlit.io)](https://eduaction-niveau-vie-benin-dashboard-noel-azonlegbe.streamlit.app/)

## 📝 À propos du projet
Ce dépôt héberge l'application web interactive (**Dashboard Streamlit**) développée dans le cadre de mon mémoire de fin d'études en Statistique et Économie (ISE 2026). 

L'étude analyse empiriquement l'impact des facteurs éducatifs (années de scolarisation, niveau d'instruction, diplômes) sur les conditions et le niveau de vie des ménages au Bénin, mesuré par le logarithme de la dépense par tête, à partir des données officielles de l'**Enquête Harmonisée sur les Conditions de Vie des Ménages (EHCVM 2021)**.

* **🔗 Lien direct de l'application :** [eduaction-niveau-vie-benin-dashboard-noel-azonlegbe.streamlit.app](https://eduaction-niveau-vie-benin-dashboard-noel-azonlegbe.streamlit.app/)
* **Auteur :** AZONLEGBE Noël Junior Azonsou
* **Spécialité :** Ingénieur Statisticien Économiste (Data Science & Marketing)

---

## 📁 Structure du Projet
```text
eduaction-niveau-vie-benin-dashboard/
├── app.py                  # Fichier principal de l'application Streamlit
├── requirements.txt        # Dépendances et modules Python requis
├── README.md               # Présentation générale (ce fichier)
└── data/
    └── base_ehcvm_education_niveauvie_benin2021.csv  # Base de données
```

---

## 🚀 Fonctionnalités du Dashboard
L'interface est structurée en 5 onglets dynamiques :
1. **🏠 Accueil** : Indicateurs clés (KPIs), contexte du mémoire et graphiques d'évolution conjointe du niveau de vie selon le profil éducatif.
2. **🔍 Exploration** : Outil d'analyse descriptive à la demande (Qualitative vs Quantitative) avec tris à plat, indices de concentration (Lorenz), distributions et matrices de corrélations de Pearson.
3. **📉 Analyse Économétrique** : Tests de spécification complets (Multicolinéarité VIF, Hétéroscédasticité de Breusch-Pagan, Normalité Jarque-Bera, Ramsey RESET) et régressions progressives MCO robustes (HC3).
4. **🤖 Machine Learning** : Comparaison rigoureuse de 7 algorithmes de régression (Ridge, Lasso, Elastic Net, Random Forest, Gradient Boosting, SVM, XGBoost) avec validation croisée, scores et importance des variables.
5. **ℹ️ À propos** : Résumé méthodologique et signatures institutionnelles.

---

## 🌐 Déploiement
L'application est déployée publiquement sur **Streamlit Community Cloud**. Vous pouvez explorer l'intégralité des visualisations et des modèles de manière interactive sans aucune configuration locale en vous rendant sur :
👉 [https://eduaction-niveau-vie-benin-dashboard-noel-azonlegbe.streamlit.app/](https://eduaction-niveau-vie-benin-dashboard-noel-azonlegbe.streamlit.app/)
