function showName() { // Laat jouw voornaam zien wanneer je deze invult bij 'Hallo,' [user/update.html]
    var firstname = document.getElementById('firstname').value;
    document.getElementById("welcome-message").innerHTML = "Hi, " + firstname;
}

function allowName() {
    var friendCode = document.getElementById("shareFilo").value;

    if (friendCode.includes("#") && friendCode != null) {
        // Create cookie with friend code
        document.cookie = `friendCode=${friendCode}`;
        window.location.href = "/user/add_friend";
    }
    else {
        document.getElementById("shareFilo").style.border = "1px solid red";
    }
}

window.onload = function () {
    var fileName = location.href.split("/").slice(-1);
    if (fileName == "add_friend") {
        var cookieValue = document.cookie.replace(/(?:(?:^|.*;\s*)friendCode\s*\=\s*([^;]*).*$)|^.*$/, "$1");
        document.getElementById("friendCodeForm").value = cookieValue;
        var friendName = cookieValue.split("#")[0]
        document.getElementById("addFriend").innerHTML = "Are you sure you want to give " + friendName + " access to your Filo?"
    }
}

var url = "https://test.findlock.site/api/rest/front/location/00000000-0000-0000-0000-000000000001";
//var url = "http://145.93.73.115:5500/auth/test.html" // html clone on same url

function getFiloLocation(theUrl) {
    var response = null;
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            response = xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET", theUrl, false);
    xmlhttp.send(null);
    return JSON.parse(response);
}

var getClientPosition = function (options) {
    return new Promise(function (resolve, reject) {
        navigator.geolocation.getCurrentPosition(resolve, reject, options);
    });
}

function getMyLocation() {
    if (navigator.geolocation) {
        return navigator.geolocation.getCurrentPosition(myLocation);
    } else {
        document.getElementById("distancePlaceholder").innerHTML = "Geolocation is not supported.";
    }
}

function myLocation(position) {
    try {
        var myLat = position.coords.latitude;
        var myLng = position.coords.longitude;
        return myLatLng = [myLat, myLng];
    }
    catch {
        return "location blocked";
    }
}

function getStreetName(filoLatLng) {
    var response = null;
    var googleUrl = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + filoLatLng["lat"] + "," + filoLatLng["lng"] + "&key=AIzaSyAClXIExou7iQYu86wCiVV43mLw90kDQ0o";

    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            response = xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET", googleUrl, false);
    xmlhttp.send(null);

    // Get right items
    var reverseLookup = JSON.parse(response);
    var reverseLookupData = reverseLookup["results"][0]["address_components"];
    var streetName = reverseLookupData[1]["short_name"];
    var streetNr = reverseLookupData[0]["short_name"];
    var city = reverseLookupData[3]["short_name"];
    return `${streetName} ${streetNr}, ${city}`;
}

function getDistance(myLatLng, filoLatLng) {
    var p1 = new google.maps.LatLng(myLatLng[0], myLatLng[1]);
    var p2 = new google.maps.LatLng(filoLatLng["lat"], filoLatLng["lng"]);
    var kmValue = (google.maps.geometry.spherical.computeDistanceBetween(p1, p2) / 1000).toFixed(1);
    return `${kmValue} km`;
}

function setLocationInfo(filoLatLng, myLatLng) {
    // Set location information
    document.getElementById("locationPlaceholder").innerHTML = getStreetName(filoLatLng);

    try {
        document.getElementById("distancePlaceholder").innerHTML = getDistance(myLatLng, filoLatLng);
    }
    catch { document.getElementById("distancePlaceholder").innerHTML = "Allow location service for distance"; }
}

function initMap() {
    // Get Filo location
    var filoLocationObj = getFiloLocation(url);
    var filoLatLng = { lat: parseFloat(filoLocationObj["lat"]), lng: parseFloat(filoLocationObj["lng"]) };

    getClientPosition().then((position) => {
        var myLatLng = [position.coords.latitude, position.coords.longitude]
        console.log("Promise loc:", myLatLng);

        setLocationInfo(filoLatLng, myLatLng);

        var map = new google.maps.Map(
            document.getElementById('map'), {
            zoom: 15,
            center: filoLatLng,
            disableDefaultUI: true,
            styles: mapStyle
        });
        var filoIcon = new google.maps.Marker({
            position: filoLatLng,
            map: map,
            icon: "/static/images/MapMarker.svg"
        })
        var myPosIcon = new google.maps.Marker({
            position: { lat: myLatLng[0], lng: myLatLng[1] },
            map: map,
            icon: "/static/images/my-location.png"
        })

        // Zoom until both markers are on screen
        var zoomValue = 15;
        var doneZooming = false;
        var latMid = (filoLatLng["lat"] + myLatLng[0]) / 2;
        var lngMid = (filoLatLng["lng"] + myLatLng[1]) / 2;
        map.setCenter({ lat: latMid, lng: lngMid });
        google.maps.event.addListener(map, 'bounds_changed', function () {
            while (!map.getBounds().contains(filoIcon.getPosition()) && !doneZooming) {
                zoomValue = zoomValue - 1.1;
                map.setZoom(zoomValue);
            }
            doneZooming = true;
        });
    })









}

var mapStyle =
    [
        {
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#f5f5f5"
                }
            ]
        },
        {
            "elementType": "labels.icon",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#616161"
                }
            ]
        },
        {
            "elementType": "labels.text.stroke",
            "stylers": [
                {
                    "color": "#f5f5f5"
                }
            ]
        },
        {
            "featureType": "administrative.land_parcel",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#bdbdbd"
                }
            ]
        },
        {
            "featureType": "poi",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#eeeeee"
                }
            ]
        },
        {
            "featureType": "poi",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#757575"
                }
            ]
        },
        {
            "featureType": "poi.park",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#e5e5e5"
                }
            ]
        },
        {
            "featureType": "poi.park",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#9e9e9e"
                }
            ]
        },
        {
            "featureType": "road",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#ffffff"
                }
            ]
        },
        {
            "featureType": "road.arterial",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#757575"
                }
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#dadada"
                }
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#616161"
                }
            ]
        },
        {
            "featureType": "road.local",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#9e9e9e"
                }
            ]
        },
        {
            "featureType": "transit.line",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#e5e5e5"
                }
            ]
        },
        {
            "featureType": "transit.station",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#eeeeee"
                }
            ]
        },
        {
            "featureType": "water",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#AED1D1"
                }
            ]
        },
        {
            "featureType": "water",
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "#9e9e9e"
                }
            ]
        }
    ]