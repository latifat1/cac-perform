#!/usr/bin/env python3
"""
Script de test pour vérifier la lecture des fichiers ODS
"""

def test_ods_import():
    try:
        from odf import table, text
        from odf.opendocument import load
        print("✅ Import odfpy réussi")
        
        # Test de base des classes
        print(f"✅ Classe table.Table: {table.Table}")
        print(f"✅ Classe table.TableRow: {table.TableRow}")
        print(f"✅ Classe table.TableCell: {table.TableCell}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Test de l'import odfpy...")
    success = test_ods_import()
    
    if success:
        print("\n🎉 Tous les tests ont réussi !")
        print("💡 Vous pouvez maintenant tester avec vos fichiers ODS")
    else:
        print("\n❌ Tests échoués")
        print("🔧 Vérifiez l'installation d'odfpy")



