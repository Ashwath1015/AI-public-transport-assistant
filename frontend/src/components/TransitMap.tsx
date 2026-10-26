'use client';
import React, { useEffect, useRef } from 'react';
import * as maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

interface TransitMapProps {
  originCoords?: [number, number];
  destCoords?: [number, number];
  pathCoords?: [number, number][];
}

export default function TransitMap({ originCoords, destCoords, pathCoords }: TransitMapProps) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const markers = useRef<maplibregl.Marker[]>([]);

  useEffect(() => {
    if (!mapContainer.current) return;

    if (!map.current) {
      try {
        map.current = new maplibregl.Map({
          container: mapContainer.current,
          style: 'https://basemaps.cartocdn.com/gl/voyager-style/style.json',
          center: [80.2707, 13.0827], // Chennai
          zoom: 12,
          attributionControl: false, // Removes the MapLibre attribution bar
        });
      } catch (e) {
        console.error("Map initialization failed:", e);
      }
    }

    return () => {
      // Cleanup handled by ref
    };
  }, []);


  useEffect(() => {
    if (!map.current) return;

    const updateMap = () => {
      console.log("TransitMap: Updating map with pathCoords:", pathCoords);

      markers.current.forEach(m => m.remove());
      markers.current = [];

      if (map.current.getSource('route')) {
        try {
          if (map.current.getLayer('route-layer')) {
            map.current.removeLayer('route-layer');
          }
          map.current.removeSource('route');
        } catch (e) {
          console.warn("Error cleaning up map layers:", e);
        }
      }

      if (pathCoords && pathCoords.length > 0) {
        if (pathCoords.length > 1) {
          map.current.addSource('route', {
            type: 'geojson',
            data: {
              type: 'Feature',
              geometry: {
                type: 'LineString',
                coordinates: pathCoords,
              },
              properties: {},
            },
          });

          map.current.addLayer({
            id: 'route-layer',
            type: 'line',
            source: 'route',
            layout: {
              'line-join': 'round',
              'line-cap': 'round'
            },
            paint: {
              'line-color': '#3b82f6',
              'line-width': 6,
              'line-opacity': 1
            },
          });
        }

        const start = pathCoords[0];
        const startMarker = new maplibregl.Marker({ color: '#3b82f6' })
          .setLngLat(start)
          .setPopup(new maplibregl.Popup().setHTML('<strong style="color:black">Origin</strong>'))
          .addTo(map.current);
        markers.current.push(startMarker);

        const end = pathCoords[pathCoords.length - 1];
        const endMarker = new maplibregl.Marker({ color: '#ef4444' })
          .setLngLat(end)
          .setPopup(new maplibregl.Popup().setHTML('<strong style="color:black">Destination</strong>'))
          .addTo(map.current);
        markers.current.push(endMarker);

        const bounds = new maplibregl.LngLatBounds();
        pathCoords.forEach(coord => bounds.extend(coord));
        map.current.fitBounds(bounds, { padding: 80, maxZoom: 14 });
      }
    };

    if (map.current.loaded()) {
      updateMap();
    } else {
      map.current.once('load', updateMap);
    }
  }, [pathCoords]);

  return <div ref={mapContainer} className="w-full h-full min-h-[400px] rounded-lg" />;
}
