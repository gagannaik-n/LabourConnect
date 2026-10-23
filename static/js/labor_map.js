/* Find Laborers page:
   - shows every laborer on a Google Map (pins come from the cards on the page)
   - "Find laborers near me": uses GPS, shows distance, sorts nearest first,
     and can hide laborers outside a chosen radius.
   The distance feature works even when no Google Maps key is set. */
(function () {
    "use strict";

    var entries = [];        // laborers that have a map location
    var noCoordCards = [];   // laborers without a map location
    var grid = null;
    var userPos = null;
    var map = null, info = null, userMarker = null;
    var collected = false;

    function msg(key) {
        var el = document.getElementById("labor-page-msgs");
        return el ? (el.getAttribute("data-" + key) || "") : "";
    }

    function setStatus(text) {
        var el = document.getElementById("nearby-status");
        if (el) el.textContent = text;
    }

    function haversineKm(lat1, lng1, lat2, lng2) {
        var R = 6371, rad = Math.PI / 180;
        var dLat = (lat2 - lat1) * rad, dLng = (lng2 - lng1) * rad;
        var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(lat1 * rad) * Math.cos(lat2 * rad) *
                Math.sin(dLng / 2) * Math.sin(dLng / 2);
        return 2 * R * Math.asin(Math.sqrt(a));
    }

    function collect() {
        if (collected) return;
        collected = true;
        var cards = document.querySelectorAll(".labor-card");
        if (cards.length) grid = cards[0].parentNode;

        Array.prototype.forEach.call(cards, function (card) {
            var lat = parseFloat(card.getAttribute("data-lat"));
            var lng = parseFloat(card.getAttribute("data-lng"));
            if (isNaN(lat) || isNaN(lng)) {
                noCoordCards.push(card);
            } else {
                entries.push({ card: card, lat: lat, lng: lng, marker: null, distance: null });
            }
        });
    }

    function infoNode(card) {
        var box = document.createElement("div");
        box.style.maxWidth = "220px";

        var name = document.createElement("strong");
        name.textContent = card.getAttribute("data-name");
        box.appendChild(name);

        var price = document.createElement("div");
        price.textContent = "\u20B9" + card.getAttribute("data-price") + " / " + msg("hour");
        box.appendChild(price);

        var links = document.createElement("div");
        links.style.marginTop = "6px";

        var profile = document.createElement("a");
        profile.href = card.getAttribute("data-url");
        profile.textContent = msg("profile");
        links.appendChild(profile);

        links.appendChild(document.createTextNode("  |  "));

        var dir = document.createElement("a");
        dir.href = card.getAttribute("data-directions");
        dir.target = "_blank";
        dir.rel = "noopener";
        dir.textContent = msg("directions");
        links.appendChild(dir);

        box.appendChild(links);
        return box;
    }

    function openEntry(entry, scrollToMap) {
        if (!map || !entry.marker) return;
        info.setContent(infoNode(entry.card));
        info.open(map, entry.marker);
        map.panTo(entry.marker.getPosition());
        if (scrollToMap) {
            document.getElementById("labor-map").scrollIntoView({ behavior: "smooth", block: "center" });
        }
    }

    function highlight(card) {
        card.classList.add("labor-card-highlight");
        setTimeout(function () { card.classList.remove("labor-card-highlight"); }, 2000);
    }

    function fitMap() {
        if (!map) return;
        var bounds = new google.maps.LatLngBounds();
        var count = 0;
        entries.forEach(function (e) {
            if (e.marker && e.marker.getVisible()) { bounds.extend(e.marker.getPosition()); count++; }
        });
        if (userPos) { bounds.extend(userPos); count++; }
        if (count === 0) return;
        if (count === 1) {
            map.setCenter(bounds.getCenter());
            map.setZoom(14);
        } else {
            map.fitBounds(bounds, 50);
        }
    }

    function applyNearby() {
        if (!userPos) return;
        var radiusEl = document.getElementById("radius-select");
        var radius = radiusEl ? (parseFloat(radiusEl.value) || 0) : 0;

        entries.forEach(function (e) {
            e.distance = haversineKm(userPos.lat, userPos.lng, e.lat, e.lng);
            var d = e.card.querySelector(".labor-distance");
            if (d) d.textContent = "\uD83D\uDCCF " + e.distance.toFixed(1) + " " + msg("away");
        });

        entries.sort(function (a, b) { return a.distance - b.distance; });

        var shown = 0;
        entries.forEach(function (e) {
            if (grid) grid.appendChild(e.card);            // re-order nearest first
            var visible = !radius || e.distance <= radius;
            e.card.style.display = visible ? "" : "none";
            if (e.marker) e.marker.setVisible(visible);
            if (visible) shown++;
        });

        // Laborers without a pin go last; their distance is unknown,
        // so they are hidden while a radius filter is active.
        noCoordCards.forEach(function (c) {
            if (grid) grid.appendChild(c);
            c.style.display = radius ? "none" : "";
        });

        setStatus(shown + " " + msg("found"));
        fitMap();
    }

    function locateUser() {
        if (!navigator.geolocation) { setStatus(msg("unsupported")); return; }
        setStatus(msg("locating"));
        navigator.geolocation.getCurrentPosition(
            function (p) {
                userPos = { lat: p.coords.latitude, lng: p.coords.longitude };
                if (map) {
                    if (userMarker) userMarker.setPosition(userPos);
                    else userMarker = new google.maps.Marker({
                        position: userPos,
                        map: map,
                        title: msg("you"),
                        icon: {
                            path: google.maps.SymbolPath.CIRCLE,
                            scale: 9,
                            fillColor: "#2563eb",
                            fillOpacity: 1,
                            strokeColor: "#ffffff",
                            strokeWeight: 3
                        }
                    });
                }
                applyNearby();
            },
            function () { setStatus(msg("denied")); },
            { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
        );
    }

    // "Show on map" buttons on the cards
    function wireCardButtons() {
        entries.forEach(function (e) {
            var btn = e.card.querySelector(".show-on-map");
            if (btn) btn.addEventListener("click", function () { openEntry(e, true); highlight(e.card); });
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        collect();
        wireCardButtons();

        var findBtn = document.getElementById("find-nearby");
        if (findBtn) findBtn.addEventListener("click", locateUser);

        var radiusEl = document.getElementById("radius-select");
        if (radiusEl) radiusEl.addEventListener("change", function () {
            if (userPos) applyNearby(); else locateUser();
        });
    });

    // Called by the Google Maps script once it has loaded
    window.initLaborMap = function () {
        collect();
        var el = document.getElementById("labor-map");
        if (!el) return;

        map = new google.maps.Map(el, {
            center: { lat: 12.9716, lng: 77.5946 },
            zoom: 11,
            mapTypeControl: false,
            streetViewControl: false
        });
        info = new google.maps.InfoWindow();

        entries.forEach(function (e) {
            e.marker = new google.maps.Marker({
                position: { lat: e.lat, lng: e.lng },
                map: map,
                title: e.card.getAttribute("data-name")
            });
            e.marker.addListener("click", function () {
                openEntry(e, false);
                highlight(e.card);
                e.card.scrollIntoView({ behavior: "smooth", block: "center" });
            });
        });

        fitMap();
        if (userPos) applyNearby();   // GPS answered before the map was ready
    };
})();
