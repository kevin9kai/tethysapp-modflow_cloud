//require(["esri/map", "dojo/domReady!"], function(Map) {
//  var map = new Map("map", {
//    center: [-108, 37],
//    zoom: 6,
//    basemap: "topo"
//  });
//});




$(document).ready(function(){

//This makes the click box show up
    var map = TETHYS_MAP_VIEW.getMap();
    closer.onclick = function() {
        overlay.setPosition(undefined);
        closer.blur();
        return false;
      };

    map.on('singleclick', function(evt) {
        var coordinate = evt.coordinate;
        console.log(coordinate);
        var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
            coordinate, 'EPSG:3857', 'EPSG:4326'));
        console.log(hdms);
        content.innerHTML = '<p>You clicked here:</p><code>' + hdms +
            '</code>';
        });

    for(var a=0;a<3;a++){
        console.log(a);
        };
})

