# 🏡 Projet LDF : Pipeline d'Analyse du Marché Immobilier

## Description

Pipeline automatisé pour analyser le marché immobilier français à partir des données DVF (Demandes de Valeurs Foncières).

🔗 **Dashboard en ligne** : [Lien Streamlit](#) 

---

## Structure du Projet

```
Projet_LDF_Pipeline/
├── .github/workflows/main.yml    # Pipeline CI/CD
├── data/
│   ├── raw/                      # Données brutes
│   └── dvf_clean.csv             # Données nettoyées
├── src/
│   ├── scraper/                  # Spider Scrapy
│   ├── ingestion/                # Téléchargement
│   ├── cleaning/                 # Nettoyage
│   └── dashboard/                # Application Streamlit
└── requirements.txt
```

---

## Installation

```bash
# Cloner le projet
git clone https://github.com/VotreUsername/Projet_LDF_Pipeline.git
cd Projet_LDF_Pipeline

# Installer les dépendances
pip install -r requirements.txt

# Lancer le dashboard
streamlit run src/dashboard/app.py
```

# 1. Lancer le spider Scrapy
cd src/scraper/dvf_scraper
scrapy crawl dvf_spider
cd ../../..

# 2. Télécharger les données DVF
python src/ingestion/download_dvf.py

# 3. Nettoyer les données
python src/cleaning/clean_dvf.py

# 4. Lancer le dashboard
streamlit run src/dashboard/app.py

---

## Fonctionnalités

### Dashboard Streamlit
- Recherche par code postal
- Prix moyen par type de bien (Maison/Appartement)
- Répartition des prix au m²
- Évolution temporelle

### Pipeline Automatisé (GitHub Actions)
- Scraping des données DVF
- Téléchargement et nettoyage
- Mise à jour automatique tous les lundis

---

## Technologies

- Python 3.10
- Scrapy (web scraping)
- Pandas (nettoyage)
- Streamlit (dashboard)
- GitHub Actions (CI/CD)

---

## Auteur

**NGUETCHEU KUINSI Dominique**  
Projet LDF - [20/10/2025]
