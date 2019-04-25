<template>
  <v-layout column justify-center align-center>
    <v-flex xs10 >
      <div class="text-xs-center">
        <!-- <img src="/v.png" alt="Vuetify.js" class="mb-5" /> -->
      </div>
      <br>
      <br>
      <br>
      <v-card max-width="800">
        <v-card-title class="headline ">Welcome to AvailabiliCalc</v-card-title>
        <v-card-text >
      
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="createRBD">Start</v-btn>
          <!-- <v-btn color="primary" flat nuxt to="/inspire">Continue</v-btn> -->
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  data: function() {
    return {};
  },

  methods: {
    createChain: async function() {
      eel.create_chain()(result => this.$router.push("/markov/" + result));
    },
    createRBD: async function() {
      eel.create_rbd()(
        result => console.log(result),
        this.$router.push("/rbd_main")
      );
    }
  }
};
</script>

