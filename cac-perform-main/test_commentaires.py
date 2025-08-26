import requests
import json

# URL de base de l'API
BASE_URL = "http://localhost:5000"

def test_update_commentaire():
    """Test de la mise à jour d'un commentaire"""
    
    # ID de mission de test (à adapter selon vos données)
    mission_id = "test_mission_id"
    numero_compte = "512000"
    commentaire_perso = "Test de commentaire personnalisé"
    
    # Données à envoyer
    data = {
        "numero_compte": numero_compte,
        "commentaire_perso": commentaire_perso
    }
    
    try:
        # Appel à l'API
        response = requests.put(
            f"{BASE_URL}/mission/revue_analytique/{mission_id}/commentaire",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Test réussi : Commentaire mis à jour")
        else:
            print("❌ Test échoué")
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur. Assurez-vous qu'il est démarré.")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_get_revue_analytique():
    """Test de récupération de la revue analytique"""
    
    mission_id = "test_mission_id"
    
    try:
        response = requests.get(f"{BASE_URL}/mission/revue_analytique/{mission_id}")
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Test réussi : Revue analytique récupérée")
        else:
            print("❌ Test échoué")
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur. Assurez-vous qu'il est démarré.")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🧪 Tests de l'API des commentaires")
    print("=" * 40)
    
    print("\n1. Test de récupération de la revue analytique:")
    test_get_revue_analytique()
    
    print("\n2. Test de mise à jour d'un commentaire:")
    test_update_commentaire()

