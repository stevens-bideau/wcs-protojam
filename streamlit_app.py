import streamlit as st
import pandas as pd
import math
from pathlib import Path


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Exo Nuno-vens',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# Intégrer le CSS pour l'image de fond
background_image_url = "https://www.phipix.com/protojam/bg_minigroot.jpg"  # Remplacez par l'URL de votre image
page_bg_img = f"""
<style>
.stApp {{
    background-image: url("{background_image_url}");
    background-size: cover;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Declare some useful functions.




# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_americas: Exo Nunovens tour operator

A la recherche de la planète de vos prochaines vacances.
'''

# Charger les données depuis le fichier CSV
url = "https://www.phipix.com/protojam/all_distance_exo.csv"
df_final = pd.read_csv(url)

# Dictionnaire pour le mapping des colonnes
column_mapping = {
    'Unnamed: 0': 'index',
    'pl_name': 'Nom de la planète',
    'pl_orbper': 'Période orbitale (jours)',
    'pl_orbsmax': "Demi-grand axe de l'orbite (unités astronomiques)",
    'pl_radj': 'Rayon de la planète (rayons de Jupiter)',
    'st_teff': "Température effective de l'étoile (Kelvin)",
    'pl_eqt': "Température d'équilibre de la planète (Kelvin)",
    'pl_radius_earth': 'Rayon de la planète (rayons terrestres)',
    'mass_me': 'Masse de la planète (masses terrestres)',
    'radius_re': 'Rayon de la planète (rayons terrestres)',
    'flux_se': 'Flux stellaire reçu par la planète (flux solaire terrestre)',
    'tsurf_k': 'Température à la surface (Kelvin)',
    'period_days': 'Période Orbitale (jours)',
    'distance_ly': 'Distance de la Terre (années lumière)',
    'age_gy': "Âge de l'étoile / du système (milliard d'années)"
}

# Interface Streamlit
st.title("La planète de vos prochaines vacances")

# Menu déroulant pour sélectionner la planète cible
selected_planet = st.selectbox("Sélectionnez votre planète ici:", df_final['pl_name'].unique())

# Fonction pour obtenir les distances des autres planètes par rapport à la planète cible
def get_distances(df, selected_planet):
    distance_col = f'distances_from_{selected_planet}'
    if distance_col in df.columns:
        distances_df = df[['pl_name', distance_col,'tsurf_k', 'flux_se']].copy()
        distances_df = distances_df.rename(columns={'pl_name': 'Planète', distance_col: 'Distance', 'tsurf_k': 'Température (Kelvin)', 'flux_se': 'Ensoleillement (flux solaire)'})
        distances_df = distances_df.sort_values(by='Distance').reset_index(drop=True)
        distances_df = distances_df[distances_df['Planète'] != selected_planet]  # Exclure la planète cible
        return distances_df
    else:
        return pd.DataFrame(columns=['Planète', 'Distance','tsurf_k', 'flux_se'])

# Afficher les distances des autres planètes par rapport à la planète cible
if selected_planet:
    distances_df = get_distances(df_final, selected_planet)
    
    if not distances_df.empty:
        st.subheader(f"Distances des autres planètes par rapport à {selected_planet}")
        st.dataframe(distances_df)
        
        # Menu déroulant pour sélectionner une planète parmi les résultats à partir de l'index 1
        selected_result_planet = st.selectbox("Sélectionnez une planète dans les résultats", distances_df['Planète'])
        
        # Afficher les détails de la planète sélectionnée dans les résultats
        if selected_result_planet:
            planet_details = df_final[df_final['pl_name'] == selected_result_planet]
            if not planet_details.empty:
                st.subheader(f"Détails de la planète {selected_result_planet}")
                
                # Renommer uniquement les colonnes existantes dans planet_details sans créer de doublons
                planet_details_renamed = planet_details.copy()
                for old_name, new_name in column_mapping.items():
                    if old_name in planet_details_renamed.columns and new_name not in planet_details_renamed.columns:
                        planet_details_renamed = planet_details_renamed.rename(columns={old_name: new_name})
                
                # Transposer le DataFrame
                planet_details_transposed = planet_details_renamed.transpose()
                planet_details_transposed.columns = ["Valeur"]
                
                # Afficher le DataFrame transposé avec les noms explicites
                st.dataframe(planet_details_transposed)

    else:
        st.write(f"Les données de distances pour **{selected_planet}** ne sont pas disponibles.")

