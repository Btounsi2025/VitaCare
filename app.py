"""
Skin Care Recommendation System
This application provides personalized skin care recommendations using AI.
"""

import streamlit as st
import os
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Dict

# Configure page
st.set_page_config(
    page_title="Conseiller en Soins de la Peau",
    layout="wide"
)
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("images/vitacare_logo.jpg", width=300)

# --- Pydantic Models ---

class Ingredient(BaseModel):
    name: str
    action: str

class Product(BaseModel):
    name: str
    type: str
    action: str

class Routine(BaseModel):
    products: List[Product]

class Recommendation(BaseModel):
    diagnostic: str
    ingredients: List[Ingredient]
    routine_jour: Routine
    routine_nuit: Routine

output_parser = PydanticOutputParser(pydantic_object=Recommendation)

# Create the prompt template
TEMPLATE = """Vous êtes un expert dermatologue spécialisé dans les soins de la peau.

Information sur le patient:
Type de peau: {skin_type}
Problèmes de peau: {skin_concerns}
Informations supplémentaires: {additional_info}

Veuillez fournir un diagnostic détaillé de la peau  et des problèmes rencontrés. Et fournissez des recommandations personnalisées d'ingrédients et de produits pour résoudre les problèmes de peau.

{format_instructions}

Assurez-vous que vos recommandations sont:
1. Spécifiques au type de peau et aux problèmes mentionnés
2. Réalistes et applicables au quotidien
3. Expliquées de manière claire et accessible
4. Basées sur des ingrédients reconnus en dermatologie. Précisez le role de chaque ingrédient par rapport a une problématique diagnostiquée.
"""

prompt = ChatPromptTemplate.from_template(TEMPLATE)

class SkinCareAdvisor:
    def __init__(self):
        """Initialize the skin care advisor with OpenAI model"""
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=st.secrets["openai"]["api_key"]
        )
        self.chain = LLMChain(
            llm=self.llm,
            prompt=prompt
        )
    
    def get_recommendations(self, skin_type: str, skin_concerns: List[str], additional_info: str) -> Recommendation:
        """Get personalized skin care recommendations"""
        try:
            concerns_str = ", ".join(skin_concerns) if skin_concerns else "Aucun problème spécifique mentionné"
            # Instruct the LLM to output in the expected JSON format
            format_instructions = output_parser.get_format_instructions()
            response = self.chain.invoke({
                "skin_type": skin_type,
                "skin_concerns": concerns_str,
                "additional_info": additional_info,
                "format_instructions": format_instructions
            })
            # Parse the response as JSON and then into the Pydantic model           
            data = json.loads(response['text'])
            return Recommendation(**data)
        except Exception as e:
            st.error(f"Une erreur s'est produite: {str(e)}")
            return None

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
    advisor = SkinCareAdvisor()
    
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