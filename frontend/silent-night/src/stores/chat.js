import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useUserStore } from './user'
import { usePlayersStore } from './players'

export const useChatStore = defineStore('chat', () => {
    const messages = ref([])
    const user = useUserStore()
    const players = usePlayersStore()

    const getSenderUsername = (msg) => {
        return (
            msg?.senderUsername ??
            msg?.sender_name ??
            msg?.sender ??
            msg?.username ??
            null
        )
    }

    const initializeMessages = (initialMessages) => {
        messages.value = initialMessages.map((message) => {
            const senderUsername = getSenderUsername(message)
            const sender = senderUsername ? players.getPlayerByUsername(senderUsername) : null
            return {
                id: message.id,
                tempId: message.tempId ?? null,
                content: message.text ?? message.content ?? '',
                senderUsername,
                username: senderUsername ?? 'Server',
                userAvatar: sender?.avatar ?? message.avatar ?? null,
                sent: Boolean(senderUsername && senderUsername === user.username),
            }
        })
    }

    // Message sent by user
    const addLocalMessage = (text) => {
        const tempId = Date.now()
        messages.value.push({
            id: tempId,
            tempId: tempId,
            content: text,
            senderUsername: user.username,
            username: user.username,
            userAvatar: user.avatar,
            sent: true,
        })
        return tempId
    }

    // Message sent by server and other players
    const addServerMessage = (msg) => {
        // Check if tempId matches
        const index = messages.value.findIndex(m => m.tempId && m.tempId === msg.tempId)

        // If found, update the id
        if (index !== -1) {
            messages.value[index].id = msg.id
            return
        }

        // Otherwise, this is a new message
        const senderUsername = getSenderUsername(msg)
        const sender = senderUsername ? players.getPlayerByUsername(senderUsername) : null

        messages.value.push({
            id: msg.id,
            tempId: msg.tempId ?? null,
            content: msg.text ?? msg.content ?? '',
            senderUsername,
            username: senderUsername ?? 'Server',
            userAvatar: sender?.avatar ?? msg.avatar ?? null,
            sent: Boolean(senderUsername && senderUsername === user.username),
        })
    }

    return { messages, addLocalMessage, addServerMessage, initializeMessages }
})

/* Client sends json {
    "text": text,
    "senderId": senderId, // current user id (auth only; do not broadcast to other clients)
    "tempId": tempId
    }

    Server responds with json {
    "id": id,
    "text": text,
    "senderUsername": username, // identify players by username (safe to broadcast)
    "tempId": tempId
    }
    
    
    Example of how to use in vue
    const tempId = chatStore.addLocalMessage(newMessage.value)
    
    socket.emit('send-message', {
        text: newMessage.value,
        senderId: user.id,
        tempId: tempId
    */

