import { defineStore } from "pinia"
import { ref, computed } from "vue"


export const useUserStore = defineStore("user", () => {
    const username = ref(null)
    const id = ref(null)
    const avatar = ref(null)
    const isHost = ref(false)
    
    
    const changeUsername = (newUsername) => {
        username.value = newUsername
    }
    
    return { username, id, avatar, isHost, changeUsername }
    })