import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useGameStore = defineStore('game', () => {
    const gameState = ref(null)
    const dayCount = ref(0)
    const hostName = ref(null)
    
    return { gameState, dayCount, hostName }
})