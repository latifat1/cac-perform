<script setup>
import { ref, inject, onMounted } from 'vue';
const props = defineProps(['grouping', 'annee_auditee'])
const axios = inject('axios')

const isSignificant = ref(false);
const groupings = ref([])
// Recuperer l'id mission dans l'URL
const id_mission = window.location.pathname.split('/')[2]

onMounted(async()=>{
    groupings.value = props.grouping;
    await showSignificantGrouping();
})

async function showSignificantGrouping() {
    const result = await axios.get(`/mission/make_final/${id_mission}`)
    console.log(result)
    const verifyResult = result.data.grouping[0]
    if (verifyResult.mat_sign) {
        isSignificant.value = true
        groupings.value = result.data.grouping

    }
}
</script>

<template>
    <!-- Tableau grouping principal -->
    <h3 class="pt-5 pb-1 pl-0 text-xl font-semibold uppercase tracking-wider">Tableau des clients CAC</h3>
    <div class="flex w-full overflow-auto">
        <table class="table w-full border-collapse border border-gray-ycube">
            <thead class="font-bold text-left bg-blue-ycube text-white text-xs h-10">
                <tr>
                    <th class="border-2 border-gray-ycube pl-2" :class="{'w-[3%]': isSignificant, 'w-[3%]': !isSignificant}">#</th>
                    <th class="border-2 border-gray-ycube pl-2" :class="{'w-[20%]': isSignificant, 'w-[37%]': !isSignificant}">Intitulé</th>
                    <th class="border-2 border-gray-ycube pl-2" :class="{'w-[10%]': isSignificant, 'w-[15%]': !isSignificant}">{{ props.annee_auditee }}</th>
                    <th class="border-2 border-gray-ycube pl-2" :class="{'w-[10%]': isSignificant, 'w-[15%]': !isSignificant}">{{ parseInt(props.annee_auditee) - 1 }}</th>
                    <th class="border-2 border-gray-ycube pl-2" :class="{'w-[10%]': isSignificant, 'w-[15%]': !isSignificant}">Variation</th>
                    <th class="border-2 border-gray-ycube pl-2" :class="{'w-[10%]': isSignificant, 'w-[15%]': !isSignificant}">Variation en %</th>

                    <th v-if="isSignificant" class="border-2 border-gray-ycube pl-2" :class="{'w-[11%]': isSignificant}">Compte quantitatif ?</th>
                    <th v-if="isSignificant" class="border-2 border-gray-ycube pl-2" :class="{'w-[11%]': isSignificant}">Compte qualitatif ?</th>
                    <th v-if="isSignificant" class="border-2 border-gray-ycube pl-2" :class="{'w-[18%]': isSignificant}">Significativié du grouping</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="data,index in groupings" :key="index" class="bg-gray-300 h-10 text-xs cursor-pointer" @click="redirectClientSpace(client._id)">
                    <td class="border-2 border-gray-ycube pl-2" :class="{'w-[3%]': isSignificant, 'w-[3%]': !isSignificant}">{{ data.compte }}</td>
                    <td class="border-2 border-gray-ycube pl-2" :class="{'w-[20%]': isSignificant, 'w-[37%]': !isSignificant}">{{ data.libelle }}</td>
                    <td class="border-2 border-gray-ycube pl-2" :class="{'w-[10%]': isSignificant, 'w-[15%]': !isSignificant}">{{ data.solde_n }}</td>
                    <td class="border-2 border-gray-ycube pl-2" :class="{'w-[10%]': isSignificant, 'w-[15%]': !isSignificant}">{{ data.solde_n1 }}</td>
                    <td class="border-2 border-gray-ycube pl-2" :class="{'w-[10%]': isSignificant, 'w-[15%]': !isSignificant}">{{ data.variation }}</td>
                    <td class="border-2 border-gray-ycube pl-2" :class="{'w-[10%]': isSignificant, 'w-[15%]': !isSignificant}">{{ Number.isInteger(data.variation_percent) ? data.variation_percent : data.variation_percent.toFixed(2) }}</td>

                    <td v-if="isSignificant" class="border-2 border-gray-ycube pl-2" :class="{'w-[11%]': isSignificant}">{{ data.materiality }}</td>
                    <td v-if="isSignificant" class="border-2 border-gray-ycube pl-2" :class="{'w-[11%]': isSignificant}">{{ data.significant }}</td>
                    <td v-if="isSignificant" class="border-2 border-gray-ycube pl-2" :class="{'w-[18%]': isSignificant}">{{ data.mat_sign }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
