
String.prototype.rsplit = function(sep){
    var array = this.split(sep);
    var last_el = array.pop();
    rest_array = array.join(sep);
    return [rest_array, last_el]
}


// Override console.log (version 1)
var console=(function(oldCons){
    return {
        log: function(text){
            text = JSON.stringify(text)
            oldCons.log(text);
        },
    };
}(window.console));
window.console = console;

// Override console.log (version 2)
(function(){
    log = console.log;
    console.log = function(){
        log.apply(this, arguments);
        log.apply(this, arguments);
    }
})()



var get_location = function(){

    var location_coordinates;
    var deferred = $.Deferred();

    navigator.geolocation.getCurrentPosition(
        function(position){
            var latitude = position.coords['latitude'];
            var longitude = position.coords['longitude'];
            location_coordinates = [latitude, longitude];
            deferred.resolve(location_coordinates);
        }
    );

    return $.when(deferred).promise()
}

var drawMarkerOnMap = function(coordinates){
    var mymap = L.map('mapid').setView(coordinates, 8);
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpandmbXliNDBjZWd2M2x6bDk3c2ZtOTkifQ._QA7i5Mpkd_m30IGElHziw', {
        attribution: 'ProgrammerHelper &copy;',
        maxZoom: 10,
        id: 'mapbox.streets',
    }).addTo(mymap);
    var marker = L.marker(coordinates).addTo(mymap);
    marker.bindPopup("Location user is here.");
}


var deffered = get_location();

deffered.done(function(location_coordinates){
    drawMarkerOnMap(location_coordinates);
}).fail(function(e){
    console.log('Could not determinate a location or it a feature is not avaible.');
});
