from langchain.prompts import ChatPromptTemplate



SHOT_LEARNING_EXAMPLES = [
    {
        "age": 37,
        "sexe": "Femme",
        "skin_type": "Peau grasse",
        "skin_concerns": "tâches pigmentaires",
        "product_type": "sérum",
        "predefined_products": [],
        "additional_info": "",
        "diagnostic": "Pour une femme de 37 ans ayant la peau grasse et souhaitant traiter des taches pigmentaires anciennes,\
        l’idéal est de choisir ou formuler un sérum antitâche qui combine agents dépigmentants efficaces, actifs anti-âge, \
        et des ingrédients adaptés aux peaux grasses (non-comédogènes, légers).\
        Objectifs principaux :\
        -  Éclaircir les taches (hyperpigmentation)\
        - Prévenir de nouvelles taches\
        - Réduire les signes de l’âge\
        - Réguler le sébum sans obstruer les pores",
        "recommendation": {
            "products": [
            {
                "name": "Sérum antitâche",
                "type": "sérum",
                "action": "traiter les taches pigmentaires",
                "contenance": 30,
                "composition": [
                    {"name": "Eau distillée", "quantity": 70.30},
                    {"name": "Acide azélaïque", "quantity": 10.00},
                    {"name": "Niacinamide", "quantity": 5},
                    {"name": "Acide tranéxamique", "quantity": 3},
                    {"name": "Alpha-arbutine", "quantity": 2},
                    {"name": "Glycérine végétale", "quantity": 3},
                    {"name": "Acide salicylique", "quantity": 1},
                    {"name": "Panthénol", "quantity": 1},
                    {"name": "Acide hyaluronique", "quantity": 0.1},
                    {"name": "Conservateur Cosgard", "quantity": 1},
                    {"name":"Extrait hydroglycériné de Centella asiatica", "quantity": 2},
                    {"name": "QS pH 5,0 – 5,5 : Solution de soude à 10%", "quantity": 0.1},
                    ],            
                }
            ]
        }
    },
    {
        "age": 37,
        "sexe": "Femme",
        "skin_type": "Peau normale",
        "skin_concerns": "tâches pigmentaires",
        "product_type": "crème",
        "predefined_products": [],
        "additional_info": "",
        "diagnostic": "Pour une femme de 37 ans avec une peau normale souffrant de taches pigmentaires\
         anciennes (comme le mélasma, les lentigos ou les taches post-inflammatoires), \
         la composition idéale d'une crème antitâche doit :\
        - Agir efficacement sur l’hyperpigmentation\
        - Maintenir l’équilibre hydratation/lipides de la peau\
        - Soutenir le renouvellement cellulaire\
        - Prévenir la réapparition des taches\
        - Être douce et non irritante pour un usage quotidien.",
        "recommendation": {
            "products": [
                {
                    "name": "Crème antitâche",
                    "type": "crème",
                    "action": "traiter les taches pigmentaires",
                    "contenance": 30,
                    "composition": [
                        {"name": "Eau purifiée", "quantity": 59.40},
                        {"name": "Glycérine végétale", "quantity": 4.00},
                        {"name": "Acide tranéxamique", "quantity": 3.00},
                        {"name": "Niacinamide", "quantity": 5.00},
                        {"name": "Alpha-arbutine", "quantity": 2.00},
                        {"name": "Acide azélaïque", "quantity": 5.00},
                        {"name": "Panthénol", "quantity": 1.00},
                        {"name": "Extrait de réglisse (glycyrrhiza glabra)", "quantity": 1.00},
                        {"name": "Allantoïne", "quantity": 0.50},
                        {"name": "Acide hyaluronique (PM moyen)", "quantity": 0.30},
                        {"name": "Huile de jojoba", "quantity": 4.00},
                        {"name": "Squalane végétal", "quantity": 4.00},
                        {"name": "Olivem 1000 (émulsifiant naturel)", "quantity": 4.00},
                        {"name": "Cosgard (conservateur)", "quantity": 0.60},
                        {"name": "Correcteur de pH (acide lactique ou NaOH)", "quantity": 0.10},
                        
                    ]
                }
            ]
        }
    }
]
                      


TEMPLATE = """Vous êtes un expert dermatologue spécialisé dans les soins de la peau.

{format_instructions}

Information sur le patient:
Age: {age}
Sexe: {sexe}
Type de peau: {skin_type}
Problèmes de peau: {skin_concerns}
Informations supplémentaires: {additional_info}

Donnez un diagnostic détaillé et accessible de la peau et des problèmes mentionnés.

L'utilisateur a besoin d'un ou plusieurs types de produits. Ces types sont: {product_type}.
Traitez séparément chaque type de produit.
Deux cas sont possibles:
1. Le type de produit demandé est nettoyant ou exfoliant.
2. Le type de produit demandé est un autre type de produit.

Dans le cas 1, utilisez seulement les produits suivants: {predefined_products} et recommandez 
le produit avec le plus haut degré de fiabilité.

Dans le cas 2, recommandez un produit générique cohérent avec le diagnostic et le type de produit demandé.
Si le type de produit demandé est une routine, recommandez une routine complète.

Le produit recommandé doit:
1. Soigner le problème identifié.
2. Réparer la peau et la renforcer.
3. Traiter les causes indirectes qui amplifient le problème.

Un produit a un nom, un type (crème, gel, sérum, nettoyant, etc.), une contenance en ml,
et son action par rapport à une problématique diagnostiquée.
Un produit a une composition galénique d'ingrédients. 
Cette composition inclue les principes actifs, le véhicule, les additifs, les colorants, les parfums, les conservateurs, etc.
Cette composition est destinée à être utilisée par un fabricant de produits cosmétiques.
Donnez le nom exact et le pourcentage de chaque ingrédient, la somme des pourcentages doit être égale à 100.

Assurez-vous que vos recommandations:
1. Sont spécifiques au type {product_type}.
2. Respectent les normes de l'industrie cosmétique.

Voici des exemples de recommandations pour des données de patients:
{examples}
"""

prompt = ChatPromptTemplate.from_template(TEMPLATE)
