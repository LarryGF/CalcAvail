<template>
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
            :fill="item.color"
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
</template>

<script>
export default {
  name: 'MarkovChain',
  props: {
    settings: Object,
    viewBox: String,
    graph: Object

  },
  data: () => ({
      item: null,
    stateIds: []
  }),
  watch: {
    items: function () {this.stateIds = this.items.map((state) => state.id)}
  },
 
  methods: {
    d: function(source, target) {
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
}
</script>