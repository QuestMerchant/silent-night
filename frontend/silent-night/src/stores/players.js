import { defineStore } from "pinia"
import { computed, ref } from 'vue'

/**
 * @typedef {Object} Player
 * @property {string} username
 * @property {string} avatar
 * @property {string} role
 */

export const usePlayersStore = defineStore("players", () => {
    /** @type {import('vue').Ref<Player[]>} */
    const players = ref([])
    const playerCount = computed(() => players.value.length)

    /** @param {Player} player */
    const addPlayer = (player) => {
        players.value.push(player)
    }

    /** @param {string} username */
    const removePlayer = (username) => {
        players.value = players.value.filter(player => player.username !== username)
    }

    /** @param {string} username @returns {Player|undefined} */
    const getPlayerByUsername = (username) => {
        return players.value.find(p => p.username === username)
    }

    return { players, playerCount, addPlayer, removePlayer, getPlayerByUsername }
})