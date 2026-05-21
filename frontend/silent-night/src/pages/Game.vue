<template>
  <div class="gameLayout row justify-center q-gutter-md">
    <div class="col-12 col-md-3 col-lg-3 col-xl-2">
      <RoleCard :role-name="roleName" />
    </div>

    <div class="col-12 col-md-8 col-xl-6">
      <div class="q-mb-sm">if day, vote, if night, select/vote nightAction</div>

      <q-scroll-area class="playersScroll">
        <div class="row justify-center q-gutter-sm">
          <q-intersection
            v-for="player in players"
            :key="player.username"
            transition="scale"
            class="user_card col-4"
          >
            <q-card flat bordered>
              <img :src="player.avatar">
              <q-badge v-if="vote">{{ vote.count }}</q-badge>
              <q-card-section>
                <div class="text-h6">{{ player.username }}</div>
                <div class="text-subtitle">{{ player.role?.name ?? player.role ?? '' }}</div>
              </q-card-section>
              <q-separator />
              <q-card-actions vertical>
                <q-btn v-if="phase === 'day'">Vote</q-btn>
                <q-btn v-else-if="user.nightAction">{{ user.nightAction }}</q-btn>
              </q-card-actions>
            </q-card>
          </q-intersection>
        </div>
      </q-scroll-area>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useUserStore } from '../stores/user'
import { usePlayersStore } from '../stores/players'
import { useGameStore } from '../stores/game'
import RoleCard from '../components/RoleCard.vue'

const user = useUserStore()
const game = useGameStore()
const phase = game.gameState
const playersStore = usePlayersStore()

// Vote section
const vote = ref('')

// Fetch players
const players = computed(() => playersStore.players)

const currentPlayer = playersStore.getPlayerByUsername(user.username)

</script>

<style lang="scss" scoped>
.gameLayout {
  width: 100%;
}

.playersScroll {
  height: min(80vh, 720px);
}

.user_card {
    max-height: 240px;
    max-width: 200px;
}
</style>