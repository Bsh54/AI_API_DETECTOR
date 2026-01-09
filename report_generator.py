
"""
Module de génération de rapports
"""
import os
from datetime import datetime
from typing import List, Dict
from config import DOSSIER_SORTIE


class GenerateurRapport:
    """Générateur de rapports d'analyse"""
    
    def __init__(self, dossier_sortie: str = DOSSIER_SORTIE):
        """
        Initialisation du générateur de rapports
        
        Args:
            dossier_sortie: Répertoire de sortie
        """
        self.dossier_sortie = dossier_sortie
        self._assurer_dossier_sortie()
    
    def _assurer_dossier_sortie(self):
        """S'assurer que le répertoire de sortie existe"""
        if not os.path.exists(self.dossier_sortie):
            os.makedirs(self.dossier_sortie)
    
    def generer_rapport(self, 
                       resultats_analyse: List[Dict], 
                       heure_debut_analyse: datetime,
                       type_analyse: str = "auto") -> str:
        """
        Générer un rapport d'analyse
        
        Args:
            resultats_analyse: Liste des résultats d'analyse
            heure_debut_analyse: Heure de début de l'analyse
            type_analyse: Type d'analyse (utilisateur/organisation/auto)
            
        Returns:
            Chemin du fichier de rapport
        """
        heure_rapport = datetime.now()
        horodatage = heure_rapport.strftime("%Y%m%d_%H%M%S")
        nom_fichier = f"rapport_analyse_{horodatage}.txt"
        chemin_fichier = os.path.join(self.dossier_sortie, nom_fichier)
        
        with open(chemin_fichier, 'w', encoding='utf-8') as f:
            # Écrire l'en-tête du rapport
            f.write("╔" + "═" * 78 + "╗\n")
            f.write("║" + " " * 78 + "║\n")
            f.write("║" + "          🔒 Scanner GitHub InCloud (cloud) - Rapport d'analyse des clés API IA".ljust(78) + "║\n")
            f.write("║" + " " * 78 + "║\n")
            f.write("╚" + "═" * 78 + "╝\n\n")
            
            # Durée de l'analyse
            duree = (heure_rapport - heure_debut_analyse).total_seconds()
            str_duree = f"{int(duree // 60)}min{int(duree % 60)}s" if duree >= 60 else f"{int(duree)}s"
            
            # Écrire les informations d'analyse
            f.write("📋 Informations d'analyse\n")
            f.write("━" * 80 + "\n")
            f.write(f"  🎯 Type d'analyse:     {self._formater_type_analyse(type_analyse)}\n")
            f.write(f"  ⏱️  Heure de début:     {heure_debut_analyse.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"  ⏱️  Heure de fin:       {heure_rapport.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"  ⏳ Durée de l'analyse:  {str_duree}\n")
            
            # Aperçu rapide
            compte_haut = sum(1 for r in resultats_analyse if r.get('confiance') == 'elevee')
            compte_moyen = sum(1 for r in resultats_analyse if r.get('confiance') == 'moyenne')
            depots_compte = len(set(r.get('url_depot') for r in resultats_analyse)) if resultats_analyse else 0
            
            emoji_statut = "🔴" if compte_haut > 0 else "🟡" if compte_moyen > 0 else "✅"
            f.write(f"  {emoji_statut} Problèmes détectés:   {len(resultats_analyse)}")
            if len(resultats_analyse) > 0:
                f.write(f" (🔴 {compte_haut} haut risque, 🟡 {compte_moyen} risque moyen)")
            f.write("\n")
            f.write(f"  📦 Dépôts concernés:   {depots_compte}\n")
            f.write("\n")
            
            # Si aucun problème n'est détecté
            if not resultats_analyse:
                f.write("✅ Aucune fuite d'informations sensibles détectée !\n")
                f.write("\nAnalyse terminée, tout est normal.\n")
            else:
                # Grouper par dépôt
                resultats_par_depot = self._grouper_par_depot(resultats_analyse)
                
                # Écrire les découvertes pour chaque dépôt
                for url_depot, decouvertes in resultats_par_depot.items():
                    self._ecrire_decouvertes_depot(f, url_depot, decouvertes)
                
                # Écrire les statistiques
                self._ecrire_statistiques(f, resultats_analyse)
            
            # Écrire la fin du rapport
            f.write("\n╔" + "═" * 78 + "╗\n")
            f.write("║" + " " * 78 + "║\n")
            f.write("║" + "                 ✅ Rapport généré - Traitez les problèmes détectés rapidement".ljust(78) + "║\n")
            f.write("║" + " " * 78 + "║\n")
            f.write("║" + f"  Heure de génération: {heure_rapport.strftime('%d/%m/%Y %H:%M:%S')}".ljust(78) + "║\n")
            f.write("║" + f"  Emplacement du rapport: {chemin_fichier}".ljust(78) + "║\n")
            f.write("║" + " " * 78 + "║\n")
            f.write("╚" + "═" * 78 + "╝\n")
        
        return chemin_fichier
    
    def _grouper_par_depot(self, resultats_analyse: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Grouper les résultats d'analyse par dépôt
        
        Args:
            resultats_analyse: Liste des résultats d'analyse
            
        Returns:
            Dictionnaire des résultats groupés par dépôt
        """
        groupes = {}
        for resultat in resultats_analyse:
            url_depot = resultat.get('url_depot', 'Inconnu')
            if url_depot not in groupes:
                groupes[url_depot] = []
            groupes[url_depot].append(resultat)
        return groupes
    
    def _formater_type_analyse(self, type_analyse: str) -> str:
        """Formater l'affichage du type d'analyse"""
        mappage_type = {
            'auto:projets-ia': '🤖 Recherche automatique de projets IA',
            'utilisateur': '👤 Analyse d\'utilisateur spécifique',
            'organisation': '🏢 Analyse d\'organisation spécifique',
            'unique': '📦 Analyse d\'un dépôt unique',
        }
        for cle, valeur in mappage_type.items():
            if type_analyse.startswith(cle):
                return valeur
        return type_analyse
    
    def _ecrire_decouvertes_depot(self, f, url_depot: str, decouvertes: List[Dict]):
        """
        Écrire les découvertes pour un dépôt spécifique
        
        Args:
            f: Objet fichier
            url_depot: URL du dépôt
            decouvertes: Liste des découvertes pour ce dépôt
        """
        # Extraire le nom du dépôt
        parties_url = url_depot.split('/')[-2:] if '/' in url_depot else [url_depot]
        nom_depot = '/'.join(parties_url) if len(parties_url) == 2 else url_depot
        
        # Calculer le niveau de risque
        compte_haut = sum(1 for d in decouvertes if d.get('confiance') == 'elevee')
        niveau_risque = "🔴 Haut risque" if compte_haut > 0 else "🟡 Risque moyen"
        
        f.write("\n╭" + "─" * 78 + "╮\n")
        f.write(f"│ 📦 Dépôt: {nom_depot}".ljust(80) + "│\n")
        f.write(f"│ 🔗 Adresse: {url_depot}".ljust(80) + "│\n")
        f.write(f"│ {niveau_risque}   {len(decouvertes)} problème(s) détecté(s)".ljust(80) + "│\n")
        f.write("╰" + "─" * 78 + "╯\n\n")
        
        for idx, decouverte in enumerate(decouvertes, 1):
            # Marque de confiance
            confiance = decouverte.get('confiance', 'inconnu')
            infos_confiance = {
                'elevee': ('🔴', 'Haut risque', 'Traitement immédiat'),
                'moyenne': ('🟡', 'Risque moyen', 'Traitement recommandé'),
                'faible': ('🟢', 'Risque faible', 'Traitement suggéré')
            }.get(confiance, ('⚪', 'Inconnu', 'Vérification requise'))
            
            f.write(f"  ┌─ Problème #{idx} {'─' * 66}\n")
            f.write(f"  │\n")
            f.write(f"  │ {infos_confiance[0]} Niveau de risque: {infos_confiance[1]} - {infos_confiance[2]}\n")
            f.write(f"  │\n")
            
            # Informations sur le fichier
            chemin_fichier = decouverte.get('chemin_fichier', 'N/A')
            f.write(f"  │ 📄 Chemin du fichier: {chemin_fichier}\n")
            
            # Numéro de ligne
            if decouverte.get('numero_ligne'):
                f.write(f"  │ 📍 Numéro de ligne: {decouverte['numero_ligne']}\n")
            
            # Clé secrète découverte
            secret = decouverte.get('secret', '')
            secret_masque = self._masquer_secret(secret)
            type_secret = self._identifier_type_secret(secret)
            f.write(f"  │\n")
            f.write(f"  │ 🔑 Type de clé: {type_secret}\n")
            f.write(f"  │ 🔐 Contenu de la clé: {secret_masque}\n")
            
            # Source de correspondance (règle de détection)
            if decouverte.get('modele'):
                desc_modele = self._expliquer_modele(decouverte['modele'])
                f.write(f"  │ 🎯 Règle de correspondance: {desc_modele}\n")
            
            # Contexte du code
            if decouverte.get('contenu_ligne'):
                contenu_ligne = decouverte['contenu_ligne'].strip()[:80]
                f.write(f"  │\n")
                f.write(f"  │ 💻 Extrait de code:\n")
                f.write(f"  │    {contenu_ligne}\n")
            
            # Heure de l'analyse
            if decouverte.get('heure_analyse'):
                f.write(f"  │\n")
                f.write(f"  │ 🕐 Heure de découverte: {decouverte['heure_analyse']}\n")
            
            f.write(f"  │\n")
            f.write(f"  └{'─' * 74}\n\n")
        
        f.write("\n")
    
    def _identifier_type_secret(self, secret: str) -> str:
        """
        Identifier le type de clé secrète
        
        Args:
            secret: Chaîne de caractères de la clé
            
        Returns:
            Description du type de clé
        """
        if secret.startswith('sk-proj-'):
            return '🤖 Clé API OpenAI (Projet)'
        elif secret.startswith('sk-ant-'):
            return '🤖 Clé API Anthropic (Claude)'
        elif secret.startswith('sk-'):
            return '🤖 Clé API OpenAI'
        elif secret.startswith('AIza'):
            return '🔍 Clé API Google AI (Gemini)'
        elif 'openai' in secret.lower():
            return '🤖 Clé OpenAI liée'
        elif 'anthropic' in secret.lower() or 'claude' in secret.lower():
            return '🤖 Clé Anthropic liée'
        elif 'api_key' in secret.lower() or 'apikey' in secret.lower():
            return '🔑 Clé API générique'
        else:
            return '🔐 Type de clé inconnu'
    
    def _expliquer_modele(self, modele: str) -> str:
        """
        Convertir un modèle regex en description lisible
        
        Args:
            modele: Chaîne d'expression régulière
            
        Returns:
            Description lisible du modèle
        """
        # Clés avec format spécifique
        if 'sk-proj-' in modele:
            return '📌 Format de clé API OpenAI Project (sk-proj-...)'
        elif 'sk-ant-' in modele:
            return '📌 Format de clé API Anthropic Claude (sk-ant-...)'
        elif modele == r'sk-[a-zA-Z0-9]{32,}':
            return '📌 Format de clé API OpenAI (sk-...)'
        elif 'AIza' in modele:
            return '📌 Format de clé API Google AI/Gemini (AIza...)'
        
        # Modèles de variables d'environnement
        elif 'OPENAI_API_KEY' in modele:
            return '📌 Assignation de variable d\'environnement OPENAI_API_KEY'
        elif 'AI_API_KEY' in modele and 'OPENAI' not in modele:
            return '📌 Assignation de variable d\'environnement AI_API_KEY'
        elif 'ANTHROPIC_AUTH_TOKEN' in modele:
            return '📌 Assignation de variable d\'environnement ANTHROPIC_AUTH_TOKEN'
        elif 'ANTHROPIC_API_KEY' in modele:
            return '📌 Assignation de variable d\'environnement ANTHROPIC_API_KEY'
        elif 'CLAUDE_API_KEY' in modele:
            return '📌 Assignation de variable d\'environnement CLAUDE_API_KEY'
        elif 'CHAT_API_KEY' in modele:
            return '📌 Assignation de variable d\'environnement CHAT_API_KEY'
        elif 'GOOGLE_API_KEY' in modele:
            return '📌 Assignation de variable d\'environnement GOOGLE_API_KEY'
        elif 'GEMINI_API_KEY' in modele:
            return '📌 Assignation de variable d\'environnement GEMINI_API_KEY'
        elif 'AZURE_OPENAI' in modele:
            return '📌 Assignation de variable d\'environnement Azure OpenAI'
        elif 'HUGGINGFACE_API_KEY' in modele:
            return '📌 Assignation de variable d\'environnement HUGGINGFACE_API_KEY'
        elif 'HF_TOKEN' in modele:
            return '📌 Assignation de variable d\'environnement HF_TOKEN'
        elif 'COHERE_API_KEY' in modele:
            return '📌 Assignation de variable d\'environnement COHERE_API_KEY'
        elif 'API_KEY' in modele and 'api_key' in modele:
            return '📌 Assignation de variable d\'environnement API_KEY/api_key'
        
        # Modèles camelCase/PascalCase
        elif 'apiKey' in modele and 'chat' not in modele.lower() and 'openai' not in modele.lower():
            return '📌 Assignation de propriété/variable apiKey'
        elif 'chatApiKey' in modele:
            return '📌 Assignation de propriété/variable chatApiKey'
        elif 'openaiApiKey' in modele or 'openAIKey' in modele:
            return '📌 Assignation de propriété/variable openaiApiKey/openAIKey'
        elif 'anthropicApiKey' in modele:
            return '📌 Assignation de propriété/variable anthropicApiKey'
        
        # Modèles génériques
        elif 'api_key' in modele.lower():
            return '📌 Assignation de variable api_key générique'
        
        # Par défaut
        else:
            return f'📌 Modèle regex: {modele[:50]}...' if len(modele) > 50 else f'📌 Modèle regex: {modele}'
    
    def _masquer_secret(self, secret: str) -> str:
        """
        Masquer partiellement la clé secrète
        
        Args:
            secret: Clé originale
            
        Returns:
            Clé masquée
        """
        if len(secret) <= 8:
            return "*" * len(secret)
        
        # Afficher les 4 premiers et 4 derniers caractères
        return f"{secret[:4]}{'*' * (len(secret) - 8)}{secret[-4:]}"
    
    def _ecrire_statistiques(self, f, resultats_analyse: List[Dict]):
        """
        Écrire les statistiques
        
        Args:
            f: Objet fichier
            resultats_analyse: Liste des résultats d'analyse
        """
        f.write("\n╔" + "═" * 78 + "╗\n")
        f.write("║" + " " * 78 + "║\n")
        f.write("║" + "                           📊 Statistiques et analyse".ljust(78) + "║\n")
        f.write("║" + " " * 78 + "║\n")
        f.write("╚" + "═" * 78 + "╝\n\n")
        
        # Statistiques par niveau de confiance
        comptes_confiance = {
            'elevee': 0,
            'moyenne': 0,
            'faible': 0
        }
        
        for resultat in resultats_analyse:
            confiance = resultat.get('confiance', 'faible')
            comptes_confiance[confiance] = comptes_confiance.get(confiance, 0) + 1
        
        f.write("┌─ Distribution des niveaux de risque\n")
        f.write("│\n")
        total = len(resultats_analyse)
        pct_haut = (comptes_confiance['elevee'] / total * 100) if total > 0 else 0
        pct_moyen = (comptes_confiance['moyenne'] / total * 100) if total > 0 else 0
        pct_faible = (comptes_confiance['faible'] / total * 100) if total > 0 else 0
        
        f.write(f"│  🔴 Haut risque: {comptes_confiance['elevee']:3d} ({pct_haut:5.1f}%)")
        f.write(f"  {'█' * int(pct_haut / 5)}\n")
        f.write(f"│  🟡 Risque moyen: {comptes_confiance['moyenne']:3d} ({pct_moyen:5.1f}%)")
        f.write(f"  {'█' * int(pct_moyen / 5)}\n")
        f.write(f"│  🟢 Risque faible: {comptes_confiance['faible']:3d} ({pct_faible:5.1f}%)")
        f.write(f"  {'█' * int(pct_faible / 5)}\n")
        f.write("│\n")
        f.write(f"│  📊 Total: {total} problème(s) potentiel(s)\n")
        f.write("└" + "─" * 78 + "\n\n")
        
        # Statistiques par dépôt
        depots = set(r.get('url_depot') for r in resultats_analyse)
        f.write("┌─ Étendue de l'impact\n")
        f.write("│\n")
        f.write(f"│  📦 Dépôts concernés: {len(depots)}\n")
        f.write(f"│  📄 Fichiers concernés: {len(set(r.get('chemin_fichier') for r in resultats_analyse))}\n")
        f.write("│\n")
        f.write("└" + "─" * 78 + "\n\n")
        
        # Statistiques par type de clé
        types_secret = {}
        for resultat in resultats_analyse:
            secret = resultat.get('secret', '')
            type_s = self._identifier_type_secret(secret)
            types_secret[type_s] = types_secret.get(type_s, 0) + 1
        
        if types_secret:
            f.write("┌─ Distribution des types de clés\n")
            f.write("│\n")
            for type_s, compte in sorted(types_secret.items(), key=lambda x: x[1], reverse=True):
                f.write(f"│  {type_s}: {compte}\n")
            f.write("│\n")
            f.write("└" + "─" * 78 + "\n\n")
        
        # Recommandations de sécurité
        f.write("╔" + "═" * 78 + "╗\n")
        f.write("║" + "                           🛡️  Recommandations de sécurité".ljust(78) + "║\n")
        f.write("╚" + "═" * 78 + "╝\n\n")
        
        f.write("⚠️  Actions immédiates (pour les problèmes à haut risque) :\n")
        f.write("  1. 🚨 Révoquer/faire tourner immédiatement toutes les clés API compromises\n")
        f.write("  2. 🔍 Vérifier les logs d'utilisation des API, confirmer toute utilisation abusive\n")
        f.write("  3. 🗑️  Supprimer complètement les informations sensibles de l'historique Git (avec git-filter-repo)\n")
        f.write("  4. 📧 Notifier les membres concernés de l'équipe\n\n")
        
        f.write("🔒 Mesures de protection à long terme :\n")
        f.write("  1. 📝 Utiliser des variables d'environnement ou un service de gestion de secrets (comme AWS Secrets Manager)\n")
        f.write("  2. 🚫 Ajouter .env, config.json et autres fichiers sensibles à .gitignore\n")
        f.write("  3. 🪝 Configurer des hooks pre-commit pour empêcher la soumission d'informations sensibles\n")
        f.write("  4. 🔄 Faire tourner régulièrement les clés API\n")
        f.write("  5. 👥 Former l'équipe à la sécurité\n")
        f.write("  6. 📊 Exécuter régulièrement cet outil d'analyse pour vérification\n\n")
        
        f.write("📚 Ressources de référence :\n")
        f.write("  • GitHub Secret Scanning: https://docs.github.com/code-security/secret-scanning\n")
        f.write("  • Nettoyage de l'historique Git: https://github.com/newren/git-filter-repo\n")
        f.write("  • Bonnes pratiques: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html\n")
    
    def generer_resume(self, chemin_rapport: str, total_decouvertes: int) -> str:
        """
        Générer un résumé succinct
        
        Args:
            chemin_rapport: Chemin du fichier de rapport
            total_decouvertes: Nombre total de problèmes détectés
            
        Returns:
            Texte du résumé
        """
        if total_decouvertes > 0:
            resume = f"""
{'━' * 80}
✅ Analyse terminée !
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 Rapport enregistré à : {chemin_rapport}

⚠️  {total_decouvertes} problème(s) de sécurité potentiel(s) détecté(s) !

🔴 Actions recommandées immédiatement :
   1. Consulter le rapport détaillé
   2. Révoquer les clés API compromises
   3. Vérifier toute utilisation abusive
   4. Supprimer les informations sensibles de l'historique Git

{'━' * 80}
"""
        else:
            resume = f"""
{'━' * 80}
✅ Analyse terminée !
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 Rapport enregistré à : {chemin_rapport}

🎉 Aucune fuite apparente de clés API détectée !

💡 Recommandations :
   • Continuer les bonnes pratiques de sécurité
   • Exécuter régulièrement des analyses
   • Former l'équipe à la sécurité

{'━' * 80}
"""
        return resume
