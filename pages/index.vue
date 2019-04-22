<template>
  <v-layout column justify-center align-center>
    <v-flex xs12 sm8 md6>
      <div class="text-xs-center">
        <img src="/v.png" alt="Vuetify.js" class="mb-5" />
      </div>
      <v-card>
        <v-card-title class="headline">Welcome to the Vuetify + Nuxt.js template</v-card-title>
        <v-card-text>
          <v-btn @click="createChain">Create chain</v-btn>
          <v-btn @click="createRBD">Create RBD</v-btn>

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
    createChain: async function () {
      eel.create_chain()((result) =>this.$router.push('/markov/'+ result)  )
      
      
    },
    createRBD: async function () {
      eel.create_rbd()((result) => console.log(result),this.$router.push('/rbd_main') )
    }
  }
}
</script>

