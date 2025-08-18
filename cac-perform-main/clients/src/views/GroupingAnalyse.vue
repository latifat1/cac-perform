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

onMounted(async () => {
  const result = (await axios.get(`/mission/affichage_infos_mission/${props.missionId}`)).data.response;
  infoMission.value = result;
});

/* === Loaders API === */
async function loadRevueAnalytique() {
  loading.value = true; errorMsg.value = "";
  try {
    const { data } = await axios.get(`/mission/revue_analytique/${props.missionId}`);
    revueAnalytique.value = data.response || [];
  } catch (e) {
    errorMsg.value = "Échec du chargement de la revue analytique.";
    console.error(e);
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

  if (type === "revue") loadRevueAnalytique();
  else if (type === "coherence") loadCoherence();
  else if (type === "intang") loadIntangibilite();
}

function back() {
  router.go(-1);
}

function exportToCsv(data, filename) {
  const csvContent = data.map(row => Object.values(row).join(',')).join('\n');
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
                  <th class="text-center p-2 border-2 border-gray-ycube">Commentaire</th>
                </tr>
              </thead>
              <tbody class="text-sm">
                <tr v-for="r in revueAnalytique" :key="r.numero_compte" class="border-t bg-gray-300 h-10 text-xs cursor-pointer">
                  <td class="p-2 text-center border-2 border-gray-ycube">{{ r.numero_compte }}</td>
                  <td class="p-2 text-center border-2 border-gray-ycube">{{ r.libelle }}</td>
                  <td class="p-2 text-center border-2 border-gray-ycube">{{ r.solde_n }}</td>
                  <td class="p-2 text-center border-2 border-gray-ycube">{{ r.solde_n1 }}</td>
                  <td class="p-2 text-center border-2 border-gray-ycube">{{ r.delta_abs }}</td>
                  <td class="p-2 text-center border-2 border-gray-ycube">{{ (r.delta_pct*100).toFixed(1) }}%</td>
                  <td class="p-2 text-center border-2 border-gray-ycube">{{ r.commentaire || '-' }}</td>
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
                    <th class="text-center p-2 border-2 border-gray-ycube">Balance</th>
                    <th class="text-center p-2 border-2 border-gray-ycube">Statut</th>
                    <th class="text-center p-2 border-2 border-gray-ycube">Type</th>
                    <th class="text-center p-2 border-2 border-gray-ycube">Compte</th>
                    <th class="text-center p-2 border-2 border-gray-ycube">Message</th>
                  </tr>
                </thead>
                <tbody class="text-sm">
                  <tr v-for="(yearReport, idx) in coherenceReport" :key="idx" class="border-t bg-gray-300 h-10 text-xs">
                    <td class="p-2 text-center border-2 border-gray-ycube" :rowspan="(yearReport.erreurs?.length || 0) + 1">{{ idx }}</td>
                    <td class="p-2 text-center border-2 border-gray-ycube" :rowspan="(yearReport.erreurs?.length || 0) + 1">
                      <span :class="yearReport.equilibre_global ? 'text-green-700' : 'text-red-700'">
                        {{ yearReport.equilibre_global ? 'OK' : 'Erreur' }}
                      </span>
                    </td>
                    <template v-if="yearReport.erreurs?.length">
                      <tr v-for="(e, i) in yearReport.erreurs" :key="`${idx}-${i}`" class="border-t bg-gray-300 h-10 text-xs">
                        <td class="p-2 text-center border-2 border-gray-ycube">{{ e.type }}</td>
                        <td class="p-2 text-center border-2 border-gray-ycube">{{ e.numero_compte || '-' }}</td>
                        <td class="p-2 text-center border-2 border-gray-ycube">{{ e.message }}</td>
                      </tr>
                    </template>
                    <template v-else>
                      <td class="p-2 text-center border-2 border-gray-ycube" colspan="3">Aucune anomalie détectée</td>
                    </template>
                  </tr>
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
          <div v-else>
            <div class="text-sm mb-3" :class="intangibiliteReport.ok ? 'text-green-700' : 'text-red-700'">
              {{ intangibiliteReport.ok ? 'OK : Bilan d\'ouverture = Clôture N-1' : 'Écarts détectés' }}
            </div>
            <button v-if="intangibiliteReport.ecarts?.length" @click="exportToCsv(intangibiliteReport.ecarts, 'controle_intangibilite')" class="mb-3 px-4 py-2 bg-green-ycube text-white rounded-md shadow-md">Télécharger (CSV)</button>
            <div v-if="intangibiliteReport.ecarts?.length" class="overflow-auto border rounded-lg bg-white">
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
            <div v-else class="overflow-auto border rounded-lg bg-white">
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
