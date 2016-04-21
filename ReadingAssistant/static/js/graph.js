/**
 * Created by LiYuntao on 2016/3/19.
 */

function refresh(size) {

    $("#map").html('');

    var json_nodes = new Array();
    var json_links = new Array();
    var nodes_id = new Array();
    //json_nodes = json.nodes;
    //json_links = json.links;
    var nodecnt = 0;
    for(nodeid in json.nodes) {
        if(json.nodes[nodeid].size >= size) {
            json_nodes[nodecnt] = json.nodes[nodeid];
            nodes_id[nodecnt] = nodeid;
            nodecnt++;
        }
    }
    var linkcnt = 0;
    for(linkid in json.links) {
        if(json.links[linkid].source.id in nodes_id && json.links[linkid].target.id in nodes_id) {
            json_links[linkcnt++] = json.links[linkid];
        } else if(json.links[linkid].source in nodes_id && json.links[linkid].target in nodes_id) {
            json_links[linkcnt++] = json.links[linkid];
        }
    }

    function zoomed() {
        container.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
    }

    function dragstartted(d) {
        d3.event.sourceEvent.stopPropagation();
        d3.select(this).classed("dragging", true);
        force.start();
    }

    function dragged(d) {
        d3.select(this)
            .attr("cx", d.x = d3.event.x)
            .attr("cy", d.y = d3.event.y);
    }

    function dragended(d) {
        d3.select(this).classed("draggind", false);
    }

    function click(type, id) {
        $.get("/map/modal/", {'type': type, 'entId': id}, function(ret) {
            $('#modal_content').html(ret);
            $('.ui.small.long.modal').modal('show');
        });
    }

    var margin = {top: -5, right: -5, bottom: -5, left: -5};

    var winWidth = -1, winHeight = -1;
    if (window.innerWidth)
        winWidth = window.innerWidth;
    else if ((document.body) && (document.body.clientWidth))
        winWidth = document.body.clientWidth;
    if (window.innerHeight)
        winHeight = window.innerHeight;
    else if ((document.body) && (document.body.clientHeight))
        winHeight = document.body.clientHeight;
    if (document.documentElement && document.documentElement.clientHeight && document.documentElement.clientWidth) {
        winHeight = document.documentElement.clientHeight;
        winWidth = document.documentElement.clientWidth;
    }

    var width, height;
    if (winWidth != -1) {
        width = winWidth - margin.left - margin.right;
    } else {
        width = 800 - margin.left - margin.right;
    }
    if (winHeight != -1) {
        height = winHeight - margin.top - margin.bottom;
    } else {
        height = 600 - margin.top - margin.bottom;
    }
    var colors = d3.scale.category20();

    var force = d3.layout.force()
        .gravity(0.05)
        .linkDistance(150)
        .charge(-2048)
        .size([width, height]);

    var zoom = d3.behavior.zoom()
        .scaleExtent([0.5, 2])
        .on("zoom", zoomed);

    var drag = d3.behavior.drag()
        .origin(function (d) {
            return d;
        })
        .on("dragstart", dragstartted)
        .on("drag", dragged)
        .on("dragend", dragended);

    var svg = d3.select("#map").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + ", " + margin.right + ")")
        //.style("background", "#FFF7DB")
        .call(zoom);

    var rect = svg.append("rect")
        .attr("width", width)
        .attr("height", height)
        .style("fill", "none")
        .style("pointer-events", "all");

    var container = svg.append("g");

    force.nodes(json_nodes)
        .links(json_links)
        .start();

    var linkPath = container.append("g")
        .selectAll(".linkPath")
        .data(json_links)
        .enter()
        .append("line")
        .style("stroke", "#ccc")
        .style("stroke-width", 1);

    var linkText = container.append("g")
        .selectAll(".linkText")
        .data(json_links)
        .enter()
        .append("text")
        .attr({
            'font-size': '12px',
            //'font-family': 'SimSun',
            'fill': '#0000ff',
            'fill-opacity': 0.0
        })
        .text(function(d) {
            return d.value;
        });

    var node = container.append("g")
        .attr("class", "nodes")
        .selectAll(".node")
        .data(json_nodes)
        .enter()
        .append("g")
        .attr("class", "node")
        .call(force.drag)
        .on("mouseover", function(d, i) {
            linkText.style("fill-opacity", function(linkText) {
                if(linkText.source == d || linkText.target == d) {
                    return 1.0;
                }
            })
        })
        .on("mouseout", function(d, i) {
            linkText.style("fill-opacity", function(linkText) {
                if(linkText.source == d || linkText.target == d) {
                    return 0.0;
                }
            });
        })
        .on("click", function (d) {
            click(d.type, d.id);
        });

    var circles = node.append("circle")
        .attr("r", function(d) {
            return d.size * 1.15 + 2;
        })
        .style("fill", function (d) {
            return colors(d.type);
        });

    node.append("image")
        .attr("xlink:href", function (d) {
            if(d.thumb != "") {
                return d.thumb;
            } else {
                return '/static/img/doge.png';
            }
        })
        .attr("x", function(d) {
            return -d.size;
        })
        .attr("y", function(d) {
            return -d.size;
        })
        .attr("width", function(d) {
            return 2 * d.size;
        })
        .attr("height", function(d) {
            return 2 * d.size;
        });

    node.append("text")
        .attr("dx", function(d) {
            return d.size * 1.5;
        })
        .attr("dy", "0.5em")
        .text(function (d) {
            return d.name
        });

    force.on("tick", function () {
        linkPath.attr("x1", function (d) {
            return d.source.x;
        })
            .attr("y1", function (d) {
                return d.source.y;
            })
            .attr("x2", function (d) {
                return d.target.x;
            })
            .attr("y2", function (d) {
                return d.target.y;
            });
        linkText.attr("x", function(d) {
            return (d.source.x + d.target.x) / 2;
        })
            .attr("y", function(d) {
                return (d.source.y + d.target.y) / 2;
            });
        node.attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
    });

}