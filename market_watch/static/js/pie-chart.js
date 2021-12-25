// set the dimensions and margins of the graph
var width_pie = 450
height_pie = 450
margin_pie = 40

// The radius of the pieplot is half the width_pie or half the height_pie (smallest one). I subtract a bit of margin_pie.
var radius = Math.min(width_pie, height_pie) / 2 - margin_pie

// append the svg object to the div called 'my_dataviz'
var svg_pie = d3.select("#my_dataviz_pie_chart")
    .append("svg")
    .attr("width", width_pie)
    .attr("height", height_pie)
    .append("g")
    .attr("transform", "translate(" + width_pie / 2 + "," + height_pie / 2 + ")");

// Create dummy data
var data_pie = { 'Positive': positive_headlines, 'Negative': negative_headlines }

// set the color scale
var color_pie = d3.scaleOrdinal().domain(data_pie)
    .range(["green", "red"])

// Compute the position of each group on the pie:
var pie = d3.pie()
    .value(function(d) { return d.value; })
var data_ready = pie(d3.entries(data_pie))
    // Now I know that group A goes from 0 degrees to x degrees and so on.

// shape helper to build arcs:
var arcGenerator = d3.arc()
    .innerRadius(0)
    .outerRadius(radius)

// Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
svg_pie
    .selectAll('mySlices')
    .data(data_ready)
    .enter()
    .append('path')
    .attr('d', arcGenerator)
    .attr('fill', function(d) { return (color_pie(d.data.key)) })
    .attr("stroke", "black")
    .style("stroke-width", "2px")
    .style("opacity", 0.7)

function get_percentage(name) {
    var count = negative_headlines
    if (name === 'Positive') {
        count = positive_headlines
    }
    var total = positive_headlines + negative_headlines
    var percentage = (count * 100) / total
    return " " + percentage + "%"
}

// Now add the annotation. Use the centroid method to get the best coordinates
svg_pie
    .selectAll('mySlices')
    .data(data_ready)
    .enter()
    .append('text')
    .text(function(d) { return d.data.key + get_percentage(d.data.key) })
    .attr("transform", function(d) { return "translate(" + arcGenerator.centroid(d) + ")"; })
    .style("text-anchor", "middle")
    .style("font-size", 17)