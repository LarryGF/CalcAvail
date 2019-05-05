<template>
  <v-layout column>
    <!-- <Dialog :dialog="dialog" :states="graph.blocks" @close="dialog=false" @save="addTransition"/> -->
    <AddBlockDialog :dialog="dialog" @close="dialog=false" @save="addBlock"/>
    <AddPathDialog :path_dialog="path_dialog" :blocks="graph.blocks" :links="graph.links" @close="path_dialog=false" @create="addPath"/>
    <AttachChainDialog :attach_dialog="attachChain" :items="graph.blocks" @close="attachChain=false" @attach="attachChainToBlock"/>
    <DeleteDialogRBD
      :delete_dialog="delete_dialog"
      :items="items_to_delete"
      :selected="delete_title"
      @close="delete_dialog=false"
      @delete="delete_element"
    />
    <SnackBar :text="snackBarText" :snackbar="openSnackBar" @close="openSnackBar=false"/>
    <!-- <SelectDialog
      :select_dialog="select_dialog"
      :items="graph.blocks"
      :selected="selectedStates"
      @close="select_dialog=false"
      @select="selectStates"
    /> -->

    <v-flex xs12>
      <RBD :viewBox="viewBox" :settings="settings" :graph="graph"/>
    </v-flex>
    <v-flex xs12>
      <v-layout row mt-1>
        <v-btn color="green" @click="solve">Solve System</v-btn>
        <v-spacer></v-spacer>
        <v-btn @click="dialog=true">
          <v-icon>add</v-icon>Add Block
        </v-btn>
        <v-btn @click="path_dialog=true"><v-icon>add</v-icon> Add path</v-btn>
        <!-- <v-btn color="primary" @click="select_dialog=true"><v-icon>check</v-icon> Select blocks</v-btn> -->
        <v-btn color="primary" @click="attachChain=true">
          <v-icon>attach_file</v-icon>Attach Chain
        </v-btn>
        <v-btn color="error" @click="delete_dialog_prepare('block')">
          <v-icon>delete</v-icon>Delete block
        </v-btn>
        <v-btn color="error" @click="delete_dialog_prepare('path')"><v-icon>delete</v-icon>Delete path</v-btn>
        <v-spacer></v-spacer>
        <v-btn outline>Availability: {{availability}}</v-btn>
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
import * as d3 from "d3";
import DeleteDialogRBD from "../components/DeleteDialogRBD";
import RBD from "../components/RBD";
import AddBlockDialog from "../components/AddBlockDialog";
import AddPathDialog from "../components/AddPathDIalog"
import AttachChainDialog from "../components/AttachChainDialog"
import SnackBar from "../components/SnackBar"

export default {
  data: function() {
    return {
      snackBarText:'loren',
      openSnackBar:false,
      attachChain:false,
      delete_dialog:false,
      availability: "?",
      dialog: false,
      path_dialog:false,
      items_to_delete: [],
      delete_title: "",
      stateNumber: 0,
      simulation: null,
      viewBox: "0 0 960 600",
      graph: {
        blocks: [],
        links: [
          
        ]
      },
      simulation: null,
      color: d3.scaleOrdinal(20),
      settings: {
        strokeColor: "#29B5FF",
        width: 100,
        svgWigth: 960,
        svgHeight: 600
      }
    };
  },
  components: {
    DeleteDialogRBD,
    RBD,
    AddBlockDialog,
    AddPathDialog,
    AttachChainDialog,
    SnackBar
  },
  
  mounted: function() {
    this.loadInitial();
    this.viewBox =
      "0 0 " +
      String(window.innerWidth * 0.8) +
      " " +
      String(window.innerHeight * 0.8);
    this.settings.svgWigth = window.innerWidth * 0.8;
    this.settings.svgHeight = window.innerHeight * 0.8;
    // this.run_simulation();
  },
  methods: {
    loadInitial: function() {
      let that = this;
      eel.get_rbd()(a => {
        console.log(a)
        this.graph = this.loadFromJson(a);
        
        this.run_simulation();
      });
    },

    // getData: async function() {
    //   eel.get_data()(a => {
    //     this.graph = this.loadFromJson(a);

    //     this.run_simulation();
    //   });
    // },

    loadFromJson: function(json) {
      for (var node in json.blocks) {
        json.blocks[node].x = 0;
        json.blocks[node].y = 100;
        json.blocks[node].vx = 0;
        json.blocks[node].vy = 0;
        json.blocks[node].color = "#fff";
        if (json.blocks[node].availability == null){
          json.blocks[node].availability = 0
        }
      }
      
      var blockids = json.blocks.map((block)=>block.id)
      blockids = blockids[blockids.length-1]
      blockids = blockids.replace('B','')
      this.stateNumber = parseInt(blockids)+1
      console.log('number')
      console.log(this.stateNumber)

      return json;
    },
    tick: function() {
      for (let i = 0; i < this.graph.blocks.length; i++) {
        const element = this.graph.blocks[i];
        //pam pam pam pam, can't touch this
        if (isNaN(element.x) || isNaN(element.y)) {
          console.log(element);
        }
        if (element.x < 0) {
          element.x = 0 + 15;
        }
        if (element.y < 0) {
          element.y = 0 + 15;
        }
        if (element.x > this.settings.svgWigth) {
          element.x = 900;
        }
        if (element.y > this.settings.svgHeight) {
          element.y = 600;
        }
      }
    },
    run_simulation: function() {
      var that = this;
      var increment = that.settings.svgWigth / that.graph.blocks.length;

      that.simulation = d3
        .forceSimulation(that.graph.blocks)
        .on("tick", this.tick)
        .force("link", d3.forceLink(that.graph.links).distance(increment))

        .force("forceY", d3.forceY(that.settings.svgHeight / 2).strength(100));

      var previousposition = -increment + 10;
      for (var node in that.graph.blocks) {
        that.graph.blocks[node].x = previousposition + increment;
        previousposition = that.graph.blocks[node].x;
      }
      if (that.graph.blocks.length != 0){

        that.graph.blocks[0].x = 10;
      that.graph.blocks[that.graph.blocks.length - 1].x =
        that.settings.svgWigth - 110;
      }
    },
    addBlock: async function(data) {
      this.dialog = false;
      eel.add_block(data.value, "B" + String(this.stateNumber), data.active)(
        result => {if (result != true){
        this.snackBarText = result
        this.openSnackBar = true
      }}
      );
      this.stateNumber++;
      this.loadInitial();
      this.run_simulation();
      
    },
    addPath: function(data) {
      this.path_dialog = false;
      
      eel.add_path(data.from,data.to)((result) => {if (result != true){
        this.snackBarText = result
        this.openSnackBar = true
      }})
      this.loadInitial();
      this.run_simulation();
    },

    delete_dialog_prepare: function(string) {
      if (string === "path") {
        for (var link in this.graph.links) {
          this.graph.links[link].id =
            this.graph.links[link].source.id +
            "=>" +
            this.graph.links[link].target.id;
        }
        this.items_to_delete = this.graph.links;

        this.delete_title = "path";
      } else if (string === "block") {
        this.items_to_delete = this.graph.blocks;
        this.delete_title = "block";
      }

      this.delete_dialog = true;
    },

    delete_element: function(data) {
      this.delete_dialog = false;
      if (this.delete_title === "path") {
        this.delete_title = "";
        eel.del_path(data)(result => {if (result != true){
        this.snackBarText = result
        this.openSnackBar = true
      }});
      } else if (this.delete_title === "block") {
        eel.del_block(data)(result => {if (result != true){
        this.snackBarText = result
        this.openSnackBar = true
      }});
      }
      this.loadInitial();
    },

    solve: function() {
      eel.solve_rbd()(result => {if(result[1] != true){
this.snackBarText = result[0]
        this.openSnackBar = true
      }else{
        this.availability = result[0]
      }});
    },
    attachChainToBlock: function (data){
      eel.attach_chain(data)((result) => this.$router.push('/markov/'+ result))
    }
  }
};
</script>

<style>
/* body {
            width: 100%;
            height: 100%;
            font-family: monospace;
        } */

.controls {
  position: fixed;
  top: 100px;
  left: 100px;
  background: #f8f8f8;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
}

.svg-container {
  display: table;
  border: 1px solid #f8f8f8;
  box-shadow: 1px 2px 4px rgba(253, 253, 253, 0.5);
}

.controls > * + * {
  margin-top: 1rem;
}

label {
  display: block;
}

.links line {
  stroke: #999;
  stroke-opacity: 0.6;
}

.blocks circle {
  stroke: #fff;
  stroke-width: 1.5px;
}

svg {
  background: transparent;
}
</style>
