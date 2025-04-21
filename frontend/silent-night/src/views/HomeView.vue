<template>
  <div class="row">
    <div class="col text-h1 text-center q-py-sm">
      Silent Night
    </div>
  </div>
  <main class="row q-mx-xl justify-center q-gutter-sm">
    <div class="col-lg-3 col-md-6 col-sm-12 col-xs-12">
      <Avatar @update="(s) => url = s" />
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
</template>

<script setup>
import { ref} from 'vue'
import Avatar from '../components/Avatar.vue'
import { useRouter } from 'vue-router'
import { setCookie } from '@/util/cookies'

const url = ref(null)
const username = ref("")
const code = ref("")
const userID = ref(null)
const router = useRouter()


async function joinLobby() {
  if (!username.value || !code.value) {
    alert('Please enter both a username and valid lobby code')
    return
  }

  try {
    const response = await axios.post('http://127.0.0.1:5000/join-lobby', {
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

  try {
    const response = await axios.post('http://127.0.0.1:5000/create-lobby', {
      name: username.value,
      avatar: url.value
    })
    code.value = response.data.lobby_code
    userID.value = response.data.host_id
    setCookie('userID', `${userID.value}`, 30)
    router.push(`/${code.value}`)
  } catch (error) {
    console.error('Error creating lobby:', error)
    alert('Failed to create a new lobby')
  }
}
</script>

