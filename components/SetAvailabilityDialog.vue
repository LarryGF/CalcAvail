<template>
  <v-layout row justify-center>
    <v-dialog v-model="set_dialog" persistent max-width="600px" dark @onShow="$refs.first.focus()">
      <!-- <v-btn slot="activator" color="primary" dark>Open Dialog</v-btn> -->
      <v-card>
        <v-card-title>
          <span class="headline">Set availability on block</span>
        </v-card-title>
        <v-card-text>
          <v-container fluid>
              <v-autocomplete
          autofocus
          v-if="set_dialog"
          v-model="item"
          dense
          :label="'Select block to set'"
          :items="stateIds"
          outline
             @keyup.enter.native="$refs.second.focus()"

        ></v-autocomplete>
            <v-text-field
            ref="second"
              v-model="value"
              label="Availability of the block"
              required
              counter
              maxlength="5"
              loading
              mask="#.####"
              return-masked-value
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
  name: "SetAvailabilityDialog",
  props: {
    set_dialog: Boolean,
    items: Array,

  },
  data: () => ({
    stateIds:[],
    value: '',
    item:'',

    
  }),
  watch: {
    items: function () {console.log(this.items),this.stateIds = this.items.map((state) => state.id)}

  },
  computed: {
    progress () {
      return Math.min(100, this.value.length * 20)
    },
    color () {
      return ['error', 'warning', 'success'][Math.floor(this.progress / 40)]
    }
  },
  methods: {
    save: function() {
        var data = {block:this.item, value:this.value}
        this.$emit("set", data);
        this.value = '';
        this.item = ''
     },
    
  }
};
</script>