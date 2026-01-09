"""
Fichier de configuration - Scanner GitHub InCloud (sur le cloud)
Version étendue avec capacités de recherche améliorées
"""
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# ================= CONFIGURATION GITHUB =================
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
GITHUB_ENTERPRISE_URL = os.getenv('GITHUB_ENTERPRISE_URL', '')  # Pour GitHub Enterprise
GITHUB_API_VERSION = os.getenv('GITHUB_API_VERSION', '2022-11-28')

# ================= CONFIGURATION DU SCAN =================
INTERVALLE_SCAN_HEURES = int(os.getenv('INTERVALLE_SCAN_HEURES', 24))
DOSSIER_SORTIE = os.getenv('DOSSIER_SORTIE', './rapports_analyse')
CONSERVE_HISTORIQUE = os.getenv('CONSERVE_HISTORIQUE', 'true').lower() == 'true'
MAX_HISTORIQUE_JOURS = int(os.getenv('MAX_HISTORIQUE_JOURS', 30))

# ================= MODÈLES D'INFORMATIONS SENSIBLES ÉTENDUES =================
MODELES_SENSIBLES = [
    # ===== OPENAI & AZURE OPENAI =====
    # Formats officiels OpenAI
    r'sk-[a-zA-Z0-9]{32,}',
    r'sk-proj-[a-zA-Z0-9_-]{32,}',
    r'org-[a-zA-Z0-9]{24}',
    
    # OpenAI API Keys - Variables d'environnement
    r'OPENAI_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'OPENAI_API_KEY[\s]*:[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'OPENAI_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'OPENAI_SECRET_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'OPENAI_ORGANIZATION[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # Azure OpenAI
    r'AZURE_OPENAI_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'AZURE_OPENAI_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'AZURE_OPENAI_ENDPOINT[\s]*=[\s]*["\']?(https?://[a-zA-Z0-9.-]+\.openai\.azure\.com)["\']?',
    
    # ===== ANTHROPIC / CLAUDE =====
    # Formats officiels Anthropic
    r'sk-ant-[a-zA-Z0-9_-]{32,}',
    
    # Anthropic variables
    r'ANTHROPIC_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'ANTHROPIC_AUTH_TOKEN[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'CLAUDE_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'ANTHROPIC_BETA[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{10,})["\']?',
    
    # ===== GOOGLE AI / GEMINI / VERTEX AI =====
    # Google AI Studio / Gemini
    r'AIza[a-zA-Z0-9_-]{35}',
    r'GOOGLE_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'GEMINI_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # Google Cloud / Vertex AI
    r'GOOGLE_APPLICATION_CREDENTIALS[\s]*=[\s]*["\']?([a-zA-Z0-9_\-./]{20,})["\']?',
    r'GOOGLE_CLOUD_PROJECT[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{6,})["\']?',
    r'GCP_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # ===== AMAZON BEDROCK / SAGEMAKER =====
    # AWS Secrets
    r'AWS_ACCESS_KEY_ID[\s]*=[\s]*["\']?(AKIA[0-9A-Z]{16})["\']?',
    r'AWS_SECRET_ACCESS_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9+/]{40})["\']?',
    r'AWS_SESSION_TOKEN[\s]*=[\s]*["\']?([a-zA-Z0-9+/=]{20,})["\']?',
    r'AWS_DEFAULT_REGION[\s]*=[\s]*["\']?([a-z]{2}-[a-z]+-\d)["\']?',
    
    # ===== HUGGING FACE =====
    r'HUGGINGFACE_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'HF_TOKEN[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'HUGGING_FACE_HUB_TOKEN[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # ===== COHERE =====
    r'COHERE_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'CO_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # ===== REPLICATE =====
    r'REPLICATE_API_TOKEN[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # ===== STABILITY AI =====
    r'STABILITY_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'STABILITY_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # ===== TOGETHER AI =====
    r'TOGETHER_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # ===== FAL AI =====
    r'FAL_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # ===== PERPLEXITY AI =====
    r'PERPLEXITY_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # ===== MISTRAL AI =====
    r'MISTRAL_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # ===== GROQ =====
    r'GROQ_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # ===== NOUS =====
    r'NOUS_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # ===== CLAUDE 3 / SONNET / HAIKU =====
    r'CLAUDE3_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'ANTHROPIC_CLAUDE_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # ===== LANGCHAIN =====
    r'LANGCHAIN_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # ===== LLAMA CLOUD =====
    r'LLAMACLOUD_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # ===== CLAUDE BEDROCK =====
    r'CLAUDE_BEDROCK_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # ===== IBM WATSON =====
    r'WATSON_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # ===== OPEN ROUTER =====
    r'OPENROUTER_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # ===== CUSTOM MODELS / LOCAL LLMs =====
    r'LLM_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'LOCAL_AI_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # ===== GÉNÉRIQUES & COURANTS =====
    # Variables snake_case
    r'AI_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'api_key[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'CHAT_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    r'ASSISTANT_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?',
    
    # Variables camelCase/PascalCase
    r'apiKey[\s]*:[\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    r'ApiKey[\s]*:[\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    r'apiKey[\s]*=[\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    r'ApiKey[\s]*=[\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    
    # Spécifiques IA
    r'openaiApiKey[\s]*[:=][\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    r'anthropicApiKey[\s]*[:=][\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    r'geminiApiKey[\s]*[:=][\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    r'claudeApiKey[\s]*[:=][\s]*["\']([a-zA-Z0-9_-]{20,})["\']',
    
    # ===== CONFIGURATION DE MODÈLES =====
    # Modèles utilisés
    r'model[\s]*[:=][\s]*["\'](gpt-4|gpt-3\.5|claude-3|gemini|llama|mistral)[a-zA-Z0-9-]*["\']',
    
    # Endpoints API
    r'base_url[\s]*[:=][\s]*["\'](https?://api\.(openai|anthropic|googleapis|together|replicate)\.(com|ai)/?[^"\']*)["\']',
    
    # ===== MOTS DE PASSE ET SECRETS GÉNÉRAUX =====
    # Secrets génériques (motif large mais utile)
    r'secret[\s]*[:=][\s]*["\']([a-zA-Z0-9_-]{16,})["\']',
    r'password[\s]*[:=][\s]*["\']([a-zA-Z0-9!@#$%^&*()_+-=]{8,})["\']',
    r'token[\s]*[:=][\s]*["\']([a-zA-Z0-9_-]{16,})["\']',
    
    # ===== CONFIGURATION DE PROXY / RÉSEAU =====
    r'https?_proxy[\s]*=[\s]*["\'](https?://[^"\']+)["\']',
    r'http_proxy[\s]*=[\s]*["\'](http://[^"\']+)["\']',
    
    # ===== FICHIERS DE CONFIGURATION =====
    # Fichiers .env, config, etc.
    r'\.env[\s\S]*?([A-Z_]+_API_KEY[\s]*=[\s]*["\']?[a-zA-Z0-9_-]{20,}["\']?)',
    r'config\.(json|yaml|yml|toml)[\s\S]*?"api[_-]?key"[\s]*:[\s]*["\'][a-zA-Z0-9_-]{20,}["\']',
]

# ================= MOTS-CLÉS DE RECHERCHE GITHUB ÉTENDU =================
MOTS_CLES_RECHERCHE_IA = [
    # OpenAI
    'openai api key',
    'openai_api_key',
    'sk-',
    'org-',
    'gpt-4',
    'gpt-3.5',
    'openai completion',
    'openai embedding',
    
    # Anthropic
    'anthropic api',
    'claude api',
    'sk-ant-',
    'anthropic_api_key',
    'claude-3',
    'claude-2',
    
    # Google
    'google ai api',
    'gemini api',
    'vertex ai',
    'aiplatform',
    'google.generativeai',
    
    # Azure
    'azure openai',
    'openai.azure',
    'azure.api',
    
    # AWS
    'amazon bedrock',
    'boto3 bedrock',
    'aws ai',
    
    # Hugging Face
    'huggingface token',
    'hf_token',
    'transformers',
    
    # Divers
    'api_key ai',
    'llm api',
    'language model api',
    'chatgpt api',
    'assistant api',
    'langchain',
    'llamaindex',
    
    # Fichiers de configuration
    '.env API_KEY',
    'config.json api',
    'secrets.toml',
    'environment variables',
    
    # Commentaires dans le code
    '# api key',
    '// api key',
    '/* api key',
    
    # Exemples de code
    'example.com/api',
    'demo key',
    'test api key',
    
    # Modèles spécifiques
    'text-davinci',
    'code-davinci',
    'whisper api',
    'dall-e',
    'stable diffusion',
    'midjourney api',
]

# ================= TERMES DE RECHERCHE AVANCÉS (Github Search Syntax) =================
QUERIES_AVANCÉES = [
    # Recherche par extension de fichier
    'extension:env AI_API_KEY',
    'extension:json apiKey',
    'extension:yaml anthropic',
    'extension:toml secret',
    'extension:py OPENAI_API_KEY',
    'extension:js apiKey',
    'extension:ts openai',
    'extension:md API_KEY',
    
    # Recherche par chemin de fichier
    'path:.env API_KEY',
    'path:config api',
    'path:secrets token',
    'filename:.env.local',
    'filename:config.yaml',
    'filename:settings.py',
    
    # Recherche par organisation/langage
    'org:github language:python api_key',
    'language:javascript openai',
    'language:typescript process.env',
    
    # Combinaisons complexes
    'sk-proj- language:python',
    'AIza language:js',
    'claude in:file',
    'huggingface_hub token',
    
    # Fichiers d'exemple/de test
    'example.env',
    'sample.config',
    'test_api_key',
    'mock_secret',
    
    # Documentation et README
    'README.md API',
    'CONTRIBUTING.md key',
    'docs/*.md secret',
]

# ================= EXPRESSIONS DE FICHIERS SPÉCIFIQUES =================
FICHIERS_CIBLES = [
    # Fichiers de configuration
    '.env',
    '.env.local',
    '.env.development',
    '.env.production',
    '.env.test',
    '.env.example',
    '.env.sample',
    
    # Configurations diverses
    'config.json',
    'config.yml',
    'config.yaml',
    'config.toml',
    'settings.py',
    'config.py',
    'constants.py',
    
    # Secrets management
    'secrets.json',
    'secrets.yml',
    'secrets.toml',
    'keys.json',
    'credentials.json',
    
    # Documentation
    'README.md',
    'README.txt',
    'CONTRIBUTING.md',
    'SETUP.md',
    
    # Docker
    'docker-compose.yml',
    'Dockerfile',
    '.dockerignore',
    
    # Cloud
    'serverless.yml',
    'terraform.tfvars',
    'pulumi.yaml',
]

# ================= EXTENSIONS DE FICHIERS À ANALYSER =================
EXTENSIONS_INCLUSES = [
    '.py', '.js', '.ts', '.jsx', '.tsx',  # Langages de programmation
    '.java', '.cpp', '.c', '.cs', '.go', '.rs', '.rb', '.php',
    '.sh', '.bash', '.zsh', '.fish',  # Shell scripts
    '.json', '.yaml', '.yml', '.toml', '.xml', '.ini', '.cfg', '.conf',  # Configurations
    '.md', '.txt', '.rst', '.tex',  # Documentation
    '.sql', '.graphql', '.gql',  # Bases de données
    '.html', '.htm', '.css', '.scss', '.sass',  # Web
    '.env', '.env.*',  # Variables d'environnement
    '.lock', '.sum', '.mod',  # Dépendances
]

EXTENSIONS_EXCLUES = [
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico', '.webp',  # Images
    '.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm',  # Vidéos
    '.mp3', '.wav', '.ogg', '.flac', '.aac',  # Audio
    '.zip', '.tar', '.gz', '.7z', '.rar', '.bz2',  # Archives
    '.exe', '.dll', '.so', '.dylib', '.bin',  # Exécutables
    '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx',  # Documents Office
    '.woff', '.woff2', '.ttf', '.eot', '.otf',  # Polices
    '.iso', '.img', '.dmg',  # Images disque
]

# ================= DOSSIERS À EXCLURE =================
DOSSIERS_EXCLUS = [
    'node_modules',
    '.git',
    'dist',
    'build',
    'out',
    '__pycache__',
    '.pytest_cache',
    '.mypy_cache',
    'venv',
    'env',
    '.venv',
    '.env',
    'vendor',
    'bower_components',
    'target',
    '.gradle',
    '.idea',
    '.vscode',
    '.vs',
    'coverage',
    '.nyc_output',
    '.next',
    '.nuxt',
    '.cache',
    'tmp',
    'temp',
    'logs',
    '.log',
    'docker',
    '.docker',
    'terraform',
    '.terraform',
    '.serverless',
]

# ================= CONFIGURATION AVANCÉE =================
# Niveaux de confiance pour les détections
NIVEAU_CONFIANCE = {
    'HIGH': ['sk-', 'AIza', 'AKIA', 'ssh-rsa', '-----BEGIN'],
    'MEDIUM': ['api_key', 'API_KEY', 'secret', 'token'],
    'LOW': ['key', 'pass', 'auth']
}

# Taille maximale des fichiers à analyser (en octets)
TAILLE_MAX_FICHIER = 10 * 1024 * 1024  # 10 MB

# Encodages de fichiers à essayer
ENCODAGES = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']

# Patterns pour les faux positifs à exclure
FAUX_POSITIFS = [
    r'example\.com',
    r'your-api-key-here',
    r'paste-your-key-here',
    r'XXXXX',
    r'\[REDACTED\]',
    r'######',
    r'placeholder',
    r'sample_key',
    r'test_key',
    r'dummy_value',
    r'changeme',
    r'your_key_here',
]

# ================= LIMITES API GITHUB =================
DEPOTS_MAX_PAR_RECHERCHE = int(os.getenv('DEPOTS_MAX_PAR_RECHERCHE', 200))
DELAI_RECHERCHE_SECONDES = int(os.getenv('DELAI_RECHERCHE_SECONDES', 2))
REQUETES_MAX_PAR_HEURE = int(os.getenv('REQUETES_MAX_PAR_HEURE', 30))
TAUX_LIMIT_RETRY = int(os.getenv('TAUX_LIMIT_RETRY', 5))

# ================= CONFIGURATION DE NOTIFICATION =================
NOTIFICATION_WEBHOOK = os.getenv('NOTIFICATION_WEBHOOK', '')
NOTIFICATION_EMAIL = os.getenv('NOTIFICATION_EMAIL', '')
NOTIFICATION_SLACK_TOKEN = os.getenv('NOTIFICATION_SLACK_TOKEN', '')
NOTIFICATION_TEAMS_WEBHOOK = os.getenv('NOTIFICATION_TEAMS_WEBHOOK', '')

# Seuils de notification
SEUIL_ALERTE_HAUTE = int(os.getenv('SEUIL_ALERTE_HAUTE', 5))
SEUIL_ALERTE_MOYENNE = int(os.getenv('SEUIL_ALERTE_MOYENNE', 10))

# ================= CONFIGURATION DE BASE DE DONNÉES =================
DB_TYPE = os.getenv('DB_TYPE', 'sqlite')  # sqlite, postgres, mysql
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '')
DB_NAME = os.getenv('DB_NAME', 'github_scanner.db')
DB_USER = os.getenv('DB_USER', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

# ================= CONFIGURATION DE LOGGING =================
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', './logs/scanner.log')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5

# ================= OPTIONS DE FILTRAGE AVANCÉ =================
# Filtrer par date de dernier commit
MIN_LAST_COMMIT_DAYS = int(os.getenv('MIN_LAST_COMMIT_DAYS', 30))
MAX_LAST_COMMIT_DAYS = int(os.getenv('MAX_LAST_COMMIT_DAYS', 365))

# Filtrer par taille de repository
MAX_REPO_SIZE_MB = int(os.getenv('MAX_REPO_SIZE_MB', 100))

# Filtrer par langue principale
LANGUAGES_INCLUDES = os.getenv('LANGUAGES_INCLUDES', '').split(',') if os.getenv('LANGUAGES_INCLUDES') else []
LANGUAGES_EXCLUDES = os.getenv('LANGUAGES_EXCLUDES', '').split(',') if os.getenv('LANGUAGES_EXCLUDES') else []

# ================= CONFIGURATION DE SÉCURITÉ =================
# Validation des tokens détectés
VALIDATE_TOKENS = os.getenv('VALIDATE_TOKENS', 'false').lower() == 'true'
VALIDATION_TIMEOUT = int(os.getenv('VALIDATION_TIMEOUT', 5))

# Masquage des résultats dans les logs
MASK_SENSITIVE_DATA = os.getenv('MASK_SENSITIVE_DATA', 'true').lower() == 'true'

# ================= CONFIGURATION DE RAPPORT =================
REPORT_FORMAT = os.getenv('REPORT_FORMAT', 'json')  # json, html, csv, markdown
REPORT_TEMPLATE = os.getenv('REPORT_TEMPLATE', 'default')
INCLUDE_CONTEXT_LINES = int(os.getenv('INCLUDE_CONTEXT_LINES', 3))
GENERATE_SUMMARY = os.getenv('GENERATE_SUMMARY', 'true').lower() == 'true'

# ================= CONFIGURATION DE PARALLÉLISME =================
MAX_WORKERS = int(os.getenv('MAX_WORKERS', 5))
BATCH_SIZE = int(os.getenv('BATCH_SIZE', 10))