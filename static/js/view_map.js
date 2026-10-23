/* Shows one or more pins. Data comes from the {{ map_markers|json_script:"map-markers" }} tag. */
function initViewMap() {
    var el = document.getElementById("view-map");
    var dataEl = document.getElementById("map-markers");
    if (!el || !dataEl) return;

    var markers = JSON.parse(dataEl.textContent);
    if (!markers.length) return;

    var map = new google.maps.Map(el, {
        center: { lat: markers[0].lat, lng: markers[0].lng },
        zoom: 15,
        mapTypeControl: false,
        streetViewControl: false
    });

    var info = new google.maps.InfoWindow();
    var bounds = new google.maps.LatLngBounds();

    markers.forEach(function (m) {
        var isCustomer = m.kind === "customer";
        var title = isCustomer ? el.getAttribute("data-label-customer") : m.title;

        var marker = new google.maps.Marker({
            position: { lat: m.lat, lng: m.lng },
            map: map,
            title: title,
            // customer = blue dot, laborer = normal red pin
            icon: isCustomer ? {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 9,
                fillColor: "#2563eb",
                fillOpacity: 1,
                strokeColor: "#ffffff",
                strokeWeight: 3
            } : null
        });

        marker.addListener("click", function () {
            var node = document.createElement("strong");
            node.textContent = title;           // textContent: safe for user-entered names
            info.setContent(node);
            info.open(map, marker);
        });

        bounds.extend(marker.getPosition());
    });

    if (markers.length > 1) {
        map.fitBounds(bounds, 60);
        google.maps.event.addListenerOnce(map, "bounds_changed", function () {
            if (map.getZoom() > 16) map.setZoom(16);
        });
    }
}
