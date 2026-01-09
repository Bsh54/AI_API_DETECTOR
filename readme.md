# 🔍 AI API Detector - GitHub Scanner

Un outil de sécurité pour détecter les clés API d'intelligence artificielle et autres informations sensibles exposées dans les dépôts GitHub publics.

## 📋 Description

AI API Detector est un scanner automatisé qui recherche et identifie les fuites de clés API dans les dépôts GitHub publics. Il supporte plusieurs fournisseurs d'IA (OpenAI, Anthropic, Google AI, etc.) et peut être utilisé de différentes manières pour améliorer la sécurité de vos projets.

## ✨ Fonctionnalités

- 🔍 **Détection multi-fournisseurs** : OpenAI, Anthropic, Google Gemini, Hugging Face, Cohere, et plus de 20 autres
- 🎯 **Recherche intelligente** : Utilise la syntaxe avancée de recherche GitHub
- 📊 **Rapports détaillés** : Génération de rapports avec niveaux de risque
- 🕐 **Historique d'analyse** : Suivi des dépôts déjà analysés
- ⚡ **Intégration GitHub Actions** : Exécution planifiée ou manuelle
- 🔒 **Validation des clés** : Option de test des clés détectées

## 🚀 Installation

### Prérequis

- Python 3.10+
- Compte GitHub avec [Personal Access Token](https://github.com/settings/tokens)
- Accès à GitHub Actions (pour les workflows automatisés)

### Installation locale

1. **Cloner le dépôt**
```bash
git clone https://github.com/Bsh54/AI_API_DETECTOR.git
cd AI_API_DETECTOR
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer les variables d'environnement**
```bash
cp .env.example .env
# Éditer .env et ajouter votre token GitHub
```

4. **Configurer le token GitHub** dans `.env`
```env
GITHUB_TOKEN=votre_token_ici
```

## 📖 Utilisation

### Analyse en ligne de commande

```bash
# Recherche automatique de projets IA
python scan_github.py --auto --depots-max 50

# Analyser un utilisateur spécifique
python scan_github.py --utilisateur nom_utilisateur

# Analyser une organisation spécifique
python scan_github.py --organisation nom_organisation

# Analyser un dépôt unique
python scan_github.py --depot proprietaire/nom_depot

# Forcer la réanalyse de tous les dépôts
python scan_github.py --auto --ne-pas-sauter-analyses
```

### Workflows GitHub Actions

Le projet inclut trois workflows GitHub Actions :

1. **📅 Analyse planifiée** (quotidienne)
2. **🤖 Analyse automatique** (déclenchement programmé et manuel)
3. **👤 Analyse manuelle** (interface web complète)

### Configuration des workflows

1. **Ajouter le secret GitHub** :
   - Allez dans `Settings → Secrets and variables → Actions`
   - Créez un nouveau secret nommé `GH_SCAN_TOKEN`
   - Collez votre Personal Access Token

2. **Activer les workflows** :
   - Par défaut, l'analyse planifiée s'exécute tous les jours à 23h UTC
   - Vous pouvez modifier l'horaire dans `.github/workflows/scheduled-scan.yml`

## 📊 Structure du projet

```
AI_API_DETECTOR/
├── .github/workflows/          # Définitions des workflows GitHub
│   ├── auto-scan.yml           # Analyse automatique
│   ├── manual-scan.yml         # Analyse manuelle
│   └── scheduled-scan.yml      # Analyse planifiée
├── rapports_analyse/           # Rapports générés
├── historique_analyse/         # Historique des analyses
├── config.py                   # Configuration principale
├── scan_github.py             # Programme principal
├── github_scanner.py          # Client GitHub
├── secret_detector.py         # Détection de secrets
├── report_generator.py        # Génération de rapports
├── scan_history.py            # Gestion historique
├── scanner.py                 # Logique principale
├── test_api.py               # Validation des clés
├── requirements.txt          # Dépendances Python
└── .env                      # Variables d'environnement
```

## 🔧 Configuration avancée

### Modèles de détection

Le fichier `config.py` contient tous les modèles de détection. Vous pouvez :

1. **Ajouter de nouveaux fournisseurs** :
```python
MODELES_SENSIBLES.append(r'NOM_FOURNISSEUR_API_KEY[\s]*=[\s]*["\']?([a-zA-Z0-9_-]{20,})["\']?')
```

2. **Modifier les niveaux de confiance** :
```python
NIVEAU_CONFIANCE = {
    'HIGH': ['sk-', 'AIza', 'AKIA'],
    'MEDIUM': ['api_key', 'secret'],
    'LOW': ['key', 'pass']
}
```

### Exclusions

Configurer les fichiers et dossiers exclus dans `config.py` :
```python
EXTENSIONS_EXCLUES = ['.jpg', '.png', '.mp4', ...]
DOSSIERS_EXCLUS = ['node_modules', '.git', 'venv', ...]
```

## 📈 Résultats

### Structure des rapports

Les rapports sont générés dans `rapports_analyse/` avec le format :
- 📊 **Statistiques** : Distribution des niveaux de risque
- 🎯 **Détails** : Fichier, ligne, type de clé, niveau de confiance
- 🛡️ **Recommandations** : Actions immédiates et mesures préventives

### Exemple de sortie
```
✅ Analyse terminée !
📄 Rapport enregistré à : ./rapports_analyse/rapport_analyse_20240115_143022.txt

📊 Statistiques :
  🔴 Haut risque: 2   🟡 Risque moyen: 5   🟢 Risque faible: 3
  📦 Dépôts concernés: 3
```

## 🛡️ Sécurité

### Bonnes pratiques

1. **Ne jamais exposer votre token** :
   - Toujours utiliser des secrets GitHub Actions
   - Ne jamais pousser `.env` avec des tokens réels

2. **Valider les clés détectées** :
   ```bash
   python test_api.py
   ```

3. **Actions recommandées après détection** :
   - Révoquer immédiatement les clés compromises
   - Supprimer l'historique Git avec `git-filter-repo`
   - Configurer GitHub Secret Scanning

### Limitations

- ⚠️ Analyse uniquement des dépôts publics
- ⏱️ Limites de l'API GitHub (5000 requêtes/heure)
- 🔒 Ne scanne pas les dépôts privés sans autorisation

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. Fork le projet
2. Créez une branche (`git checkout -b feature/amélioration`)
3. Commitez vos changements (`git commit -m 'Ajout: nouvelle fonctionnalité'`)
4. Poussez la branche (`git push origin feature/amélioration`)
5. Ouvrez une Pull Request

### Améliorations possibles

- [ ] Interface web
- [ ] Notifications supplémentaires (Slack, Email)
- [ ] Support de GitLab/Bitbucket
- [ ] Détection de base de données et autres secrets

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## ⚠️ Avertissement

Cet outil est destiné à des fins éducatives et de sécurité. Veuillez :
- Obtenir l'autorisation avant de scanner des dépôts
- Respecter les conditions d'utilisation de l'API GitHub
- Utiliser de manière responsable et éthique

## 📞 Support

Pour les problèmes et questions :
1. Vérifiez la [documentation GitHub](https://docs.github.com/en/rest)
2. Ouvrez une [Issue](https://github.com/Bsh54/AI_API_DETECTOR/issues)
3. Contactez l'équipe de développement

---

**✨ Fait avec ❤️ pour la communauté de sécurité**