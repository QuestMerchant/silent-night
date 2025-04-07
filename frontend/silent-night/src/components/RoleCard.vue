<template>
    <q-card class="roleCard">
        <q-img :src="roleImage">
            <div class="absolute-bottom text-h6">
                {{ roleTitle }}
            </div>
        </q-img>
        <q-card-section>
            {{ roleDescription }}
        </q-card-section>
    </q-card>
</template>