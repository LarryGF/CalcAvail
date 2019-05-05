<template>
  <v-layout row justify-center>
    <v-dialog v-model="save_dialog" persistent max-width="600px" dark>
      <!-- <v-btn slot="activator" color="primary" dark>Open Dialog</v-btn> -->
      <v-card>
        
        <v-card-title>
          <span class="headline">Name of the file to save</span>
        </v-card-title>
        <v-card-text>
          <v-container fluid >
        
        <v-text-field
        v-if="save_dialog"
          autofocus
          v-model="item"
          dense
          label="Type the name of the file"
          outline
              @keyup.enter.native="saveFile"

        ></v-text-field>
      </v-container >
      
          
          <!-- <small>*indicates required field</small> -->
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="$emit('close')">Close</v-btn>
          <v-btn color="blue darken-1" flat @click="saveFile">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>

<script>
export default {
  name: 'DeleteDialogRBD',
  props: {
    save_dialog: Boolean,

  },
  data: () => ({
      item: null,
    stateIds: []
  }),
  watch: {
    items: function () {this.stateIds = this.items.map((state) => state.id)}
  },
 
  methods: {
    saveFile: function () {
        this.$emit('save',this.item)
      this.item = null
    }
  }
}
</script>