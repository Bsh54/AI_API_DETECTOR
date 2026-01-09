import re
from typing import List, Dict, Pattern
from datetime import datetime
from .config import Config

class SecretDetector:
    """Détecteur d'informations sensibles"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.patterns = self.config.SENSITIVE_PATTERNS
        self.example_keywords = self.config.EXAMPLE_KEYWORDS
    
    def detect_secrets_in_text(self, text: str, file_path: str = "") -> List[Dict]:
        """Détecte les informations sensibles dans un texte"""
        findings = []
        lines = text.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Vérifie si c'est une ligne de commentaire
            is_comment = self._is_comment_line(line, file_path)
            
            for pattern in self.patterns:
                matches = pattern.finditer(line)
                for match in matches:
                    secret = match.group(0)
                    secret_value = match.group(1) if len(match.groups()) > 0 else secret
                    
                    # Filtre le code d'exemple
                    if self._is_likely_example(line, secret_value):
                        continue
                    
                    # Vérifie la validité basique
                    if not self._is_valid_secret(secret_value):
                        continue
                    
                    findings.append({
                        'file_path': file_path,
                        'line_number': line_num,
                        'line_content': line.strip(),
                        'secret': secret_value,
                        'pattern': pattern.pattern,
                        'confidence': self._calculate_confidence(secret_value, line, is_comment),
                        'timestamp': datetime.now().isoformat()
                    })
        
        return findings
    
    def _is_comment_line(self, line: str, file_path: str) -> bool:
        """Vérifie si la ligne est un commentaire"""
        line_stripped = line.strip()
        
        # Commentaires Python, JavaScript, Java, etc.
        if (line_stripped.startswith('#') or 
            line_stripped.startswith('//') or 
            line_stripped.startswith('/*') or
            (line_stripped.startswith('*') and not line_stripped.startswith('**')) or
            line_stripped.startswith('<!--')):
            return True
        
        # Commentaires spécifiques selon l'extension
        if file_path.endswith('.py'):
            return line_stripped.startswith('#')
        elif file_path.endswith(('.js', '.ts', '.java', '.cpp', '.c')):
            return line_stripped.startswith('//') or line_stripped.startswith('/*')
        elif file_path.endswith('.html'):
            return line_stripped.startswith('<!--')
        
        return False
    
    def _is_likely_example(self, line: str, secret: str) -> bool:
        """Détermine si c'est probablement du code d'exemple"""
        line_lower = line.lower()
        
        # Vérifie les mots-clés d'exemple
        for keyword in self.example_keywords:
            if keyword in line_lower:
                return True
        
        # Vérifie les valeurs d'exemple communes
        example_patterns = [
            r'xxxx', r'yyyy', r'1234', r'0000', r'fake_',
            r'test_', r'dummy_', r'sample_', r'example_'
        ]
        
        for pattern in example_patterns:
            if re.search(pattern, secret, re.IGNORECASE):
                return True
        
        return False
    
    def _is_valid_secret(self, secret: str) -> bool:
        """Valide la structure de base d'un secret"""
        # Trop court pour être une vraie clé API
        if len(secret) < 16:
            return False
        
        # Vérifie les patterns invalides
        invalid_patterns = [
            r'^[0-9]+$',  # Uniquement des chiffres
            r'^[a-zA-Z]+$',  # Uniquement des lettres
            r'^test',  # Commence par "test"
            r'^demo',  # Commence par "demo"
            r'^example',  # Commence par "example"
        ]
        
        for pattern in invalid_patterns:
            if re.match(pattern, secret, re.IGNORECASE):
                return False
        
        return True
    
    def _calculate_confidence(self, secret: str, line: str, is_comment: bool) -> str:
        """Calcule le niveau de confiance"""
        # Faible confiance si dans un commentaire
        if is_comment:
            return "low"
        
        # Vérifie les patterns haute confiance
        high_confidence_patterns = [
            (r'^sk-', 40),  # OpenAI, longueur > 40
            (r'^sk-ant-', 32),  # Anthropic
            (r'^AIza', 35),  # Google AI
            (r'^hf_', 34),  # Hugging Face
            (r'^AKIA', 16),  # AWS
        ]
        
        for pattern, min_length in high_confidence_patterns:
            if re.match(pattern, secret) and len(secret) >= min_length:
                # Vérifie que ce n'est pas dans un contexte d'exemple
                if not any(keyword in line.lower() for keyword in ['example', 'demo', 'test']):
                    return "high"
        
        # Confiance moyenne pour les autres patterns valides
        if len(secret) >= 24 and not is_comment:
            return "medium"
        
        return "low"