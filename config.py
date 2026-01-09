"""
Fichier de configuration - Scanner GitHub InCloud (sur le cloud)
"""
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Configuration GitHub
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')

# Configuration du scan
INTERVALLE_SCAN_HEURES = int(os.getenv('INTERVALLE_SCAN_HEURES', 24))
DOSSIER_SORTIE = os.getenv('DOSSIER_SORTIE', './rapports_analyse')

# Modèles d'informations sensibles liées à l'IA
MODELES_SENSIBLES = [
    # Format des clés API OpenAI
    r'sk-[a-zA-Z0-9]{32,}',
    r'sk-proj-[a-zA-Z0-9_-]{32,}',
    
    # Format des clés API Anthropic
    r'sk-ant-[a-zA-Z0-9_-]{32,}',
    
    # Format des clés API Google AI (Gemini)
    r'AIza[a-zA-Z0-9_-]{35}',
    
    # ===== Modèles courants de noms de variables d'environnement (snake_case) =====
    # Clés API IA
    r'AI_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'ai_api_key[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # OpenAI
    r'OPENAI_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'openai_api_key[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'OPENAI_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # Anthropic
    r'ANTHROPIC_AUTH_TOKEN[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'ANTHROPIC_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'anthropic_api_key[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # Claude
    r'CLAUDE_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'claude_api_key[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # Clé API générique
    r'API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'api_key[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # Clé API Chat
    r'CHAT_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'chat_api_key[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # ===== Modèles camelCase et PascalCase =====
    # Assignation de propriété d'objet : apiKey: "valeur"
    r'apiKey[\s]*:[\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    r'ApiKey[\s]*:[\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    
    # Assignation de variable : apiKey = "valeur"
    r'apiKey[\s]*=[\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    r'ApiKey[\s]*=[\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    
    # Modèle chatApiKey
    r'chatApiKey[\s]*[:=][\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    r'ChatApiKey[\s]*[:=][\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    
    # Modèle openaiApiKey
    r'openaiApiKey[\s]*[:=][\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    r'OpenaiApiKey[\s]*[:=][\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    r'openAIKey[\s]*[:=][\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    
    # Modèle anthropicApiKey
    r'anthropicApiKey[\s]*[:=][\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    r'AnthropicApiKey[\s]*[:=][\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    
    # ===== Autres services d'IA =====
    # Google AI / Gemini
    r'GOOGLE_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'GEMINI_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # Hugging Face
    r'HUGGINGFACE_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'HF_TOKEN[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # Cohere
    r'COHERE_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # Azure OpenAI
    r'AZURE_OPENAI_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'AZURE_OPENAI_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
]

# Mots-clés de recherche GitHub
MOTS_CLES_RECHERCHE_IA = [
    'openai api',
    'anthropic claude',
    'gpt api',
    'AI_API_KEY',
    'ANTHROPIC_AUTH_TOKEN',
    'chat_api_key',
    'apiKey',
    'sk-ant-',
    'sk-proj-',
    'OPENAI_API_KEY',
    'chatApiKey',
]

# Extensions de fichiers à exclure
EXTENSIONS_EXCLUES = [
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg',
    '.mp4', '.avi', '.mov', '.wmv',
    '.zip', '.tar', '.gz', '.rar',
    '.exe', '.dll', '.so', '.dylib',
    '.pdf', '.doc', '.docx',
]

# Dossiers à exclure
DOSSIERS_EXCLUS = [
    'node_modules',
    '.git',
    'dist',
    'build',
    '__pycache__',
    'venv',
    'env',
]

# Limites de taux d'API GitHub
DEPOTS_MAX_PAR_RECHERCHE = 200
DELAI_RECHERCHE_SECONDES = 2