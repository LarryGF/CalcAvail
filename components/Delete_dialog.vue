<template>
  <v-layout row justify-center>
    <v-dialog v-model="delete_dialog" persistent max-width="600px" dark>
      <!-- <v-btn slot="activator" color="primary" dark>Open Dialog</v-btn> -->
      <v-card>
        
        <v-card-title>
          <span class="headline">Delete {{selected}}</span>
        </v-card-title>
        <v-card-text>
          <v-container fluid >
        
        <v-autocomplete
          autofocus
          v-if="delete_dialog"
          v-model="item"
          dense
          :label="'Select '+ this.selected + ' to delete'"
          :items="stateIds"
          outline
              @keyup.enter.native="delete_item"

        ></v-autocomplete>
      </v-container >
      
          
          <!-- <small>*indicates required field</small> -->
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="$emit('close')">Close</v-btn>
          <v-btn color="blue darken-1" flat @click="delete_item">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>

<script>
export default {
  name: 'DeleteDialog',
  props: {
    delete_dialog: Boolean,
    items: Array,
    selected: String

  },
  data: () => ({
      item: null,
    stateIds: []
  }),
  watch: {
    items: function () {this.stateIds = this.items.map((state) => state.id)}
  },
 
  methods: {
    delete_item: function () {
        this.$emit('delete',this.item)
      this.item = null
    }
  }
}
</script>