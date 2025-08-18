<script setup>
import { ref, inject, onMounted } from 'vue';
import router from "@/router";
const axios = inject('axios');
const listClients = ref([])

onMounted(async() => {
  try {
    listClients.value = (await axios.get('/client/afficher_clients/')).data.response
  } catch (error) {
    console.error(error)
  }
})

function redirectClientSpace(id) {
  router.push(`/client/${id}`)
}

function newClient() {
  router.push(`/newClient`)
}
</script>

<template>
  <div class="w-screen h-screen bg-white flex overflow-auto">
    <!-- Sidebar -->
    <div class="w-1/5 bg-blue-ycube flex flex-col">
      <img src="../assets/logo.png" alt="logo ycube">
      <div class="flex justify-center mt-10">
        <button class="uppercase font-bold bg-green-ycube text-gray-ycube px-12 py-3 rounded-md" @click="newClient">Nouveau client</button>
      </div>
    </div>
    
    <!-- Main Body -->
    <div class="flex-auto bg-gray-ycube flex flex-col overflow-auto">
      <!-- Search bar -->
      <div class="bg-green-ycube h-16 flex items-center justify-end pr-5">
        <div class="search">
          <input type="search" placeholder="Rechercher un client..." class="w-[250px] pl-3 rounded-md placeholder:text-xs border-2 focus:outline-none focus:ring-0">
        </div>
      </div>

      <!-- Tableau des clients -->
      <div class="flex-auto flex flex-col mx-4 overflow-auto">
        <h3 class="pt-5 pb-1 pl-0 text-2xl font-semibold uppercase tracking-wider">Tableau des clients CAC</h3>
        <div class="flex w-full overflow-auto mb-5">
          <table class="table w-full border-collapse border border-gray-ycube">
            <thead class="font-bold text-left bg-blue-ycube text-white h-10">
              <tr>
                <th class="w-10 border-2 border-gray-ycube pl-2">#</th>
                <th class="w-1/5 border-2 border-gray-ycube pl-2">Client</th>
                <th class="w-1/5 border-2 border-gray-ycube pl-2">Activité</th>
                <th class="w-1/5 border-2 border-gray-ycube pl-2">Adresse</th>
                <th class="w-1/5 border-2 border-gray-ycube pl-2">Référentiel comptable</th>
                <th class="w-1/5 border-2 border-gray-ycube pl-2">Date dernière mission</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="client, index in listClients" :key="index" class="bg-gray-300 h-10 cursor-pointer" @click="redirectClientSpace(client._id)">
                <td class="w-10 border-2 border-gray-ycube pl-2">{{ index + 1 }}</td>
                <td class="w-1/5 border-2 border-gray-ycube pl-2">{{ client.nom }}</td>
                <td class="w-1/5 border-2 border-gray-ycube pl-2">{{ client.activite }}</td>
                <td class="w-1/5 border-2 border-gray-ycube pl-2">{{ client.adresse }}</td>
                <td class="w-1/5 border-2 border-gray-ycube pl-2">{{ client.referentiel }}</td>
                <td class="w-1/5 border-2 border-gray-ycube pl-2">{{ client.date_mission }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
