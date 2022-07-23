mapboxgl.accessToken = 'pk.eyJ1IjoidmljdG9yY2M4OCIsImEiOiJja3lhdnl1NzQwOWc5MnBta3A2cjZscThqIn0.M8o_N_BSN_MpTlGAhgGgvA';

const map = new mapboxgl.Map({
container: 'map',
style: 'mapbox://styles/mapbox/streets-v11',
center: [-72.52, -37.42],
zoom: 11
});

map.on('load', () => {
  map.addSource('points', {
    'type': 'geojson',
    'data': './geojson.geojson'
  });
  map.addSource('points2', {
    'type': 'geojson',
    'data': './geojson1.geojson'
  });
  map.addLayer({
    'id': 'asdf',
    'type': 'fill',
    'source': 'points',
    'layout': {},
    'paint': {
      'fill-color': ['get', 'fill'],
      'fill-opacity': 0.5
    }
  });
  map.addLayer({
    'id': 'asdf2',
    'type': 'fill',
    'source': 'points2',
    'layout': {
      'visibility': 'none'
    },
    'paint': {
      'fill-color': ['get', 'fill'],
      'fill-opacity': 0.5
    }

  });

  document.getElementById('slider').addEventListener('input', (e) => {
    const value = parseInt(e.target.value);
    /*map.jumpTo({
      center: [0, 0]
    });*/
    map.setLayoutProperty('asdf', 'visibility', 'none');
    map.setLayoutProperty('asdf2', 'visibility', 'visible');
  });
});





