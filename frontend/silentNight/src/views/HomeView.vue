<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const gameCode = ref('')
</script>

<template>
  <main>
    <h1>Silent Night</h1>
    <button @click="createGame">Host Game</button>
    <div>
      <input v-model="gameCode" placeholder="Enter Game Code" />
      <button @click="joinGame">Join Game</button>
    </div>
  </main>
</template>
