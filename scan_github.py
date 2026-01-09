
#!/usr/bin/env python3
"""
Scanner GitHub InCloud (cloud) - Programme principal
Pour scanner les clés API IA et les informations sensibles divulguées dans les dépôts GitHub
"""
import argparse
import sys
import os
from datetime import datetime
from config import GITHUB_TOKEN
from scanner import CloudScanner


def afficher_banniere():
    """Afficher la bannière du programme"""
    banniere = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        Scanner GitHub InCloud (cloud)                     ║
║        Scanner de fuites de clés API IA                   ║
║                                                           ║
║        Version: 1.0.0                                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banniere)


def valider_token_github() -> bool:
    """Vérifier l'existence du token GitHub"""
    if not GITHUB_TOKEN:
        print("❌ Erreur : Token GitHub non trouvé")
        print("\nVeuillez suivre ces étapes :")
        print("1. Copier .env.example en .env")
        print("2. Créer un Personal Access Token sur https://github.com/settings/tokens")
        print("3. Ajouter le Token à la variable GITHUB_TOKEN dans le fichier .env")
        return False
    return True


def main():
    """Fonction principale"""
    afficher_banniere()
    
    # Créer l'analyseur d'arguments de ligne de commande
    parser = argparse.ArgumentParser(
        description='Scanner les clés API IA et les informations sensibles divulguées dans les dépôts GitHub',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  # Scanner tous les dépôts publics d'un utilisateur spécifique
  python scan_github.py --utilisateur nom_utilisateur
  
  # Scanner tous les dépôts publics d'une organisation spécifique
  python scan_github.py --organisation nom_organisation
  
  # Scanner un dépôt unique
  python scan_github.py --depot proprietaire/nom_depot
  
  # Recherche et analyse automatique de projets liés à l'IA
  python scan_github.py --auto
  
  # Recherche et analyse automatique d'un nombre spécifique de dépôts
  python scan_github.py --auto --depots-max 100
        """
    )
    
    # Ajouter les paramètres
    parser.add_argument(
        '--utilisateur',
        type=str,
        help='Scanner tous les dépôts publics d\'un utilisateur GitHub spécifique'
    )
    
    parser.add_argument(
        '--organisation',
        type=str,
        help='Scanner tous les dépôts publics d\'une organisation GitHub spécifique'
    )
    
    parser.add_argument(
        '--depot',
        type=str,
        help='Scanner un dépôt unique (format: proprietaire/nom_depot)'
    )
    
    parser.add_argument(
        '--auto',
        action='store_true',
        help='Recherche et analyse automatique de projets liés à l\'IA'
    )
    
    parser.add_argument(
        '--depots-max',
        type=int,
        default=200,
        help='Nombre maximum de dépôts à scanner en mode automatique (par défaut: 200)'
    )
    
    parser.add_argument(
        '--token',
        type=str,
        help='GitHub Personal Access Token (optionnel, par défaut lu depuis .env)'
    )
    
    parser.add_argument(
        '--dossier-sortie',
        type=str,
        help='Répertoire de sortie des rapports (optionnel, par défaut: ./rapports_analyse)'
    )
    
    parser.add_argument(
        '--ne-pas-sauter-analyses',
        action='store_true',
        help='Ne pas sauter les dépôts déjà analysés, forcer la réanalyse de tous les dépôts'
    )
    
    # Analyser les arguments
    args = parser.parse_args()
    
    # Vérifier si au moins une option d'analyse est fournie
    if not any([args.utilisateur, args.organisation, args.depot, args.auto]):
        parser.print_help()
        print("\n❌ Erreur : Veuillez spécifier au moins une option d'analyse (--utilisateur, --organisation, --depot, ou --auto)")
        sys.exit(1)
    
    # Valider le token GitHub
    token = args.token or GITHUB_TOKEN
    if not token:
        if not valider_token_github():
            sys.exit(1)
    
    # Définir le répertoire de sortie
    if args.dossier_sortie:
        os.environ['DOSSIER_SORTIE'] = args.dossier_sortie
    
    try:
        # Créer une instance du scanner
        sauter_analyses = not args.ne_pas_sauter_analyses
        scanner = CloudScanner(token, sauter_analyses=sauter_analyses)
        
        # Exécuter différentes analyses selon les paramètres
        if args.utilisateur:
            chemin_rapport = scanner.analyser_utilisateur(args.utilisateur)
        elif args.organisation:
            chemin_rapport = scanner.analyser_organisation(args.organisation)
        elif args.depot:
            chemin_rapport = scanner.analyser_depot_unique(args.depot)
        elif args.auto:
            chemin_rapport = scanner.analyser_projets_ia(depots_max=args.depots_max)
        
        print(f"\n✅ Analyse terminée !")
        print(f"📄 Rapport enregistré à : {chemin_rapport}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analyse interrompue par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur pendant l'analyse : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
