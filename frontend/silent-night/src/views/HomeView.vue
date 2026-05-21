<template>
  <div class="homeView">
    <div class="row">
      <div class="col text-h1 text-center q-py-sm">
        Silent Night
      </div>
    </div>
    <main class="row q-mx-xl justify-center q-gutter-sm">
      <div class="col-lg-3 col-md-6 col-sm-12 col-xs-12">
        <Avatar />
      </div>
      <div class="column col-lg-2 col-md-6 col-sm-12 col-xs-12 flex-center q-gutter-sm">
        <div class="">      
          <q-input outlined v-model="username" label="Username" />
        </div>
        <div class="">
          <q-input outlined v-model="code" label="Room Code" />
        </div>
      </div>
      <div class="column col-lg-2 col-md-6 col-sm-12 col-xs-12 flex-center q-gutter-sm">
        <div class="">
          <q-btn @click="joinLobby" push color="primary" label="Join" />
        </div>
        <div class="">
          Or
        </div>
        <div class="">
          <q-btn @click="createLobby" push color="primary" label="Create new Game" />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref} from 'vue'
import Avatar from '../components/Avatar.vue'
import { useRouter } from 'vue-router'
import { setCookie } from '../util/cookies'
import { useUserStore } from '../stores/user'
import { useGameStore } from '../stores/game'

const user = useUserStore()
const username = ref("")
const code = ref("")
const router = useRouter()
const game = useGameStore()
const apiUrl = import.meta.env.VITE_SILENT_NIGHT_API



async function joinLobby() {
  if (!username.value || !code.value) {
    alert('Please enter both a username and valid lobby code')
    return
  }
  try {
    const response = await axios.post(`${apiUrl}/join-lobby`, {
      name: username.value,
      lobby_code: code.value,
      avatar: user.avatar
    })
    user.changeUsername(username.value)
    user.id = response.data.user_id
    setCookie('userID', `${user.id}`, 30)
    router.push(`/${code.value}`)
  } catch (error) {
    console.error('Error joining lobby:', error)
    alert('Failed to join lobby:' + (error.response?.data?.error || 'Unknown error'))
  }
}

async function createLobby() {
  if (!username.value) {
    alert('Please enter a username')
  }
  try {
    const response = await axios.post(`${apiUrl}/create-lobby`, {
      name: username.value,
      avatar: user.avatar
    })
    game.hostName = username.value
    code.value = response.data.lobby_code
    user.id = response.data.host_id
    user.isHost = true
    user.changeUsername(username.value)
    setCookie('userID', `${user.id}`, 30)
    router.push(`/${code.value}`)
  } catch (error) {
    console.error('Error creating lobby:', error)
    alert('Failed to create a new lobby')
  }
}
</script>

<style scoped>
.homeView {
  min-height: 100vh;
  background-color: #0b0f14;
  background-image: url("/Silent-Night-landscape.png");
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
  background-attachment: fixed;
}

@media (max-width: 768px), (orientation: portrait) {
  .homeView {
    background-image: url("/Silent-Night-Portrait.png");
    background-attachment: scroll;
  }
}
</style>

