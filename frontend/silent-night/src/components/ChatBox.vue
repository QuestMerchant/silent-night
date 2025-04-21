<template>
    <div class="column justify-center">
        <div class="col-md-6 col-lg-6 col-lg-6 col-sm-10 col-xs-10">
        <q-scroll-area class="fit" ref="messageArea">
            <div class="q-pa-sm">
            <q-chat-message  
                v-for="msg in chat" 
                :key="msg.id"
                :name="msg.username"
                :avatar="msg.userAvatar"
                :text="[msg.content]"
                :sent="msg.userID === userID ? true : false"
            />
            </div>
        </q-scroll-area>
        </div>
        <div class="col-2">
            <q-form @submit="sendMessage">
                <q-input  v-model="newMessage" placeholder="Type a message..."></q-input>
                <q-btn push rounded label="Send" type="submit" />
            </q-form>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { io } from 'socket.io-client'

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