import os
import json
from datetime import datetime
from typing import List, Dict
from .config import Config

class ReportGenerator:
    """Générateur de rapports"""
    
    def __init__(self, output_dir: str = "scan_reports"):
        self.config = Config()
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_report(self, scan_results: List[Dict],
                       scan_start_time: datetime,
                       scan_type: str = "auto") -> str:
        """Génère un rapport de scan"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scan_report_{scan_type}_{timestamp}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # En-tête du rapport
            self._write_header(f, scan_type, scan_start_time)
            
            # Groupement par dépôt
            results_by_repo = self._group_by_repo(scan_results)
            
            if not results_by_repo:
                f.write("✅ Aucune fuite de clé API détectée.\n")
            else:
                # Détails par dépôt
                for repo_url, findings in results_by_repo.items():
                    self._write_repo_findings(f, repo_url, findings)
                
                # Résumé et statistiques
                self._write_statistics(f, scan_results)
                
                # Recommandations
                self._write_recommendations(f)
            
            # Pied de page
            self._write_footer(f)
        
        # Génère également un fichier JSON
        self._generate_json_report(scan_results, timestamp, scan_type)
        
        print(f"📄 Rapport généré: {filepath}")
        return filepath
    
    def _write_header(self, f, scan_type: str, start_time: datetime):
        """Écrit l'en-tête du rapport"""
        f.write("╔══════════════════════════════════════════════════════════════════════════════════╗\n")
        f.write("║                    🔒 InCloud GitHub Scanner - Rapport de Scan                   ║\n")
        f.write("╚══════════════════════════════════════════════════════════════════════════════════╝\n\n")
        
        f.write(f"Type de scan: {scan_type}\n")
        f.write(f"Début du scan: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Fin du scan: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("─" * 80 + "\n\n")
    
    def _group_by_repo(self, findings: List[Dict]) -> Dict[str, List[Dict]]:
        """Groupe les résultats par dépôt"""
        grouped = {}
        for finding in findings:
            repo_url = finding.get('repo_url', 'Unknown')
            if repo_url not in grouped:
                grouped[repo_url] = []
            grouped[repo_url].append(finding)
        return grouped
    
    def _write_repo_findings(self, f, repo_url: str, findings: List[Dict]):
        """Écrit les résultats pour un dépôt spécifique"""
        f.write(f"📦 Dépôt: {repo_url}\n")
        f.write(f"   Découvertes: {len(findings)}\n")
        f.write("   " + "─" * 60 + "\n")
        
        for idx, finding in enumerate(findings, 1):
            confidence_emoji = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }.get(finding['confidence'], '⚪')
            
            f.write(f"\n   {idx}. {confidence_emoji} Confiance: {finding['confidence'].upper()}\n")
            f.write(f"      📄 Fichier: {finding['file_path']}\n")
            f.write(f"      📍 Ligne: {finding['line_number']}\n")
            f.write(f"      🗝️ Clé: {self._mask_secret(finding['secret'])}\n")
            f.write(f"      📝 Contenu: {finding['line_content'][:100]}...\n")
            f.write(f"      🔍 Pattern: {finding['pattern'][:50]}...\n")
        
        f.write("\n" + "=" * 80 + "\n\n")
    
    def _mask_secret(self, secret: str) -> str:
        """Masque partiellement un secret"""
        if len(secret) <= 8:
            return "*" * len(secret)
        
        # Montre les premiers 4 et derniers 4 caractères
        visible_start = secret[:4]
        visible_end = secret[-4:] if len(secret) > 8 else ""
        hidden_length = len(secret) - 8
        
        if hidden_length > 0:
            return f"{visible_start}{'*' * hidden_length}{visible_end}"
        else:
            return f"{visible_start}{visible_end}"
    
    def _write_statistics(self, f, findings: List[Dict]):
        """Écrit les statistiques"""
        f.write("📊 STATISTIQUES DU SCAN\n")
        f.write("─" * 40 + "\n")
        
        # Comptage par niveau de confiance
        confidence_counts = {'high': 0, 'medium': 0, 'low': 0}
        for finding in findings:
            confidence = finding['confidence']
            confidence_counts[confidence] = confidence_counts.get(confidence, 0) + 1
        
        f.write(f"🔴 Haute confiance: {confidence_counts['high']}\n")
        f.write(f"🟡 Moyenne confiance: {confidence_counts['medium']}\n")
        f.write(f"🟢 Basse confiance: {confidence_counts['low']}\n")
        f.write(f"📈 Total des découvertes: {len(findings)}\n")
        
        # Comptage par type de clé
        key_types = {}
        for finding in findings:
            secret = finding['secret']
            if secret.startswith('sk-'):
                key_type = "OpenAI"
            elif secret.startswith('sk-ant-'):
                key_type = "Anthropic"
            elif secret.startswith('AIza'):
                key_type = "Google AI"
            elif secret.startswith('hf_'):
                key_type = "Hugging Face"
            elif secret.startswith('AKIA'):
                key_type = "AWS"
            else:
                key_type = "Autre"
            
            key_types[key_type] = key_types.get(key_type, 0) + 1
        
        f.write("\n🔑 RÉPARTITION PAR TYPE DE CLÉ:\n")
        for key_type, count in sorted(key_types.items(), key=lambda x: x[1], reverse=True):
            f.write(f"   {key_type}: {count}\n")
    
    def _write_recommendations(self, f):
        """Écrit les recommandations de sécurité"""
        f.write("\n💡 RECOMMANDATIONS DE SÉCURITÉ\n")
        f.write("─" * 40 + "\n")
        f.write("1. Stockez les clés API dans des variables d'environnement\n")
        f.write("2. Utilisez des fichiers .env (ajoutez-les à .gitignore)\n")
        f.write("3. Pour GitHub, utilisez GitHub Secrets\n")
        f.write("4. Régénérez immédiatement toute clé exposée\n")
        f.write("5. Utilisez des services de gestion de secrets\n")
        f.write("6. Revoyez régulièrement les autorisations des clés API\n")
    
    def _write_footer(self, f):
        """Écrit le pied de page"""
        f.write("\n" + "─" * 80 + "\n")
        f.write("⚠️ Ce rapport est généré automatiquement. Vérifiez manuellement les résultats.\n")
        f.write("🔒 Sécurité des données: Les clés sont partiellement masquées dans ce rapport.\n")
        f.write("📅 Prochain scan recommandé: Dans 7 jours\n")
    
    def _generate_json_report(self, findings: List[Dict], timestamp: str, scan_type: str):
        """Génère un rapport JSON pour traitement ultérieur"""
        json_filename = f"scan_report_{scan_type}_{timestamp}.json"
        json_filepath = os.path.join(self.output_dir, json_filename)
        
        report_data = {
            'metadata': {
                'scan_type': scan_type,
                'timestamp': timestamp,
                'total_findings': len(findings)
            },
            'findings': findings
        }
        
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)