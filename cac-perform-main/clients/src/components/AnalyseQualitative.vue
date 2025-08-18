<script setup>
import { ref, inject } from 'vue';
import { useNotyf } from '@/composables/useNotyf';
const axios = inject('axios')
const notyf = useNotyf();
const props = defineProps(['grouping'])

const questions = ref([
    "Volume d'activité, complexité et homogénéité des transactions enregistrées, existence de transactions significatives inhabituelles ou anormales dans le COTABD",
    "Changements identifiés dans le COTABD et détermination si un ou de nouveaux risque(s) sont apparus du fait de changement au sein de l'entité ou de son environnement (économique, légal, réglementaire, normatif ou méthodes comptables)",
    "Sensibilité de l'entité aux anomalies issues de fraudes (Si oui, le risque est obligatoirement Significant)",
    "Niveau de complexité des normes, règles, méthodes comptables, notes annexes, estimations ou jugements liées aux comptes ou aux notes annexes",
    "Exposition du COTABD à des pertes (charges ou dépréciations)",
    "Probabilité que des passifs éventuels significatifs (procès, contentieux, litiges etc…) puissent être issus des transactions enregistrées dans le COTABD",
    "Existence de transactions avec des parties liées dans le COTABD"
])

const listQuestions = ref([])

// Recuperer l'id mission dans l'URL
const id_mission = window.location.pathname.split('/')[2]

function handleQuestion(compte, indexRow, indexCol, checked) {
    const field = {
        "compte" : compte,
        "significant" : checked,
        // "indexRow" : indexRow,
        "question" : indexCol + 1
    }
    // listQuestions.value.push(field)
    uniqueValue(field)
}

function uniqueValue(group) {
    if (listQuestions.value.length === 0) {
        listQuestions.value.push(group)
    } else {
        // Vérifier si group existe déjà dans la liste
        const existingIndex = listQuestions.value.findIndex(item => item.compte === group.compte && item.question === group.question)

        if (existingIndex !== -1) {
            listQuestions.value[existingIndex] = group
        } else {
            listQuestions.value.push(group)
        }
    }
}

async function validate() {
    const field = {
        "listGrouping" : listQuestions.value
    }
    const result = (await axios.put(`http://localhost:5000/cors/mission/qualitative_analysis/${id_mission}`, field)).data.response
    console.log(result)

    if (result === 1) {
        notyf.trigger('Enregistré avec succès', 'success')
    }
    console.log(listQuestions.value)
}
</script>

<template>
    <!-- Tableau grouping principal -->
    <div class="flex flex-col overflow-auto">
        <h3 class="pt-3 pb-1 pl-0 text-xl font-semibold uppercase tracking-wider">Questionnaire pour déterminer les comptes significatifs</h3>
        <div class="flex w-full overflow-auto">
            <table class="table w-full border-collapse border border-gray-ycube">
                <thead class="font-bold text-left bg-blue-ycube text-white text-[9px] h-10">
                    <tr>
                        <th class="w-10 border-2 border-gray-ycube text-base pl-2">#</th>
                        <th class="border-2 border-gray-ycube pl-2" v-for="q, index in questions" :key="index">{{ q }}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="group, indexRow in props.grouping" :key="indexRow" class="bg-gray-300 h-12 text-[9xl]">
                        <td class="w-10 border-2 border-gray-ycube text-[10px] pl-2">{{ group.compte }}</td>
                        <td class="border-2 border-gray-ycube pl-2" v-for="q, indexCol in questions" :key="indexCol">
                            <label :for="'check'+indexRow.toString()+indexCol.toString()" class="w-full h-12 flex items-center">
                                <input :id="'check'+indexRow.toString()+indexCol.toString()" class="w-5 h-5" type="checkbox" @change="(e) => handleQuestion(group.compte, indexRow, indexCol, e.target.checked)">
                            </label>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <button class=" mt-2 mx-6 mb-2 py-2 bg-blue-ycube rounded-md text-base font-semibold text-white" @click="validate">Valider</button>
    </div>
</template>
