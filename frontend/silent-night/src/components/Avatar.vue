<template>
  <q-card class="avatar-card" style="height: 100%">
    <q-card-section>
      <div class="text-h6 text-center">Customize Your Avatar</div>
    </q-card-section>
    <q-separator />
    <img :src=avatar alt="avatar" style="padding: 4px; max-width: 90%; margin-left: auto; margin-right: auto;" />
    <q-separator />
    <q-card-section>
      <q-card-actions align="around">
        <q-btn @click="selectedEyes--" :disabled="selectedEyes === 0" push color="primary" rounded :icon="fasLeftLong" size="sm" />
        <span class="q-mx-sm text-center">Eyes</span>
        <q-btn @click="selectedEyes++" :disable="selectedEyes === eyes.length - 1" push color="primary" rounded :icon="fasRightLong" size="sm" />
      </q-card-actions>
      <q-card-actions align="around">
        <q-btn @click="selectedEyebrows--" :disabled="selectedEyebrows === 0" push color="primary" rounded :icon="fasLeftLong" size="sm" />
        <span class="q-mx-sm text-center">Eyebrows</span>
        <q-btn @click="selectedEyebrows++" :disabled="selectedEyebrows === eyebrows.length - 1" push color="primary" rounded :icon="fasRightLong" size="sm" />
      </q-card-actions>
      <q-card-actions align="around">
        <q-btn @click="selectedFeat--" :disabled="selectedFeat === 0" push color="primary" rounded :icon="fasLeftLong" size="sm" />
        <span class="q-mx-sm text-center">Features</span>
        <q-btn @click="selectedFeat++" :disabled="selectedFeat === features.length - 1" push color="primary" rounded :icon="fasRightLong" size="sm" />
      </q-card-actions>
      <q-card-actions align="around">
        <q-btn @click="selectedGlasses--" :disabled="selectedGlasses === 0" push color="primary" rounded :icon="fasLeftLong" size="sm" />
        <span class="q-mx-sm text-center">Glasses</span>
        <q-btn @click="selectedGlasses++" :disabled="selectedGlasses === glasses.length - 1" push color="primary" rounded :icon="fasRightLong" size="sm" />
      </q-card-actions>
      <q-card-actions align="around">
        <q-btn @click="selectedHair--" :disabled="selectedHair === 0" push color="primary" rounded :icon="fasLeftLong" size="sm" />
        <span class="q-mx-sm text-center">Hair Style</span>
        <q-btn @click="selectedHair++" :disabled="selectedHair === hair.length - 1" push color="primary" rounded :icon="fasRightLong" size="sm" />
      </q-card-actions>
      <q-card-actions align="around">
        <q-btn @click="selectedHairColor--" :disabled="selectedHairColor === 0" push color="primary" rounded :icon="fasLeftLong" size="sm" />
        <span class="q-mx-sm text-center">Hair Colour</span>
        <q-btn @click="selectedHairColor++" :disabled="selectedHairColor === hairColor.length - 1" push color="primary" rounded :icon="fasRightLong" size="sm" />
      </q-card-actions>
      <q-card-actions align="around">
        <q-btn @click="selectedMouth--" :disabled="selectedMouth === 0" push color="primary" rounded :icon="fasLeftLong" size="sm" />
        <span class="q-mx-sm text-center">Mouth</span>
        <q-btn @click="selectedMouth++" :disabled="selectedMouth === mouth.length - 1" push color="primary" rounded :icon="fasRightLong" size="sm" />
      </q-card-actions>
      <q-card-actions align="around">
        <q-btn @click="selectedSkinColor--" :disabled="selectedSkinColor === 0" push color="primary" rounded :icon="fasLeftLong" size="sm" />
        <span class="q-mx-sm text-center">Skin Colour</span>
        <q-btn @click="selectedSkinColor++" :disabled="selectedSkinColor === skinColor.length - 1" push color="primary" rounded :icon="fasRightLong" size="sm" />
      </q-card-actions>
    </q-card-section>
  </q-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { fasLeftLong, fasRightLong } from '@quasar/extras/fontawesome-v6'


const emit = defineEmits({
  update: (url) => {
    // Validate update event
    if (url) {
      return true
    } else {
      console.warn('Invalid event payload')
      return false
    }
  }
})

// Options. Do Not Change!
const eyes = ["variant01", "variant02", "variant03", "variant04", "variant05", "variant06", "variant07", 
  "variant08", "variant09", "variant10", "variant11", "variant12", "variant13", "variant14", "variant15", 
  "variant16", "variant17", "variant18", "variant19", "variant20", "variant21", "variant22", "variant23", 
  "variant24", "variant25", "variant26"]
const eyebrows = ["variant01", "variant02", "variant03", "variant04", "variant05", "variant06", "variant07", 
  "variant08", "variant09", "variant10", "variant11", "variant12", "variant13", "variant14", "variant15"]
const features = ["None", "birthmark", "blush", "freckles", "mustache"] // Add function for none
const glasses = ["None", "variant01", "variant02", "variant03", "variant04", "variant05"] // Add function for none
const hair = ["long01", "long02", "long03", "long04", "long05", "long06", "long07", "long08", "long09", "long10", 
  "long11", "long12", "long13", "long14", "long15", "long16", "long17", "long18", "long19", "long20", "long21", 
  "long22", "long23", "long24", "long25", "long26", "short01", "short02", "short03", "short04", "short05", 
  "short06", "short07", "short08", "short09", "short10", "short11", "short12", "short13", "short14", "short15", 
  "short16", "short17", "short18", "short19"]
const hairColor = ["0e0e0e", "562306", "6a4e35", "796a45", "85c2c6", "3eac2c", "ab2a18", "cb6820", "ac6511", 
  "b9a05f", "e5d7a3", "afafaf", "dba3be"]
const mouth = ["variant01", "variant02", "variant03", "variant04", "variant05", "variant06", "variant07", 
  "variant08", "variant09", "variant10", "variant11", "variant12", "variant13", "variant14", "variant15", 
  "variant16", "variant17", "variant18", "variant19", "variant20", "variant21", "variant22", "variant23", 
  "variant24", "variant25", "variant26", "variant27", "variant28", "variant29", "variant30"]
const skinColor = ["9e5622", "763900", "ecad80", "f2d3b1"]

// Selections
const selectedEyes = ref(0)
const selectedEyebrows = ref(0)
const selectedFeat = ref(0)
const selectedGlasses = ref(0)
const selectedHair = ref(0)
const selectedHairColor = ref(0)
const selectedMouth = ref(0)
const selectedSkinColor = ref(0)

// URL
const avatar = computed(() => {
  let url = `https://api.dicebear.com/9.x/adventurer/svg?eyes=${eyes[selectedEyes.value]}`
  url += `&eyebrows=${eyebrows[selectedEyebrows.value]}`
  url += `&hair=${hair[selectedHair.value]}`
  url += `&hairColor=${hairColor[selectedHairColor.value]}`
  url += `&mouth=${mouth[selectedMouth.value]}`
  url += `&skinColor=${skinColor[selectedSkinColor.value]}`
  if (selectedFeat.value !== 0) {
    url += `&features=${features[selectedFeat.value]}&featuresProbability=100`
  }
  if (selectedGlasses.value !== 0) {
    url += `&glasses=${glasses[selectedGlasses.value]}&glassesProbability=100`
  }
  emit('update', url)
  return url // Send to redis as well
})

/* Navigation
function prev(selected) {
  if (selected.value > 0) {
    selected.value--
  }
}
function next(array, selected) {
  console.log("Next clicked", selected, array.length); // Debugging line
  if (selected.value < (array.length - 1)) {
    selected.value ++
    console.log("Updated selectedFeat:", selected); // Debugging line
  }
}*/ // Can't figure out how to receive the variable instead of the value. Perhaps use reactive instead of ref
</script>
