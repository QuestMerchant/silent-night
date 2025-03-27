<template>
  <div class="row justify-evenly">
    <div class="col">
      <h1>Silent Night</h1>
    </div>
  </div>
  <main class="row">
    <div class="col-3">
      <Avatar @update="(s) => url = s" />
    </div>
    <div class="column col-3 flex-center">
      <div class="col-2">      
        <q-input outlined v-model="username" label="Username" />
      </div>
      <div class="col-1">
        <q-input outlined v-model="code" label="Room Code" />
      </div>
    </div>
    <div class="column col-2 flex-center">
      <div class="col-1">
        <q-btn @click="joinLobby" push color="primary" label="Join" />
      </div>
      <div class="col-1">
        <p>Or</p>
      </div>
      <div class="col-1">
        <q-btn @click="createLobby" push color="primary" label="Create new Game" />
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref} from 'vue'
import Avatar from '../components/Avatar.vue'
import { useRouter } from 'vue-router'

const url = ref(null)
const username = ref("")
const code = ref("")
const userID = ref(null)

async function joinLobby() {
  if (!username.value || !code.value) {
    alert('Please enter both a username and valid lobby code')
    return
  }

  try {
    const response = await axios.post('/api/join-lobby', {
      name: username.value,
      lobby_code: code.value
    })
    userID.value = response.data.user_id

  } catch (error) {
    console.error('Error joining lobby:', error)
    alert('Failed to join lobby:' + (error.response?.data?.error || 'Unknown error'))
  }
}

async function createLobby() {
  if (!username.value) {
    alert('Please enter a username')
  }
  
  const router = useRouter()

  try {
    const response = await axios.post('/api/create-lobby', {
      name: username.value
    })
    code.value = response.data.lobby_code
    userID.value = response.data.host_id
    router.push(`/${code}`)
  } catch (error) {
    console.error('Error creating lobby:', error)
    alert('Failed to create a new lobby')
  }
}
</script>