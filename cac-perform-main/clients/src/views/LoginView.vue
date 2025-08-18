<template>
  <div class="w-screen h-screen bg-gradient-to-r from-blue-ycube to-green-ycube flex justify-center items-center">
    <main class="w-[500px] h-[400px] bg-white rounded-2xl flex flex-col justify-between px-5 py-3">
      <h1 class="uppercase font-bold tracking-widest text-3xl text-[#022a41] mx-auto">Connexion</h1>

      <div class="flex flex-col space-y-6">
        <div class="flex flex-col space-y-2">
          <label for="username" class="uppercase font-semibold text-[#022a41]">Nom d'utilisateur</label>
          <input type="text" id="username" v-model="username" class="p-2 w-full bg-transparent border-2 border-[#022a41] focus:outline-none ring-0 placeholder:italic rounded-[10px] text-[#022a41]" placeholder="Saisir le nom d'utilisateur...">
        </div>

        <div class="flex flex-col space-y-2 mb-3">
          <label for="password" class="uppercase font-semibold text-[#022a41]">Mot de passe</label>
          <input type="password" id="password" v-model="password" class="p-2 w-full bg-transparent border-2 border-[#022a41] focus:outline-none ring-0 placeholder:italic rounded-[10px] text-[#022a41]" placeholder="Saisir le mot de passe...">
        </div>
      </div>

      <button class="px-8 py-3 bg-[#4f778d] rounded-full uppercase text-white font-bold w-[200px] mx-auto mb-5 hover:bg-[#36637d] active:bg-[#4f778d]" @click="login">Se connecter</button>
    </main>
  </div>
</template>
  
<script setup>
import { ref, /*inject*/ } from 'vue';
// const axios = inject('axios')
import { useNotyf } from '@/composables/useNotyf';
import router from '@/router';
const notyf = useNotyf();

const username = ref("")
const password = ref("")

async function login() {
  const field = {
    username: username.value,
    password: password.value
  }

  // const result = (await axios.post('/clients/login', field)).data.response
  // console.log(result)
  if (field.username === "Axel" && field.password === "12345") {
    router.push('/')
  } else {
    notyf.trigger("Nom d'utilisateur ou mot de passe erroné", "error")
  }
}
</script>