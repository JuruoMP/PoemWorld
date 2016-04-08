/**
 * Created by LiYuntao on 2016/3/19.
 */

function refresh() {

    var linkedByIndex = {};

    function isConnected(a, b) {
        return linkedByIndex[a.index + "," + b.index] || linkedByIndex[b.index + "," + a.index];
    }

    function dottype(d) {
        d.x = +d.x;
        d.y = +d.y;
        return d;
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

    function click(type, name) {
        //$('.ui.modal').modal('show');
        window.showModalDialog("type=" + type + "&eneity=" + name + "/", window,
        "dialogHeight:" + window.innerHeight / 2 + "px;dialogWidth:" + window.innerWidth / 2 + "px;status=no;");
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
        .charge(-4096)
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

    force.nodes(json.nodes)
        .links(json.links)
        .start();

    var link = container.append("g")
        .attr("class", "links")
        .selectAll(".link")
        .data(json.links)
        .enter()
        .append("line")
        .attr("class", "link")
        .attr("id", function (d, i) {
            return 'edge' + i
        })
        .attr("marker-end", 'url(#arrowhead)')
        .style("stroke", "#ccc")
        .style("stroke-width", 1)
        .style("pointer-events", "none");

    var node = container.append("g")
        .attr("class", "nodes")
        .selectAll(".node")
        .data(json.nodes)
        .enter()
        .append("g")
        .attr("class", "node")
        .call(force.drag)
        .on("click", function (d) {
            click(d.type, d.name);
        });

    node.append("circle")
        .attr("r", 16)
        .style("fill", function (d, i) {
            return colors(i);
            console.log(color);
        });
    //.attr("cx", function(d) { return d.x; })
    //.attr("cy", function(d) { return d.y; }

    node.append("image")
        .attr("xlink:href", function (d) {
            return d.icon;
        })
        .attr("x", -8)
        .attr("y", -8)
        .attr("width", 16)
        .attr("height", 16);

    node.append("text")
        .attr("dx", 16)
        .attr("dy", ".35em")
        .text(function (d) {
            return d.name
        });

    var linkPath = container.append("g")
        .selectAll(".linkPath")
        .data(json.links)
        .enter()
        .append("path")
        .attr({
            'd': function (d) {
                return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y
            },
            'class': 'linkPath',
            'fill-opacity': 0,
            'stroke-opacity': 0,
            'fill': 'blue',
            'stroke': 'red',
            'id': function (d, i) {
                return 'linkPath' + i
            }
        })
        .style("pointer-events", "none");

    var linkText = container.append("g")
        .selectAll(".linkText")
        .data(json.links)
        .enter()
        .append("text")
        .style("pointer-events", "none")
        .attr({
            'class': 'linkText',
            'id': function (d, i) {
                return 'linkText' + i
            },
            'dx': 80,
            'dy': 0,
            'font-size': 10,
            'fill': '#aaa'
        });
    linkText.append("textPath")
        .attr("xlink:href", function (d, i) {
            return '#linkPath' + i
        })
        .style("pointer-events", "none")
        .text(function (d, i) {
            return d.value;
        });

    force.on("tick", function () {
        link.attr("x1", function (d) {
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
        node.attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });

        linkPath.attr('d', function (d) {
            var path = 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y;
            //console.log(d)
            return path
        });

        linkText.attr('transform', function (d, i) {
            if (d.target.x < d.source.x) {
                bbox = this.getBBox();
                rx = bbox.x + bbox.width / 2;
                ry = bbox.y + bbox.height / 2;
                return 'rotate(180 ' + rx + ' ' + ry + ')';
            }
            else {
                return 'rotate(0)';
            }
        });
    });

    link.forEach(function (d) {
        linkedByIndex[d.source + "," + d.target] = 1;
    });

//d3.select('rect#no-drag').on('mousedown.drag', null);
}