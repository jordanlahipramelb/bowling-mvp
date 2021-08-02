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
