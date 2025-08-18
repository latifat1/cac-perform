<script setup>
import { ref, h, onMounted } from 'vue';
import ActifComponent from './ActifComponent.vue';
import PassifComponent from './PassifComponent.vue';
import PnlComponent from './PnlComponent.vue';
const props = defineProps(['data'])
const selectedValue = ref('')
const componentKey = ref('')
const renderComponent = ref()

onMounted(()=>{
    console.log(props.data)
})

function showComp(type) {
    let vnode;
    selectedValue.value = type

    if (type === 'actif') {
        const subProps = {
            efiActif: props.data.efi.actif,
            annee_auditee: props.data.annee_auditee
        }
        vnode = h(ActifComponent, subProps)
    } else if (type === 'passif') {
        const subProps = {
            efiPassif: props.data.efi.passif,
            annee_auditee: props.data.annee_auditee
        }
        vnode = h(PassifComponent, subProps)
    } else if (type === 'pnl') {
        const subProps = {
            efiPnl: props.data.efi.pnl,
            annee_auditee: props.data.annee_auditee
        }
        vnode = h(PnlComponent, subProps)
    }
    renderComponent.value = vnode;
    componentKey.value = type;
}
</script>

<template>
    <div class="h-full w-full flex flex-col space-y-2 overflow-auto">
        <div class="min-h-10 flex space-x-3 px-4 pt-2 items-center">
            <button class="w-[250px] h-8 bg-blue-ycube text-white rounded-md shadow-md" :class="{'bg-green-ycube transition-all ease-in-out duration-300': selectedValue === 'actif'}" @click="showComp('actif')">Actifs</button>
            <button class="w-[250px] h-8 bg-blue-ycube text-white rounded-md shadow-md" :class="{'bg-green-ycube transition-all ease-in-out duration-300': selectedValue === 'passif'}" @click="showComp('passif')">Passifs</button>
            <button class="w-[250px] h-8 bg-blue-ycube text-white rounded-md shadow-md" :class="{'bg-green-ycube transition-all ease-in-out duration-300': selectedValue === 'pnl'}" @click="showComp('pnl')">Compte de résultat</button>
        </div>

        <!--  -->
        <div class="flex-auto flex flex-col overflow-auto">
            <div class="w-full h-full flex flex-col overflow-auto">
                <component :is="renderComponent" :key="componentKey" />
            </div>
        </div>
    </div>
</template>
