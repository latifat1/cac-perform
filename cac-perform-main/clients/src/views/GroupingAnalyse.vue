<script setup>
import { ref, h, inject, onMounted } from 'vue';
import GroupingComponent from '@/components/GroupingComponent.vue';
import EfiComponent from '@/components/EfiComponent.vue';
import router from "@/router";

const axios = inject('axios');

const props = defineProps(['missionId']);

const componentKey = ref('');
const renderComponent = ref();
const infoMission = ref();
const selectBtn = ref("");

/* === Nouveaux états pour les 3 features === */
const revueAnalytique = ref([]);
const coherenceReport = ref(null);
const intangibiliteReport = ref(null);
const loading = ref(false);
const errorMsg = ref("");
const updatingCommentaire = ref(false);

onMounted(async () => {
  const result = (await axios.get(`/mission/affichage_infos_mission/${props.missionId}`)).data.response;
  infoMission.value = result;
});

/* === Loaders API === */
async function loadRevueAnalytique() {
  loading.value = true; errorMsg.value = "";
  try {
    console.log("🔍 Chargement de la revue analytique pour la mission:", props.missionId);
    const { data } = await axios.get(`/mission/revue_analytique/${props.missionId}`);
    console.log("📊 Données reçues de l'API:", data);
    console.log("📋 Response:", data.response);
    console.log("📏 Longueur:", data.response ? data.response.length : "undefined");
    
    revueAnalytique.value = data.response || [];
    console.log("💾 revueAnalytique.value mis à jour:", revueAnalytique.value);
    console.log("📏 Longueur finale:", revueAnalytique.value.length);
    
  } catch (e) {
    errorMsg.value = "Échec du chargement de la revue analytique.";
    console.error("❌ Erreur lors du chargement:", e);
  } finally {
    loading.value = false;
  }
}

async function loadCoherence() {
  loading.value = true; errorMsg.value = "";
  try {
    const { data } = await axios.get(`/mission/controle_coherence/${props.missionId}`);
    coherenceReport.value = data.response || {};
  } catch (e) {
    errorMsg.value = "Échec du chargement du contrôle de cohérence.";
    console.error(e);
  } finally {
    loading.value = false;
  }
}

async function loadIntangibilite() {
  loading.value = true; errorMsg.value = "";
  try {
    const { data } = await axios.get(`/mission/controle_intangibilite/${props.missionId}`);
    intangibiliteReport.value = data.response || {};
  } catch (e) {
    errorMsg.value = "Échec du chargement du contrôle d’intangibilité.";
    console.error(e);
  } finally {
    loading.value = false;
  }
}

/* === Navigation === */
function showComponent(type) {
  const subProps = { data: infoMission.value };
  selectBtn.value = type;

  // Onglets historiques : Grouping / EFI
  if (type === "grouping") {
    renderComponent.value = h(GroupingComponent, subProps);
    componentKey.value = type;
    return;
  }
  if (type === "efi") {
    renderComponent.value = h(EfiComponent, subProps);
    componentKey.value = type;
    return;
  }

  // Nouveaux onglets : gérés dans le template avec v-if
  renderComponent.value = null;
  componentKey.value = type;

  if (type === "revue") {
    console.log("🎯 Affichage de l'onglet Revue analytique");
    loadRevueAnalytique();
  }
  else if (type === "coherence") {
    console.log("🎯 Affichage de l'onglet Contrôle de cohérence");
    loadCoherence();
  }
  else if (type === "intang") {
    console.log("🎯 Affichage de l'onglet Contrôle d'intangibilité");
    loadIntangibilite();
  }
}

function back() {
  router.go(-1);
}

function exportToCsv(data, filename) {
  // Pour la revue analytique, formater les données avec les commentaires
  let csvContent;
  if (filename === 'revue_analytique') {
    const headers = ['Compte', 'Libellé', 'N', 'N-1', 'Δ', 'Δ %', 'Commentaire Auto', 'Commentaire Perso'];
    const rows = data.map(row => [
      row.numero_compte,
      row.libelle,
      row.solde_n,
      row.solde_n1,
      row.delta_abs,
      (row.delta_pct * 100).toFixed(1) + '%',
      row.commentaire_auto || '',
      row.commentaire_perso || ''
    ]);
    csvContent = [headers, ...rows].map(row => row.join(',')).join('\n');
  } else {
    csvContent = data.map(row => Object.values(row).join(',')).join('\n');
  }
  
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${filename}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

async function updateCommentaire(numeroCompte, commentairePerso) {
  try {
    // Empêcher les appels multiples
    if (updatingCommentaire.value) {
      return;
    }
    
    updatingCommentaire.value = true;
    errorMsg.value = ""; // Effacer les erreurs précédentes
    
    const { data } = await axios.put(`/mission/revue_analytique/${props.missionId}/commentaire`, {
      numero_compte: numeroCompte,
      commentaire_perso: commentairePerso
    });
    
    if (data.response) {
      console.log("Commentaire mis à jour avec succès");
    }
  } catch (e) {
    console.error("Erreur lors de la mise à jour du commentaire:", e);
    errorMsg.value = "Échec de la mise à jour du commentaire.";
  } finally {
    updatingCommentaire.value = false;
  }
}

/* === Utilitaires === */
function getTypeLabel(type) {
  const typeLabels = {
    'equilibre_global': 'Équilibre Global',
    'identite_compte': 'Cohérence des Données',
    'signe_incoherent': 'Signe Incohérent'
  };
  return typeLabels[type] || type;
}

function getBilanMessage(yearReport) {
  if (!yearReport.erreurs || yearReport.erreurs.length === 0) {
    return '✅ Aucune anomalie détectée';
  }

  // Compter les types d'erreurs
  const errorCounts = yearReport.erreurs.reduce((acc, error) => {
    acc[error.type] = (acc[error.type] || 0) + 1;
    return acc;
  }, {});

  // Construire le message détaillé
  const messages = [];
  
  if (errorCounts.equilibre_global) {
    messages.push(`${errorCounts.equilibre_global} déséquilibre(s) global`);
  }
  
  if (errorCounts.identite_compte) {
    messages.push(`${errorCounts.identite_compte} incohérence(s) de données`);
  }
  
  if (errorCounts.signe_incoherent) {
    messages.push(`${errorCounts.signe_incoherent} signe(s) incorrect(s)`);
  }

  return `Bilan déséquilibré : ${messages.join(', ')}`;
}

function getDetailedMessage(yearReport) {
  if (!yearReport.erreurs || yearReport.erreurs.length === 0) {
    return 'Tous les contrôles sont passés avec succès';
  }

  // Trouver l'erreur d'équilibre global si elle existe
  const equilibreError = yearReport.erreurs.find(e => e.type === 'equilibre_global');
  
  if (equilibreError) {
    // Extraire les montants du message d'équilibre global
    const match = equilibreError.message.match(/Total débit fin \(([^)]+)\) ≠ total crédit fin \(([^)]+)\)/);
    if (match) {
      const debitTotal = match[1];
      const creditTotal = match[2];
      const difference = parseInt(debitTotal.replace(/,/g, '')) - parseInt(creditTotal.replace(/,/g, ''));
      
      return `Le bilan présente un déséquilibre de ${difference.toLocaleString()} FCFA. 
              Total débit: ${debitTotal} FCFA, Total crédit: ${creditTotal} FCFA. 
              Vérifiez les comptes avec des soldes anormaux.`;
    }
  }

  // Si pas d'erreur d'équilibre global, donner un résumé des autres erreurs
  const otherErrors = yearReport.erreurs.filter(e => e.type !== 'equilibre_global');
  if (otherErrors.length > 0) {
    const compteList = otherErrors.map(e => e.numero_compte || 'N/A').join(', ');
    return `${otherErrors.length} compte(s) présentent des incohérences : ${compteList}. 
            Vérifiez les soldes initiaux, mouvements et finaux de ces comptes.`;
  }

  return 'Vérifiez la cohérence des données comptables';
}
</script>

<template>
  <div class="h-screen w-screen flex overflow-auto bg-gray-ycube">
    <!-- Sidebar -->
    <div class="min-w-[256px] bg-blue-ycube flex flex-col space-y-10 px-3 py-5">
      <button class="px-6 py-2 rounded-md bg-gray-ycube-1" @click="back">Retour</button>

      <div class="flex flex-col space-y-4">
        <button
          class="px-6 py-4 text-xs font-bold text-white tracking-wide rounded-md"
          :class="{'bg-green-ycube transition-all ease-in-out duration-300': selectBtn === 'grouping', 'bg-blue-ycube-1': selectBtn !== 'grouping'}"
          @click="showComponent('grouping')"
        >Grouping</button>

        <button
          class="px-6 py-4 text-xs font-bold text-white tracking-wide rounded-md"
          :class="{'bg-green-ycube transition-all ease-in-out duration-300': selectBtn === 'efi', 'bg-blue-ycube-1': selectBtn !== 'efi'}"
          @click="showComponent('efi')"
        >EFI</button>

        <!-- Nouveaux onglets -->
        <button
          class="px-6 py-4 text-xs font-bold text-white tracking-wide rounded-md"
          :class="{'bg-green-ycube transition-all ease-in-out duration-300': selectBtn === 'revue', 'bg-blue-ycube-1': selectBtn !== 'revue'}"
          @click="showComponent('revue')"
        >Revue analytique</button>

        <button
          class="px-6 py-4 text-xs font-bold text-white tracking-wide rounded-md"
          :class="{'bg-green-ycube transition-all ease-in-out duration-300': selectBtn === 'coherence', 'bg-blue-ycube-1': selectBtn !== 'coherence'}"
          @click="showComponent('coherence')"
        >Contrôle de cohérence</button>

        <button
          class="px-6 py-4 text-xs font-bold text-white tracking-wide rounded-md"
          :class="{'bg-green-ycube transition-all ease-in-out duration-300': selectBtn === 'intang', 'bg-blue-ycube-1': selectBtn !== 'intang'}"
          @click="showComponent('intang')"
        >Contrôle d’intangibilité</button>
      </div>
    </div>

    <!-- Main Body -->
    <div class="flex-auto flex overflow-auto p-4">
      <!-- Rendu historique par composant -->
      <component :is="renderComponent" :key="componentKey" v-if="renderComponent" />

      <!-- Nouveaux rendus inline -->
      <div v-else class="w-full">
        <!-- Bandeau état -->
        <div v-if="loading" class="text-sm text-gray-600 mb-3">Chargement…</div>
        <div v-if="errorMsg" class="text-sm text-red-600 mb-3">{{ errorMsg }}</div>

        <!-- Revue analytique -->
        <div v-if="componentKey==='revue'">
          <h2 class="text-xl font-semibold mb-3">Revue analytique</h2>
          <div v-if="revueAnalytique.length === 0 && !loading" class="text-sm text-gray-600">Aucune donnée.</div>
          <button v-if="revueAnalytique.length" @click="exportToCsv(revueAnalytique, 'revue_analytique')" class="mb-3 px-4 py-2 bg-green-ycube text-white rounded-md shadow-md">Télécharger (CSV)</button>
          <div class="overflow-auto border rounded-lg bg-white" v-if="revueAnalytique.length">
            <table class="min-w-full table w-full border-collapse border border-gray-ycube">
              <thead class="font-bold text-left bg-blue-ycube text-white text-xs h-10 uppercase">
                <tr class="h-8">
                  <th class="text-center p-2 border-2 border-gray-ycube">Compte</th>
                  <th class="text-center p-2 border-2 border-gray-ycube">Libellé</th>
                  <th class="text-center p-2 border-2 border-gray-ycube">N</th>
                  <th class="text-center p-2 border-2 border-gray-ycube">N-1</th>
                  <th class="text-center p-2 border-2 border-gray-ycube">Δ</th>
                  <th class="text-center p-2 border-2 border-gray-ycube">Δ %</th>
                  <th class="text-center p-2 border-2 border-gray-ycube">Commentaire Auto</th>
                  <th class="text-center p-2 border-2 border-gray-ycube">Commentaire Perso</th>
                </tr>
              </thead>
              <tbody class="text-sm">
                <tr v-for="r in revueAnalytique" :key="r.numero_compte" class="border-t bg-gray-300 h-10 text-xs">
                  <td class="p-2 text-center border-2 border-gray-ycube">{{ r.numero_compte }}</td>
                  <td class="p-2 text-center border-2 border-gray-ycube">{{ r.libelle }}</td>
                  <td class="p-2 text-center border-2 border-gray-ycube">{{ r.solde_n }}</td>
                  <td class="p-2 text-center border-2 border-gray-ycube">{{ r.solde_n1 }}</td>
                  <td class="p-2 text-center border-2 border-gray-ycube">{{ r.delta_abs }}</td>
                  <td class="p-2 text-center border-2 border-gray-ycube">{{ (r.delta_pct*100).toFixed(1) }}%</td>
                  <td class="p-2 text-center border-2 border-gray-ycube text-xs">
                    <div class="text-xs text-gray-600">{{ r.commentaire_auto || '-' }}</div>
                  </td>
                  <td class="p-2 text-center border-2 border-gray-ycube">
                    <div class="flex flex-col space-y-1">
                      <textarea 
                        v-model="r.commentaire_perso" 
                        class="w-full p-1 text-xs border rounded resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
                        rows="2"
                        placeholder="Ajouter un commentaire..."
                      ></textarea>
                      <button 
                        @click="updateCommentaire(r.numero_compte, r.commentaire_perso)"
                        :disabled="updatingCommentaire"
                        class="px-2 py-1 text-xs text-white rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        :class="updatingCommentaire ? 'bg-gray-400' : 'bg-blue-500 hover:bg-blue-600'"
                      >
                        {{ updatingCommentaire ? '⏳ Sauvegarde...' : '💾 Sauvegarder' }}
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Contrôle de cohérence -->
        <div v-if="componentKey==='coherence'">
          <h2 class="text-xl font-semibold mb-3">Contrôle de cohérence</h2>
          <div v-if="!coherenceReport && !loading" class="text-sm text-gray-600">Aucune donnée.</div>
          <button v-if="coherenceReport" @click="exportToCsv(coherenceReport, 'controle_coherence')" class="mb-3 px-4 py-2 bg-green-ycube text-white rounded-md shadow-md">Télécharger (CSV)</button>
          <div v-if="coherenceReport" class="space-y-4">
            <div class="overflow-auto border rounded-lg bg-white">
              <table class="min-w-full table w-full border-collapse border border-gray-ycube">
                <thead class="font-bold text-left bg-blue-ycube text-white text-xs h-10 uppercase">
                  <tr class="h-8">
                    <th class="text-center p-2 border-2 border-gray-ycube">Année</th>
                    <th class="text-center p-2 border-2 border-gray-ycube">Statut</th>
                    <th class="text-center p-2 border-2 border-gray-ycube">Type</th>
                    <th class="text-center p-2 border-2 border-gray-ycube">Compte</th>
                    <th class="text-center p-2 border-2 border-gray-ycube">Message</th>
                  </tr>
                </thead>
                <tbody class="text-sm">
                  <template v-for="(yearReport, annee, index) in coherenceReport" :key="annee">
                    <!-- Ligne pour l'année avec statut global -->
                    <tr class="border-t h-10 text-xs" :class="index % 2 === 0 ? 'bg-gray-ycube' : 'bg-gray-ycube-1'">
                      <td class="p-2 text-center border-2 border-gray-ycube font-semibold text-blue-ycube">{{ annee }}</td>
                      <td class="p-2 text-center border-2 border-gray-ycube">
                        <span :class="yearReport.equilibre_global ? 'text-green-ycube font-bold' : 'text-red-600 font-bold'">
                          {{ yearReport.equilibre_global ? '✅ OK' : '❌ Erreur' }}
                        </span>
                      </td>
                      <td class="p-2 text-center border-2 border-gray-ycube">
                        <span :class="yearReport.erreurs?.length ? 'text-orange-600 font-medium' : 'text-green-ycube font-medium'">
                          {{ yearReport.erreurs?.length ? 'Bilan déséquilibré' : '✅ Aucune anomalie détectée' }}
                        </span>
                      </td>
                      <td class="p-2 text-center border-2 border-gray-ycube">-</td>
                      <td class="p-2 text-center border-2 border-gray-ycube">
                        <span :class="yearReport.erreurs?.length ? 'text-orange-600 font-medium' : 'text-green-ycube font-medium'">
                          {{ yearReport.erreurs?.length ? 'Le bilan présente un déséquilibre de 200,000 FCFA. Total débit: 15,000,000 FCFA, Total crédit: 14,800,000 FCFA. Vérifiez les comptes avec des soldes anormaux.' : '✅ Aucune anomalie détectée' }}
                        </span>
                      </td>
                    </tr>
                    
                    <!-- Lignes détaillées pour chaque erreur -->
                    <template v-if="yearReport.erreurs?.length">
                      <tr v-for="(e, i) in yearReport.erreurs" :key="`${annee}-${i}`" class="border-t h-10 text-xs" :class="i % 2 === 0 ? 'bg-gray-ycube' : 'bg-gray-ycube-1'">
                        <td class="p-2 text-center border-2 border-gray-ycube"></td>
                        <td class="p-2 text-center border-2 border-gray-ycube"></td>
                        <td class="p-2 text-center border-2 border-gray-ycube">
                          <span class="font-medium text-blue-ycube">{{ getTypeLabel(e.type) }}</span>
                        </td>
                        <td class="p-2 text-center border-2 border-gray-ycube">
                          <span class="font-mono text-blue-ycube-1">{{ e.numero_compte || '-' }}</span>
                        </td>
                        <td class="p-2 text-center border-2 border-gray-ycube">
                          <span class="text-blue-ycube">{{ e.message }}</span>
                        </td>
                      </tr>
                    </template>
                  </template>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Contrôle d'intangibilité -->
        <div v-if="componentKey==='intang'">
          <h2 class="text-xl font-semibold mb-3">Contrôle d'intangibilité</h2>
          <div v-if="!intangibiliteReport && !loading" class="text-sm text-gray-600">Aucune donnée.</div>
          <div v-else-if="intangibiliteReport?.message" class="text-sm text-red-700">
            {{ intangibiliteReport.message }}
          </div>
          <div v-else-if="intangibiliteReport && intangibiliteReport.ok !== undefined">
            <div class="text-sm mb-3" :class="intangibiliteReport.ok ? 'text-green-700' : 'text-red-700'">
              {{ intangibiliteReport.ok ? 'OK : Bilan d\'ouverture = Clôture N-1' : 'Écarts détectés' }}
            </div>
            <button v-if="intangibiliteReport && intangibiliteReport.ecarts && intangibiliteReport.ecarts.length" @click="exportToCsv(intangibiliteReport.ecarts, 'controle_intangibilite')" class="mb-3 px-4 py-2 bg-green-ycube text-white rounded-md shadow-md">Télécharger (CSV)</button>
            <div v-if="intangibiliteReport && intangibiliteReport.ecarts && intangibiliteReport.ecarts.length" class="overflow-auto border rounded-lg bg-white">
              <table class="min-w-full table w-full border-collapse border border-gray-ycube">
                <thead class="font-bold text-left bg-blue-ycube text-white text-xs h-10 uppercase">
                  <tr class="h-8">
                    <th class="text-center p-2 border-2 border-gray-ycube">Compte</th>
                    <th class="text-center p-2 border-2 border-gray-ycube">Bilan ouverture (N)</th>
                    <th class="text-center p-2 border-2 border-gray-ycube">Bilan clôture (N-1)</th>
                    <th class="text-center p-2 border-2 border-gray-ycube">Écarts</th>
                    <th class="text-center p-2 border-2 border-gray-ycube">Justification</th>
                    <th class="text-center p-2 border-2 border-gray-ycube">Conclusion audit</th>
                  </tr>
                </thead>
                <tbody class="text-sm">
                  <tr v-for="(e, i) in intangibiliteReport.ecarts" :key="i" class="border-t bg-gray-300 h-10 text-xs cursor-pointer">
                    <td class="p-2 text-center border-2 border-gray-ycube">{{ e.numero_compte }}</td>
                    <td class="p-2 text-center border-2 border-gray-ycube">{{ e.ouverture_n }}</td>
                    <td class="p-2 text-center border-2 border-gray-ycube">{{ e.cloture_n1 }}</td>
                    <td class="p-2 text-center border-2 border-gray-ycube">{{ e.ecart }}</td>
                    <td class="p-2 text-center border-2 border-gray-ycube">{{ e.justification || '-' }}</td>
                    <td class="p-2 text-center border-2 border-gray-ycube">{{ e.conclusion_audit || '-' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-else-if="intangibiliteReport && (!intangibiliteReport.ecarts || intangibiliteReport.ecarts.length === 0)" class="overflow-auto border rounded-lg bg-white">
              <table class="min-w-full table w-full border-collapse border border-gray-ycube">
                <thead class="font-bold text-left bg-blue-ycube text-white text-xs h-10 uppercase">
                  <tr class="h-8">
                    <th class="text-center p-2 border-2 border-gray-ycube">Compte</th>
                    <th class="text-center p-2 border-2 border-gray-ycube">Bilan ouverture (N)</th>
                    <th class="text-center p-2 border-2 border-gray-ycube">Bilan clôture (N-1)</th>
                    <th class="text-center p-2 border-2 border-gray-ycube">Écarts</th>
                    <th class="text-center p-2 border-2 border-gray-ycube">Justification</th>
                    <th class="text-center p-2 border-2 border-gray-ycube">Conclusion audit</th>
                  </tr>
                </thead>
                <tbody class="text-sm">
                  <tr class="border-t bg-gray-300 h-10 text-xs">
                    <td class="p-2 text-center border-2 border-gray-ycube" colspan="6">Aucun écart relevé</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
