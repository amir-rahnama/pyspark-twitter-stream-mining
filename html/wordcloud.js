window.onresize = function(event) {
    update();
};

var layout;
var svg = d3.select("#vis").append("svg");
var g = svg.append("g");
var fontSize;
var w = window.innerWidth;
var h = window.innerHeight - 50;
var vis;
var fill = d3.scale.category20b();
var datum = [];

function init(data) {   
  svg
    .attr("width", w)
    .attr("height", h);

  vis = g.attr("transform", "translate(" + [w >> 1, h >> 1] + ")");

  layout = d3.layout.cloud()
    .timeInterval(Infinity)
    .size([w, h])
    .fontSize(function (d) {
      return fontSize(+d.value);
    })
    .text(function (d) {
      return d.key;
    })
    .on("end", draw);

    update(data);
}

function draw(data, bounds) {
  var scale = bounds ? Math.min(
    w / Math.abs(bounds[1].x - w / 2),
    w / Math.abs(bounds[0].x - w / 2),
    h / Math.abs(bounds[1].y - h / 2),
    h / Math.abs(bounds[0].y - h / 2)) / 2 : 1;

  var text = vis.selectAll("text")
    .data(data, function (d) {
      return d.text.toLowerCase();
    });
  text.transition()
    .duration(1000)
    // .attr("transform", function (d) {
    //   return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
    // })
    .style("font-size", function (d) {
      return d.size + "px";
    });
  text.enter().append("text")
    .attr("text-anchor", "middle")
    .attr("transform", function (d) {
      return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
    })
    .style("font-size", function (d) {
      return d.size + "px";
    })
    .style("opacity", 1e-6)
    .transition()
    .duration(1000)
    .style("opacity", 1);
  text.style("font-family", function (d) {
    return d.font;
  })
    .style("fill", function (d) {
      return fill(d.text.toLowerCase());
    })
    .text(function (d) {
      return d.text;
    });

  vis.transition().attr("transform", "translate(" + [w >> 1, h >> 1] + ")scale(" + scale + ")");

}

function update() {
    layout.font('impact').spiral('archimedean');
    fontSize = d3.scale['sqrt']().range([10, 100]);
    if (datum.length){
        fontSize.domain([+datum[datum.length - 1].value || 1, +datum[0].value]);
    }
    layout.stop().words(datum).start();
}

var ws = new WebSocket("ws://localhost:8888");

ws.onopen = function () {
  console.log('Conneting to Socket ...');
};

ws.onmessage = function (evt) {
  var raw = JSON.parse(evt.data);

  raw.map(function (e, i) {
    datum[i] = {
      key: e[0],
      value: e[1]
    };
  });

  setTimeout(function() {
    init();  
  }, 5000);
  
};