console.log('is this thing on?');

const BASE_URL = 'https://www.mapquestapi.com/search/v4/place';
const API_KEY = 'v4KuKoAupEpfVrIWVZamuZx187hh4qaS';

// !Example
// https://www.mapquestapi.com/search/v4/place?location=-115.06814,36.159487999999996&sort=distance&key=v4KuKoAupEpfVrIWVZamuZx187hh4qaS&limit=10&q=bowling

let geoBtn = $('#get-geolocation');

geoBtn.click(function () {
  navigator.geolocation.getCurrentPosition(function (position) {
    let lat = position.coords.latitude;
    let long = position.coords.longitude;

    const location = [long, lat];
    let strLocation = location.toString();
    localStorage.setItem('geoLocation', strLocation);
  });
});

async function searchWithGeo(query) {
  let coordinates = localStorage.getItem('geoLocation');

  const response = await axios.get(`${BASE_URL}`, {
    params: {
      location: coordinates,
      sort: 'distance',
      key: `${API_KEY}`,
      limit: 10,
      q: `${query}`,
    },
  });

  let places = response.data.results.map((obj) => {
    let place = obj;
    return {
      name: place.name,
      street: place.place.properties.street,
      city: place.place.properties.city,
      state: place.place.properties.stateCode,
      postalCode: place.place.properties.postalCode,
    };
  });

  return places;
}

function populatePlaces(places) {
  const $placesList = $('#places-list');
  $placesList.empty();

  for (let place of places) {
    let $item = $(
      `<div class="card m-2">
      <div class="card-body">
      <h5 class="card-title">${place.name}</h5>
      <p class="card-text">${place.street} ${place.city}, ${place.state} ${place.postalCode}</p>
      </div>
      </div>`
    );

    $placesList.append($item);
  }
}

$('#search-form-geolocation').on('submit', async function handleSearch(evt) {
  evt.preventDefault();

  let searchTerm = $('#search-term').val();
  let places = await searchWithGeo(searchTerm);

  populatePlaces(places);
});
