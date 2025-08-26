import requests
import json

def test_routes():
    """Test de différentes routes pour diagnostiquer le problème"""
    base_url = "http://localhost:5000"
    
    print("🔍 Diagnostic de l'API backend...")
    print("=" * 60)
    
    # Test 1: Route racine
    print("1. Test route racine /")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"   Erreur: {e}")
    
    print()
    
    # Test 2: Route /cors
    print("2. Test route /cors")
    try:
        response = requests.get(f"{base_url}/cors")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"   Erreur: {e}")
    
    print()
    
    # Test 3: Route /cors/mission
    print("3. Test route /cors/mission")
    try:
        response = requests.get(f"{base_url}/cors/mission")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"   Erreur: {e}")
    
    print()
    
    # Test 4: Route /cors/mission/revue_analytique
    print("4. Test route /cors/mission/revue_analytique (sans ID)")
    try:
        response = requests.get(f"{base_url}/cors/mission/revue_analytique")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"   Erreur: {e}")
    
    print()
    
    # Test 5: Route avec ID fictif
    print("5. Test route /cors/mission/revue_analytique/test_mission")
    try:
        response = requests.get(f"{base_url}/cors/mission/revue_analytique/test_mission")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"   Erreur: {e}")
    
    print()
    
    # Test 6: Test de l'endpoint commentaire
    print("6. Test endpoint commentaire (PUT)")
    try:
        test_data = {
            "numero_compte": "512000",
            "commentaire_perso": "Test de commentaire"
        }
        response = requests.put(
            f"{base_url}/cors/mission/revue_analytique/test_mission/commentaire",
            json=test_data
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"   Erreur: {e}")
    
    print()
    print("=" * 60)
    print("📋 Résumé du diagnostic:")
    print("   - Si toutes les routes retournent 404, il y a un problème de configuration")
    print("   - Si certaines routes fonctionnent, le problème est spécifique")
    print("   - Vérifiez les logs du serveur Python pour plus de détails")

if __name__ == "__main__":
    test_routes()


