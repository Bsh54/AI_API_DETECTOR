

### `README.md`
```markdown
# InCloud GitHub Scanner

Outil automatisé de détection des fuites de clés API IA sur GitHub.

## 📋 Fonctionnalités

- 🔍 Détection automatique des clés API IA (OpenAI, Anthropic, Google AI, etc.)
- 📊 Génération de rapports détaillés avec niveaux de confiance
- 🤖 Intégration GitHub Actions pour scans automatisés
- 🎯 Filtrage intelligent du code d'exemple
- 📈 Historique des scans pour éviter les doublons
- ⏱️ Protection contre le timeout (optimisé pour GitHub Actions)
- 📧 Notifications automatiques via Issues GitHub

## 🚀 Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/votre-username/InCloudGitHub.git
cd InCloudGitHub
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurez votre token GitHub :
   - Copiez `config.py.example` vers `config.py`
   - Ajoutez votre token GitHub : `GITHUB_TOKEN = "votre_token_ici"`

## 💻 Utilisation

### En ligne de commande

```bash
# Scan automatique des projets AI (50 dépôts max)
python scan_github.py --auto --max-repos 50

# Scan d'un utilisateur spécifique
python scan_github.py --user username --max-repos 30

# Scan d'une organisation
python scan_github.py --org organization --max-repos 50

# Scan d'un dépôt unique
python scan_github.py --repo owner/repo_name

# Aide complète
python scan_github.py --help
```

### Via GitHub Actions

1. Configurez un token GitHub dans les secrets du dépôt
2. Lancez manuellement un scan via l'onglet Actions
3. Les rapports sont automatiquement commités et disponibles en artifacts

## 📊 Clés API Supportées

- **OpenAI** : `sk-...`, `sk-proj-...`, `org-...`
- **Anthropic Claude** : `sk-ant-...`
- **Google AI/Gemini** : `AIza...`
- **Hugging Face** : `hf_...`
- **Cohere** : `cohere-...`
- **AWS Bedrock** : `AKIA...`
- Variables d'environnement : `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.

## ⚙️ Configuration

Modifiez `src/config.py` pour :
- Ajouter de nouveaux patterns de détection
- Modifier les extensions de fichiers à scanner
- Ajuster les répertoires exclus
- Configurer les paramètres de scan

## 🔒 Sécurité

- Les clés détectées sont partiellement masquées dans les rapports
- Les scans sont non-intrusifs (read-only sur GitHub API)
- Respect des limites de rate limiting de GitHub
- Aucune clé n'est stockée en clair



## ⚠️ Avertissement

Cet outil est destiné à :
- Tests de sécurité de vos propres dépôts
- Sensibilisation aux bonnes pratiques de sécurité
- Recherche académique sur la sécurité des clés API

**N'utilisez pas cet outil pour scanner des dépôts sans autorisation.**

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :
1. Forkez le dépôt
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Créez une Pull Request

## 📄 Licence

MIT License - Voir le fichier LICENSE pour plus de détails.

## 🙏 Remerciements

- GitHub pour l'API et GitHub Actions
- La communauté open source pour les librairies Python
- Tous les contributeurs et testeurs
```



### Exemple de Rapport Généré

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║                    🔒 InCloud GitHub Scanner - Rapport de Scan                   ║
╚══════════════════════════════════════════════════════════════════════════════════╝

Type de scan: auto:ai-projects
Début du scan: 2024-01-15 10:30:00
Fin du scan: 2024-01-15 10:45:15
Généré le: 2024-01-15 10:45:16

📦 Dépôt: https://github.com/example/ai-project
   Découvertes: 2
   ────────────────────────────────────────────────────────────

   1. 🔴 Confiance: HIGH
      📄 Fichier: src/config.py
      📍 Ligne: 42
      🗝️ Clé: sk-proj-abc123xxxxyz789
      📝 Contenu: api_key = "sk-proj-abc123xxxxyz789"
      🔍 Pattern: sk-proj-[a-zA-Z0-9_-]{32,}...

📊 STATISTIQUES DU SCAN
────────────────────────────────────────
🔴 Haute confiance: 1
🟡 Moyenne confiance: 2
🟢 Basse confiance: 5
📈 Total des découvertes: 8

🔑 RÉPARTITION PAR TYPE DE CLÉ:
   OpenAI: 3
   Google AI: 2
   Anthropic: 1
   Autre: 2

💡 RECOMMANDATIONS DE SÉCURITÉ
────────────────────────────────────────
1. Stockez les clés API dans des variables d'environnement
2. Utilisez des fichiers .env (ajoutez-les à .gitignore)
3. Pour GitHub, utilisez GitHub Secret