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

class QuantifiedIngredient(BaseModel):
    name: str
    quantity: float

class Product(BaseModel):
    name: str
    type: str
    action: str
    contenance: int
    composition: List[QuantifiedIngredient]

class Routine(BaseModel):
    products: List[Product]

class Recommendation(BaseModel):
    type: str
    product: Product

class SkinCareAnalyse(BaseModel):
    diagnostic: str
    ingredients: List[Ingredient]
    recommendation: Product

output_parser = PydanticOutputParser(pydantic_object=SkinCareAnalyse)


# Create the prompt template
TEMPLATE = """Vous êtes un expert dermatologue spécialisé dans les soins de la peau.

Information sur le patient:
Age: {age}
Sexe: {sexe}
Type de peau: {skin_type}
Problèmes de peau: {skin_concerns}
Informations supplémentaires: {additional_info}

Donnez un diagnostic détaillé de la peau  et des problèmes rencontrés.
Fournissez une recommendation pour le besoin {product_type}, pour traiter efficacement les problèmes de peau diagnostiqués.
Une recommendation est composée d'un type de produit (routine jour, routine nuit, crème, gel, sérum, nettoyant, etc.) et d'un produit.
Un produit a un nom, un type (crème, gel, sérum, nettoyant, etc.), une contenance en ml, et son action par rapport à une problématique diagnostiquée.
Un produit a une composition de tous les ingrédients nécessaires pour la production de ce produit.
Cette composition donne la quantité de chaque ingrédient en pourcentage, la somme des pourcentages doit être égale à 100.
Expliquez le role de chaque produit par rapport a une problématique diagnostiquée.

{format_instructions}

Assurez-vous que vos recommandations:
1. Sont spécifique au besoin {product_type}
2. Sont réalistes et applicables au quotidien
3. Sont expliquées de manière claire et accessible
4. Respectent les normes de l'industrie cosmétique.
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
    
    def get_skin_care_analyse(self,
        age: int,
        sexe: str,
        skin_type: str,
        skin_concerns: List[str],
        additional_info: str,
        product_type: List[str]
    ) -> SkinCareAnalyse:
        """Get personalized skin care recommendations"""
        concerns_str = ", ".join(skin_concerns) if skin_concerns else "Aucun problème spécifique mentionné"
        product_type_str = ", ".join(product_type) if product_type else "Routine jour et nuit"
        # Instruct the LLM to output in the expected JSON format
        format_instructions = output_parser.get_format_instructions()
        response = self.chain.invoke({
            "age": age,
            "sexe": sexe,
            "skin_type": skin_type,
            "skin_concerns": concerns_str,
            "additional_info": additional_info,
            "product_type": product_type_str,
            "format_instructions": format_instructions
        })
        # Parse the response as JSON and then into the Pydantic model   
        data = json.loads(response['text'])
        return SkinCareAnalyse(**data)
        