<template>
  <v-layout>
    <v-flex xs12>

      <div  class="svg-container" :style="{width: settings.width + '%'}">
        <svg
          id="svg"
          pointer-events="all"
          :viewBox="viewBox"
          preserveAspectRatio="xMinYMin meet"
        >
          <circle
            
            r="20"
            v-for="(item, index) in graph.nodes"
            :cx="item.x"
            :cy="item.y"
            :key="index"
            fill="#fff"
          ></circle>

          <path
            fill="none"
            stroke="yellow"
            stroke-width="5"
            v-for="(item, index) in graph.links"
            :key="index"
            :d="d(item.source, item.target)"
          ></path>
        </svg>
      </div>
    </v-flex>
    <v-btn>Loren</v-btn>
  </v-layout>
</template>

<script>
import * as d3 from "d3";
export default {
  data: function() {
    return {
      viewBox: '0 0 960 600' ,
      graph: {
        nodes: [
          {
            id: "Alice",
            x: 10.0,
            y: 10.0
          },
          {
            id: "Bob",
            x: 200.0,
            y: 200.0
          },
          
          
        ],
        links: [
        //   {
        //     source: 0,
        //     target: 1
        //   },
        //   {
        //     source: 1,
        //     target: 2
        //   }
        ]
      },
      simulation: null,
      color: d3.scaleOrdinal(20),
      settings: {
        strokeColor: "#29B5FF",
        width: 100,
        svgWigth: '960',
        svgHeight: '600'
      }
    };
  },
  mounted () {
      this.viewBox = '0 0 ' + String(window.innerWidth*0.8) + ' ' + String(window.innerHeight*0.8)
  },
  computed: {
    nodes: function() {
      var that = this;
      console.log("Nodes: ");
      console.log(that.graph);
      if (that.graph) {
        return d3
          .select("svg")
          .append("g")
          .attr("class", "nodes")
          .selectAll("circle")
          .data(that.graph.nodes)
          .enter()
          .append("circle")
          .attr("r", 20)
          .attr("fill", function(d, i) {
            return that.color(i);
          })
          .call(
            d3
              .drag()
              .on("start", function dragstarted(d) {
                if (!d3.event.active)
                  that.simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
              })
              .on("drag", function dragged(d) {
                d.fx = d3.event.x;
                d.fy = d3.event.y;
              })
              .on("end", function dragended(d) {
                if (!d3.event.active) that.simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
              })
          );
      }
    }
    // links: function () {
    //     var that = this;
    //     if (that.graph) {
    //         return d3.select("svg").append("g")
    //             .attr("class", "links")
    //             .selectAll("line")
    //             .data(that.graph.links)
    //             .enter().append("line")
    //             .attr("stroke-width", function (d) { return Math.sqrt(d.value); });
    //     }
    // },

    // links: function () {
    //     var that = this;
    //     if (that.graph) {
    //         return d3.select("svg").append("g")
    //             .attr("class", "links")
    //             .selectAll("path")
    //             .data(that.graph.links)
    //             .enter().append("path")
    //             .attr("stroke-width", function (d) { return Math.sqrt(d.value); });
    //     }
    // },
  },
  updated: function() {
    // var that = this;
    // that.simulation.nodes(that.graph.nodes).on("tick", function ticked() {
    //   that.links
    //     .attr("x1", function(d) {
    //       return d.source.x;
    //     })
    //     .attr("y1", function(d) {
    //       return d.source.y;
    //     })
    //     .attr("x2", function(d) {
    //       return d.target.x;
    //     })
    //     .attr("y2", function(d) {
    //       return d.target.y;
    //     });

    //   that.nodes
    //     .attr("cx", function(d) {
    //       return d.x;
    //     })
    //     .attr("cy", function(d) {
    //       return d.y;
    //     });
    // });
  },
  methods: {
    print: function (event) {
       this.graph.nodes = this.graph.nodes.concat([
           {
               id:'loren',
               x: event.offsetX - 10,
               y: event.offsetY - 10
           },
           
       ])


      console.log(event)
    },
    d: function(source, target) {
      // console.
      source = this.graph.nodes[source];
      target = this.graph.nodes[target];
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
  background: black;
}
</style>