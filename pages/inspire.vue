<template>
  <v-layout>
    <v-flex text-xs-center>
     <div class="controls">
            <div>
                <label>Adjust width</label>
                <input type="range" v-model="settings.width" min="0" max="100" />
            </div>
        </div>
        <div class="svg-container" :style="{width: settings.width + '%'}">
            <svg id="svg" pointer-events="all" viewBox="0 0 960 600" preserveAspectRatio="xMinYMin meet">
                <g :id="links"></g>
                <g :id="nodes"></g>
            </svg>
        </div>
    </v-flex>
  </v-layout>
</template>

<script>
import * as d3 from 'd3';
export default {
data: function () {
                return {
                    graph: null,
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
            mounted: function () {
                var that = this;
                console.log("mounted");
                var graph = {
    nodes: [
        {
            id: "Alice"
        },
        {
            id: "Bob"
        },
        {
            id: "Carol"
        },
        {
            id:'loren'
        }
    ],
    links: [
        {
            source: 0,
            target: 1
        },
        {
            source: 1,
            target: 2
        }
    ]
}
                // d3.json("http://localhost:3000/animate-force-data.json", function (error, graph) {
                    // console.log(error)
                    // console.log(graph)
                    // if (error) {console.log(error, graph, "FEo"); throw error};
                    that.graph = graph;
                    console.log("json");

                    that.simulation = d3.forceSimulation(that.graph.nodes)
                        .force("link", d3.forceLink(that.graph.links).distance(100).strength(0.1))
                        .force("charge", d3.forceManyBody())
                        .force("center", d3.forceCenter(that.settings.svgWigth / 2, that.settings.svgHeight / 2));
                // });
            },
            computed: {
                nodes: function () {
                    var that = this;
                    console.log("Nodes: ")
                    console.log(that.graph)
                    if (that.graph) {
                        return d3.select("svg").append("g")
                            .attr("class", "nodes")
                            .selectAll("circle")
                            .data(that.graph.nodes)
                            .enter().append("circle")
                            .attr("r", 20)
                            .attr("fill", function (d ,i) {
                                return that.color(i);
                            })
                            .call(d3.drag()
                                .on("start", function dragstarted(d) {
                                    if (!d3.event.active) that.simulation.alphaTarget(0.3).restart();
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
                                }));
                    }
                },
                links: function () {
                    var that = this;
                    if (that.graph) {
                        return d3.select("svg").append("g")
                            .attr("class", "links")
                            .selectAll("line")
                            .data(that.graph.links)
                            .enter().append("line")
                            .attr("stroke-width", function (d) { return Math.sqrt(d.value); });
                    }
                },

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
            updated: function () {
                var that = this;
                that.simulation.nodes(that.graph.nodes).on('tick', function ticked() {
                    that.links
                        .attr("x1", function (d) { return d.source.x; })
                        .attr("y1", function (d) { return d.source.y; })
                        .attr("x2", function (d) { return d.target.x; })
                        .attr("y2", function (d) { return d.target.y; });

                    that.nodes
                        .attr("cx", function (d) { return d.x; })
                        .attr("cy", function (d) { return d.y; });
                });
            }
}
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

        .controls>*+* {
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