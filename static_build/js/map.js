const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
var map = L.map('map', {
    center:[0, 0],
    zoom: 3
});

// var map = L.map('map')

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: attribution, noWrap: true }).addTo(map);
const markers = JSON.parse(document.getElementById('markers-data').textContent);

// console.log(markers);

let feature = L.geoJSON(markers).bindPopup(function (layer) {
    var popup_text = layer.feature.properties.bandname + ', ' + layer.feature.properties.city;
    return popup_text;
}).addTo(map);


var newMarker;
map.on('click', function test(e) {
    if (newMarker) {
        map.removeLayer(newMarker);
    }
    newMarker = new L.marker(e.latlng, title='Your band location').addTo(map)
    // map.addLayer(newMarker);
    console.log(newMarker.getLatLng());
    document.getElementById('lng').value = newMarker.getLatLng().lng;
    document.getElementById('lat').value = newMarker.getLatLng().lat;
    document.getElementById('createBandButton').disabled = false;
})

function resetinputs() {
    document.getElementById('bandname').value="";
    document.getElementById('city').value="";
    document.getElementById('genre').value="";
    map.removeLayer(newMarker);
    document.getElementById('createBandButton').disabled = true;
}

// map.fitWorld();

// map.fitBounds(feature.getBounds(), { padding: [20, 20] });

