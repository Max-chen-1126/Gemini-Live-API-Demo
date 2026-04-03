/**
 * Google Maps handler for route visualization and place markers.
 */

export class MapHandler {
    constructor() {
        this.map = null;
        this.routePolyline = null;
        this.markers = [];
        this.infoWindows = [];
        this.bounds = null;
        this.containerEl = null;
    }

    /**
     * Initialize the Google Map instance.
     * @param {string} containerId - The ID of the map container element
     * @param {HTMLElement} containerEl - The map container wrapper element (for show/hide)
     */
    initialize(containerId, containerEl) {
        this.containerEl = containerEl;

        // Default center: Taipei
        const defaultCenter = { lat: 25.0330, lng: 121.5654 };

        this.map = new google.maps.Map(document.getElementById(containerId), {
            center: defaultCenter,
            zoom: 12,
            disableDefaultUI: false,
            zoomControl: true,
            mapTypeControl: false,
            streetViewControl: false,
            fullscreenControl: true,
        });
    }

    /**
     * Draw a route on the map from an encoded polyline.
     * @param {string} encodedPolyline - The encoded polyline string from Routes API
     * @param {object} [originLatLng] - Origin coordinates {lat, lng}
     * @param {object} [destinationLatLng] - Destination coordinates {lat, lng}
     */
    drawRoute(encodedPolyline, originLatLng, destinationLatLng) {
        // Clear previous route
        if (this.routePolyline) {
            this.routePolyline.setMap(null);
        }

        // Decode the polyline
        const path = google.maps.geometry.encoding.decodePath(encodedPolyline);

        // Draw the polyline
        this.routePolyline = new google.maps.Polyline({
            path: path,
            geodesic: true,
            strokeColor: '#4285F4',
            strokeOpacity: 0.9,
            strokeWeight: 5,
        });

        this.routePolyline.setMap(this.map);

        // Fit bounds to show the entire route
        this.bounds = new google.maps.LatLngBounds();
        path.forEach((point) => this.bounds.extend(point));

        // Add origin marker
        if (originLatLng) {
            const originMarker = new google.maps.Marker({
                position: originLatLng,
                map: this.map,
                label: {
                    text: 'A',
                    color: 'white',
                    fontWeight: 'bold',
                },
                title: 'Origin',
            });
            this.markers.push(originMarker);
            this.bounds.extend(originLatLng);
        }

        // Add destination marker
        if (destinationLatLng) {
            const destMarker = new google.maps.Marker({
                position: destinationLatLng,
                map: this.map,
                label: {
                    text: 'B',
                    color: 'white',
                    fontWeight: 'bold',
                },
                title: 'Destination',
            });
            this.markers.push(destMarker);
            this.bounds.extend(destinationLatLng);
        }

        this.map.fitBounds(this.bounds, { padding: 50 });
        this.show();
    }

    /**
     * Add place markers to the map.
     * @param {Array} places - Array of place objects {name, address, lat, lng, rating, description}
     */
    addPlaceMarkers(places) {
        // Close any open info windows
        this.infoWindows.forEach((iw) => iw.close());

        places.forEach((place, index) => {
            if (!place.lat || !place.lng) return;

            const position = { lat: place.lat, lng: place.lng };

            const marker = new google.maps.Marker({
                position: position,
                map: this.map,
                icon: {
                    url: 'https://maps.google.com/mapfiles/ms/icons/yellow-dot.png',
                },
                title: place.name,
                animation: google.maps.Animation.DROP,
            });

            // Build info window content
            let content = `<div style="max-width:250px;font-family:sans-serif;">`;
            content += `<h3 style="margin:0 0 4px;font-size:14px;color:#1a73e8;">${place.name}</h3>`;
            if (place.rating) {
                content += `<p style="margin:0 0 4px;font-size:12px;color:#f4b400;">`;
                content += '★'.repeat(Math.round(place.rating));
                content += ` ${place.rating}</p>`;
            }
            if (place.address) {
                content += `<p style="margin:0 0 4px;font-size:12px;color:#666;">${place.address}</p>`;
            }
            if (place.description) {
                content += `<p style="margin:0;font-size:12px;color:#333;">${place.description}</p>`;
            }
            content += `</div>`;

            const infoWindow = new google.maps.InfoWindow({ content });

            marker.addListener('click', () => {
                // Close other info windows
                this.infoWindows.forEach((iw) => iw.close());
                infoWindow.open(this.map, marker);
            });

            this.markers.push(marker);
            this.infoWindows.push(infoWindow);

            // Extend bounds if we have them
            if (this.bounds) {
                this.bounds.extend(position);
            }
        });

        // Re-fit bounds to include new markers
        if (this.bounds && places.length > 0) {
            this.map.fitBounds(this.bounds, { padding: 50 });
        }
    }

    /**
     * Clear all routes and markers from the map.
     */
    clearAll() {
        if (this.routePolyline) {
            this.routePolyline.setMap(null);
            this.routePolyline = null;
        }
        this.markers.forEach((m) => m.setMap(null));
        this.markers = [];
        this.infoWindows.forEach((iw) => iw.close());
        this.infoWindows = [];
        this.bounds = null;
    }

    /**
     * Show the map container.
     */
    show() {
        if (this.containerEl) {
            this.containerEl.classList.remove('hidden');
            this.containerEl.classList.remove('collapsed');
            // Trigger map resize after showing
            if (this.map) {
                google.maps.event.trigger(this.map, 'resize');
                if (this.bounds) {
                    this.map.fitBounds(this.bounds, { padding: 50 });
                }
            }
        }
    }

    /**
     * Hide the map container.
     */
    hide() {
        if (this.containerEl) {
            this.containerEl.classList.add('hidden');
        }
    }

    /**
     * Toggle the map container visibility.
     */
    toggle() {
        if (this.containerEl) {
            if (this.containerEl.classList.contains('hidden') || this.containerEl.classList.contains('collapsed')) {
                this.show();
            } else {
                this.containerEl.classList.add('collapsed');
            }
        }
    }
}
