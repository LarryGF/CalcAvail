<template>
  <v-layout row justify-center>
    <v-dialog v-model="select_dialog" persistent max-width="600px" dark>
      <v-card>
        
        <v-card-title>
          <span class="headline">Select available States</span>
        </v-card-title>
        <v-card-text>
          <v-container fluid >
        <v-checkbox v-for="state in stateIds" :key="state" v-model="selected" :label="state" :value="state"></v-checkbox>
       
      </v-container >
      
          
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="$emit('close')">Close</v-btn>
          <v-btn color="blue darken-1" flat @click="select_items">Accept</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>

<script>
export default {
  name: 'SelectedDialog',
  props: {
    select_dialog: Boolean,
    items: Array,
    selected: Array

  },
  data: () => ({
    stateIds: [],
    // selected:[]
  }),
  watch: {
    items: function () {this.stateIds = this.items.map((state) => state.id)}
  },
 
  methods: {
    select_items: function () {
        this.$emit('select',this.selected)
    //   this.selected = null
    }
  }
}
</script>