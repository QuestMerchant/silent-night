<template>
    <div class="row justify-center">
        <div>if day, vote, if night, select/vote nightAction</div>
        <q-scroll-area class="col-md-8 col-xl-6 col-sm-12">
            <div class="row justify-center q-gutter-sm">
                <q-intersection
                    v-for="user in users"
                    :key="userID"
                    transition="scale"
                    class="user_card col-4"
                >
                    <q-card flat bordered>
                        <img :src="avatar">
                        <q-badge v-if="vote">{{ vote.count }}</q-badge>
                        <q-card-section>
                            <div class="text-h6">{{ userName }}</div>
                            <div class="text-subtitle">{{ userRole }}</div>
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
</template>

<script setup>
import { ref } from 'vue'


</script>

<style lang="scss" scoped>
.user_card {
    max-height: 240px;
    max-width: 200px;
}
</style>