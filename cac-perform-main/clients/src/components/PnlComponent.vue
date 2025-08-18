<script setup>
const props = defineProps(['efiPnl', 'annee_auditee'])
</script>

<template>
    <!-- Tableau grouping principal -->
    <h3 class="pt-5 pb-1 pl-0 text-xl font-semibold uppercase tracking-wider">Compte de résultat</h3>
    <div class="flex w-full overflow-auto">
        <table class="table w-full border-collapse border border-gray-ycube">
            <thead class="font-bold text-left bg-blue-ycube text-white text-xs h-10">
                <tr class="h-8">
                    <th class="border-2 border-gray-ycube pl-2">REF</th>
                    <th class="w-[60%] border-2 border-gray-ycube pl-2">Intitulé</th>
                    <th class="w-[18%] border-2 border-gray-ycube pl-2">EXERCICE AU 31/12/{{ props.annee_auditee }}</th>
                    <th class="w-[18%] border-2 border-gray-ycube pl-2">EXERCICE AU 31/12/{{ parseInt(props.annee_auditee) - 1 }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="data,index in props.efiPnl" :key="index" class="bg-gray-300 h-10 text-xs cursor-pointer" @click="redirectClientSpace(client._id)">
                    <td class="border-2 border-gray-ycube pl-2">{{ data.ref }}</td>
                    <td class="w-[60%] border-2 border-gray-ycube pl-2">{{ data.libelle }}</td>
                    <td class="w-[18%] border-2 border-gray-ycube pl-2">{{ data.net_solde_n }}</td>
                    <td class="w-[18%] border-2 border-gray-ycube pl-2">{{ data.net_solde_n1 }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
