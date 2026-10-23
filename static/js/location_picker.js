/* Lets a user pin a location: click the map, drag the pin, or use GPS.
   Used on the labour profile form and the booking form. */
function initLocationPicker() {
    var el = document.getElementById("location-map");
    if (!el) return;

    var latInput = document.getElementById(el.getAttribute("data-lat-input"));
    var lngInput = document.getElementById(el.getAttribute("data-lng-input"));
    var statusEl = document.getElementById("location-status");
    var gpsBtn = document.getElementById("use-my-location");
    if (!latInput || !lngInput) return;

    var BENGALURU = { lat: 12.9716, lng: 77.5946 };
    var hasPoint = latInput.value !== "" && lngInput.value !== "";
    var start = hasPoint
        ? { lat: parseFloat(latInput.value), lng: parseFloat(lngInput.value) }
        : BENGALURU;

    var map = new google.maps.Map(el, {
        center: start,
        zoom: hasPoint ? 16 : 11,
        mapTypeControl: false,
        streetViewControl: false
    });

    var marker = null;

    function say(key) {
        if (statusEl) statusEl.textContent = el.getAttribute("data-msg-" + key) || "";
    }

    function setPoint(lat, lng, moveMap) {
        latInput.value = lat.toFixed(7);   // matches DecimalField(decimal_places=7)
        lngInput.value = lng.toFixed(7);

        var pos = { lat: lat, lng: lng };
        if (!marker) {
            marker = new google.maps.Marker({ position: pos, map: map, draggable: true });
            marker.addListener("dragend", function (e) {
                setPoint(e.latLng.lat(), e.latLng.lng(), false);
            });
        } else {
            marker.setPosition(pos);
        }

        if (moveMap) {
            map.panTo(pos);
            if (map.getZoom() < 15) map.setZoom(16);
        }
        say("saved");
    }

    if (hasPoint) setPoint(start.lat, start.lng, false);

    map.addListener("click", function (e) {
        setPoint(e.latLng.lat(), e.latLng.lng(), false);
    });

    if (gpsBtn) {
        gpsBtn.addEventListener("click", function () {
            if (!navigator.geolocation) { say("unsupported"); return; }
            say("locating");
            navigator.geolocation.getCurrentPosition(
                function (p) { setPoint(p.coords.latitude, p.coords.longitude, true); },
                function () { say("denied"); },
                { enableHighAccuracy: true, timeout: 10000 }
            );
        });
    }
}
