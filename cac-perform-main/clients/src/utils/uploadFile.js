import axios from 'axios';

export async function uploadFile(annee_auditee, balances, date_debut, date_fin, id_client) {
    const config = {
        baseURL: 'http://localhost:5000/cors'
        // Ne pas fixer Content-Type; axios gère le boundary multipart
    };

    const formData = new FormData();

    // N'envoyer que de vrais fichiers (ignorer les placeholders "")
    const validFiles = (balances || []).filter(f => !!f && (f.name || f.size !== undefined));
    validFiles.forEach(f => formData.append('files[]', f));

    formData.append('annee_auditee', annee_auditee);
    formData.append('date_debut', date_debut);
    formData.append('date_fin', date_fin);
    formData.append('id', id_client);

    let isUploaded = null;

    try {
        console.log("Envoi de la requête vers:", `/mission/nouvelle_mission`);
        console.log("FormData contenu:", {
            annee_auditee: formData.get('annee_auditee'),
            date_debut: formData.get('date_debut'),
            date_fin: formData.get('date_fin'),
            id: formData.get('id'),
            fichiers: validFiles.map(f => f.name)
        });
        
        const response = await axios.post(`/mission/nouvelle_mission`, formData, config);
        console.log("Réponse reçue:", response.data);
        
        if (response.status === 200) {
            if (response.data.success) {
                isUploaded = response.data.data;
            } else {
                throw new Error(response.data.error || "Erreur inconnue");
            }
        }
    } catch (error) {
        console.error("Erreur lors de l'upload:", error);
        const msg = error?.response?.data?.error || error?.response?.data?.message || error.message || "Erreur réseau";
        alert(`Erreur: ${msg}`);
    }

    return isUploaded;
}