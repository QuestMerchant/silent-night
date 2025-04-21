<template>
  <div v-if="gameState === 'lobby'">
    <!-- Not sending lobby settings as changing values from a child adds more complexity -->
    <Lobby 
      :code="lobbyCode" 
      :host-name="hostName"
      :is-host="isHost"
    />
  </div>
  <div v-else-if="gameState === 'game'">

  </div>
  <q-drawer show-if-above v-model="chatOpen" side="right" bordered :breakpoint="800">
    <ChatBox 
      :username="username" 
      :room-id="lobbyCode" 
      :user-id="userId"
    />
    <div class="q-mini-drawer-hide">
      <q-btn
        dense
        round
        unelevated
        icon="chat"
        color="accent"
        @click="toggleChat"
        style="top: 15px; left: 15px"
      />
    </div>
    <div class="q-mini-drawer-only">
      <q-btn
        dense
        round
        unelevated
        icon="chat"
        color="accent"
        @click="toggleChat"
        style="top: 15px; left: -15px" 
      /> <!-- Adjust to show icon right side -->
    </div>
  </q-drawer>
</template>

<script setup>
import ChatBox from '../components/ChatBox.vue'
import Lobby from '../components/Lobby.vue'
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchCookie } from '../util/cookies'



const route = useRoute()
const lobbyCode = route.params.lobbyCode
const userId = fetchCookie('userID')

const hostName = ref('')
const hostId = ref('')

const isHost = computed(() => hostId === userId)

// Chat section
const chatOpen = ref(false)

const toggleChat = () => {
    chatOpen.value = !chatOpen.value
}

// Fetch sockets
onMounted(() => {
  
})

// Fetch users, and other info that will be shared across lobby and game states
async function getLobbyData() {
  try {
    const response = await fetch('http://127.0.0.1:5000/lobby_data')
    if (!response.ok) {
        console.log(`HTTP error! Status: ${response.status}`)
        alert("Error with request. Try again")
    }
    const data = await response.json()
    hostName.value = data.host_name
  } catch (error) {
    console.error("Error fetching lobby data:", error)
    alert("Error fetching lobby information!")
  }
}
</script>

<style>
@media (min-width: 1024px) {

}
</style>
