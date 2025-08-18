
from array import array
from ast import If
from genericpath import exists
from mongoengine import Document, StringField, EmbeddedDocument, EmbeddedDocumentField, ListField, DictField
import openpyxl
from pymongo import MongoClient
from bson import ObjectId
import json

clit = MongoClient(host=['localhost:27017'], port=27017,
                   document_class=dict, tz_aware=False, connect=True)
db = clit.get_default_database("cac_perform")

#################################################################################################
class Revue(Document):

    def __init__(self):
        self.list_tableaux = ["CR", "BI", "ERE", "MA", "APE", "TSE", "IT", "PE", "ADP", "ACE", "RF", "PA", "IC", "AAVI", "IF", "ST", "AC", "TR", "CP", "DF", "DCRA", "FCR", "DFS", "AD"]


    def init_revue(self, mission_id):
        # Recupérer les balances
        balances = db.Mission1.find_one({"_id": ObjectId(mission_id)}, {"_id":0})['balances']
        # balance_variation = db.Mission1.find_one({"_id": ObjectId(mission_id)}, {"_id":0})['balance_variation']
        
        id_balance_n = balances[0]
        id_balance_n1 = balances[1]

        balance_n = db.Balance.find_one({"_id": ObjectId(id_balance_n)})['balance']
        balance_n1 = db.Balance.find_one({"_id": ObjectId(id_balance_n1)})['balance']

        # Produire structure à partir d'un fichier JSON
        with open('revue.json', 'r') as file:
            result = json.load(file)
        
        result['mission_id'] = mission_id
        structure = result['structure']

        for struct in result['structure']:
            compte = struct['compte']
            
            struct['solde_n'] = sum(((item['debit_fin'] if item['debit_fin'] is not None else 0) - (item['credit_fin'] if item['credit_fin'] is not None else 0)) for item in balance_n if item['numero_compte'].startswith(str(compte)))
            struct['solde_n1'] = sum(((item['debit_fin'] if item['debit_fin'] is not None else 0) - (item['credit_fin'] if item['credit_fin'] is not None else 0)) for item in balance_n1 if item['numero_compte'].startswith(str(compte)))
            struct['variation'] = struct['solde_n'] - struct['solde_n1']

            if struct['solde_n1'] == 0:
                struct['variation_pourcent'] = 0
            else :
                struct['variation_pourcent'] = (struct['solde_n'] - struct['solde_n1']) / struct['solde_n1']
                struct['variation_pourcent'] = struct['variation_pourcent'] * 100

        created = db.Revue.insert_one(result)
    
        return str(created.inserted_id)
    

    def return_tab_ma(self, mission_id, length_tab, tab):
        query = {"mission_id": mission_id}
        result = db.Revue.find_one(query, {"_id":0})
        structure = result['structure']

        data = []

        for i in range(length_tab):
            row = {}
            cell = tab + str(i + 1)

            row['solde_n1'] = sum(item['solde_n1'] for item in structure if cell in item['ref_revue'])
            row['solde_n'] = sum(item['solde_n'] for item in structure if cell in item['ref_revue'])
            row['variation'] = sum(item['variation'] for item in structure if cell in item['ref_revue'])
            row['variation_pourcent'] = sum(item['variation_pourcent'] for item in structure if cell in item['ref_revue'])

            data.append(row)
        
        return data
        

# creation de nouveaux clients et d'afficher les clients existants
class Client(Document):

    # fonction pour afficher tous les clients existants dans la BD
    @classmethod
    def afficher_clients(cls):

        try:

            cust_data = list(db.Client.find().sort({"_id": -1}))
            for client in cust_data:
                client['_id'] = str(client['_id'])

            return cust_data
        except Exception as e:
            print(f"An exception : {str(e)}")

    @classmethod
    def afficher_missions(cls, id):
        results = []
        final = []
        query = {"id_client": id}
        results = db.Mission1.find(query, {"_id": 0})

        for result in results:
            # result['_id'] = str(result['_id'])
            final.append(result)

        return final

    # fonction pour ajouter un nouveau client
    @classmethod
    def ajouter_client(cls, data):
        try:
            cust_data = db.Client.insert_one(data)

            inserted_id = str(cust_data.inserted_id)

            return inserted_id
        except Exception as e:
            print(f'An exception occurred: {str(e)}')

    @classmethod
    def modifier_client(cls, data):

        try:
            _id = str(data['_id'])

            id_client = ObjectId(_id)

            nom = data['nom']
            activite = data['activite']
            referentiel = data['referentiel']
            forme_juridique = data['forme_juridique']
            capital = data['capital']
            siege_social = data['siege_social']
            adresse = data['adresse']
            n_cc = data['n_cc']
            # date_mission = data['date_mission']

            if id_client:
                db.Client.update_one(
                    {"_id": id_client},

                    {"$set": {
                        "nom": nom,
                        "activite": activite,
                        "referentiel": referentiel,
                        "forme_juridique": forme_juridique,
                        "capital": capital,
                        "siege_social": siege_social,
                        "adresse": adresse,
                        "n_cc": n_cc,
                        # "date_mission": date_mission
                    }
                    })
                return "Updated succeeded"
        except Exception as e:
            print(f'An exception occurred: {str(e)}')

    @classmethod
    def info_client(cls, id_clit):

        try:

            id_client = id_clit
            print(id_client)
            info = db.Client.find_one({"_id": id_client})
            print(info)

            valeurs = {}
            if info:
                # Accédez directement aux champs du document info
                valeurs = {
                    "_id": str(id_client),
                    "nom": info['nom'],
                    "activite": info['activite'],
                    "siege_social": info['siege_social'],
                    "adresse": info['adresse'],
                    "referentiel": info['referentiel'],
                    "forme_juridique": info['forme_juridique'],
                    "capital": info['capital'],
                    "n_cc": info['n_cc'],
                    # "date_mission": info['date_mission']
                }
                print(valeurs)

            return valeurs

        # except pymongo.errors.PyMongoError as e:
        #     print(f"A MongoDB error : {str}")
        except Exception as e:
            print(f"An exception : {str(e)}")
            return None

    def choix_referentiel(self):

        try:

            ref = db.Grouping.find()

            return ref
        except Exception as e:
            print(f"An exception as occured: {str(e)}")


# creation de la classe manager
class Manager(Document):

    _id = StringField()
    email = StringField(required=True)
    mot_de_passe = StringField(required=True)

    def sign_in(self, data):

        try:
            email = data['mail']
            mdp = data['pwd']

            if db.Manager.find_one({"email": email, "mot_de_passe": mdp}):
                return "success"
                # tab = email.split('@')
                # name = tab.pop(0)
                # return f"Connected ! Bienvenue {name}"

        except Exception as e:
            print(f"An exception occurred : {str(e)}")
            return None


# creation des elements de la classe Mission
class LigneComptable(EmbeddedDocument):
    num_compte = StringField(required=True, unique=True)
    libelle = StringField()
    solde = DictField()


class BalanceComptable(EmbeddedDocument):
    lignes = ListField(EmbeddedDocumentField(LigneComptable))


class Mission(Document):
    # stocker des fichiers ou BinaryField()
    balance = EmbeddedDocumentField(BalanceComptable)
    annee_auditee = ListField()

    def nouvelle_mission(self, balances, annee_auditee, id_client, date_debut, date_fin):
        # try:

            balance_ids = []
            les_balance_n_n1 = []
            annee_balance = annee_auditee
            for balance in balances:
                balance_created = self.creation_balance(
                    balance, int(annee_auditee), id_client)
                annee_auditee = int(annee_auditee) - 1

                tuple_en_tableau = list(*[balance_created])

                balance_ids.append(tuple_en_tableau[0])
                les_balance_n_n1.append(tuple_en_tableau[1])

            balance_variation = self.rapprochement_des_balances(
                les_balance_n_n1[0], les_balance_n_n1[1])
            
            print(balance_variation)

            # appel de la fonction de grouping
            grouping_model = self.grouping(balance_variation)

            # appel de la fonction de formation d'etats
            etats = self.prod_efi(balance_variation)
            # etats = self.recuperation_efi(balance_variation)
            # print(etats)
            # creation mission
            result = db.Mission1.insert_one(
                {"id_client": id_client, "annee_auditee": str(annee_balance), "date_debut": date_debut,  "date_fin": date_fin, "balances": balance_ids, "balance_variation": balance_variation, "grouping": grouping_model, "efi": etats})

            insert_id = str(result.inserted_id)
            res = {"id_client": id_client, "annee_auditee": str(
                annee_balance), "date_debut": date_debut,  "date_fin": date_fin, "balances": balance_ids, "balance_variation": balance_variation, "grouping": grouping_model, "efi": etats}

            format_id = {"_id": insert_id, "mission": res}
            return format_id

        # except Exception as e:
        #     print(f'An exception occurred : {str(e)}')
        #     return None

    def creation_balance(self, balance_data, annee_auditee, id_client):
        #try:
            balance = balance_data

            data = []

            # Ouvrir le fichier Excel et accéder à la feuille active
            workbook = openpyxl.load_workbook(balance)
            sheet = workbook['Balance_des_comptes']

            for row in sheet.iter_rows(min_row=2, values_only=True):
                if row[0] == None and row[1] == None:
                    break
                ligne = {}
                ligne['numero_compte'] = row[0]
                ligne['libelle'] = row[1]
                ligne['debit_initial'] = row[2] or 0
                ligne['credit_initial'] = row[3] or 0
                ligne['debit_mvt'] = row[4] or 0
                ligne['credit_mvt'] = row[5] or 0
                ligne['debit_fin'] = int(row[6] or 0)
                ligne['credit_fin'] = int(row[7] or 0)
                ligne['solde'] = ligne['debit_fin'] - ligne['credit_fin']

                data.append(ligne)

            result = db.Balance.insert_one(
                {"id_client": id_client, "annee_balance": annee_auditee, "balance": data})

            # Extraire l'identifiant du document inséré
            inserted_id = str(result.inserted_id)

            # result_data = []
            # result_data.append(inserted_id)
            # result_data.append(data)

            return inserted_id, data
        # except Exception as e:
        #     print(f'An exception occurred : {str(e)}')
        #     return None

    # formation du grouping de classe par nature

    def grouping(self, balances_rapprochee):
        # print(balances_rapprochee)
        # try:
            id = str("658200b45ccab4c870c4cf65")

            _id = ObjectId(id)

            groupe = []

            # Définir les comptes

            grouping_sysco = list(db.Grouping.find({"_id": _id}))

            for item in grouping_sysco[0]['syscohada']:

                somme_n = 0
                somme_n1 = 0
                ligne = {}

                for data in balances_rapprochee:

                    if item['numero'] == data['numero_compte'][0:2]:
                        # print(item['numero'], data['numero_compte'][0:2])

                        if data['solde_n'] == None and data['solde_n1'] != None:
                            somme_n = somme_n + 0
                            somme_n1 = somme_n1 + data['solde_n1']

                        elif data['solde_n'] != None and data['solde_n1'] == None:
                            # data['variation'] = data['solde_n']
                            somme_n = somme_n + data['solde_n']
                            somme_n1 = somme_n1 + 0

                        elif data['solde_n'] != None and data['solde_n1'] != None:
                            somme_n = somme_n + data['solde_n']
                            somme_n1 = somme_n1 + data['solde_n1']

                    ligne['numero'] = item['numero']
                    ligne['libelle'] = item['libelle']
                    ligne['solde_n'] = somme_n if somme_n != 0 and somme_n != None else 0
                    ligne['solde_n1'] = somme_n1 if somme_n1 != 0 and somme_n1 != None else 0

                    if somme_n1 != None and somme_n1 != 0 and somme_n != None:
                        ligne['variation'] = abs(somme_n - somme_n1)
                        ligne['variation_percent'] = round((
                            ligne['variation'] / somme_n1) * 100, 2)
                    else:
                        ligne['variation'] = ''
                        ligne['variation_percent'] = ''
                if ligne['solde_n'] == 0 and ligne['solde_n1'] == 0:
                    print(ligne['solde_n'])
                else:
                    groupe.append(ligne)

            return groupe

        # except Exception as e:
        #     print(f'An exception occurred : {str(e)}')

    # Calculer les variations entre deux variables

    def rapprochement_des_balances(self, balance_n, balance_n1):

        variation_des_balances = []

        for bal in balance_n:
            ligne = {}

            ligne['numero_compte'] = bal['numero_compte']
            ligne['libelle'] = bal['libelle']
            ligne['solde_n'] = bal['solde']
            ligne['solde_n1'] = next((item['solde'] for item in balance_n1 if item.get('numero_compte') == bal['numero_compte']), 0)

            variation_des_balances.append(ligne)
        
        return variation_des_balances

    # determiner le seuil de signification
    def seuil_de_signification(self):

        try:
            ""
        except Exception as e:
            print(f"An error there: {str(e)}")
            return None

    # afficher les informations sur toutes les missions
    def afficher_informations_missions(self, id_client):
        try:

            _id = id_client

            query = list(db.Mission1.find({"_id": _id}).sort({"_id":-1}))

            for data in query:
                data['_id'] = str(data['_id'])

            return query
        except Exception as e:
            print(f"An exception as occured: {str(e)}")

    def prod_efi(self, balance_variation):
        with open('mapping_efi.json', 'r') as file:
            result = json.load(file)
        mapping = result['structure']

        # Traiter le mapping pour obtenir des listes et supprimer les espaces au niveau des *_cpt
        # A supprimer lorsque le mapping sera correctement préparé
        for mapp in mapping:
            mapp['brut_cpt'] = mapp['brut_cpt'].split(',') if mapp.get('brut_cpt') is not None else mapp.get('brut_cpt')
            mapp['amor_cpt'] = mapp['amor_cpt'].split(',') if mapp.get('amor_cpt') is not None else mapp.get('amor_cpt')
            mapp['net_cpt'] = mapp['net_cpt'].split(',') if mapp.get('net_cpt') is not None else mapp.get('net_cpt')
            mapp['brut_except_cpt'] = mapp['brut_except_cpt'].split(',') if mapp.get('brut_except_cpt') is not None else mapp.get('brut_except_cpt',[])
            mapp['amor_except_cpt'] = mapp['amor_except_cpt'].split(',') if mapp.get('amor_except_cpt') is not None else mapp.get('amor_except_cpt',[])
            mapp['net_except_cpt'] = mapp['net_except_cpt'].split(',') if mapp.get('net_except_cpt') is not None else mapp.get('net_except_cpt',[])

        datum = {}
        list_efi = ['actif', 'passif', 'pnl']
        for efi in list_efi:
            structure = []
            select_mapping = (elt for elt in mapping if elt['nature'] == efi)
            for data in select_mapping:
                row = {}
                # Si brut_cpt ou amor_cpt existe, realise l'opération
                if data.get('brut_cpt') and data.get('amor_cpt'):
                    # Calculer net n
                    brut_solde_n = sum(item['solde_n'] for item in balance_variation if any(item['numero_compte'].startswith(cpt) for cpt in data['brut_cpt']))
                    amor_solde_n = sum(item['solde_n'] for item in balance_variation if any(item['numero_compte'].startswith(cpt) for cpt in data['amor_cpt']))
                    # data['net_solde_n'] = data['brut_solde_n'] - data['amor_solde_n']

                    brut_except_n = sum(item['solde_n'] for item in balance_variation if any(str(item['numero_compte']).startswith(cpt) for cpt in data.get('brut_except_cpt',[])))
                    amor_except_n = sum(item['solde_n'] for item in balance_variation if any(str(item['numero_compte']).startswith(cpt) for cpt in data.get('amor_except_cpt',[])))

                    data['brut_solde_n'] = brut_solde_n - brut_except_n
                    data['amor_solde_n'] = amor_solde_n - amor_except_n
                    data['net_solde_n'] = data['brut_solde_n'] - data['amor_solde_n']

                    # Calculer net n-1
                    brut_n1 = sum(item['solde_n1'] for item in balance_variation if any(str(item['numero_compte']).startswith(cpt) for cpt in data['brut_cpt']))
                    amor_n1 = sum(item['solde_n1'] for item in balance_variation if any(str(item['numero_compte']).startswith(cpt) for cpt in data['amor_cpt']))
                    net_except_n1 = sum(item['solde_n1'] for item in balance_variation if any(str(item['numero_compte']).startswith(cpt) for cpt in data.get('net_except_cpt',[])))
                    data['net_solde_n1'] = brut_n1 - amor_n1 - net_except_n1
                # Ne se réalise que dans le cas des EFI actifs
                else:
                    net_solde_n = sum(item['solde_n'] for item in balance_variation if any(str(item['numero_compte']).startswith(cpt) for cpt in data['net_cpt']))
                    net_solde_n1 = sum(item['solde_n1'] for item in balance_variation if any(str(item['numero_compte']).startswith(cpt) for cpt in data['net_cpt']))
                    
                    net_except_n = sum(item['solde_n'] for item in balance_variation if any(str(item['numero_compte']).startswith(cpt) for cpt in data.get('net_except_cpt',[])))
                    net_except_n1 = sum(item['solde_n1'] for item in balance_variation if any(str(item['numero_compte']).startswith(cpt) for cpt in data.get('net_except_cpt',[])))
                    
                    data['net_solde_n'] = net_solde_n - net_except_n
                    data['net_solde_n1'] = net_solde_n1 - net_except_n1

                # Soustraire les exceptions des soldes
                # brut_except_n = sum(item['solde_n'] for item in balance_variation if any(str(item['numero_compte']).startswith(cpt) for cpt in data.get('brut_except_cpt',[])))
                
                # amor_except_n = sum(item['solde_n'] for item in balance_variation if any(str(item['numero_compte']).startswith(cpt) for cpt in data.get('amor_except_cpt',[])))
               
                # net_except_n = sum(item['solde_n'] for item in balance_variation if any(str(item['numero_compte']).startswith(cpt) for cpt in data.get('net_except_cpt',[])))
                # # net_except_n1 = sum(item['solde_n1'] for item in balance_variation if any(str(item['numero_compte']).startswith(cpt) for cpt in data.get('net_except_cpt',[])))


                # data['brut_solde_n'] = data['brut_solde_n'] - brut_except_n
                # data['amor_solde_n'] = data['amor_solde_n'] - amor_except_n
                # data['net_solde_n'] = data['net_solde_n'] - net_except_n
                # data['net_solde_n1'] = data['net_solde_n1'] - net_except_n1
                
                row['ref'] = data['ref']
                row['libelle'] = data['libelle']
                row['compte_to_be_used'] = str(data.get('brut_cpt')) + str(data.get('amor_cpt')) + str(data.get('net_cpt')) + str(data.get('brut_except_cpt')) + str(data.get('amor_except_cpt')) + str(data.get('net_except_cpt'))
                row['compte_to_be_used'] = row['compte_to_be_used'].replace('None', '')
                row['brut_solde_n'] = data['brut_solde_n']
                row['amor_solde_n'] = data['amor_solde_n']
                row['net_solde_n'] = data['net_solde_n']
                row['net_solde_n1'] = data['net_solde_n1']
                
                structure.append(row)

            datum[efi] = structure

        return datum 


    def recuperation_efi(self, balance_variation):
        # try:
            balance_efi = []

            # Récupérer les données de la collection Mapping
            model_inter = list(db.Mapping.find())

            # Récupérer un document de la collection Model_EFI
            model_efi = db.Model_EFI.find_one(
                {"referentiel": "syscohada", "nature": "actif"})

            # Vérifier si un document a été trouvé dans Model_EFI
            if model_efi:

                # Initialiser la somme à zéro pour chaque élément dans model_inter
                for data in model_inter:
                    somme = 0
                    # print(data['structure'])
                    # Parcourir les éléments de balance_variation et model_inter simultanément
                    for dat in data['structure']:
                        somme_brut_n = 0
                        somme_brut_n1 = 0
                        somme_amor_n = 0
                        somme_amor_n1 = 0
                        ligne = {}
                        for num_compte in dat[0]['numero_compte']:

                            for bal in balance_variation:

                                if num_compte == bal['numero_compte'][0:len(str(num_compte))]:
                                    # print(bal['numero_compte'][0:len(str(num_compte))], num_compte)

                                    if dat[0]['ref'].endswith('1'):

                                        if bal['solde_n'] != None and bal['solde_n'] != 0:
                                            somme_brut_n = somme_brut_n + \
                                                bal['solde_n']
                                            # print(somme_brut_n)
                                        elif bal['solde_n1'] != None and bal['solde_n1'] != 0:
                                            somme_brut_n1 = somme_brut_n1 + \
                                                bal['solde_n1']
                                            # print(somme_brut_n1)
                                    else:
                                        if dat[0]['nature'] == 'actifs':
                                            if bal['solde_n'] != None and bal['solde_n'] != 0:
                                                somme_amor_n = somme_amor_n + \
                                                    bal['solde_n']
                                            elif bal['solde_n1'] != None and bal['solde_n1'] != 0:
                                                somme_amor_n1 = somme_amor_n1 + \
                                                    bal['solde_n1']
                                        else:
                                            if bal['solde_n'] != None and bal['solde_n'] != 0:
                                                somme_brut_n = somme_brut_n + \
                                                    bal['solde_n']
                                            elif bal['solde_n1'] != None and bal['solde_n1'] != 0:
                                                somme_brut_n1 = somme_brut_n1 + \
                                                    bal['solde_n1']

                        ligne['nature'] = dat[0]['nature']

                        if len(dat[0]['ref']) == 3:
                            ligne['ref'] = dat[0]['ref'][:-1]
                        else:
                            ligne['ref'] = dat[0]['ref']

                        if dat[0]['nature'] == 'actifs':
                            ligne['libelle'] = dat[0]['libelle']
                            ligne['brut_n'] = somme_brut_n
                            # ligne['brut_n1'] = somme_brut_n1
                            ligne['amort_n'] = somme_amor_n
                            # ligne['amort_n1'] = somme_amor_n1
                            ligne['net_n'] = somme_brut_n - somme_amor_n
                            ligne['net_n1'] = somme_brut_n1 - somme_amor_n1
                            balance_efi.append(ligne)
                        else:
                            ligne['libelle'] = dat[0]['libelle']
                            ligne['net_n'] = somme_brut_n
                            ligne['net_n1'] = somme_brut_n1
                            balance_efi.append(ligne)

            return balance_efi

        # except Exception as e:
        #     print(f'An exception occurred : {str(e)}')
