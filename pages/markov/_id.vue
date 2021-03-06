<template>
  <v-layout column>
    <AddNodeDialog :add_dialog="add_dialog" @close="add_dialog=false" @save="addNode"></AddNodeDialog>
    <Dialog :dialog="dialog" :states="graph.nodes" @close="dialog=false" @save="addTransition"/>
    <DeleteDialog
      :delete_dialog="delete_dialog"
      :items="items_to_delete"
      :selected="delete_title"
      @close="delete_dialog=false"
      @delete="delete_element"
    />
    <SnackBar :text="snackBarText" :snackbar="openSnackBar" @close="openSnackBar=false"/>

    <SelectDialog
      :select_dialog="select_dialog"
      :items="graph.nodes"
      :selected="selectedStates"
      @close="select_dialog=false"
      @select="selectStates"
    />

    <v-flex xs12>
      <MarkovChain :viewBox="viewBox" :settings="settings" :graph="graph" />
    </v-flex>
    <v-flex xs12>
      <v-layout row mt-1>
        <v-btn color="green" @click="select_dialog=true">Solve chain</v-btn>
        <v-spacer></v-spacer>
        <v-btn @click="add_dialog=true"><v-icon>add</v-icon> Add Node</v-btn>
        <v-btn @click="dialog=true"><v-icon>add</v-icon> Add transition</v-btn>
        <!-- <v-btn color="primary" @click="select_dialog=true"><v-icon>check</v-icon> Select nodes</v-btn> -->
        <v-btn color="error" @click="delete_dialog_prepare('node')"><v-icon>delete</v-icon>Delete node</v-btn>
        <v-btn color="error" @click="delete_dialog_prepare('transition')"><v-icon>delete</v-icon>Delete transition</v-btn>
        <v-spacer></v-spacer>
        <v-slider
          v-model="slider"
          thumb-label
          max="600"
          min="100"
          @change="run_simulation"
          height="20"
          append-icon="zoom_in"
        prepend-icon="zoom_out"
        ></v-slider>
        
        <v-spacer ></v-spacer>

        <v-btn  outline > Availability: {{availability}}</v-btn>
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
import * as d3 from "d3";
import Dialog from "../../components/Dialog";
import DeleteDialog from "../../components/Delete_dialog";
import SelectDialog from "../../components/SelectDialog"
import MarkovChain from "../../components/MarkovChain"
import SnackBar from "../../components/SnackBar"
import AddNodeDialog from "../../components/AddNodeDialog"

export default {
  data: function() {
    return {
      slider:100,
      add_dialog:false,
      snackBarText:'loren',
      openSnackBar:false,
      availability:'?',
      dialog: false,
      delete_dialog: false,
      select_dialog: false,
      selectedStates: [],
      items_to_delete: [],
      delete_title: "",
      stateNumber: 0,
      simulation: null,
      viewBox: "0 0 960 600",
      graph: {
        nodes: [
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
    Dialog,
    DeleteDialog,
    SelectDialog,
    MarkovChain,
    SnackBar,
    AddNodeDialog
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
    this.run_simulation();
  },
  methods: {
    loadInitial: function() {
      let that = this;
      eel.get_initial_data(document.location.pathname)(a => {
        // console.log(a);
        this.graph = this.loadFromJson(a);

        this.selectStates(this.selectedStates)
        
        this.run_simulation();
      });
    },

    getData: async function () {
      eel.get_data()(a => {
        this.graph = this.loadFromJson(a);
        console.log(this.selectedStates)
        console.log('bin')

        this.selectStates(this.selectedStates)
        this.run_simulation();
      });
    },

    loadFromJson: function(json) {
      var m = 1
      for (var node in json.nodes) {
        json.nodes[node].x = Math.random() * this.settings.svgWigth;
        json.nodes[node].y = Math.random() * this.settings.svgHeight;
        json.nodes[node].vx = 0;
        json.nodes[node].vy = 0;
        json.nodes[node].color = '#fff'
      }
      if (json.links.length > 0){
         m = json.links.map((j) => j.ratio).reduce((a,b) => Math.max(a,b))

      } 
     

      for (var link in json.links) {
        json.links[link].text = json.links[link].ratio
        json.links[link].width = (json.links[link].ratio / m) *3 + 2
       
      }

      this.selectedStates = json.selected_states

      // var nodeids = json.nodes.map((node)=>node.id)
      // console.log('number')
      // console.log(nodeids[nodeids.length-1])
      // nodeids = nodeids[nodeids.length-1]

      // console.log(nodeids)

      // nodeids = nodeids.replace('S','')
      // console.log('without')
      // console.log(nodeids)

      // this.stateNumber = parseInt(nodeids)+1

      return json;
    },
    tick: function() {
      for (let i = 0; i < this.graph.nodes.length; i++) {
        const element = this.graph.nodes[i];
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

      that.simulation = d3
        .forceSimulation(that.graph.nodes)
        .on("tick", this.tick)
        .force(
          "link",
          d3
            .forceLink(that.graph.links)
            .distance(this.slider)
            .strength(0.3)
        )
        .force(
          "center",
          d3.forceCenter(
            that.settings.svgWigth / 2,
            that.settings.svgHeight / 2
          )
        )
        .force("collision", d3.forceCollide().radius(100))
        .force('forceY',
        d3.forceY());

    
    },
    addNode: async function(name) {
      if (this.graph.nodes.map((node) => node.id).includes(name)){
        this.snackBarText = "There's already a node with that name"
        this.openSnackBar = true
      } else{

        eel.add_node(name)((result) => {if (result != true){
          this.snackBarText = result
        this.openSnackBar = true
      }else{
        this.add_dialog = false

      }})
      this.getData()
      }
      // this.run_simulation();
    },
    addTransition: function(data) {
      this.dialog = false;
      eel.add_transition(data.fromState,data.toState,data.rate)((result) => {if (result != true){
        this.snackBarText = result
        this.openSnackBar = true
      }})
      this.getData()
    },

    delete_dialog_prepare: function(string) {
      if (string === "transition") {
        for (var link in this.graph.links){
          this.graph.links[link].id = this.graph.links[link].source.id + "=>" + this.graph.links[link].target.id
        }
        this.items_to_delete = this.graph.links;
        
        this.delete_title = "transition";
      } else if (string === "node") {
        this.items_to_delete = this.graph.nodes;
        this.delete_title = "node";
      }

      this.delete_dialog = true;
    },

    delete_element: function(data) {
      this.delete_dialog = false;
      if (this.delete_title === "transition") {
        this.delete_title = "";
        eel.delete_transition(data)((result) => {if (result != true){
        this.snackBarText = result
        this.openSnackBar = true
      }})
      } else if (this.delete_title === "node") {
        eel.delete_node(data)((result) => {if (result != true){
        this.snackBarText = result
        this.openSnackBar = true
      }})
      }
        this.getData()

    },

    selectStates: function(data) {
      console.log('here')
        for (var state in this.graph.nodes){
          // for (var selectedState in data){
            console.log(this.graph.nodes[state].id)
            console.log(data)
            if (data.includes(this.graph.nodes[state].id)){
              this.graph.nodes[state].color = 'yellow'
              console.log('check me')
            } else{
              this.graph.nodes[state].color = '#fff'

            }
          // }
        }
        this.select_dialog = false
        this.selectedStates = data
        eel.set_nodelist(this.selectedStates)((result) => {if (result != true){
        this.snackBarText = result
        this.openSnackBar = true
      }})
        if(this.selectedStates.length >0){

          this.solve()
        }

    },

    solve: function(){
      eel.solve_chain()((result) => {if (result[1] != true){
        this.snackBarText = result[0]
        this.openSnackBar = true
      }else{
        this.availability=result[0]
      }})
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

.nodes circle {
  stroke: #fff;
  stroke-width: 1.5px;
}

svg {
  background: transparent;
}
</style>
