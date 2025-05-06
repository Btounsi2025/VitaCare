# 🧴 Conseiller en Soins de la Peau (AI Skin Care Advisor)

Une application web intelligente qui fournit des recommandations personnalisées pour les soins de la peau en utilisant l'IA via le modèle GPT-3.5 d'OpenAI.

## ✨ Fonctionnalités

- 🎯 Recommandations personnalisées basées sur votre type de peau
- 🔍 Analyse détaillée des besoins de votre peau
- 💊 Suggestions d'ingrédients adaptés
- ⏰ Routines détaillées pour le jour et la nuit
- 🌐 Interface entièrement en français
- 📱 Design responsive et moderne

## 🛠️ Technologies Utilisées

- **Frontend**: Streamlit
- **IA**: OpenAI GPT-3.5 via LangChain
- **Language**: Python 3.8+
- **Validation des données**: Pydantic
- **Gestion des variables d'environnement**: python-dotenv

## 📋 Prérequis

- Python 3.8 ou supérieur
- Une clé API OpenAI valide
- pip (gestionnaire de paquets Python)

## 🚀 Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/votre-username/skincare-advisor.git
   cd skincare-advisor
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\\Scripts\\activate  # Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement**
   - Créer un fichier `.env` à la racine du projet
   - Ajouter votre clé API OpenAI :
     ```
     OPENAI_API_KEY=votre-clé-api
     ```

## 💻 Utilisation

1. **Démarrer l'application**
   ```bash
   streamlit run app.py
   ```

2. **Accéder à l'interface**
   - Ouvrir votre navigateur
   - Accéder à `http://localhost:8501`

3. **Utiliser l'application**
   - Sélectionner votre type de peau
   - Indiquer vos préoccupations cutanées
   - Ajouter des informations supplémentaires si nécessaire
   - Cliquer sur "Obtenir mes recommandations"

## 📊 Structure du Projet

```
skincare-advisor/
├── app.py              # Application principale
├── requirements.txt    # Dépendances du projet
├── .env               # Variables d'environnement
└── README.md          # Documentation
```

## 🔧 Dépendances Principales

```plaintext
# Core dependencies
streamlit==1.32.0
python-dotenv==1.0.0

# OpenAI and LangChain dependencies
openai==1.12.0
langchain==0.1.12
langchain-openai==0.0.8

# Data validation and type hints
pydantic==2.6.1
typing-extensions==4.9.0
```

## ⚠️ Notes Importantes

- Les recommandations sont générées par IA et sont fournies à titre informatif uniquement
- Pour des problèmes de peau spécifiques, consultez un dermatologue professionnel
- L'application nécessite une connexion internet stable
- Les réponses peuvent varier en fonction de la qualité des informations fournies

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forker le projet
2. Créer une branche pour votre fonctionnalité
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commiter vos changements
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Pousser vers la branche
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Ouvrir une Pull Request

## 📝 License

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.

## 📧 Contact

Votre Nom - [@votre_twitter](https://twitter.com/votre_twitter)

Lien du projet: [https://github.com/votre-username/skincare-advisor](https://github.com/votre-username/skincare-advisor) 