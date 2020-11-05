let map = L.map('map').fitWorld();
let positionMarker;

function redraw() {
    map.redraw()
}

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 20,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
        '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1
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
        document.getElementById('refreshButton').style.boxShadow = "0 0 10px darkgreen";
        setTimeout(function () {
            document.getElementById('refreshButton').style.boxShadow = "";
        }, 300);
    }
    document.getElementById('latitude').value = e.latitude;
    document.getElementById('longitude').value = e.longitude;
}

function onLocationError(e) {
    alert(e.message);
}

map.on('locationfound', onLocationFound);

function onSubmit() {
    map.locate({setView: false, enableHighAccuracy: true});
}

map.locate({setView: true, maxZoom: 18});