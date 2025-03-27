<template>
  <div>
    <h4>Lobby Code: {{ lobbyCode }}</h4>
    <section name="settings">
      <div class="row">
        <div class="col">
          Serial Killers:
        </div>
        <div class="col">
          button minus
        </div>
        <div class="col">
          number
        </div>
        <div class="col">
          button plus
        </div>
      </div>
      <div class="row">
        <div class="col">
          Detectives:
        </div>
        <div class="col">
          button minus
        </div>
        <div class="col">
          number
        </div>
        <div class="col">
          button plus
        </div>
      </div>
      <div class="row">
        <div class="col">
          Doctors:
        </div>
        <div class="col">
          button minus
        </div>
        <div class="col">
          number
        </div>
        <div class="col">
          button plus
        </div>
      </div>
      <div class="row">
        <div class="col">
          Spies:
        </div>
        <div class="col">
          button minus
        </div>
        <div class="col">
          number
        </div>
        <div class="col">
          button plus
        </div>
      </div>     
    </section>
    <p>Host: </p>
    <div>no. users: </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router';

const route = useRoute()
const lobbyCode = route.params.lobbyCode
</script>

<style>
@media (min-width: 1024px) {

}
</style>
