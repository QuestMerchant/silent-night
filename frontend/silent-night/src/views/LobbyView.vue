<template>
  <div class="row justify-evenly no-wrap">
    <div v-if="gameState === 'lobby'">
      <!-- Not sending lobby settings as changing values from a child adds more complexity -->
      <Lobby 
        :code="lobbyCode" 
        :host-name="hostName"
        :is-host="isHost"
      />
    </div>
    <div v-else-if="gameState === 'day' || gameState === 'night'">
      <Game :game-state="gameState" />
    </div>
    <ChatBox 
      :username="username" 
      :room-id="lobbyCode" 
      :user-id="userId"
    />
  </div>
</template>

<script setup>
import ChatBox from '../components/ChatBox.vue'
import Lobby from '../pages/Lobby.vue'
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchCookie } from '../util/cookies'
import Game from '../pages/Game.vue'
import { useUserStore } from '../stores/user'
import { usePlayersStore } from '../stores/user'
import { useGameStore } from '../stores/game'

const user = useUserStore()
const players = usePlayersStore()
const game = useGameStore()
const route = useRoute()
const lobbyCode = route.params.lobbyCode
const userId = fetchCookie('userID')

const hostName = game.hostName || ref('')
const gameState = ref('')

const isHost = user.isHost

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
    gameState.value = data.game_state
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
