
 function load(page,section) {
    loadPageSection(page, section, assignToTarget);
    function assignToTarget (source) {
        container = document.getElementById('cuerpo');
        container.replaceChildren();
        document.getElementById('cuerpo').appendChild(source)
    }
};

function verMapa() {
    //TODO: cargar mapa
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



