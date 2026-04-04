"""
Google Maps API integration for route planning and place search.
"""

import asyncio
import logging
import math
import re
from typing import Optional

import httpx

from config.config import api_config

logger = logging.getLogger(__name__)

ROUTES_API_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"
PLACES_API_URL = "https://places.googleapis.com/v1/places:searchText"

PLACES_FIELD_MASK = (
    "places.displayName,"
    "places.formattedAddress,"
    "places.location,"
    "places.rating,"
    "places.editorialSummary"
)


def _get_api_key() -> str:
    """Get the Google Maps API key."""
    if not api_config.maps_api_key:
        raise ValueError("GOOGLE_MAPS_API_KEY is not configured")
    return api_config.maps_api_key


def _parse_location(location_str: str) -> dict:
    """Parse a location string into an API-compatible format."""
    coord_pattern = r"^(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)$"
    match = re.match(coord_pattern, location_str.strip())
    if match:
        return {
            "location": {
                "latLng": {
                    "latitude": float(match.group(1)),
                    "longitude": float(match.group(2)),
                }
            }
        }
    return {"address": location_str}


def _decode_polyline(encoded: str) -> list[tuple[float, float]]:
    """Decode a Google encoded polyline into a list of (lat, lng) tuples."""
    if not encoded:
        return []
    points = []
    index = 0
    lat = 0
    lng = 0
    try:
        while index < len(encoded):
            # Decode latitude
            shift = 0
            result = 0
            while True:
                if index >= len(encoded):
                    return points
                b = ord(encoded[index]) - 63
                index += 1
                result |= (b & 0x1F) << shift
                shift += 5
                if b < 0x20:
                    break
            lat += (~(result >> 1) if (result & 1) else (result >> 1))

            # Decode longitude
            shift = 0
            result = 0
            while True:
                if index >= len(encoded):
                    return points
                b = ord(encoded[index]) - 63
                index += 1
                result |= (b & 0x1F) << shift
                shift += 5
                if b < 0x20:
                    break
            lng += (~(result >> 1) if (result & 1) else (result >> 1))

            points.append((lat / 1e5, lng / 1e5))
    except (IndexError, ValueError):
        logger.warning(f"Failed to decode polyline (length={len(encoded)}), returning {len(points)} points decoded so far")
    return points


def _haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Calculate distance in meters between two lat/lng points."""
    R = 6371000  # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _compute_cumulative_distances(points: list[tuple[float, float]]) -> list[float]:
    """Compute cumulative distances along a polyline."""
    distances = [0.0]
    for i in range(1, len(points)):
        d = _haversine_distance(points[i - 1][0], points[i - 1][1], points[i][0], points[i][1])
        distances.append(distances[-1] + d)
    return distances


def _sample_points_evenly(points: list[tuple[float, float]], n: int) -> list[tuple[float, float]]:
    """Sample n evenly-spaced points along a polyline (excluding endpoints)."""
    if n <= 0 or len(points) < 2:
        return []

    cumulative = _compute_cumulative_distances(points)
    total_distance = cumulative[-1]
    if total_distance == 0:
        return [points[len(points) // 2]]

    # Sample at positions 1/(n+1), 2/(n+1), ..., n/(n+1) along the route
    sampled = []
    for i in range(1, n + 1):
        target_dist = total_distance * i / (n + 1)
        # Find the segment containing this distance
        for j in range(1, len(cumulative)):
            if cumulative[j] >= target_dist:
                # Interpolate between points[j-1] and points[j]
                seg_len = cumulative[j] - cumulative[j - 1]
                if seg_len == 0:
                    sampled.append(points[j])
                else:
                    ratio = (target_dist - cumulative[j - 1]) / seg_len
                    lat = points[j - 1][0] + ratio * (points[j][0] - points[j - 1][0])
                    lng = points[j - 1][1] + ratio * (points[j][1] - points[j - 1][1])
                    sampled.append((lat, lng))
                break
    return sampled


def _find_nearest_point_on_route(
    points: list[tuple[float, float]],
    target_lat: float,
    target_lng: float,
) -> tuple[int, float]:
    """Find the index and distance of the nearest point on the route to a target location."""
    min_dist = float("inf")
    min_idx = 0
    for i, (lat, lng) in enumerate(points):
        d = _haversine_distance(lat, lng, target_lat, target_lng)
        if d < min_dist:
            min_dist = d
            min_idx = i
    return min_idx, min_dist


async def _search_single_point(
    client: httpx.AsyncClient,
    api_key: str,
    query: str,
    lat: float,
    lng: float,
    radius: float = 3000,
    max_results: int = 1,
) -> list[dict]:
    """Search for places near a single point."""
    request_body = {
        "textQuery": query,
        "locationBias": {
            "circle": {
                "center": {"latitude": lat, "longitude": lng},
                "radius": radius,
            }
        },
        "languageCode": "zh-TW",
        "maxResultCount": max_results,
    }
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": PLACES_FIELD_MASK,
    }

    response = await client.post(PLACES_API_URL, json=request_body, headers=headers)
    response.raise_for_status()
    data = response.json()

    places = []
    for place in data.get("places", []):
        display_name = place.get("displayName", {})
        location = place.get("location", {})
        editorial = place.get("editorialSummary", {})
        places.append({
            "name": display_name.get("text", ""),
            "address": place.get("formattedAddress", ""),
            "lat": location.get("latitude"),
            "lng": location.get("longitude"),
            "rating": place.get("rating"),
            "description": editorial.get("text", ""),
        })
    return places


async def compute_route(
    origin: str, destination: str, travel_mode: str = "DRIVE"
) -> dict:
    """Compute a route between origin and destination using Google Routes API."""
    api_key = _get_api_key()

    request_body = {
        "origin": _parse_location(origin),
        "destination": _parse_location(destination),
        "travelMode": travel_mode,
        "computeAlternativeRoutes": False,
        "languageCode": "zh-TW",
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": (
            "routes.duration,"
            "routes.distanceMeters,"
            "routes.polyline.encodedPolyline,"
            "routes.legs.startLocation,"
            "routes.legs.endLocation,"
            "routes.legs.steps.navigationInstruction"
        ),
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                ROUTES_API_URL, json=request_body, headers=headers
            )
            response.raise_for_status()
            data = response.json()

        if not data.get("routes"):
            return {"error": "No routes found", "origin": origin, "destination": destination}

        route = data["routes"][0]
        duration_str = route.get("duration", "0s")
        duration_seconds = int(duration_str.rstrip("s"))
        duration_minutes = round(duration_seconds / 60)

        steps = []
        legs = route.get("legs", [])
        for leg in legs:
            for step in leg.get("steps", []):
                nav = step.get("navigationInstruction", {})
                if nav.get("instructions"):
                    steps.append(nav["instructions"])

        origin_latlng = None
        destination_latlng = None
        if legs:
            start_loc = legs[0].get("startLocation", {}).get("latLng", {})
            end_loc = legs[-1].get("endLocation", {}).get("latLng", {})
            if start_loc:
                origin_latlng = {
                    "lat": start_loc.get("latitude"),
                    "lng": start_loc.get("longitude"),
                }
            if end_loc:
                destination_latlng = {
                    "lat": end_loc.get("latitude"),
                    "lng": end_loc.get("longitude"),
                }

        result = {
            "origin": origin,
            "destination": destination,
            "distance_meters": route.get("distanceMeters", 0),
            "distance_km": round(route.get("distanceMeters", 0) / 1000, 1),
            "duration_seconds": duration_seconds,
            "duration_minutes": duration_minutes,
            "encoded_polyline": route.get("polyline", {}).get("encodedPolyline", ""),
            "steps": steps[:10],
            "origin_latlng": origin_latlng,
            "destination_latlng": destination_latlng,
        }

        logger.info(
            f"Route computed: {origin} -> {destination}, "
            f"{result['distance_km']}km, {duration_minutes}min"
        )
        return result

    except httpx.HTTPStatusError as e:
        logger.error(f"Routes API error: {e.response.status_code} - {e.response.text}")
        return {"error": f"Routes API error: {e.response.status_code}", "details": e.response.text}
    except Exception as e:
        logger.error(f"Error computing route: {e}")
        return {"error": str(e)}


async def search_places_along_route(
    query: str,
    route_polyline: str,
    focus_location: Optional[str] = None,
    max_results: int = 5,
) -> dict:
    """Search for places along a route with even distribution or focused on a specific area.

    When focus_location is provided, searches are concentrated around that area on the route.
    When not provided, results are evenly distributed along the entire route.

    Args:
        query: Search query (e.g., "景點", "餐廳", "休息站")
        route_polyline: Encoded polyline from compute_route result
        focus_location: Optional location name to focus the search (e.g., "內湖", "新竹")
        max_results: Maximum number of results (default 5)
    """
    api_key = _get_api_key()

    try:
        points = _decode_polyline(route_polyline)
        if len(points) < 2:
            return {"error": "Invalid or missing route polyline. Please call compute_route first to get a valid route.", "query": query}

        cumulative = _compute_cumulative_distances(points)
        total_distance = cumulative[-1]

        async with httpx.AsyncClient(timeout=15.0) as client:

            if focus_location:
                # Geocode the focus location to get coordinates
                focus_coords = await _geocode_location(client, api_key, focus_location)

                if focus_coords:
                    focus_lat, focus_lng = focus_coords
                    # Find the nearest point on the route
                    nearest_idx, nearest_dist = _find_nearest_point_on_route(
                        points, focus_lat, focus_lng
                    )
                    focus_point = points[nearest_idx]

                    # Determine search radius based on route length
                    # Use ~15% of total route length, minimum 2km, maximum 10km
                    radius = max(2000, min(10000, total_distance * 0.15))

                    logger.info(
                        f"Focus search near {focus_location} ({focus_lat:.4f}, {focus_lng:.4f}), "
                        f"nearest route point index={nearest_idx}, radius={radius:.0f}m"
                    )

                    # Search near the focus point with all results
                    places = await _search_single_point(
                        client, api_key, query,
                        focus_point[0], focus_point[1],
                        radius=radius,
                        max_results=max_results,
                    )
                else:
                    # Geocoding failed, fall back to text search with location bias
                    logger.warning(f"Could not geocode focus_location: {focus_location}, using text search fallback")
                    places = await _search_single_point(
                        client, api_key, f"{query} {focus_location}",
                        points[len(points) // 2][0], points[len(points) // 2][1],
                        radius=10000,
                        max_results=max_results,
                    )
            else:
                # Even distribution: sample N points along the route, 1 result per point
                sample_points = _sample_points_evenly(points, max_results)
                logger.info(
                    f"Even distribution search: {len(sample_points)} sample points "
                    f"along {total_distance / 1000:.1f}km route"
                )

                # Search all points concurrently
                tasks = [
                    _search_single_point(
                        client, api_key, query,
                        pt[0], pt[1],
                        radius=max(2000, min(5000, total_distance / max_results * 0.3)),
                        max_results=2,  # Get 2 per point, then deduplicate and pick best
                    )
                    for pt in sample_points
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)

                # Collect results, 1 best per sample point, deduplicate by name
                places = []
                seen_names = set()
                for result in results:
                    if isinstance(result, Exception):
                        logger.warning(f"Search point failed: {result}")
                        continue
                    for place in result:
                        if place["name"] and place["name"] not in seen_names:
                            places.append(place)
                            seen_names.add(place["name"])
                            break  # Only take 1 per sample point

        places = places[:max_results]
        logger.info(f"Found {len(places)} places along route for query: {query}")
        return {"query": query, "places": places, "count": len(places)}

    except httpx.HTTPStatusError as e:
        logger.error(f"Places API error: {e.response.status_code} - {e.response.text}")
        return {"error": f"Places API error: {e.response.status_code}", "details": e.response.text, "query": query}
    except Exception as e:
        logger.error(f"Error searching places along route: {e}")
        return {"error": str(e), "query": query}


async def _geocode_location(
    client: httpx.AsyncClient, api_key: str, location_name: str
) -> Optional[tuple[float, float]]:
    """Geocode a location name to (lat, lng) using Places API text search."""
    try:
        response = await client.post(
            PLACES_API_URL,
            json={"textQuery": location_name, "languageCode": "zh-TW", "maxResultCount": 1},
            headers={
                "Content-Type": "application/json",
                "X-Goog-Api-Key": api_key,
                "X-Goog-FieldMask": "places.location",
            },
        )
        response.raise_for_status()
        data = response.json()
        places = data.get("places", [])
        if places:
            loc = places[0].get("location", {})
            return (loc.get("latitude"), loc.get("longitude"))
    except Exception as e:
        logger.error(f"Geocoding failed for {location_name}: {e}")
    return None


async def search_nearby_places(
    query: str,
    latitude: float,
    longitude: float,
    radius_meters: float = 5000,
) -> dict:
    """Search for places near a location using Google Places API (Text Search)."""
    api_key = _get_api_key()

    request_body = {
        "textQuery": query,
        "locationBias": {
            "circle": {
                "center": {"latitude": latitude, "longitude": longitude},
                "radius": radius_meters,
            }
        },
        "languageCode": "zh-TW",
        "maxResultCount": 5,
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": PLACES_FIELD_MASK,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                PLACES_API_URL, json=request_body, headers=headers
            )
            response.raise_for_status()
            data = response.json()

        places = []
        for place in data.get("places", []):
            display_name = place.get("displayName", {})
            location = place.get("location", {})
            editorial = place.get("editorialSummary", {})
            places.append({
                "name": display_name.get("text", ""),
                "address": place.get("formattedAddress", ""),
                "lat": location.get("latitude"),
                "lng": location.get("longitude"),
                "rating": place.get("rating"),
                "description": editorial.get("text", ""),
            })

        logger.info(f"Found {len(places)} nearby places for query: {query}")
        return {"query": query, "places": places, "count": len(places)}

    except httpx.HTTPStatusError as e:
        logger.error(f"Places API error: {e.response.status_code} - {e.response.text}")
        return {"error": f"Places API error: {e.response.status_code}", "details": e.response.text, "query": query}
    except Exception as e:
        logger.error(f"Error searching nearby places: {e}")
        return {"error": str(e), "query": query}
