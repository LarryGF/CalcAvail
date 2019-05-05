<template>
  <v-layout row justify-center>
    <v-dialog v-model="add_dialog" persistent max-width="600px" dark @onShow="$refs.first.focus()">
      <!-- <v-btn slot="activator" color="primary" dark>Open Dialog</v-btn> -->
      <v-card>
        <v-card-title>
          <span class="headline">Name of the new node</span>
        </v-card-title>
        <v-card-text>
          <v-container fluid>
            <v-text-field
              v-if="add_dialog"
              autofocus
              v-model="value"
              label="Name of the node"
              required
              counter
              maxlength="4"
              loading
              @keyup.enter.native="save"
            >
              <v-progress-linear slot="progress" :value="progress" :color="color" height="7"></v-progress-linear>
            </v-text-field>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="$emit('close')">Close</v-btn>
          <v-btn color="blue darken-1" flat @click="save">Create</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>

<script>
export default {
  name: "AddNodeDialog",
  props: {
    add_dialog: Boolean
  },
  data: () => ({
    value: '',
    
  }),
  watch: {},
  computed: {
    progress () {
      return Math.min(100, this.value.length * 25)
    },
    color () {
      return ['error', 'warning', 'success'][Math.floor(this.progress / 40)]
    }
  },
  methods: {
    save: function() {
        this.$emit("save", this.value);
        this.value = '';
     },
    
  }
};
</script>