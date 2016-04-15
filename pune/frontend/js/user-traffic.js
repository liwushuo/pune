$(function(){
  function formatBytes(bytes, axis) {
     decimals = 1;
     if(bytes == 0) return '0';
     var k = 1000; // or 1024 for binary
     var dm = decimals;
     var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
     var i = Math.floor(Math.log(bytes) / Math.log(k));
     return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + '' + sizes[i];
  }

  function formatDate(d, fmt, monthNames, dayNames) {

    if (typeof d.strftime == "function") {
      return d.strftime(fmt);
    }

    var leftPad = function(n, pad) {
      n = "" + n;
      pad = "" + (pad == null ? "0" : pad);
      return n.length == 1 ? pad + n : n;
    };

    var r = [];
    var escape = false;
    var hours = d.getHours();
    var isAM = hours < 12;

    if (monthNames == null) {
      monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    }

    if (dayNames == null) {
      dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    }

    var hours12;

    if (hours > 12) {
      hours12 = hours - 12;
    } else if (hours == 0) {
      hours12 = 12;
    } else {
      hours12 = hours;
    }

    for (var i = 0; i < fmt.length; ++i) {

      var c = fmt.charAt(i);

      if (escape) {
        switch (c) {
          case 'a': c = "" + dayNames[d.getDay()]; break;
          case 'b': c = "" + monthNames[d.getMonth()]; break;
          case 'd': c = leftPad(d.getDate()); break;
          case 'e': c = leftPad(d.getDate(), " "); break;
          case 'h': // For back-compat with 0.7; remove in 1.0
          case 'H': c = leftPad(hours); break;
          case 'I': c = leftPad(hours12); break;
          case 'l': c = leftPad(hours12, " "); break;
          case 'm': c = leftPad(d.getMonth() + 1); break;
          case 'M': c = leftPad(d.getMinutes()); break;
          // quarters not in Open Group's strftime specification
          case 'q':
            c = "" + (Math.floor(d.getMonth() / 3) + 1); break;
          case 'S': c = leftPad(d.getSeconds()); break;
          case 'y': c = leftPad(d.getFullYear() % 100); break;
          case 'Y': c = "" + d.getFullYear(); break;
          case 'p': c = (isAM) ? ("" + "am") : ("" + "pm"); break;
          case 'P': c = (isAM) ? ("" + "AM") : ("" + "PM"); break;
          case 'w': c = "" + d.getDay(); break;
        }
        r.push(c);
        escape = false;
      } else {
        if (c == "%") {
          escape = true;
        } else {
          r.push(c);
        }
      }
    }

    return r.join("");
  }

  function build_options(time_range) {
      return {
      series: {
          lines: {
              show: true,
              lineWidth: 1,
              fill: false,
              fillColor: {
                  colors: [{
                      opacity: 0.2
                  }, {
                      opacity: 0.2
                  }]
              }
          },
          points: {
              radius: 2,
              show: true,
              fillColor: '#1ccacc',
          },
          shadowSize: 2,
          valueLabels: {
            show: true,
            labelFormatter: formatBytes,
          },
      },
      grid: {
          hoverable: true,
          clickable: true,
          tickColor: "#f0f0f0",
          borderWidth: 1,
          color: '#f0f0f0'
      },
      colors: ["#1ccacc"],
      xaxis:{
        mode: "time",
        timeformat: (time_range == 'day' ? "%m/%e<br>%I:%M %P" : "%m/%e"),
        timezone: "browser",
        minTickSize: (time_range == 'day' ? [1, "hour"] : [1, "day"])
      },
      yaxis: {
        ticks: 4,
        tickFormatter: formatBytes,
        hideZero: true,
      },
      tooltip: true,
      tooltipOpts: {
        xDateFormat: "%Y-%m-%d<br>%I:%M %P",
        content: function(label, xval, yval, flotItem) {
          if (time_range=='day') {
            return "%x ~ "+formatDate(new Date(xval+3540000), "%I:%M %P")+"<br>流量：%y";
          }
          else {
            return formatDate(new Date(xval), "%Y-%m-%d")+"<br>流量：%y";
          }
        },
        // content: "%x<br>流量：%y",
        defaultTheme: false,
      }
    }
  }

  $('#range-select li a').on('click', function(){
      build_report($(this).data('value'));
  });

  build_report('week');

  function build_report(time_range) {
    $.ajax({
      url: "/traffic/stats",
      type: 'GET',
      dataType: 'json',
      data: {
        time_range: time_range,
      }
    }).done(function(data) {
      var times = data.time;
      var values = data.value;
      var d1 = [];
      for (var i = 0; i <= times.length; i += 1) {
        d1.push([times[i]*1000, values[i]]);
      }
     $("#flot-1ine").length && $.plot($("#flot-1ine"), [{data: d1 }], build_options(time_range));
    });
  }
});
