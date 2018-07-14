// configure navigation bar

var nav = [
  ["nc-air-baloon", "Overview", "index.html"],
  ["nc-bank", "HQ", "hq.html"],
  ["nc-square-pin", "Node A", "nodeA.html"],
  ["nc-square-pin", "Node B", "nodeB.html"],
  ["nc-alien-33", "Node C", "nodeC.html"],
  ["nc-sun-fog-29", "Weather", "weather.html"],
  ["nc-ambulance", "Hygiene", "hygiene.html"]
];

// utility functions

var responsive = [
  ['screen and (max-width: 640px)', {
    axisX: { labelInterpolationFnc: function(value) { return value[0]; } }
  }]
];

function guidGenerator() {
  var S4 = function() {
     return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
  };
  return "nq-"+S4()+S4()+S4()+S4()+S4()+S4()+S4()+S4();
}

// populate web page

$(function() {
  $(".nq-navbar").html(function() {
    var path = window.location.pathname;
    var page = path.split("/").pop();
    var s = '<ul class="nav">';
    for (var i = 0; i < nav.length; i++) {
      if (page == nav[i][2]) s += `<li class="nav-item active"><span class="nav-link"><i class="nc-icon ${nav[i][0]}"></i><p>${nav[i][1]}</p></span></li>`;
      else s += `<li class="nav-item"><a href="${nav[i][2]}" class="nav-link"><i class="nc-icon ${nav[i][0]}"></i><p>${nav[i][1]}</p></a></li>`;
    }
    s += '</ul>';
    return s;
  });
  $(".nq-chart-card")
    .attr("class", "card")
    .attr("data-chart-id", function() { return guidGenerator(); })
    .html(function() {
      var legend = $(this).attr("data-legend");
      var legendHtml = "";
      if (legend !== undefined) {
        legendHtml = "<div class='card-footer'><div class='legend'>";
        if (legend == "") legendHtml += "&nbsp;";
        else {
          var entries = legend.split(",");
          var color = ["text-info", "text-danger", "text-warning"];
          for (var i = 0; i < entries.length && i < 3; i++) {
            legendHtml += "<i class='fa fa-circle " + color[i] + "'></i> " + entries[i].trim();
          }
        }
        legendHtml += "</div></div>";
      }
      return `
        <div class="card-header">
          <h4 class="card-title">${$(this).attr("data-title")}</h4>
          <p class="card-category">${$(this).attr("data-category")}</p>
        </div>
        <div class="card-body">
          <div id="${$(this).attr("data-chart-id")}" class="ct-chart"></div>
        </div>
        ${legendHtml}
      `;
    })
    .each(function() {
      var chartID = "#"+$(this).attr("data-chart-id");
      var chartType = $(this).attr("data-chart");
      var process = $(this).attr("data-process");
      var opts = $(this).attr("data-options");
      if (!opts) opts = {};
      else {
        opts = '{"' + opts.replace(/:/g, '":').replace(/, +/g, ', "') + '}';
        opts = JSON.parse(opts);
      }
      $.ajax({
        url: $(this).attr("data-url"),
        dataType: 'application/json',
        complete: function(data) {
          if (data.status == 200) {
            data = JSON.parse(data['responseText']);
            if (process) eval(process+"(data)");
            if (chartType == "line") {
              if (!Array.isArray(data.series[0])) data.series = [data.series];
              opts.fullWidth = true;
              Chartist.Line(chartID, data, opts, responsive);
            } else if (chartType == "pie") {
              Chartist.Pie(chartID, data);
            }
          }
        }
      })
    })
});
