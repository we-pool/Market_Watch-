// set the dimensions and margins of the graph
var margin = { top: 10, right: 30, bottom: 30, left: 80 },
    width = 800 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#my_dataviz")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

//Read the data
var result = []
for (var i in prediction_data) {
    var obj = {
        date: d3.timeParse("%Y-%m-%dT%H:%M:%SZ")(prediction_data[i].date),
        open: prediction_data[i].open,
        close: prediction_data[i].close,
        low: prediction_data[i].low,
        high: prediction_data[i].high,
        volume: prediction_data[i].volume
    }
    result.push(obj)
}

function draw_graph(data) {
    var allGroup = columns
        // add the options to the button
    d3.select("#selectButton")
        .selectAll('myOptions')
        .data(allGroup)
        .enter()
        .append('option')
        .text(function(txt) { return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase(); }) // text showed in the menu
        .attr("value", function(d) { return d; }) // corresponding value returned by the button

    // A color scale: one color for each group
    var myColor = d3.scaleOrdinal()
        .domain(allGroup)
        .range(d3.schemeCategory10);

    var domainXMin = d3.min(data, function(d) { return d.date; });
    var domainXMax = d3.max(data, function(d) { return d.date; });


    var x = d3.scaleTime()
        .domain([domainXMin, domainXMax])
        .range([0, width]);

    var xAxis = d3.axisBottom(x)
        .ticks(d3.timeDay.every(1))
        .tickFormat(d3.timeFormat(""));

    svg.append('g')
        .attr('class', 'x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(xAxis);

    var x_days = d3.scaleLinear()
        .domain([0, data.length])
        .range([0, width]);

    var x_days_axis = d3.axisBottom(x_days)
        .tickFormat(function(d) { return "Day " + d });

    svg.append('g')
        .attr('class', 'x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(x_days_axis);

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([d3.min(data, function(d) { return d[allGroup[0]]; }), d3.max(data, function(d) { return d[allGroup[0]]; })])
        .range([height, 0]);

    svg.append("g")
        .attr('class', 'y-axis')
        .call(d3.axisLeft(y));

    var days_to_predict = 15

    function predicted_data(data) {
        filtered_data = data.filter(function(d, i, a) { return i > data.length - days_to_predict })
        return filtered_data
    }

    function actual_data(data) {
        filtered_data = data.filter(function(d, i, a) { return i <= data.length - days_to_predict + 1 })
        return filtered_data
    }

    // Add the line
    var actual_line = svg.append("path")
        .datum(actual_data(data))
        .attr("fill", "none")
        .attr("stroke", "grey")
        .attr("stroke-width", 2)
        .attr("d", d3.line()
            .x(function(d) { return x(d.date) })
            .y(function(d) { return y(d[allGroup[0]]) })
        )

    var predicted_line = svg.append("path")
        .datum(predicted_data(data))
        .attr("fill", "none")
        .attr("stroke", "grey")
        .attr("stroke-width", 2)
        .attr("stroke-dasharray", '5,4')
        .attr("d", d3.line()
            .x(function(d) { return x(d.date) })
            .y(function(d) { return y(d[allGroup[0]]) })
        )



    function update(selectedGroup) {
        y = d3.scaleLinear()
            .domain([d3.min(data, function(d) { return d[selectedGroup]; }), d3.max(data, function(d) { return d[selectedGroup]; })])
            .range([height, 0]);
        svg.selectAll(".y-axis").remove();
        svg.append("g")
            .attr('class', 'y-axis')
            .call(d3.axisLeft(y));
        actual_line
            .datum(actual_data(data))
            .transition()
            .duration(1000)
            .attr("d", d3.line()
                .x(function(d) { return x(+d.date) })
                .y(function(d) { return y(+d[selectedGroup]) })
            )
            .attr("stroke", function(d) { return myColor(selectedGroup) })

        predicted_line
            .datum(predicted_data(data))
            .transition()
            .duration(1000)
            .attr("d", d3.line()
                .x(function(d) { return x(+d.date) })
                .y(function(d) { return y(+d[selectedGroup]) })
            )
            .attr("stroke", "black")
    }
    update(allGroup[0])

    // When the button is changed, run the updateChart function
    d3.select("#selectButton").on("change", function(d) {
        // recover the option that has been chosen
        var selectedOption = d3.select(this).property("value")
            // run the updateChart function with this selected option
        update(selectedOption)
    })

}

draw_graph(result)