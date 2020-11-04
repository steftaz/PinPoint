// LEAFLET script:


let map = L.map('map').fitWorld();
let positionMarker;

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 20,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
        '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
}).addTo(map);

function onLocationFound(e) {
    if (positionMarker == null) {
        positionMarker = L.circleMarker(e.latlng, {
            radius: 7,
            color: '#FFFFFF',
            fillOpacity: 1,
            fillColor: '#FF0000',
            opacity: 0.5
        })
            .addTo(map).bindPopup("You are here");
    } else {
        positionMarker.setLatLng(e.latlng);
    }
}

function onLocationError(e) {
    alert(e.message);
}


map.on('locationfound', onLocationFound);

function onEachFeature(feature, layer) {
    if (feature.properties && feature.properties["Test text"]) {
        layer.bindPopup(feature.properties["Test text"]);
    }
}

function locate() {
    map.locate({setView: false, enableHighAccuracy: true});
}

// call locate every 3 seconds... forever
setInterval(locate, 1000);

{% for key, value in overview.items %}
var marker = L.marker([{{value.latitude}}, {{value.longitude}}]).addTo(map);

marker.bindPopup('<table class="table table-stripped" >' +
    '<thead>' +
    '<tr>' +
    '<th scope="col"><b>Latitude</b></th>' +
    '<th scope="col"><b>Longitude </b></th>' +
    '{% for attribute in attributes %}' +
    '<th scope="col"> <b>{{ attribute.name }}</b></th>' +
    '{% endfor %}' +
    '</tr>' +
    '</thead>' +
    '<tbody>' +
    '<tr>' +
    '{% for data in value.values %}' +
    '<td > <b>{{ data }}</b></td>' +
    '{% endfor %}' +
    '</tr>' +
    '</tbody>' +
    '</table>');
{%
    endfor %
}

map.locate({setView: true, maxZoom: 16});