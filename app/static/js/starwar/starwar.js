/**
 * Created by admin on 2017/8/7.
 */

$(document).ready(function () {
    var svg = d3.select("#svg-map"),
        width = svg.attr('width'),
        height = svg.attr('height');

    var names = ['Films', 'Characters', 'Planets',
        'Starships', 'Vehicles', 'Species'];
    var colors = ['#6ca46c', '#4e88af', '#ca635f',
        '#d2907c', '#d6744d', '#ded295'];

    for (var i = 0; i < names.length; i++) {
        $('#indicator').append(
            "<div><span style='background-color: " +
            colors[i] + "'></span>" + names[i] + "</div>");
    }

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function (d) {
            return d.id;
        }))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    var graph;

    d3.json("/starwar/starwar.json/", function (error, data) {
        if (error) throw error;

        graph = data;
        // console.log(graph);

        var link = svg.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(graph.links)
            .enter().append("line")
            .attr("stroke-width", function (d) {
                return 1;
            });

        var node = svg.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(graph.nodes)
            .enter().append('circle')
            .attr("r", function (d) {
                return d.size;
            })
            .attr("fill", function (d) {
                return colors[d.group];
            })
            .attr("stroke", "none")
            .attr("name", function (d) {
                return d.id;
            })
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        var text = svg.append("g")
            .attr("class", "texts")
            .selectAll("text")
            .data(graph.nodes)
            .enter().append("text")
            .attr("font-size", function (d) {
                return d.size;
            })
            .attr("fill", function (d) {
                return colors[d.group];
            })
            .attr("name", function (d) {
                return d.id;
            })
            .text(function (d) {
                return d.id;
            })
            .attr("text-anchor", "middle")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        node.append("title").text(function (d) {
            return d.id;
        });

        simulation
            .nodes(graph.nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(graph.links);

        function ticked() {
            link
                .attr("x1", function (d) {
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

            node
                .attr("cx", function (d) {
                    return d.x;
                })
                .attr("cy", function (d) {
                    return d.y;
                });

            text
                .attr("transform", function (d) {
                    return "translate(" + d.x + "," + (d.y + d.size / 2) + ")";
                });

        }
    });

    var dragging = false;

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
        dragging = true;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;

        dragging = false;
    }

    $('#mode span').click(function (event) {
        $('#mode span').removeClass('active');
        $(this).addClass('active');
        if ($(this).text() == 'Circles') {
            $('.texts text').hide();
            $('.nodes circle').show();
        }
        else {
            $('.texts text').show();
            $('.nodes circle').hide();
        }
    });

    $("#svg-map").on('mouseenter', '.nodes circle', function (event) {

        if (!dragging) {
            var name = $(this).attr('name');

            $('#info h4').css('color', $(this).attr('fill')).text(name);
            $('#info p').remove();
            for (var key in info[name]) {
                if (typeof (info[name][key]) == 'object') {
                    continue;
                }

                if (key == 'url' || key == 'title' || key == 'name' || key == 'edited' ||
                    key == 'created' || key == 'homeworld') {
                    continue;
                }

                $('#info').append('<p><span>' + key + '</span>' + info[name][key] + '</p>');
            }

            d3.select("#svg-map .nodes")
                .selectAll('circle')
                .attr('class', function (d) {
                    if (d.id == name) {
                        return '';
                    }

                    for (var i = 0; i < graph.links.length; i++) {
                        if (graph.links[i]['source'].id == name && graph.links[i]['target'].id == d.id) {
                            return '';
                        }
                        if (graph.links[i]['target'].id == name && graph.links[i]['source'].id == d.id) {
                            return '';
                        }
                    }

                    return 'inactive';
                });

            d3.select("#svg-map .links")
                .selectAll('line')
                .attr('class', function (d) {
                    if (d.source.id == name || d.target.id == name) {
                        return '';
                    }
                    else {
                        return 'inactive';
                    }

                });
        }
    });

    $("#svg-map").on('mouseleave', '.nodes circle', function (event) {
        if (!dragging) {
            d3.select("#svg-map .nodes")
                .selectAll('circle')
                .attr('class', '');
            d3.select("#svg-map .links")
                .selectAll('line')
                .attr('class', '');
        }
    });

    $("#svg-map").on('mouseenter', '.texts text', function (event) {

        if (!dragging) {
            var name = $(this).attr('name');

            $('#info h4').css('color', $(this).attr('fill')).text(name);
            $('#info p').remove();
            for (var key in info[name]) {
                if (typeof(info[name][key]) == 'object') {
                    continue;
                }
                if (key == 'url' || key == 'title' || key == 'name' || key == 'edited' ||
                    key == 'created' || key == 'homeworld') {
                    continue;
                }
                $('#info').append('<p><spqn>' + key + '</spqn>' + info[name][key] + '</p>');
            }
            d3.select("#svg-map .texts")
                .selectAll('text')
                .attr('class', function (d) {
                    if (d.id == name) {
                        return '';
                    }
                    for (var i = 0; i < graph.links.length; i++) {
                        if (graph.links[i]['source'].id == name && graph.links[i]['target'].id == d.id) {
                            return '';
                        }
                        if (graph.links[i]['target'].id == name && graph.links[i]['source'].id == d.id) {
                            return '';
                        }
                    }
                    return 'inactive';
                });

            d3.select("#svg-map .links")
                .selectAll('line')
                .attr('class', function (d) {
                    if (d.source.id == name || d.target.id == name) {
                        return '';
                    }
                    else {
                        return 'inactive';
                    }

                });
        }
    });

    $("#svg-map").on('mouseleave', '.texts text', function (event) {
        if (!dragging) {
            d3.select("#svg-map .texts")
                .selectAll('text')
                .attr('class', '');
            d3.select("#svg-map .links")
                .selectAll('line')
                .attr('class', '');
        }
    });

    d3.json('/starwar/timeline.json/', function (error, data) {
        if (error) throw error;

        var height2 = 240 - 40;
        var width2 = 960;

        // console.log(data);

        d3.select("#svg-axis g")
            .selectAll("text.film")
            .data(data['films'])
            .enter().append('text')
            .text(function (d) {
                return d[0];
            })
            .attr('transform', function (d, i) {
                return 'translate(150,' + (40 + (i + 0.5) * height2 / data['films'].length) + ')';
            })
            .attr('fill', '#fff')
            .attr('font-size', 12)
            .attr('text-anchor', 'end')
            .attr('class', 'film');

        d3.select("#svg-axis g")
            .selectAll("text.title")
            .data(data['data'])
            .enter().append('text')
            .text(function (d) {
                return d['name'];
            })
            .attr('name', function (d) {
                return d['name'];
            })
            .attr('transform', function (d, i) {
                return 'translate(' + (165 + i * (width2 - 165) / data['data'].length) + ',25)';
            })
            .attr('fill', '#fff')
            .attr('font-size', 12)
            .attr('text-anchor', 'middle')
            .attr('class', 'title')
            .attr('fill-opacity', 0);

        var color2 = ['#4e88af', '#ca635f', '#d2907c', '#d6744d', '#ded295']

        for (var i = 0; i < data['data'].length; i++) {
            var tmp = data['data'][i];
            d3.select("#svg-axis g")
                .append('g')
                .attr('id', tmp['name'])
                .attr('class', 'row')
                .selectAll('rect')
                .data(tmp['vector'])
                .enter().append('rect')
                .attr('width', Math.floor((width2 - 165) / data['data'].length))
                .attr('height', (height2 / data['films'].length - 1))
                .attr('fill', function () {
                    return color2[tmp['group']];
                })
                .attr('transform', function (d, j) {
                    return 'translate(' + (165 + i * (width2 - 165) / data['data'].length) +
                        ',' + (40 + j * height2 / data.films.length) + ')';
                })
                .attr('fill-opacity', function (d) {
                    if (d == 1) {
                        return 1;
                    }
                    else if (d == 0) {
                        return 0;
                    }
                });
        }
    });

    $('#svg-axis').on('mouseenter', 'g.row', function (event) {
        event.preventDefault();
        $('#svg-axis text.title').attr('fill-opacity', 0);
        $('#svg-axis text.title[name="' + $(this).attr('id') + '"]')
            .attr('fill-opacity', 1);
    });

    $('#svg-axis').on('mouseleave', 'g.row', function (event) {
        event.preventDefault();
        $('#svg-axis text.title').attr('fill-opacity', 0);
    });

    var info;
    d3.json("/starwar/all.json/", function (error, data) {
        if (error) throw error;
        info = data;
    });

    $('#search input').keyup(function (event) {
        if ($(this).val() == '') {
            d3.select('#svg-map .texts')
                .selectAll('text')
                .attr('class', '');
            d3.select('#svg-map .nodes')
                .selectAll('circle')
                .attr('class', '');
            d3.select('#svg-map .links')
                .selectAll('line')
                .attr('class', '');
        }
        else {
            var name = $(this).val();
            d3.select('#svg-map .texts')
                .selectAll('text')
                .attr('class', function (d) {
                    if (d.id.toLowerCase().indexOf(name.toLowerCase()) >= 0) {
                        return '';
                    }
                    else {
                        return 'inactive';
                    }
                });
            d3.select('#svg-map .nodes')
                .selectAll('circle')
                .attr('class', function (d) {
                    if (d.id.toLowerCase().indexOf(name.toLowerCase()) >= 0) {
                        return '';
                    }
                    else {
                        return 'inactive';
                    }
                });
            d3.select('#svg-map .links')
                .selectAll('line')
                .attr('class', function (d) {
                    return 'inactive';
                });
        }
    });

});