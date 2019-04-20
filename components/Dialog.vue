<template>
  <v-layout row justify-center>
      
    <v-dialog v-model="dialog" persistent max-width="600px" dark @onShow="$refs.first.focus()">
      <!-- <v-btn slot="activator" color="primary" dark>Open Dialog</v-btn> -->
      <v-card>
        
        <v-card-title>
          <span class="headline">Create a new transition</span>
        </v-card-title>
        <v-card-text>
          <v-container fluid >
        <v-autocomplete
        v-if="dialog"
          v-model="from"
          dense
          outline
          label = "From State"
          :items="stateIds"
          autofocus
              @keyup.enter.native="$refs.second.focus()"

        ></v-autocomplete>
        <v-autocomplete
          ref="second"
          v-model="to"
          dense
          label="To State"
          :items="stateIds"
          outline
              @keyup.enter.native="$refs.third.focus()"

        ></v-autocomplete>
      </v-container >
      
          <v-container fluid>
            <!-- <v-layout > -->
            <!-- <v-flex xs12 sm6 md4> -->
            <v-text-field
              ref="third"
              v-model="value"
              label="Transition rate"
              required
              :rules="[rules.required]"
              counter
              maxlength="5"
              loading
              mask="#.###"
              return-masked-value
              @keyup.enter.native="save"

            >
            <v-progress-linear slot="progress" :value="progress" :color="color" height="7"></v-progress-linear>
            </v-text-field>
          </v-container>
          <!-- <small>*indicates required field</small> -->
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="$emit('close')">Close</v-btn>
          <v-btn color="blue darken-1" flat @click="save">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>

<script>
export default {
  name: 'Dialog',
  props: {
    dialog: Boolean,
    states: Array

  },
  data: () => ({
    value: '',
    custom: true,
    from:'',
    to:'',
    auto:false,
    rules: {
      required: value => !!value || 'Required'
    },
    stateIds: []
  }),
  watch: {
    states: function () {this.stateIds = this.states.map((state) => state.id)}
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
    save: function () {
      var data = {rate:this.value,fromState:this.from,toState:this.to}
      this.value = ''
      this.from = ''
      this.to = ''
      this.$emit('save',data)
    },
    change_focus: function (data) {
      
      this.$refs.data.focus()
    }
  }
}
</script>