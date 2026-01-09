import openai

def test_openai_key(api_key):
    """
    Teste rapidement une clé API OpenAI
    """
    try:
        # Configuration
        openai.api_key = api_key
        client = openai.OpenAI(api_key=api_key)
        
        # Test simple
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Bonjour"}],
            max_tokens=5
        )
        
        print(f"✅ Clé VALIDE")
        print(f"📝 Réponse: {response.choices[0].message.content}")
        return True
        
    except openai.AuthenticationError:
        print("❌ Clé INVALIDE - Authentification échouée")
        return False
    except openai.RateLimitError:
        print("⚠️  Limite de taux dépassée")
        return True  # La clé est valide mais limitée
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

# Liste des clés à tester depuis votre rapport
keys_to_test = [
    "",
    ""
]

print("🔍 Test des clés API OpenAI détectées\n")

for i, key in enumerate(keys_to_test, 1):
    print(f"\n{'='*50}")
    print(f"Test de la clé #{i}: {key[:10]}...{key[-6:]}")
    test_openai_key(key)
    print(f"{'='*50}")