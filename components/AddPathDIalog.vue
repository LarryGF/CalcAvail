<template>
  <v-layout row justify-center>
    <v-dialog v-model="path_dialog" persistent max-width="600px" dark @onShow="$refs.first.focus()">
      <!-- <v-btn slot="activator" color="primary" dark>Open Dialog</v-btn> -->
      <v-card>
        <v-card-title>
          <span class="headline">Set a path</span>
        </v-card-title>
        <v-card-text>
          <v-container fluid>
            <v-autocomplete
              v-if="path_dialog"
              v-model="value"
              dense
              outline
              label="From"
              :items="generate()"
              autofocus
              @keyup.enter.native="$refs.second.focus()"
            ></v-autocomplete>
            <v-autocomplete
              v-if="value"
              v-model="active"
              ref="second"
              dense
              outline
              label="To"
              :items="determine()"
              @keyup.enter.native="create"
            ></v-autocomplete>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="$emit('close')">Close</v-btn>
          <v-btn color="blue darken-1" flat @click="create">Create</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>

<script>
export default {
  name: "AddPathDialog",
  props: {
    path_dialog: Boolean,
    links: Array,
    blocks: Array
  },
  data: () => ({
    value: null,
    custom: true,
    active: null,
    fromBlocks: [],
    toBlocks: []
  }),
  watch: {},
  computed: {},
  methods: {
    create: function() {
      var data = { from: this.value, to: this.active };
      this.value = null;
      this.active = null;
      this.$emit("create", data);
    },
    determine: function() {
      var to = [];
      for (var link in this.links) {
        // from.splice([this.links[link].source.index],1)
        for (var block in this.blocks) {
          console.log(block)
          if (block != this.links[link].target.index) {
            console.log(this.links[link].target.index)
            to.push(this.blocks[block]);
          }
        }
      }
      return this.blocks.map(block => block.id);
    },
    generate: function() {
      var source = [];
      var from = this.blocks
        for (var block in this.blocks) {
      for (var link in this.links) {
          if (block == this.links[link].source.index) {

            source.push(block);
          }
        }
      }

      
      return from.map(block => block.id);
    }
  }
};
</script>