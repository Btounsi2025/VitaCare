"""
Skin Care Recommendation System
This application provides personalized skin care recommendations using AI.
"""

import streamlit as st
from model import SkinCareAdvisor
# Configure page
st.set_page_config(
    page_title="Conseiller en Soins de la Peau",
    layout="wide"
)
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("images/vitacare_logo.jpg", width=300)


def create_sidebar():
    """Create and handle sidebar elements"""
    with st.sidebar:
        st.title("À propos")
        st.write("""
        Ce conseiller en soins de la peau utilise l'intelligence artificielle pour fournir 
        des recommandations personnalisées basées sur vos besoins spécifiques.
        """)
        
        st.markdown("---")
        st.markdown("### Comment ça marche?")
        st.write("""
        1. Sélectionnez votre type de peau
        2. Indiquez vos préoccupations
        3. Ajoutez des informations supplémentaires
        4. Obtenez des recommandations personnalisées
        """)

def main():
    create_sidebar()
    
    st.write("Obtenez des recommandations personnalisées pour votre routine de soins.")    
    # Initialize the advisor
    advisor = SkinCareAdvisor(api_key=st.secrets["openai"]["api_key"])    
    # Create the main form
    with st.form("skin_care_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            skin_type = st.selectbox(
                "Quel est votre type de peau?",
                ["Normal", "Sec", "Gras", "Mixte", "Sensible"],
                help="Choisissez le type qui correspond le mieux à votre peau"
            )
        
        with col2:
            skin_concerns = st.multiselect(
                "Quelles sont vos préoccupations principales?",
                [
                    "Acné", "Rides", "Taches brunes", 
                    "Rougeurs", "Pores dilatés", "Déshydratation",
                    "Teint terne", "Sensibilité", "Cicatrices"
                ],
                help="Sélectionnez une ou plusieurs préoccupations"
            )
        
        additional_info = st.text_area(
            "Informations supplémentaires",
            placeholder="Ex: allergies, préférences pour certains ingrédients, routine actuelle...",
            help="Ajoutez toute information pertinente pour des recommandations plus précises"
        )
        
        submitted = st.form_submit_button("Obtenir mes recommandations")
    
    if submitted:
        with st.spinner("Analyse en cours..."):
            recommendations = advisor.get_recommendations(
                skin_type, 
                skin_concerns, 
                additional_info
            )
            
            if recommendations:
                st.success("Analyse complétée! Voici vos recommandations personnalisées:")
                
                # Diagnostic
                st.markdown("### 🔍 Diagnostic")
                st.markdown(recommendations.diagnostic)
                
                # Ingredients
                st.markdown("### 🧪 Ingrédients recommandés")
                st.markdown("- " + "\n- ".join(
                    f"{ing.name}: {ing.action}" for ing in recommendations.ingredients
                ))
                
                # Daily Routine
                st.markdown("### ☀️ Routine du jour")
                for prod in recommendations.routine_jour.products:
                    st.markdown(f"- **{prod.name}** ({prod.type}): {prod.action}")
                
                # Night Routine
                st.markdown("### 🌙 Routine de nuit")
                for prod in recommendations.routine_nuit.products:
                    st.markdown(f"- **{prod.name}** ({prod.type}): {prod.action}")
                
                # Add a note
                st.info("""
                💡 Note: Ces recommandations sont générées par IA à titre informatif. 
                Pour des problèmes de peau spécifiques, consultez un dermatologue.
                """)

if __name__ == "__main__":
    main() 