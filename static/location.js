const BASE_URL = 'https://www.mapquestapi.com/search/v4/place';
const API_KEY = 'v4KuKoAupEpfVrIWVZamuZx187hh4qaS';

// !Example
// https://www.mapquestapi.com/search/v4/place?location=-115.22650890529648%2C%2036.05910693309517&sort=distance&feedback=false&key=v4KuKoAupEpfVrIWVZamuZx187hh4qaS&limit=10&q=orleans

let geoBtn = document.getElementById('get-geolocation');
let latText = document.getElementById('latitude');
let longText = document.getElementById('longitude');

geoBtn.addEventListener('click', function () {
  navigator.geolocation.getCurrentPosition(function (position) {
    let lat = position.coords.latitude;
    let long = position.coords.longitude;

    latText.innerText = lat.toFixed(2);
    longText.innerText = long.toFixed(2);
  });
});

function generateHTML(resp) {
  return;
}

let searchTerm = $('#search-term');
