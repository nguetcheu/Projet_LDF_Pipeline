import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🏡 Analyse du marché immobilier (DVF)")

df = pd.read_csv("data/dvf_clean.csv")

if df.empty:
    st.warning("Le fichier CSV est vide.")
    st.stop()

codes_postaux = sorted(df["Code postal"].unique())

# Saisie du code postal
col1, col2 = st.columns([2, 1])
with col1:
    selected_cp = st.text_input("Entrer un code postal", value=str(codes_postaux[0]))
with col2:
    st.write(f"Codes disponibles : {len(codes_postaux)}")

# Conversion en int si nécessaire
try:
    selected_cp = int(selected_cp)
except:
    st.error("Veuillez entrer un code postal valide")
    st.stop()

if selected_cp not in codes_postaux:
    st.error(f"Code postal {selected_cp} non trouvé dans la base de données")
    st.stop()

filtered_df = df[df["Code postal"] == selected_cp].copy()

st.write(f"Nombre de biens : {len(filtered_df)}")

# Prix moyen par type de bien
type_stats = filtered_df.groupby('Type local')['prix_m2'].mean().reset_index()
fig_bar = px.bar(type_stats, x='Type local', y='prix_m2', 
                 title="Prix moyen au m² par type de bien",
                 labels={"prix_m2": "Prix moyen au m²", "Type local": "Type de bien"})
st.plotly_chart(fig_bar)

# Répartition des prix au m²
if len(filtered_df) == 1:
    # Si un seul bien, afficher une carte de prix
    st.subheader("Prix au m²")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Prix au m²", f"{filtered_df['prix_m2'].iloc[0]:.0f}€")
    with col2:
        st.metric("Surface", f"{filtered_df['Surface reelle bati'].iloc[0]:.0f}m²")
    with col3:
        st.metric("Valeur totale", f"{filtered_df['Valeur fonciere'].iloc[0]:.0f}€")
else:
    # Sinon, afficher l'histogramme
    fig_hist = px.histogram(filtered_df, x="prix_m2", nbins=20, 
                            title="Répartition des prix au m²",
                            labels={"prix_m2": "Prix au m²"})
    fig_hist.update_yaxes(title_text="Nombre de biens")
    st.plotly_chart(fig_hist)

# Évolution dans le temps
filtered_df['Date mutation'] = pd.to_datetime(filtered_df['Date mutation'], dayfirst=True)
filtered_df['Annee'] = filtered_df['Date mutation'].dt.year
prix_par_annee = filtered_df.groupby('Annee')['prix_m2'].mean().reset_index()
fig_line = px.line(prix_par_annee, x='Annee', y='prix_m2', 
                   title="Evolution du prix moyen au m²",
                   markers=True)

fig_line.update_yaxes(title_text="Prix moyen au m²")
st.plotly_chart(fig_line)

st.markdown("Made with Streamlit")