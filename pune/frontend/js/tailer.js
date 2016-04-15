$(function(){
  function declare(module_name, exports) {
    window[module_name] = exports
  }
var LogTailer = {
  timeout_id: null,
  timeout: 1000,
  scroll: true,
  deploy_id: null,
  last_position: null,
}

LogTailer.getHistory = function ( callback ){
  LogTailer.currentScrollPosition = $("#log-window").scrollTop();
  $.ajax({
    url: '/deploys/'+LogTailer.deploy_id+'/log',
    success: function(result){
            LogTailer.printLines(result);
                    callback && callback();
           },
    dataType: "json"
  });
  console.log('12345');
}

LogTailer.getLines = function (){
  LogTailer.currentScrollPosition = $("#log-window").scrollTop();
  $.ajax({
    url: '/deploys/'+LogTailer.deploy_id+'/log',
    data: {
      'last_position': LogTailer.last_position,
    },
    success: function(result){
            LogTailer.printLines(result);
           },
    dataType: "json"
  });
}

LogTailer.printLines = function(result){;
  console.log('1234');
  LogTailer.last_position = result.last_position;
  result = result.content;
  for(var i=0;i<result.length;i++){
    if(result[i].length>0){
      var html = ansi2html(result[i]);
      $("#log-window").append(html+'<br>');
    }
  }

  if(LogTailer.scroll && result.length){
    $("#log-window").scrollTop($("#log-window")[0].scrollHeight - $("#log-window").height());
  }
  else{
    $("#log-window").scrollTop(LogTailer.currentScrollPosition);
  }
  window.clearTimeout(LogTailer.timeout_id);
  LogTailer.timeout_id = window.setTimeout(LogTailer.getLines, LogTailer.timeout);
}


LogTailer.startReading = function (){
    if ($('#log-window').is(":empty") ) {
        LogTailer.getHistory( function(){
            LogTailer.timeout_id = window.setTimeout(LogTailer.getLines, LogTailer.timeout);
        });
    } else {
        alert("set getlines timeout");
        LogTailer.timeout_id = window.setTimeout(LogTailer.getLines, LogTailer.timeout);
    }
}
declare('LogTailer', LogTailer);
});
