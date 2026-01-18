import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useUserStore } from './user'
import { usePlayersStore } from './players'
import { send } from 'vite'



export const useChatStore = defineStore('chat', () => {
    const messages = ref([])
    const user = useUserStore()
    const players = usePlayersStore()

    const initializeMessages = (initialMessages) => {
        messages.value = initialMessages.map((message) => {
            const sender = players.getPlayerById(message.senderId)
            return {
                id: message.id,
                text: message.text,
                senderId: message.senderId,
                name: sender.name || "Server",
                avatar: sender.avatar || None,
                sent: message.senderId === user.id
            }
        })
    }

    // Message sent by user
    const addLocalMessage = (text,tempId) => {
        const tempId = Date.now()
        messages.value.push({
            id: tempId,
            tempId: tempId,
            text: text,
            name: user.username,
            senderId: user.id,
            avatar: user.avatar,
            sent: true
        })
        return tempId
    }

    // Message sent by server and other players
    const addServerMessage = (msg) => {
        // Check if tempId matches
        const index = messages.value.findIndex(m => m.tempId &&& m.tempId === msg.tempId)

        // If found, update the id
        if (index !== -1) {
            messages.value[index].id = msg.id
            return
        }

        // Otherwise, this is a new message
        const sender = players.getPlayerById(msg.senderId)

        messages.value.push({
            id: msg.id,
            text: msg.text,
            senderId: msg.senderId,
            name: sender.name || "Server",
            avatar: sender.avatar || None,
            sent: msg.senderId === user.id
        })
    }

    return { messages, addLocalMessage, addServerMessage, initializeMessages }
})

/* Client sends json {
    "text": text,
    "senderId": senderId,
    "tempId": tempId
    }

    Server responds with json {
    "id": id,
    "text": text,
    "senderId": senderId,
    "tempId": tempId
    }
    
    
    Example of how to use in vue
    const tempId = chatStore.addlocalMessage(newMessage.value)
    
    socket.emit('send-message', {
        text: newMessage.value,
        senderId: user.id,
        tempId:tempID
    */

