<template>
    <v-snackbar
      v-model="snackbar"
      auto-height
      color="error"
      top
      center
      :timeout="timeout"
    >
      {{ text }}
      <v-btn
        dark
        flat
        icon
        @click="$emit('close')"
      >
        <v-icon>close</v-icon>
      </v-btn>
    </v-snackbar>
</template>

<script>
  export default {
    data () {
      return {
          color: '',
        mode: '',
        timeout:0
      }
    },
    props:{
        snackbar: Boolean,
        text: String

    }
  }
</script>