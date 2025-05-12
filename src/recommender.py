import pandas as pd
from langchain_openai import OpenAIEmbeddings
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import Chroma
from pydantic import BaseModel
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
import json
from langchain.output_parsers import PydanticOutputParser

from advisor import SkinCareAnalyse, Ingredient, Product

class Recommendation(BaseModel):
    products: list[Product]

output_parser = PydanticOutputParser(pydantic_object=Product)


# Create the prompt template
TEMPLATE = """Vous êtes un expert en produits de soins de la peau.

Veuillez fournir un produit qui contient l'ingrédient {name} et qui répondent a l'action {action}
dans la liste des produits suivants {products}.

{format_instructions}

Assurez-vous de:
1. Retourner toujours un seul produit
2. Si la liste des produits est vide ne recommandez rien
3. Si aucun ingrédient n'est présent, recommandez un produit qui répond à l'action {action}
avec le degré de fiabilité le plus élevé.

"""

prompt = ChatPromptTemplate.from_template(TEMPLATE)


class ProductRecommender:
    def __init__(self, api_key: str):
        """Initialize the product recommender with RAG capabilities"""
        self.embeddings = OpenAIEmbeddings(api_key=api_key)
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
            prompt=prompt,
        )
        self._initialize_vector_store()
        
    def _initialize_vector_store(self):
        """Create vector store from product descriptions"""
        # Prepare documents for embedding
        PRODUCTS_CSV_PATH = "data/products.csv"
        PRODUCTS_CHROMA_PATH = "chroma_data"

        loader = CSVLoader(file_path=PRODUCTS_CSV_PATH, source_column="description")
        products = loader.load()

        self.vector_store = Chroma.from_documents(
            products, self.embeddings, persist_directory=PRODUCTS_CHROMA_PATH
        )
    
    def _find_matching_product(self, ingredient: Ingredient) -> Product | None:
        """Find the best matching product for a given ingredient"""
        # Search for products matching the ingredient's action
        query = f"Product that contains {ingredient.name} for {ingredient.action}"
        product_retriever  = self.vector_store.as_retriever(k=3)
        products = product_retriever.invoke(query)
        if products:            
            # Instruct the LLM to output in the expected JSON format
            format_instructions = output_parser.get_format_instructions()
            response = self.chain.invoke({
                "name": ingredient.name,
                "action": ingredient.action,
                "products": products,
                "format_instructions": format_instructions
            })
            # Parse the response as JSON and then into the Pydantic model    
            data = json.loads(response['text'])
            return Product(**data)
        return None

    def get_recommended_products(self, skin_care_analyse: SkinCareAnalyse) -> Recommendation:
        """Get recommended products based on the recommendation"""
        recommendation = Recommendation(products=[])
        
        if skin_care_analyse.ingredients:
            # For each ingredient, find a matching product
            for ingredient in skin_care_analyse.ingredients:
                product = self._find_matching_product(ingredient)
                if product:
                    recommendation.products.append(product)
        
        return recommendation
