from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

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
