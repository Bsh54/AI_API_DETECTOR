import re
from typing import List, Pattern

class Config:
    """Configuration de l'application"""
    
    # GitHub API settings
    GITHUB_TOKEN = ""  # À définir via les secrets GitHub
    GITHUB_API_URL = "https://api.github.com"
    
    # Patterns de détection des clés API
    SENSITIVE_PATTERNS: List[Pattern] = [
        # OpenAI API Keys
        re.compile(r'sk-[a-zA-Z0-9]{32,}'),
        re.compile(r'sk-proj-[a-zA-Z0-9_-]{32,}'),
        re.compile(r'org-[a-zA-Z0-9]{32,}'),
        
        # Anthropic Claude API Keys
        re.compile(r'sk-ant-[a-zA-Z0-9_-]{32,}'),
        
        # Google AI/Gemini API Keys
        re.compile(r'AIza[a-zA-Z0-9_-]{35}'),
        
        # Cohere API Keys
        re.compile(r'cohere-[a-zA-Z0-9]{40}'),
        
        # Hugging Face API Keys
        re.compile(r'hf_[a-zA-Z0-9]{34}'),
        
        # Amazon Bedrock
        re.compile(r'AKIA[0-9A-Z]{16}'),
        
        # Environment variables patterns
        re.compile(r'OPENAI_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?'),
        re.compile(r'ANTHROPIC_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?'),
        re.compile(r'GEMINI_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?'),
        re.compile(r'GOOGLE_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?'),
        
        # JavaScript/TypeScript patterns
        re.compile(r'apiKey[\s]*:[\s]*["\']([a-zA-Z0-9_-]{20,})["\']'),
        re.compile(r'openaiApiKey[\s]*[:=][\s]*["\']([a-zA-Z0-9_-]{20,})["\']'),
        re.compile(r'authToken[\s]*:[\s]*["\']([a-zA-Z0-9_-]{20,})["\']'),
        re.compile(r'secretKey[\s]*:[\s]*["\']([a-zA-Z0-9_-]{20,})["\']'),
        
        # Configuration files
        re.compile(r'["\'](api_key|api_key_id|access_key|secret_key|private_key)["\']\s*:\s*["\']([a-zA-Z0-9_-]{20,})["\']'),
        
        # Generic API keys (catch-all)
        re.compile(r'(?i)(key|token|secret)[\s]*[=:][\s]*["\']([a-zA-Z0-9_-]{20,})["\']'),
    ]
    
    # Keywords pour identifier le code d'exemple
    EXAMPLE_KEYWORDS = [
        'example', 'sample', 'demo', 'test', 'placeholder',
        'your_api_key', 'xxx', 'todo', 'replace', 'change_me',
        'put_your_key_here', 'fill_me', 'fake', 'mock',
        'dummy', 'sample_key', 'test_token', 'example_secret'
    ]
    
    # Extensions de fichier à scanner
    SCAN_EXTENSIONS = [
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.cs',
        '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala',
        '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf',
        '.env', '.env.example', '.env.local', '.env.development',
        '.txt', '.md', '.rst', '.html', '.xml', '.sh', '.bash', '.zsh'
    ]
    
    # Répertoires à exclure
    EXCLUDE_DIRS = [
        '.git', '.github', '.vscode', '.idea',
        'node_modules', '__pycache__', 'venv', 'env',
        'dist', 'build', 'target', 'bin', 'obj',
        'vendor', 'bower_components', 'jspm_packages',
        'coverage', '.next', '.nuxt', '.cache'
    ]
    
    # Fichiers à exclure
    EXCLUDE_FILES = [
        'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
        '*.min.js', '*.min.css', '*.bundle.js',
        '*.jpg', '*.jpeg', '*.png', '*.gif', '*.svg',
        '*.pdf', '*.zip', '*.tar', '*.gz', '*.mp4', '*.mp3'
    ]
    
    # Paramètres de scan
    MAX_REPOS_DEFAULT = 50
    TIMEOUT_MINUTES = 50  # Moins que la limite de 60 minutes de GitHub Actions
    RATE_LIMIT_DELAY = 1  # Délai en secondes entre les requêtes API