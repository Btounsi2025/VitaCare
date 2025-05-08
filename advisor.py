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

class SkinCareAnalyse(BaseModel):
    diagnostic: str
    ingredients: List[Ingredient]
    day_routine: Routine
    night_routine: Routine

output_parser = PydanticOutputParser(pydantic_object=SkinCareAnalyse)


# Create the prompt template
TEMPLATE = """Vous êtes un expert dermatologue spécialisé dans les soins de la peau.

Information sur le patient:
Age: {age}
Sexe: {sexe}
Type de peau: {skin_type}
Problèmes de peau: {skin_concerns}
Informations supplémentaires: {additional_info}

Veuillez fournir un diagnostic détaillé de la peau  et des problèmes rencontrés. 
Fournissez des recommandations personnalisées d'ingrédients nécessaires pour résoudre les problèmes de peau.
Expliquer le role de chaque ingrédient par rapport a une problématique diagnostiquée.
Fournisser un exemple de routine de soins qui traitent efficacement les problèmes de peau diagnostiqués en 
se basant sur les ingrédients identifiés.
La routine qui se compose d'une routine de jour et d'une routine de nuit.
Chaque routine de soins se compose d'un ensemble de produits de soins de la peau.
Pour chaque produit, préciser le type de produit (crème, gel, lotion, etc.),
Chaque produit peut contenir en plus des ingrédients identifiées d'autres ingrédients pour les besoin de la production.
la contenance en ml, et la composition en ingrédients avec le pourcentage de chaque ingrédient.
La somme des pourcentages des ingrédients doit être égale à 100.
Cette formule de composition est destinée a une unité de production de produit de soins de la peau.

{format_instructions}

Assurez-vous que vos recommandations sont:
1. Spécifiques au type de peau et aux problèmes mentionnés
2. Réalistes et applicables au quotidien
3. Expliquées de manière claire et accessible
4. Basées sur des ingrédients reconnus en dermatologie.
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
    
    def get_skin_care_analyse(self, age: int, sexe: str, skin_type: str, skin_concerns: List[str], additional_info: str) -> SkinCareAnalyse:
        """Get personalized skin care recommendations"""
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
        return SkinCareAnalyse(**data)
        