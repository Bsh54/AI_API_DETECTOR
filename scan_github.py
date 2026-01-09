#!/usr/bin/env python3
"""
InCloud GitHub Scanner - Outil de détection des fuites de clés API IA
"""

import argparse
import sys
import os
from datetime import datetime

# Ajout du chemin src au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from scanner import CloudScanner
from config import Config

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description='Scanner GitHub pour la détection des fuites de clés API IA',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  # Scan automatique des projets AI (50 dépôts maximum)
  python scan_github.py --auto --max-repos 50
  
  # Scan des dépôts d'un utilisateur spécifique
  python scan_github.py --user username --max-repos 30
  
  # Scan d'une organisation
  python scan_github.py --org organization --max-repos 50
  
  # Scan d'un dépôt unique
  python scan_github.py --repo owner/repo_name
  
  # Scan avec token personnalisé
  python scan_github.py --auto --token YOUR_GITHUB_TOKEN
        """
    )
    
    # Arguments principaux
    parser.add_argument('--auto', action='store_true',
                       help='Scan automatique des projets AI')
    parser.add_argument('--user', type=str,
                       help='Scan les dépôts d\'un utilisateur spécifique')
    parser.add_argument('--org', type=str,
                       help='Scan les dépôts d\'une organisation')
    parser.add_argument('--repo', type=str,
                       help='Scan un dépôt spécifique (format: owner/repo_name)')
    
    # Options
    parser.add_argument('--max-repos', type=int, default=50,
                       help='Nombre maximum de dépôts à scanner (défaut: 50)')
    parser.add_argument('--token', type=str, default='',
                       help='Token GitHub personnel (prioritaire sur les variables d\'env)')
    parser.add_argument('--no-skip', action='store_true',
                       help='Ne pas sauter les dépôts déjà scannés')
    parser.add_argument('--timeout', type=int, default=50,
                       help='Timeout en minutes (défaut: 50)')
    parser.add_argument('--output', type=str, default='scan_reports',
                       help='Répertoire de sortie pour les rapports (défaut: scan_reports)')
    
    args = parser.parse_args()
    
    # Validation des arguments
    if not any([args.auto, args.user, args.org, args.repo]):
        parser.print_help()
        print("\n❌ Erreur: Vous devez spécifier un mode de scan")
        sys.exit(1)
    
    # Récupération du token GitHub
    github_token = args.token
    if not github_token:
        github_token = os.environ.get('GITHUB_TOKEN') or Config.GITHUB_TOKEN
    
    if not github_token:
        print("❌ Erreur: Aucun token GitHub fourni")
        print("   Options:")
        print("   1. Utilisez --token YOUR_TOKEN")
        print("   2. Définissez la variable d'environnement GITHUB_TOKEN")
        print("   3. Configurez GITHUB_TOKEN dans config.py")
        sys.exit(1)
    
    try:
        # Initialisation du scanner
        print("🔧 Initialisation du scanner...")
        scanner = CloudScanner(
            github_token=github_token,
            skip_scanned=not args.no_skip
        )
        
        # Configuration du timeout
        scanner.timeout_minutes = args.timeout
        
        # Exécution du scan
        report_path = ""
        
        if args.auto:
            print("🤖 Mode: Scan automatique des projets AI")
            report_path = scanner.scan_ai_projects(max_repos=args.max_repos)
        
        elif args.user:
            print(f"👤 Mode: Scan de l'utilisateur {args.user}")
            report_path = scanner.scan_user_repos(args.user, max_repos=args.max_repos)
        
        elif args.org:
            print(f"🏢 Mode: Scan de l'organisation {args.org}")
            report_path = scanner.scan_organization(args.org, max_repos=args.max_repos)
        
        elif args.repo:
            print(f"📦 Mode: Scan du dépôt {args.repo}")
            report_path = scanner.scan_single_repo(args.repo)
        
        # Résumé
        if report_path:
            print(f"\n✅ Scan terminé avec succès!")
            print(f"📄 Rapport disponible: {report_path}")
            
            # Affichage du chemin absolu
            abs_path = os.path.abspath(report_path)
            print(f"📁 Chemin absolu: {abs_path}")
            
            # Vérification de la taille du rapport
            if os.path.exists(report_path):
                size_kb = os.path.getsize(report_path) / 1024
                print(f"📏 Taille du rapport: {size_kb:.1f} KB")
        else:
            print("⚠️ Scan terminé mais aucun rapport généré")
        
        # Affichage des statistiques
        history_summary = scanner.scan_history.get_scan_summary()
        print(f"\n📊 Statistiques d'historique:")
        print(f"   Total des scans: {history_summary['total_scans']}")
        print(f"   Scans récents (30 jours): {history_summary['recent_scans']}")
        
    except KeyboardInterrupt:
        print("\n⏹️ Scan interrompu par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur lors du scan: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()