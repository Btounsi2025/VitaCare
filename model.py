from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from typing import List, Dict
import json

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
Age: {age}
Sexe: {sexe}
Type de peau: {skin_type}
Problèmes de peau: {skin_concerns}
Informations supplémentaires: {additional_info}

Veuillez fournir un diagnostic détaillé de la peau  et des problèmes rencontrés. 
Fournissez des recommandations personnalisées d'ingrédients et de produits pour résoudre les problèmes de peau.

{format_instructions}

Assurez-vous que vos recommandations sont:
1. Spécifiques au type de peau et aux problèmes mentionnés
2. Réalistes et applicables au quotidien
3. Expliquées de manière claire et accessible
4. Basées sur des ingrédients reconnus en dermatologie.
   Précisez le role de chaque ingrédient par rapport a une problématique diagnostiquée.
5. Précisez le ou les ingrédients actifs de chaque produit pour résoudre une problématique diagnostiquée.
"""

prompt = ChatPromptTemplate.from_template(TEMPLATE)


class SkinCareAdvisor:
    def __init__(self, api_key: str):
        """Initialize the skin care advisor with OpenAI model"""
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=api_key,
        )
        self.chain = LLMChain(
            llm=self.llm,
            prompt=prompt
        )
    
    def get_recommendations(self, age: int, sexe: str, skin_type: str, skin_concerns: List[str], additional_info: str) -> Recommendation:
        """Get personalized skin care recommendations"""
        try:
            concerns_str = ", ".join(skin_concerns) if skin_concerns else "Aucun problème spécifique mentionné"
            # Instruct the LLM to output in the expected JSON format
            format_instructions = output_parser.get_format_instructions()
            response = self.chain.invoke({
                "age": age,
                "sexe": sexe,
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