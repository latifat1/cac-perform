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
        const response = await axios.post(`/mission/nouvelle_mission`, formData, config);
        if (response.status === 200) {
            isUploaded = response.data;
        }
    } catch (error) {
        const msg = error?.response?.data?.error || error?.response?.data || error.message;
        alert(msg);
    }

    return isUploaded;
}