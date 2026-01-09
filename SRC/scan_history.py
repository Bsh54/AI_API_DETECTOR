import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional

class ScanHistory:
    """Gestionnaire de l'historique des scans"""
    
    def __init__(self, history_file: str = "scan_history.json"):
        self.history_file = history_file
        self.history = self._load_history()
    
    def _load_history(self) -> Dict:
        """Charge l'historique depuis le fichier"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_history(self):
        """Sauvegarde l'historique dans le fichier"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"⚠️ Erreur lors de la sauvegarde de l'historique: {e}")
    
    def is_scanned(self, repo_name: str, days_threshold: int = 30) -> bool:
        """Vérifie si un dépôt a été scanné récemment"""
        if repo_name not in self.history:
            return False
        
        last_scan_str = self.history[repo_name].get('last_scan')
        if not last_scan_str:
            return False
        
        try:
            last_scan = datetime.fromisoformat(last_scan_str)
            threshold_date = datetime.now() - timedelta(days=days_threshold)
            return last_scan > threshold_date
        except ValueError:
            return False
    
    def mark_as_scanned(self, repo_name: str, findings_count: int, scan_type: str):
        """Marque un dépôt comme scanné"""
        self.history[repo_name] = {
            'last_scan': datetime.now().isoformat(),
            'findings_count': findings_count,
            'scan_type': scan_type,
            'scanned_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self._save_history()
    
    def get_scan_summary(self) -> Dict:
        """Récupère un résumé des scans"""
        total_scans = len(self.history)
        recent_scans = 0
        findings_by_type = {}
        
        threshold_date = datetime.now() - timedelta(days=30)
        
        for repo_data in self.history.values():
            try:
                last_scan = datetime.fromisoformat(repo_data['last_scan'])
                if last_scan > threshold_date:
                    recent_scans += 1
                
                scan_type = repo_data.get('scan_type', 'unknown')
                findings_by_type[scan_type] = findings_by_type.get(scan_type, 0) + 1
            except (KeyError, ValueError):
                continue
        
        return {
            'total_scans': total_scans,
            'recent_scans': recent_scans,
            'findings_by_type': findings_by_type
        }
    
    def clear_old_entries(self, days_old: int = 90):
        """Supprime les entrées anciennes de l'historique"""
        threshold_date = datetime.now() - timedelta(days=days_old)
        old_entries = []
        
        for repo_name, repo_data in list(self.history.items()):
            try:
                last_scan = datetime.fromisoformat(repo_data['last_scan'])
                if last_scan < threshold_date:
                    old_entries.append(repo_name)
            except ValueError:
                old_entries.append(repo_name)
        
        for repo_name in old_entries:
            del self.history[repo_name]
        
        if old_entries:
            print(f"🗑️ Supprimé {len(old_entries)} entrées anciennes de l'historique")
            self._save_history()