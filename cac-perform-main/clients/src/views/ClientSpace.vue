<script setup>
import { ref, inject, onMounted } from 'vue';
import router from "@/router";
const axios = inject('axios');

const infos = ref({})
const missions = ref([])
const props = defineProps(['clientId'])

onMounted(async() => {
    const response = (await axios.get(`/client/info_client/${props.clientId}`)).data.response
    console.log(response)
    infos.value = response.info
    missions.value = response.missions
})

async function newMission() {
    router.push(`/newMission/${props.clientId}`)
}

async function updateClient() {

}

function seeMore(missionId) {
    router.push(`/grouping-analyse/${missionId}`)
}

function back() {
    router.push(`/`)
}
</script>

<template>
  <div class="h-screen w-screen flex flex-col overflow-auto bg-gray-ycube">
    <!-- En-tête contenant les boutons et les infos du client -->
    <div class="bg-green-ycube-1 flex flex-col">
        <div class="flex justify-between items-center px-4 py-2">
            <button class="px-6 py-2 rounded-md bg-gray-ycube-1" @click="back">Retour</button>
            <div class="flex space-x-2">
                <button class="py-2 w-[200px] rounded-md bg-blue-ycube font-semibold text-white shadow-lg" @click="newMission">Nouvelle mission</button>
                <button class="py-2 w-[200px] rounded-md bg-blue-ycube font-semibold text-white shadow-lg" @click="updateClient">Modifier client</button>
            </div>
        </div>
        <div class="flex-auto flex px-4 py-2 justify-between items-center">
            <ul class="space-y-2">
                <li class="text-blue-ycube">Client : <span class="font-bold">{{ infos.nom }}</span></li>
                <li class="text-blue-ycube">Activité : <span class="font-bold">{{ infos.activite }}</span></li>
                <li class="text-blue-ycube">Adresse : <span class="font-bold">{{ infos.adresse }}</span></li>
                <li class="text-blue-ycube">Siège social : <span class="font-bold">{{ infos.siege_social }}</span></li>
            </ul>

            <ul class="space-y-2">
                <li class="text-blue-ycube">Forme juridique : <span class="font-bold">{{ infos.forme_juridique }}</span></li>
                <li class="text-blue-ycube">N°CC : <span class="font-bold">{{ infos.n_cc }}</span></li>
                <li class="text-blue-ycube">Capital : <span class="font-bold">{{ infos.capital }}</span></li>
                <li class="text-blue-ycube">Référentiel comptable : <span class="font-bold">{{ infos.referentiel }}</span></li>
            </ul>
        </div>
    </div>

    <!-- Tableau des missions -->
    <div class="flex-auto flex flex-col mx-4 overflow-auto">
        <h3 class="pt-5 pb-1 pl-0 text-2xl font-semibold uppercase tracking-wider">Tableau des missions</h3>
        <div class="flex w-full overflow-auto mb-5">
          <table class="table w-full border-collapse border border-gray-ycube">
            <thead class="font-bold text-left text-xs bg-blue-ycube text-white h-10">
              <tr>
                <th class="w-2 border-2 border-gray-ycube pl-2">#</th>
                <th class="w-1/5 border-2 border-gray-ycube pl-2">Année auditée</th>
                <th class="w-1/5 border-2 border-gray-ycube pl-2">Date de début</th>
                <th class="w-1/5 border-2 border-gray-ycube pl-2">Date de fin</th>
                <th class="w-1/5 border-2 border-gray-ycube pl-2">Afficher détails</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="mission, index in missions" :key="index" class="bg-gray-300 h-12 cursor-pointer text-xs select-none">
                <td class="w-10 border-2 border-gray-ycube pl-2">{{ index + 1 }}</td>
                <td class="w-1/5 border-2 border-gray-ycube pl-2">{{ mission.annee_auditee }}</td>
                <td class="w-1/5 border-2 border-gray-ycube pl-2">{{ mission.date_debut }}</td>
                <td class="w-1/5 border-2 border-gray-ycube pl-2">{{ mission.date_fin }}</td>
                <td class="w-1/5 border-2 border-gray-ycube pl-2 text-center">
                    <button class="py-2 px-8 bg-blue-ycube rounded-md text-xs font-semibold text-white" @click="seeMore(mission._id)">Voir</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
  </div>
</template>
