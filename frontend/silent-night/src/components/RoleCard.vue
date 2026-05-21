<template>
  <q-card class="roleCard">
    <q-img :src="roleDetails.image" ratio="16/9">
      <div class="absolute-bottom text-h6">
        {{ roleDetails.title }}
      </div>
    </q-img>
    <q-card-section>
      {{ roleDetails.description }}
    </q-card-section>
  </q-card>
</template>

<script setup>
import { computed } from 'vue'
import { getRoleDetails } from '../util/roles'

const props = defineProps({
  roleName: {
    type: [String, Object, null],
    default: ''
  }
})

const roleDetails = computed(() => {
  const roleValue =
    typeof props.roleName === 'object' && props.roleName !== null
      ? props.roleName.name
      : props.roleName

  return getRoleDetails(roleValue)
})
</script>

<style scoped>
.roleCard {
  width: 100%;
}
</style>