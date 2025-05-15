from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from typing import List, Dict
import json
import csv
class Ingredient(BaseModel):
    name: str = Field(description="nom de l'ingrédient")
    action: str = Field(description="action de l'ingrédient")

class QuantifiedIngredient(BaseModel):
    name: str = Field(description="nom de l'ingrédient")
    quantity: float = Field(description="quantité de l'ingrédient")

class Product(BaseModel):
    name: str = Field(description="nom du produit")
    type: str = Field(description="type du produit")
    action: str = Field(description="action du produit")
    contenance: int = Field(description="contenance du produit")
    composition: List[QuantifiedIngredient] = Field(description="composition du produit")

class Routine(BaseModel):
    products: List[Product] = Field(description="produits de la routine")

class Recommendation(BaseModel):
    products: List[Product] = Field(description="produits recommandés")

class SkinCareAnalyse(BaseModel):
    diagnostic: str = Field(description="diagnostic de la peau")
    ingredients: List[Ingredient] = Field(description="ingrédients de la routine")
    recommendation: Recommendation = Field(description="produits recommandés")

output_parser = PydanticOutputParser(pydantic_object=SkinCareAnalyse)

# Create the prompt template
TEMPLATE = """Vous êtes un expert dermatologue spécialisé dans les soins de la peau.

{format_instructions}

Information sur le patient:
Age: {age}
Sexe: {sexe}
Type de peau: {skin_type}
Problèmes de peau: {skin_concerns}
Informations supplémentaires: {additional_info}

Donnez un diagnostic détaillé de la peau et des problèmes mentionnés.

L'utilisateur a besoin d'un ou plusieurs types de produits. Ces types sont: {product_type}.
Traitez séparément chaque type de produit.
Deux cas sont possibles:
1. Le type de produit demandé est nettoyant ou exfoliant.
2. Le type de produit demandé est un autre type de produit.

Dans le cas 1, utilisez seulement les produits suivants: {predefined_products} et recommandez 
le produit avec le plus haut degré de fiabilité.

Dans le cas 2, recommandez un produit générique cohérent avec le diagnostic et le type de produit demandé.
diagnostiqué.  Si le type de produit demandé est une routine, recommandez une routine complète.

Un produit a un nom, un type (crème, gel, sérum, nettoyant, etc.), une contenance en ml, et son action par rapport à une problématique diagnostiquée.
Un produit a une composition de tous les ingrédients nécessaires pour la production de ce produit.
Donnez le nom exact et le pourcentage de chaque ingrédient, la somme des pourcentages doit être égale à 100.

Assurez-vous que vos recommandations:
1. Sont spécifiques au type {product_type}.
2. Sont réalistes et applicables au quotidien
3. Sont expliquées de manière claire et accessible
4. Respectent les normes de l'industrie cosmétique.
"""

prompt = ChatPromptTemplate.from_template(TEMPLATE)


class SkinCareAdvisor:
    def __init__(self, api_key: str):
        with open('data/products.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self.predefined_products = [row for row in reader]
        """Initialize the skin care advisor with OpenAI model"""
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=api_key,
        )
        self.chain = prompt | self.llm | output_parser
    
    def get_skin_care_analyse(self,
        age: int,
        sexe: str,
        skin_type: str,
        skin_concerns: List[str],
        additional_info: str,
        product_type: List[str],
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
            "format_instructions": format_instructions,
            "predefined_products": self.predefined_products
        })
        return response
