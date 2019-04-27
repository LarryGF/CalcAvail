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
          <path d="M 0,-5 L 10 ,0 L 0,5" fill="yellow" stroke="yellow"></path>
        </marker>
      </defs>

      <path
        fill="none"
        stroke="yellow"
        v-for="(item, index) in graph.links"
        stroke-width="2.7"
        :key="'line'+index"
        :d="d(item.source, item.target)"
        :id="'edge' + index"
        marker-end="url(#arrowhead)"

      ></path>
     
      <g v-for="(item, index) in graph.blocks" :key="'rect' + index">
        <rect
          v-if="item.amount>1"
          width="100"
          height="200"
          rx="10"
          ry="10"
          :x="item.x"
          :y="settings.svgHeight/2-70"
          fill="none"
          stroke="#fff"
          @dblclick="goChain(item)"
        ></rect>

        <rect
          v-if="item.amount==1"
          width="100"
          height="50"
          rx="10"
          ry="10"
          :x="item.x"
          :y="settings.svgHeight/2 +3"
          fill="none"
          stroke="#fff"
          @dblclick="goChain(item)"
        ></rect>

        <rect
          v-for="i in item.amount"
          :key="'smallWhite'+i"
          width="80"
          height="40"
          rx="10"
          ry="10"
          :x="item.x+10"
          :y="adjustRectHeight(item,i)"
          fill="#fff"
          @dblclick="goChain(item)"

        ></rect>

        <rect
          v-for="i in item.valid"
          :key="'small'+i"
          width="80"
          height="40"
          rx="10"
          ry="10"
          :x="item.x+10"
          :y="adjustRectHeight(item,i)"
          fill="yellow"
          @dblclick="goChain(item)"

        ></rect>

        <text
          v-for="i in item.amount"
          :key="i"
          stroke="black"
          :x="item.x +43"
          :y="adjustTextHeight(item,i)"
          class="nodelabel"
        >{{item.id}}.{{i}}</text>
      </g>

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
  name: "RBD",
  props: {
    settings: Object,
    viewBox: String,
    graph: Object
  },
  data: () => ({
    item: null,
    stateIds: []
  }),
  // watch: {
  //   // items: function() {
  //   //   this.stateIds = this.items.map(state => state.id);
  //   // }
  // },
  mounted: function () {
    console.log(this.graph)
  },
  methods: {
    adjustRectHeight: function(item, i) {
      if (item.amount > 1) {
        return this.settings.svgHeight/2 - 45 + i * 50 - 70;
      } else {
        return this.settings.svgHeight/2 - 42 + i * 50;
      }
    },
    adjustTextHeight: function(item, i) {
      if (item.amount > 1) {
        return this.settings.svgHeight/2 - 20 + i * 50 - 70;
      } else {
        return this.settings.svgHeight/2 - 20 + i * 50;
      }
    },


    d: function(source, target) {
      
      var x1 = source.x +100 ,
        y1 = source.y + 30,
        x2 = target.x -10,
        y2 = target.y + 30,
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
        drx = 0,
        dry = 0,
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
        // "A" +
        // drx +
        // "," +
        // dry +
        // " " +
        // xRotation +
        // "," +
        // largeArc +
        // "," +
        // sweep +
        " " +
        x2 +
        "," +
        y2
      );
    },
    goChain: function (item) {
      console.log(item)
      if (item.chainid != null){
        this.$router.push('/markov/'+ String(item.chainid))
      }
      else{
        console.log('none')
      }

    }
  }
};
</script>