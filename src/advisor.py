from typing import List
import json
import csv
from llm_factory import get_llm
from output_parser import output_parser, SkinCareAnalyse
from prompt import prompt


class SkinCareAdvisor:
    def __init__(self, api_key: str):
        with open('data/products.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self.predefined_products = [row for row in reader]
        """Initialize the skin care advisor with OpenAI model"""
        self.llm = get_llm(api_key)
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
