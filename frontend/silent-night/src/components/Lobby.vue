<template>
  <div class="column flex-center">
    <div class="text-h6 text-left">
      Lobby Code: {{ code }}
      Host: {{ hostName }}
      Current player count:
    </div>
    <div v-if="isHost">
      <div class="row">
        <div class="col">
          <q-input 
            v-for="value, roleName in settings['roles']"
            :label="roleName"
            :hint="`How many ${roleName}?`"
            type="number"
            v-model.number="settings.roles[roleName]" 
          />
          <!-- v-model can't bind to scoped variable unless iterating through an array -->
          <q-input v-model.number="settings['night length']" label="Night Duration" type="number" hint="How long is night phase in seconds" />
          <q-input v-model.number="settings['day length']" label="Day Duration" type="number" hint="How long is day phase in seconds" />
          <q-btn @click="settingsSave">Save Settings</q-btn>
          <q-btn @click="gameStart">Start Game</q-btn>
        </div>        
      </div>
    </div>
    <div v-else>
      <q-card>
        <q-card-section>
          <p class="text-h6 text-left">Settings:</p>
          <q-list dense>
            <q-item>Night Length = {{ settings['night length'] }} seconds</q-item>
            <q-item>Day Length = {{ settings['day length'] }} seconds</q-item>
            <q-item v-for="value, roleName in settings['roles']">{{ roleName }} = {{ value }}</q-item>
          </q-list>
          <p class="text-center">Waiting for game to start</p>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { io } from 'socket.io-client'

const socket = io('http://127.0.0.1:5000'); // change when deployed


props = defineProps(['code', 'hostName', 'isHost'])

const settings = ref({})
/* ref({
 'roles': {'Serial Killers':n, etc.},
 'night length': n,
 'day length': n 
 })*/

// Fetch lobby settings
onMounted(() => {
  socket.on('settings_updated', (data) => {
    if (data.code === props.code) {
      settings.value = data.settings
    }
  })
})
</script>


<style lang=scss scoped>
#test {
  background:url(https://images.unsplash.com/photo-1742626157100-a25483dda2ea?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D) no-repeat center;
  background-size:cover;
  min-height: 100vh;
  overflow:hidden;
}
</style>