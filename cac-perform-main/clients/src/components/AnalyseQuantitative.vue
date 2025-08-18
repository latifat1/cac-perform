<script setup>
import { ref, onMounted, inject, watch } from 'vue';

import { useNotyf } from '@/composables/useNotyf';
const axios = inject('axios')
const notyf = useNotyf()
const FACTOR_PERFORMANCE_MATERIALITY = 0.08
const FACTOR_THRESHOLD = 0.05

const listBenchmark = ref([
    {
        id: "ebitda",
        name: "EBITDA",
        balance_value: null,
        factor: null,
        amount_based_on_factor: null,
        performance_materiality: null,
        thresold: null,
        text: "Fourchette de facteur attendue : 3-5 % (peut aller jusqu'à 5 % compte tenu de la taille de l'entité). Consultez le guide de matérialité pour plus de détails.)"

    },
    {
        id: "expenses",
        name: "Expenses",
        balance_value: null,
        factor: null,
        amount_based_on_factor: null,
        performance_materiality: null,
        thresold: null,
        text: "Fourchette de facteur attendue : 3-5 % (peut aller jusqu'à 5 % compte tenu de la taille de l'entité). Consultez le guide de matérialité pour plus de détails."

    },
    {
        id: "profit_before_tax",
        name: "Profit Before Tax",
        balance_value: null,
        factor: null,
        amount_based_on_factor: null,
        performance_materiality: null,
        thresold: null,
        text: "Fourchette de facteur attendue : 5-10%. Voir le guide de matérialité pour plus de détails."

    },
    {
        id: "revenue",
        name: "Revenue",
        balance_value: null,
        factor: null,
        amount_based_on_factor: null,
        performance_materiality: null,
        thresold: null,
        text: "Fourchette de facteur attendue : 0,8-2 % (peut aller jusqu'à 5 % compte tenu de la taille de l'entité). Consultez le guide de matérialité pour plus de détails."

    },
    {
        id: "total_assets",
        name: "Total Assets",
        balance_value: null,
        factor: null,
        amount_based_on_factor: null,
        performance_materiality: null,
        thresold: null,
        text: "Fourchette de facteur attendue : 1-2%. Consultez le guide de matérialité pour plus de détails."

    }
])
const listMaterialities = ref([])

// Une variable qui est utilisé pour maj la liste des seuils de signification quand on enregistre un nouveau
const isValidate = ref(1)

const selectedBench = ref("")
const bench = ref({
    id: "",
    balanceValue: "",
    factor: "",
    amount_based_on_factor: null,
    performance_materiality: null,
    thresold: null,
    text: ""
})

// Recuperer l'id mission dans l'URL
const id_mission = window.location.pathname.split('/')[2]

onMounted(async() =>{
    const result = (await axios.get(`/mission/get_benchmarks/${id_mission}`)).data.response
    
    await getListMaterialities()

    const _keys = Object.keys(result)
    // Remplis la variable listBenchmark avec les benchmarks issus en adressant correctement via la clé id
    listBenchmark.value.forEach(obj => {
        if (_keys.includes(obj.id)) {
            obj.balance_value = result[obj.id]
        }
    })
    console.log(listBenchmark.value)
})

watch(selectedBench, (newValue)=>{
    bench.value.id = newValue
    listBenchmark.value.map(obj => {
        if (obj.id === newValue) {
            bench.value.balanceValue = obj.balance_value
            bench.value.text = obj.text
        }
    })
})

watch(isValidate, async(newValue)=> {
    console.log(newValue)
    await getListMaterialities()
})

async function getListMaterialities() {
    const materialities = (await axios.get(`/mission/get_materiality/${id_mission}`)).data.response.materiality
    console.log(materialities)
    listMaterialities.value = materialities
}

// Calculer les valeurs dépendants du facteur saisi
function updateSelectBenchmark() {
    const factor = parseFloat(bench.value.factor)
    bench.value.amount_based_on_factor = Math.round((bench.value.balanceValue * factor) / 100)
    bench.value.performance_materiality = Math.round(bench.value.amount_based_on_factor * FACTOR_PERFORMANCE_MATERIALITY)
    bench.value.thresold = Math.round(bench.value.amount_based_on_factor * FACTOR_THRESHOLD)
}

// Calculer seuil de signification et enregistrer dans la BD
async function validerSeuil() {
    updateSelectBenchmark()

    const field = {
        benchmark: bench.value.id,
        materiality : bench.value.amount_based_on_factor,
        performance_materiality : bench.value.performance_materiality,
        trivial_misstatements: bench.value.thresold,
        factor: bench.value.factor
    }
    const result = (await axios.put(`/mission/save_materiality/${id_mission}`, field)).data.response
    console.log(result)
    if (result === 1) {
        notyf.trigger('Seuil enregsitré avec succès', 'success')
        isValidate.value = isValidate.value + 1
    } else {
        notyf.trigger('Veuillez réessayer', 'error')
    }
}

async function applySeuil(benchmark) {
    const field = {
        "benchmark": benchmark
    }
    const response = await axios.put(`/mission/validate_materiality/${id_mission}`, field)
    if (response.data['response'] === 1) {
        const res = await axios.put(`/mission/quantitative_analysis/${id_mission}`)
        notyf.trigger("Seuil appliqué au grouping avec succès", "success")
        console.log(res.data['response'])
    } else {
        // Ajouter une notification pour dire que ce n'est pas possible
        notyf.trigger("Echec d'application du seuil au grouping", "error")
    }
}
</script>

<template>
    <!-- Liste des seuils de signification -->
    <div class="flex flex-col overflow-auto">
        <h3 class="pt-3 pb-1 pl-0 text-xl font-bold uppercase tracking-wider flex space-x-2 items-center">
            <span>Détermination du seuil de signification</span>
        </h3>
        <div class="overflow-auto flex flex-col space-y-4">
            <!-- <component :is="renderComponent" :key="componentKey" /> -->

            <!-- Calcul du seuil de signification -->
            <div class="mx-auto w-[95%] h-[180px] flex flex-col px-6 pb-6 bg-gray-300 rounded-md">
                <h3 class="pt-3 pb-1 pl-0 text-base font-semibold uppercase tracking-wider">Calcul du seuil</h3>
                <div class="flex space-x-2">
                    <div class="w-[30%]">
                        <label for="" class="font-bold uppercase text-xs">Choisir benchmark</label>
                        <select v-model="selectedBench" name="" id="" class="px-2 border-2 border-blue-ycube w-full h-8">
                            <option value="" disabled>Aucun benchmark choisi</option>
                            <option v-for="bench, index in listBenchmark" :key="index" :value="bench.id">{{ bench.name }}</option>
                        </select>
                        <!-- <div v-if="selectedBench.balance_value" class="px-2 border-2 border-blue-ycube w-full h-8">{{ selectedBench.balance_value }}</div>
                        <div v-else class="px-2 border-2 border-blue-ycube w-full italic h-8">Aucune benchmark choisi</div> -->
                    </div>
                    <div class="w-[30%]">
                        <label for="" class="font-bold uppercase text-xs">Benchmark Balance</label>
                        <div v-if="bench.id" class="px-2 border-2 border-blue-ycube w-full h-8">{{ bench.balanceValue }}</div>
                        <div v-else class="px-2 border-2 border-blue-ycube w-full italic h-8">Aucun benchmark choisi</div>
                    </div>

                    <div class="w-[30%]">
                        <label for="">Facteur</label>
                        <input v-model="bench.factor" class="px-2 border-2 border-blue-ycube w-full h-8 placeholder:italic" type="text" placeholder="Saisir facteur...">
                        <div v-if="bench.id" class="mt-2 text-xs italic"><i class="mdi mdi-information font-bold text-base"></i> {{ bench.text }}</div>
                        <!-- <button @click="console.log(selectedBench)">Test</button> -->
                    </div>
                    <div class="w-[10%]">
                        <button class="mt-6 py-2 px-8 bg-blue-ycube rounded-md text-xs font-semibold text-white" @click="validerSeuil">Valider</button>
                    </div>
                </div>
            </div>

            <!-- Liste des seuils de signification calculés -->
            <div class="flex flex-col overflow-auto">
                <h3 class="pt-3 pb-1 pl-0 text-base font-semibold uppercase tracking-wider">Liste des seuils de signification</h3>
                <div class="flex w-full overflow-auto">
                    <table class="table w-full border-collapse border border-gray-ycube">
                        <thead class="font-bold text-left bg-blue-ycube text-white text-xs h-10">
                            <tr>
                                <th class="w-[3%] border-2 border-gray-ycube pl-2">#</th>
                                <th class="w-[15%] border-2 border-gray-ycube pl-2">Benchmark</th>
                                <th class="w-[15%] border-2 border-gray-ycube pl-2">Facteur</th>
                                <th class="w-[15%] border-2 border-gray-ycube pl-2">Seuil de matérialité</th>
                                <th class="w-[15%] border-2 border-gray-ycube pl-2">Performance de matérialité</th>
                                <th class="w-[15%] border-2 border-gray-ycube pl-2">Seuil pour les inexactitudes manifestement insignifiantes</th>
                                <th class="w-[17%] border-2 border-gray-ycube pl-2">Appliquer au grouping</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="mat, index in listMaterialities" :key="index" class="bg-gray-300 h-12 text-base select-none">
                                <td class="w-[3%] border-2 border-gray-ycube  pl-2">{{ index + 1 }}</td>
                                <td class="w-[15%] border-2 border-gray-ycube pl-2">{{ mat.benchmark }}</td>
                                <td class="w-[15%] border-2 border-gray-ycube pl-2">{{ mat.factor }}</td>
                                <td class="w-[15%] border-2 border-gray-ycube pl-2">{{ mat.materiality }}</td>
                                <td class="w-[15%] border-2 border-gray-ycube pl-2">{{ mat.performance_materiality }}</td>
                                <td class="w-[15%] border-2 border-gray-ycube pl-2">{{ mat.trivial_misstatements }}</td>
                                <td class="w-[17%] border-2 border-gray-ycube pl-2 text-center">
                                    <button class="py-2 px-8 bg-blue-ycube rounded-md text-xs font-semibold text-white" @click="applySeuil(mat.benchmark)">Appliquer</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>
