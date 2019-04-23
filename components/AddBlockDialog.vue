<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="600px" dark @onShow="$refs.first.focus()">
      <!-- <v-btn slot="activator" color="primary" dark>Open Dialog</v-btn> -->
      <v-card>
        <v-card-title>
          <span class="headline">Create a new block or group of blocks</span>
        </v-card-title>
        <v-card-text>
          <v-container fluid>
            <v-autocomplete
              v-if="dialog"
              v-model="value"
              dense
              outline
              label="How many blocks in parallel?"
              :items="stateIds"
              autofocus
              @keyup.enter.native="determine"
            ></v-autocomplete>
            <v-autocomplete
              v-if="value && value!=1"
              v-model="active"
              ref="second"
              dense
              outline
              label="How many need to be running?"
              :items="generate()"
              @keyup.enter.native="save"
            ></v-autocomplete>
            <!-- <v-autocomplete
          ref="second"
          v-model="to"
          dense
          label="To State"
          :items="stateIds"
          outline
              @keyup.enter.native="$refs.third.focus()"

            ></v-autocomplete>-->
          </v-container>

          <!-- <v-container fluid>
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
          </v-container>-->
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
  name: "AddBlockDialog",
  props: {
    dialog: Boolean
  },
  data: () => ({
    value: null,
    custom: true,
    active: null,
    auto: false,

    stateIds: [1, 2, 3, 4]
  }),
  watch: {
    // states: function () {this.stateIds = this.states.map((state) => state.id)}
  },
  computed: {
    // progress () {
    //   return Math.min(100, this.value.length * 20)
    // },
    // color () {
    //   return ['error', 'warning', 'success'][Math.floor(this.progress / 40)]
    // }
  },
  methods: {
    save: function() {
        console.log(this.value)
        console.log(this.active)

        if (this.value && this.active || this.value ==1){

    var data = {value:this.value,active:this.active};
      this.value = null;
      this.active = ""
      this.$emit("save", data);
      } else {
      this.value = null;
      this.active = null
          
      }
    },
    determine: function () {
        if (this.value ==1){
            return this.save()
        }
        else if (this.value){
            return this.$refs.second.focus()
        }
    },
    generate: function (){
        var newList = []
        for (var element in this.stateIds){
            if (this.stateIds[element] != this.value){
                newList.push(this.stateIds[element])
            }
            else{
                newList.push(this.stateIds[element])
                return newList
            }
        }
    }
  }
};
</script>