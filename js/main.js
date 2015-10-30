(function() {
'use strict';

var map = new GMaps({
  el: '#map',
  lat: 51.05031,
  lng: 13.73754
});

var baseurl = "https://staging.park-api.higgsboson.tk/";
$.get(baseurl, function(data) {

  var urls = _.map(data.cities, function (value, key) {
    return baseurl+key;
  });

  _.forEach(urls, addDataToMap);
});

function addDataToMap(url) {
  $.get(url, function (data) {
    data.lots.forEach(function (lot) {
      if(!lot.coords) {
        console.log("no coordinates for lots found");
        return;
      }
      map.addMarker({
            lat: lot.coords.lat,
            lng: lot.coords.lng,
            title: lot.name,
            infoWindow: {
              content: "<p>"+lot.name+"<br/>Status: "+lot.state+"<br/>Freie Parkplätze: "+lot.free+"/"+lot.total
            }
      });
    });
  });
}

})();
