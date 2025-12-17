import { defineStore } from "pinia"
import { ref } from 'vue'

export const usePlayersStore = defineStore("players", () => {
    const players = ref([])
    const playerCount = computed(() => players.value.length)

    const addPlayer = (player) => {
        players.value.push(player)
    }

    const removePlayer = (playerId) => {
        players.value = players.value.filter(player => player.id !== playerId)
    }

    const getPlayerById = (id) => {
        return players.value.find(p => p.id === id)
    }

    return { players, playerCount, addPlayer, removePlayer, getPlayerById }
}