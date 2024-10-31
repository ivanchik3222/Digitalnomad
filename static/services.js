function showMap(coordinates, name) {
    const mapModal = document.getElementById('map-modal');
    mapModal.style.display = 'flex';
    ymaps.ready(function () {
        var map = new ymaps.Map('map', {
            center: coordinates.split(',').map(Number),
            zoom: 15
        });
        var placemark = new ymaps.Placemark(coordinates.split(',').map(Number), {
            balloonContent: name
        }, {
            preset: 'islands#icon',
            iconColor: '#0095b6'
        });
        map.geoObjects.add(placemark);
    });
}

function closeMap() {
    const mapModal = document.getElementById('map-modal');
    mapModal.style.display = 'none';
    document.getElementById('map').innerHTML = '';
}