<template>
  <v-layout column>
    <Dialog :dialog="dialog" :states="graph.nodes" @close="dialog=false" @save="addTransition"/>
    <DeleteDialog
      :delete_dialog="delete_dialog"
      :items="items_to_delete"
      :selected="delete_title"
      @close="delete_dialog=false"
      @delete="delete_element"
    />

    <v-flex xs12>
      <div class="svg-container" :style="{width: settings.width + '%' }">
        <svg id="svg" pointer-events="all" :viewBox="viewBox" preserveAspectRatio="xMinYMin meet">
          <defs>
            <marker
              id="arrowhead"
              viewBox="-0 -5 100 100"
              refX="0"
              refY="0"
              orient="auto"
              markerWidth="10%"
              markerHeight="5%"
              xoverflow="visible"
              preserveAspectRatio="xMinYMin meet"
            >
              <path
              d="M 0,-5 L 10 ,0 L 0,5"
              fill= yellow
              stroke= yellow
              >

              </path>
            </marker>
          </defs>
          

          <path
            fill="none"
            stroke="yellow"
            v-for="(item, index) in graph.links"
            :stroke-width="item.width"
            :key="'line'+index"
            :d="d(item.source, item.target)"
            :id="'edge' + index"
            marker-mid="url(#arrowhead)"
            pointer-events= none

          ></path>
          <circle
            r="40"
            v-for="(item, index) in graph.nodes"
            :cx="item.x"
            :cy="item.y"
            :key="'circle' + index"
            fill="#fff"
          ></circle>

          <text
            v-for="(item, index) in graph.nodes"
            stroke="black"
            :x="item.x -8"
            :y="item.y +3"
            :key="'label' + index"
            class="nodelabel"
          >{{item.id}}</text>

          <text
            v-for="(item, index) in graph.links"
            :key="'labeledge' + index"
            class="edgelabel"
            :id="'edgelabel' + index"
            font-size="20"
            fill="#aaa"
            style="pointer-events: none;"
            dy="-15"
          >
            <textPath
              stroke="white"
              stroke-width="1.5"
              :href="'#edge' + index"
              startOffset="47%"
            >{{item.text}}</textPath>
          </text>


        </svg>
      </div>
    </v-flex>
    <v-flex xs12>
      <v-layout row>
        <v-spacer></v-spacer>
        <v-btn @click="addNode">Add Node</v-btn>
        <v-btn @click="dialog=true">Add transition</v-btn>
        <v-btn @click="delete_dialog_prepare('node')">Delete node</v-btn>
        <v-btn @click="delete_dialog_prepare('transition')">Delete transition</v-btn>
        <v-spacer></v-spacer>
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
import * as d3 from "d3";
import Dialog from "../../components/Dialog.vue";
import DeleteDialog from "../../components/Delete_dialog.vue";

export default {
  data: function() {
    return {
      dialog: false,
      delete_dialog: false,
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
    DeleteDialog
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
        this.run_simulation();
      });
    },

    getData: async function () {
      eel.get_data()(a => {
        // console.log(a);
        this.graph = this.loadFromJson(a);
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
      }
      if (json.links.length > 0){
         m = json.links.map((j) => j.ratio).reduce((a,b) => Math.max(a,b))

      } 
     

      for (var link in json.links) {
        json.links[link].text = json.links[link].ratio
        json.links[link].width = (json.links[link].ratio / m) *3 + 2
        // console.log(json.links[json.links[link].source])
        // json.links[link].id = json.links[link].source.id + '=>' + json.links[link].target.id

      }

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
            .distance(200)
            .strength(0.01)
        )
        .force(
          "center",
          d3.forceCenter(
            that.settings.svgWigth / 2,
            that.settings.svgHeight / 2
          )
        )
        .force("collision", d3.forceCollide().radius(100));

      // .force(
      //   "charge",
      //   d3
      //     .forceManyBody()
      //     .strength(-300)
      //     .distanceMin(200)
      // )

      // d3.layout
      //   .force()
      //   .nodes(dataset.nodes)
      //   .links(dataset.edges)
      //   .size([w, h])
      //   .linkDistance([linkDistance])
      //   .charge([-500])
      //   .theta(0.1)
      //   .gravity(0.05)
      //   .start();
    },
    addNode: async function() {
      eel.add_node("S" + String(this.stateNumber))((result) => console.log(result))
      this.stateNumber++;
      this.getData()
      // this.run_simulation();
    },
    addTransition: function(data) {
      this.dialog = false;
      // for (var node in this.graph.nodes) {
      //   console.log(node);
      //   if (this.graph.nodes[node].id === data.fromState) {
      //     data.fromState = this.graph.nodes[node];
      //     if (this.graph.nodes[node].id === data.toState) {
      //       data.toState = this.graph.nodes[node];
      //     }
      //   } else if (this.graph.nodes[node].id === data.toState) {
      //     data.toState = this.graph.nodes[node];
      //     if (this.graph.nodes[node].id === data.fromState) {
      //       data.fromState = this.graph.nodes[node];
      //     }
      //   }
      // }
      // this.graph.links.push({
      //   id: data.fromState.id + "=>" + data.toState.id,
      //   source: this.graph.nodes.indexOf(data.fromState),
      //   target: this.graph.nodes.indexOf(data.toState),
      //   text: parseFloat(data.rate)
      // });
      eel.add_transition(data.fromState,data.toState,data.rate)((result) => console.log(result))
      // this.run_simulation();
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
        eel.delete_transition(data)((result) => console.log(result))
      } else if (this.delete_title === "node") {
        // this.delete_title = "";
        // var links_to_delete = [];
        // for (var node in this.graph.nodes) {
        //   if (this.graph.nodes[node].id === data) {
        //     this.graph.nodes.splice(node, 1);
        //     for (var link in this.graph.links) {
        //       console.log(this.graph.links[link]);
        //       if (
        //         this.graph.links[link].source.id === data ||
        //         this.graph.links[link].target.id === data
        //       ) {
        //         links_to_delete.push(link);
        //       }
        //     }
        //     for (var link in links_to_delete) {
        //       this.graph.links.splice(link, 1);
        //     }
        //   }
        // }
        eel.delete_node(data)((result) => console.log(result))
      }
      // this.run_simulation();
        this.getData()

    },
    d: function(source, target) {
      // console.log("Source: ");
      // console.log(source);
      //   source = this.graph.nodes[source];
      //   target = this.graph.nodes[target];
      // console.log(source);
      // console.log("Target: ");

      // console.log(target);
      var x1 = source.x,
        y1 = source.y,
        x2 = target.x,
        y2 = target.y,
        dx = x2 - x1,
        dy = y2 - y1,
        ff;

      if (isNaN(source.x) || isNaN(target.x)) {
        x1 = 0;
        x2 = 100;
        dx = 100;
      }
      if (isNaN(source.y) || isNaN(target.y)) {
        y1 = 0;
        y2 = 100;
        dy = 100;
      }
      // console.log(Math);
      // console.log(Math.sqrt(dx * dx + dy * dy));
      var dr = Math.sqrt(dx * dx + dy * dy),
        // Defaults for normal edge.
        drx = dr,
        dry = dr,
        xRotation = 0, // degrees
        largeArc = 0, // 1 or 0
        sweep = 1; // 1 or 0

      // Self edge.
      if (x1 === x2 && y1 === y2) {
        // Fiddle with this angle to get loop oriented.
        xRotation = -45;

        // Needs to be 1.
        largeArc = 1;

        // Change sweep to change orientation of loop.
        //sweep = 0;

        // Make drx and dry different to get an ellipse
        // instead of a circle.
        drx = 30;
        dry = 20;

        // For whatever reason the arc collapses to a point if the beginning
        // and ending points of the arc are the same, so kludge it.
        x2 = x2 + 1;
        y2 = y2 + 1;
      }

      return (
        "M" +
        x1 +
        "," +
        y1 +
        "A" +
        drx +
        "," +
        dry +
        " " +
        xRotation +
        "," +
        largeArc +
        "," +
        sweep +
        " " +
        x2 +
        "," +
        y2
      );
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
