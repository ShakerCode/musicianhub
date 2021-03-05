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
    console.log("layer");
    var fields = {
        bandname: layer.feature.properties.bandname,
        city: layer.feature.properties.city,
        leader: layer.feature.properties.leader,
        total_members: layer.feature.properties.total_members,
        genre: layer.feature.properties.genre

    }
    var popup_text = "<p><strong>" + fields['bandname'] + "</strong><br>" + fields['total_members'] + " members" + "<br>" + "City: " + fields['city'] + "</p>";
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
    document.getElementById('description').value="";
    document.getElementById('createBandButton').disabled = true;

    if(map.hasLayer(newMarker)) {
        map.removeLayer(newMarker);
    }
}

// map.fitWorld();

// map.fitBounds(feature.getBounds(), { padding: [20, 20] });

