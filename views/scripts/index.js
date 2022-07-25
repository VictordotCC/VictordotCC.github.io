
 function load(page,section) {
    loadPageSection(page, section, assignToTarget);
    function assignToTarget (source) {
        container = document.getElementById('cuerpo');
        container.replaceChildren();
        document.getElementById('cuerpo').appendChild(source)
    }
};

function verMapa() {
    //TODO: HIDE API KEY
    mapboxgl.accessToken = 'pk.eyJ1IjoidmljdG9yY2M4OCIsImEiOiJja3lhdnl1NzQwOWc5MnBta3A2cjZscThqIn0.M8o_N_BSN_MpTlGAhgGgvA';

    //show console
    document.getElementById('console').classList.remove('d-none');
    document.getElementById('console').classList.add('d-block');

    //create map
    const map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/satellite-streets-v11',
        center: [-72.52, -37.42],
        zoom: 11
    });
    //TODO: add sources with loop
    map.on('load', () => {
        map.addSource('points', {
            type: 'geojson',
            data: './content/source/geojson.geojson'
        });
        map.addSource('points2', {
            'type': 'geojson',
            'data': './content/source/geojson1.geojson'
        });
        //TODO: add layers with loop
        map.addLayer({
            'id': '1',
            'type': 'fill',
            'source': 'points',
            'layout': {},
            'paint': {
            'fill-color': ['get', 'fill'],
            'fill-opacity': 0.5
            }
        });
        map.addLayer({
            'id': '2',
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
            const date = document.getElementById('active-date');
            //TODO: update layers visibility with loop
            if (value == 1) {
                map.setLayoutProperty('1', 'visibility', 'visible');
                map.setLayoutProperty('2', 'visibility', 'none');
                date.innerHTML = `0${value}`;
            } else {
                map.setLayoutProperty('1', 'visibility', 'none');
                map.setLayoutProperty('2', 'visibility', 'visible');
                date.innerHTML = `0${value}`;
            }
        });
    });
}


navlinks = document.querySelectorAll('.nav-link');

navlinks.forEach(function(link) {
    link.addEventListener('click', function(e) {
        navlinks.forEach(function(link) {
            link.classList.remove('current');
            link.classList.add('notselected');
        });
        e.target.classList.add('current');
        e.target.classList.remove('notselected');
        load(e.target.getAttribute('data-page'), '#contenido');

    });
});



