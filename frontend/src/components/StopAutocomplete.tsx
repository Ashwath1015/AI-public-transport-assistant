'use client';
import React, { useState, useEffect } from 'react';

interface Stop {
  stop_id: string;
  stop_name: string;
  stop_lat: number;
  stop_lon: number;
}

interface StopAutocompleteProps {
  label: string;
  value: string;
  onChange: (value: string, stopId?: string) => void;
  placeholder: string;
}

export default function StopAutocomplete({ label, value, onChange, placeholder }: StopAutocompleteProps) {
  const [suggestions, setSuggestions] = useState<Stop[]>([]);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const fetchStops = async () => {
      if (value.length < 2) {
        setSuggestions([]);
        return;
      }
        try {
          const res = await fetch(`http://127.0.0.1:8000/api/stops/search?q=${encodeURIComponent(value)}`);
          const data = await res.json();
        setSuggestions(data);
      } catch (e) {
        console.error("Error fetching stops:", e);
      }
    };

    const timer = setTimeout(fetchStops, 300);
    return () => clearTimeout(timer);
  }, [value]);

  return (
    <div className="relative w-full group">
      <input
        type="text"
        className="w-full p-3 bg-slate-800 border border-slate-700 rounded-xl text-white outline-none focus:ring-2 focus:ring-blue-500 transition-all placeholder-slate-500"
        placeholder={placeholder}
        value={value}
        onChange={(e) => {
          onChange(e.target.value);
          setIsOpen(true);
        }}
        onFocus={() => setIsOpen(true)}
      />
      {isOpen && suggestions.length > 0 && (
        <ul className="absolute z-50 w-full mt-2 bg-slate-900 border border-slate-700 rounded-xl shadow-2xl max-h-60 overflow-auto py-2 animate-in fade-in slide-in-from-top-2 duration-200">
          {suggestions.map((stop) => (
            <li
              key={stop.stop_id}
              className="px-4 py-3 hover:bg-blue-600 hover:text-white cursor-pointer text-slate-300 transition-colors flex items-center gap-3 border-b border-slate-800 last:border-b-0"
              onClick={() => {
                onChange(stop.stop_name, stop.stop_id);
                setIsOpen(false);
              }}
            >
              <span className="text-slate-500 group-hover:text-blue-300">📍</span>
              <span className="text-sm font-medium">{stop.stop_name}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
