<template>
  <v-layout row justify-center>
    <v-dialog v-model="load_dialog" persistent max-width="600px" dark>
      <v-card>
        <v-card-title>
          <span class="headline">Select a file to load</span>
        </v-card-title>
        <v-card-text>
          <v-container fluid >
              <v-radio-group v-model="radioGroup">
        <v-radio v-for="state in items" :key="state"  :label="state" :value="state" color="primary"></v-radio>
              </v-radio-group>
       
      </v-container >
      
          
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="$emit('close')">Close</v-btn>
          <v-btn color="blue darken-1" flat @click="$emit('load',radioGroup)">Load</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>

<script>
export default {
  name: 'LoadDialog',
  props: {
    load_dialog: Boolean,
    items: Array,

  },
  data: () => ({

    radioGroup:'',
    stateIds: ['1','2','3',],
    // selected:[]
  }),
  watch: {
    // items: function () {this.stateIds = this.items.map((state) => state.id)}
  },
 
  methods: {
    select_items: function () {
        this.$emit('select',this.selected)
    //   this.selected = null
    }
  }
}
</script>