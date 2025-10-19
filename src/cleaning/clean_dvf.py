import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
TXT_FILES = list(RAW_DIR.glob("*.txt"))
OUT_FILE = Path(__file__).resolve().parents[2] / "data" / "dvf_clean.csv"
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

if not TXT_FILES:
    print("❌ Aucun fichier TXT trouvé.")
    exit()

print("📂 Chargement des fichiers...")
dfs = []
for f in TXT_FILES:
    try:
        temp_df = pd.read_csv(f, sep="|", low_memory=False, decimal=",")
        dfs.append(temp_df)
    except Exception as e:
        print(f"   ⚠️  Erreur sur {f.name}: {e}")

df = pd.concat(dfs, ignore_index=True)
print(f"   {len(df)} lignes chargées")

# Sélection des colonnes
cols = ["Date mutation", "Valeur fonciere", "Code postal", "Commune", 
        "Type local", "Surface reelle bati", "Nombre pieces principales"]
df = df[[c for c in cols if c in df.columns]]

# Nettoyage des valeurs numériques
# Avec decimal="," dans read_csv, les valeurs sont déjà converties
df["Valeur fonciere"] = pd.to_numeric(df["Valeur fonciere"], errors="coerce")
df["Surface reelle bati"] = pd.to_numeric(df["Surface reelle bati"], errors="coerce")

# Suppression des lignes sans valeur ou surface
df = df.dropna(subset=["Valeur fonciere", "Surface reelle bati"])
df = df[df["Surface reelle bati"] > 0]
df = df[df["Valeur fonciere"] > 0]
print(f"   {len(df)} lignes après suppression des valeurs manquantes")

# Calcul du prix au m²
df["prix_m2"] = df["Valeur fonciere"] / df["Surface reelle bati"]

# Nettoyage code postal
df["Code postal"] = pd.to_numeric(df["Code postal"], errors="coerce")
df = df.dropna(subset=["Code postal"])
df["Code postal"] = df["Code postal"].astype(int)

# Filtre sur type de bien
df = df[df["Type local"].isin(["Maison", "Appartement"])]
print(f"   {len(df)} lignes après filtre Maison/Appartement")

# Filtres de cohérence de base
df = df[(df["Surface reelle bati"] >= 10) & (df["Surface reelle bati"] <= 500)]
df = df[(df["Valeur fonciere"] >= 10000) & (df["Valeur fonciere"] <= 10000000)]
print(f"   {len(df)} lignes après filtres surface et valeur")

# Filtres sur prix au m² par département
df["departement"] = (df["Code postal"] // 1000).astype(str).str.zfill(2)

prix_max_dept = {
    "75": 20000,  # Paris
    "92": 15000,  # Hauts-de-Seine
    "78": 8000,   # Yvelines
    "91": 6000,   # Essonne
    "93": 6000,   # Seine-Saint-Denis
    "94": 8000,   # Val-de-Marne
    "95": 6000,   # Val-d'Oise
}

df["prix_max"] = df["departement"].map(prix_max_dept).fillna(10000)
df = df[(df["prix_m2"] >= 500) & (df["prix_m2"] <= df["prix_max"])]
df = df.drop(columns=["departement", "prix_max"])
print(f"   {len(df)} lignes après filtres prix au m²")

# Suppression des doublons
df = df.drop_duplicates()
print(f"   {len(df)} lignes après suppression des doublons")

# Sauvegarde
df.to_csv(OUT_FILE, index=False)
print(f"✅ Fichier nettoyé : {OUT_FILE}")
print(f"   Lignes finales : {len(df)}")
print(f"   Prix moyen au m² : {df['prix_m2'].mean():.0f}€")