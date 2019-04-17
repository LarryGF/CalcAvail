<template>
  <v-layout column>
    <Dialog :dialog="dialog" :states="graph.nodes" @close="dialog=false" @save="add_transition"/>
    <v-flex xs12>
      <div class="svg-container" :style="{width: settings.width + '%' }">
        <svg id="svg" pointer-events="all" :viewBox="viewBox" preserveAspectRatio="xMinYMin meet">
          <path
            fill="none"
            stroke="yellow"
            stroke-width="5"
            v-for="(item, index) in graph.links"
            :key="'line'+index"
            :d="d(item.source, item.target)"
            :id="'edge' + index"
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
            :y="item.y +4"
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
          >
            <textPath
              stroke="white"
              stroke-width="1.5"
              :href="'#edge' + index"
              startOffset="42%"
            >{{item.text}}</textPath>
          </text>
        </svg>
      </div>
    </v-flex>
    <v-flex xs12>
      <v-layout row>
        <v-spacer></v-spacer>
        <v-btn @click="add_node">Add Node</v-btn>
        <v-btn @click="dialog=true">Add transition</v-btn>
        <v-spacer></v-spacer>
      </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
import * as d3 from "d3";
import Dialog from "../components/Dialog.vue";

export default {
  data: function() {
    return {
      dialog: false,
      stateNumber: 0,
      simulation: null,
      viewBox: "0 0 960 600",
      graph: {
        nodes: [
          // {
          //   id: "Alice",
          //   x: 10.0,
          //   y: 10.0
          // },
          // {
          //   id: "Bob",
          //   x: 200.0,
          //   y: 200.0
          // },
          // {
          //   id: "Carol",
          //   x: 300.0,
          //   y: 300.0
          // }
        ],
        links: [
          // {
          //   source: 1,
          //   target: 1,
          //   text: "0.5"
          // },
          // {
          //   source: 1,
          //   target: 2,
          //   text: "0.6"
          // },
          // {
          //   source: 2,
          //   target: 1,
          //   text: "0.45"
          // }
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
    Dialog
  },
  mounted: function() {
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
    run_simulation: function() {
      var that = this;

      that.simulation = d3
        .forceSimulation(that.graph.nodes)
        .force(
          "link",
          d3
            .forceLink(that.graph.links)
            .distance(200)
            .strength(0.1)
        )
        .force("charge", d3.forceManyBody())
        .force(
          "center",
          d3.forceCenter(
            that.settings.svgWigth / 2,
            that.settings.svgHeight / 2
          )
        );
    },
    add_node: function() {
      this.graph.nodes.push({
        id: "S" + String(this.stateNumber),
        x: 10.0,
        y: 10.0
      });
      this.stateNumber++;
      this.run_simulation();
    },
    add_transition: function(data) {
      this.dialog = false
      for (var node in this.graph.nodes) {
        console.log(node);
        if (this.graph.nodes[node].id === data.fromState) {
          data.fromState = this.graph.nodes[node];
        } else if (this.graph.nodes[node].id === data.toState) {
          data.toState = this.graph.nodes[node];
        }
      }
      console.log("index");
      console.log(this.graph.nodes.indexOf(data.fromState));
      this.graph.links.push({
        source: this.graph.nodes.indexOf(data.fromState),
        target: this.graph.nodes.indexOf(data.toState),
        text: parseFloat(data.rate)
      });
      // this.graph.links.push({
      //   source: 1,
      //   target: 1,
      //   text: "0.5"
      // });
      this.run_simulation();

    },
    d: function(source, target) {
      console.log("Source: ");
      console.log(source);
      //   source = this.graph.nodes[source];
      //   target = this.graph.nodes[target];
      console.log(source);
      console.log(target);
      var x1 = source.x,
        y1 = source.y,
        x2 = target.x,
        y2 = target.y,
        dx = x2 - x1,
        dy = y2 - y1,
        ff;
      console.log(Math);
      console.log(Math.sqrt(dx * dx + dy * dy));
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
