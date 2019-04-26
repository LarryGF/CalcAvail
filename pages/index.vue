<template>
  <v-layout column justify-center align-center>
    <v-flex xs10 >
      <div class="text-xs-center">
        <!-- <img src="/v.png" alt="Vuetify.js" class="mb-5" /> -->
        <VuetoNuxtLogo/>
      </div>
      <br>
      <br>
      <br>
      <v-card max-width="800">
        <v-card-title class="display-1">Welcome to AvailabiliCalc</v-card-title>
        <v-card-text class="subheading">
          AvailabiliCalc is a software built to allow the user to estimate the availability of a Data Center
          from very early stages in the DC design. It uses the Python library AvailabiliPy to do all the calculations and 
          uses Nuxt.js and Vue.js to provide a clean, easy to use frontend. For more information about how to use it, visit 
          the <nuxt-link to='/FAQ'>Guide</nuxt-link>, or, if you are already familiar with the software click the <b>Start</b>
          button to start working.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="createRBD()">Start</v-btn>
          <!-- <v-btn color="primary" flat nuxt to="/inspire">Continue</v-btn> -->
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import VuetoNuxtLogo from "../components/NuxtLogo";
export default {
  data: function() {
    return {};
  },
  components: {
    VuetoNuxtLogo
  },
  methods: {
    
    createRBD: async function() {
      console.log('here')
      eel.create_rbd()(
        result => console.log(result),
        this.$router.push("/rbd_main")
      );
    }
  }
};
</script>

