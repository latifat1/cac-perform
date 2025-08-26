import os
from flask import jsonify, make_response, request, send_file
from src.mission import mission
from src.model import BalanceComptable, LigneComptable, Mission
# from src.model_revue import Revue_analytique  # Désactivé pour éviter le crash si le docx n'existe pas
from werkzeug.utils import secure_filename
from bson import ObjectId




# =========================
# Revue / Cohérence / Intangibilité (UNIQUE)
# =========================
@mission.get('/revue_analytique/<id_mission>')
def revue_analytique_route(id_mission):
    cls = Mission()
    result = cls.revue_analytique(id_mission)
    return make_response(jsonify({"response": result}), 200)

@mission.put('/revue_analytique/<id_mission>/commentaire')
def update_commentaire_route(id_mission):
    """
    Met à jour le commentaire personnalisé pour un compte spécifique
    """
    try:
        data = request.get_json()
        numero_compte = data.get('numero_compte')
        commentaire_perso = data.get('commentaire_perso')
        
        if not numero_compte:
            return make_response(jsonify({"error": "Numéro de compte requis"}), 400)
        
        cls = Mission()
        success = cls.update_commentaire_perso(id_mission, numero_compte, commentaire_perso)
        
        if success:
            return make_response(jsonify({"response": "Commentaire mis à jour avec succès"}), 200)
        else:
            return make_response(jsonify({"error": "Échec de la mise à jour du commentaire"}), 500)
            
    except Exception as e:
        return make_response(jsonify({"error": f"Erreur serveur: {str(e)}"}), 500)

@mission.get('/controle_coherence/<id_mission>')
def controle_coherence_route(id_mission):
    cls = Mission()
    report = cls.controle_coherence(id_mission)
    return make_response(jsonify({"response": report}), 200)

@mission.get('/controle_intangibilite/<id_mission>')
def controle_intangibilite_route(id_mission):
    cls = Mission()
    report = cls.controle_intangibilite(id_mission)
    return make_response(jsonify({"response": report}), 200)

# =========================
# Création mission
# =========================
@mission.post('/nouvelle_mission')
def new_assign():
    try:
        uploaded_files = request.files.getlist('files[]')
        annee_auditee = request.form.get('annee_auditee')
        id_client = request.form.get('id')
        date_debut = request.form.get('date_debut')
        date_fin = request.form.get('date_fin')
        
        # Validation des données reçues
        if not uploaded_files or len(uploaded_files) < 2:
            return make_response(jsonify({"error": "Au moins 2 fichiers de balance sont requis (N et N-1)"}), 400)
        
        if not all([annee_auditee, id_client, date_debut, date_fin]):
            return make_response(jsonify({"error": "Tous les champs sont requis"}), 400)
        
        # Filtrer les fichiers valides (non vides)
        valid_files = [f for f in uploaded_files if f and f.filename]
        if len(valid_files) < 2:
            return make_response(jsonify({"error": f"Seulement {len(valid_files)} fichier(s) valide(s) reçu(s), 2 requis"}), 400)
        
        print(f"Fichiers reçus: {[f.filename for f in valid_files]}")
        print(f"Données reçues: annee={annee_auditee}, client={id_client}, debut={date_debut}, fin={date_fin}")
        
        cls = Mission()
        donnees = cls.nouvelle_mission(
            valid_files, annee_auditee, id_client, date_debut, date_fin
        )

        if donnees:
            return make_response(jsonify({"success": True, "data": donnees}), 200)
        else:
            return make_response(jsonify({"error": "Erreur lors de la création de la mission"}), 500)
            
    except Exception as e:
        print(f"Erreur dans new_assign: {str(e)}")
        return make_response(jsonify({"error": f"Erreur serveur: {str(e)}"}), 500)

# =========================
# Grouping (si encore utilisé)
# =========================
@mission.get('/grouping_model/')
def make_grouping():
    data = request.files.getlist('file[]')
    model_mission = Mission()
    groupe = model_mission.grouping(balances_rapprochee=data)
    if groupe:
        return make_response(jsonify({"response": groupe}), 200)
    else:
        return make_response(jsonify({"response": "Impossible"}), 201)

#################################################################################################
# Tests liés à Revue_analytique — DÉSACTIVÉS
#################################################################################################
# @mission.get('/test/<id_mission>')
# def test(id_mission):
#     data = Revue_analytique()
#     res = data.init_revue(id_mission)
#     if res == 1:
#         return make_response(jsonify({"response": "Ok"}), 200)
#     else:
#         return make_response(jsonify({"response": "Nop"}), 200)

# @mission.get('/marges/<id_mission>')
# def poptab(id_mission):
#     data = Revue_analytique()
#     res = data.return_tab_ma(id_mission, 12, "MA")
#     if res:
#         return make_response(jsonify({"response": res}), 200)
#     else:
#         return make_response(jsonify({"response": "Nop"}), 200)

# =========================
# Infos mission
# =========================
@mission.get('/affichage_infos_mission/<_id>')
def show_assign_info(_id):
    id_str = str(_id)
    id_object = ObjectId(id_str)

    cls = Mission()
    infos = cls.afficher_informations_missions(id_object)
    if infos:
        return make_response(jsonify({"response": infos}), 200)
    return make_response(jsonify({"response": "Aucune information"}), 200)

# =========================
# EFI (placeholder ancien)
# =========================
@mission.post('/recuperation_etats_financier/')
def generate_efi():
    balances = request.files.getlist('file[]')
    cls = Mission()
    tous = cls.prod_efi(balances)
    return tous

#################################################################################################
# Seuil de signification
#################################################################################################
@mission.get('/get_benchmarks/<id_mission>')
def get_benchmarks(id_mission):
    cls = Mission()
    benchmarks = cls.get_benchmarks(id_mission)
    return make_response(jsonify({"response": benchmarks}), 200)

@mission.put('/save_materiality/<id_mission>')
def save_materiality(id_mission):
    materialities = request.get_json()
    cls = Mission()
    result = cls.save_materiality(id_mission, materialities)
    return make_response(jsonify({"response": result}), 200)

@mission.put('/validate_materiality/<id_mission>')
def validate_materiality(id_mission):
    req = request.get_json()
    bench = req['benchmark']
    cls = Mission()
    result = cls.validate_materiality(id_mission, bench)
    if result:
        return make_response(jsonify({"response": result}), 200)
    else:
        return make_response(jsonify({"response": "Echec"}), 200)

@mission.get('/get_materiality/<id_mission>')
def get_materiality(id_mission):
    cls = Mission()
    materiality = cls.get_materiality(id_mission)
    return make_response(jsonify({"response": materiality}), 200)

@mission.put('/quantitative_analysis/<id_mission>')
def make_quantitative_analysis(id_mission):
    cls = Mission()
    result = cls.make_quantitative_analysis(id_mission)
    return make_response(jsonify({"response": result}), 200)

@mission.put('/qualitative_analysis/<id_mission>')
def make_qualitative_analysis(id_mission):
    cls = Mission()
    listGrouping = request.get_json()
    listGrouping = listGrouping['listGrouping']

    _list_unique_compte = list(set((item['compte'] for item in listGrouping)))

    _listGrouping = []
    for compte in _list_unique_compte:
        data = {}
        data['compte'] = compte
        _list = [{"question": item['compte'], "significant": item['significant']}
                 for item in listGrouping if item['compte'] == compte]
        data['data'] = _list
        _listGrouping.append(data)

    for group in _listGrouping:
        value_sign = any((item['significant'] for item in group['data']))
        group['significant'] = value_sign
        del group['data']

    result = cls.make_qualitative_analysis(id_mission, _listGrouping)
    return make_response(jsonify({"response": result}), 200)

@mission.get('/make_final/<id_mission>')
def make_final(id_mission):
    cls = Mission()
    result, grouping = cls.make_final_sm(id_mission)
    return make_response(jsonify({"response": result, "grouping": grouping}), 200)

@mission.get('/download_grouping/<id_mission>')
def download_grouping(id_mission):
    cls = Mission()
    excel_result = cls.extract_grouping(id_mission)
    return send_file(
        excel_result,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name="grouping.xlsx"
    )
