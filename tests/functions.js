function ajax(type, url, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
      if (xmlhttp.readyState == XMLHttpRequest.DONE && xmlhttp.status == 200) {
        var data = xmlhttp.responseText;
        if (callback) callback(data);
      }
    };
    xmlhttp.open(type, url, true);
    xmlhttp.send();
  }
  