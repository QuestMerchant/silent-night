<template>
    <div
        class="col-12 col-sm-6 col-lg-4"
        :class="{ 'fixed-bottom': $q.screen.lt.sm }"
        :style="{
          zIndex: 10,
          height: $q.screen.gt.xs ? '80vh' : 'auto',
          transform: $q.screen.lt.sm && !chatDrawer ? 'translateY(100%)' : 'translateY(0)',
          transition: 'transform 0.3s ease',
          borderTopLeftRadius: $q.screen.lt.sm ? '16px' : '',
          borderTopRightRadius: $q.screen.lt.sm ? '16px' : '',
          background: $q.screen.lt.sm ? 'white' : '',
          boxShadow: $q.screen.lt.sm ? '0 -4px 10px rgba(0,0,0,0.2)' : '',
        }"
    >
        <div class="column justify-center">
            <div class="col-md-6 col-lg-6 col-lg-6 col-sm-10 col-xs-10">
                <q-scroll-area class="q-pa-sm" ref="messageArea" style="height: 80vh">
                    <div class="q-pa-md row justify-center">
                        <div style="width: 90%">
                            <q-chat-message  
                                v-for="msg in chat" 
                                :key="msg.id"
                                :name="msg.username"
                                :avatar="msg.userAvatar"
                                :text="[msg.content]"
                                :sent="msg.sent"
                            />
                        </div>
                    </div>
                </q-scroll-area>
            </div>
            <div class="col-2">
                <q-form class="row" @submit="sendMessage">
                    <q-input class="col" v-model="newMessage" placeholder="Type a message..."></q-input>
                    <q-btn push rounded label="Send" type="submit" />
                </q-form>
            </div>
        </div>
        <!-- FAB button for small screens -->
        <div
            class="row justify-center lt-sm"
            :style="{
            position: 'absolute',
            left: 0,
            right: 0,
            margin: '0 auto',
            display: $q.screen.lt.sm ? 'flex' : 'none',
            top: chatDrawer ? '-30px' : '-70px',
            }"
        >
            <q-fab color="primary" icon="chat" @click="chatDrawer = !chatDrawer" />
        </div>    
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { io } from 'socket.io-client'

const chatDrawer = ref(false)
props = defineProps({
    username: {
        type: String,
        required: true
    },
    roomId: {
        type: String,
        required: true
    },
    userId: {
        type: String
    }
})

// Refs
const socket = io('http://127.0.0.1:5000') // change when deployed
const messageArea = ref(null)
const newMessage = ref('')
const chat = ref([])

// Connect socket

function sendMessage() {
    chat.push({
        text: newMessage,
        userID: userId,
        username: '',
        userAvatar: ''
    })
}
</script>

<style>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.3s ease;
}
.slide-up-enter,
.slide-up-leave-to {
  transform: translateY(100%);
}
</style>