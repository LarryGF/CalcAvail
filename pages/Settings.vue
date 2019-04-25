<template>
  <v-layout column justify-center align-center>
    <v-flex xs12 sm8 md6>
      <div class="text-xs-center">
        <img src="/v.png" alt="Vuetify.js" class="mb-5" />
      </div>
      <v-card>
        <v-card-title class="headline">Settings</v-card-title>
        <v-card-text>
          <v-btn @click="save">Save</v-btn>
          <v-btn @click="load">Load</v-btn>

        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" flat nuxt to="/inspire">Continue</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  data: function () {
    return {

    }
  },
  methods: {
    save: async function () {
      eel.save()((result) =>console.log(result)  )
      
      
    },
    load: async function () {
      eel.load()((result) => console.log(result) )
    }
  }
}
</script>

