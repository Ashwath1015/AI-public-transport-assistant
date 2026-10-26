'use client';
import React, { useState } from 'react';
import StopAutocomplete from './StopAutocomplete';
import ResultsList from './ResultsList';
import TransitMap from './TransitMap';

export default function SearchForm({ onSearch }: { onSearch: (params: any) => void }) {
  const [origin, setOrigin] = useState({ name: '', id: '' });
  const [dest, setDest] = useState({ name: '', id: '' });
  const [time, setTime] = useState('08:00'); // Default 8:00 AM (HH:mm)

  const convertToMinutes = () => {
    const [hours, minutes] = time.split(':').map(Number);
    return hours * 60 + minutes;
  };

  return (
    <div className="p-8 bg-slate-900/50 backdrop-blur-md rounded-3xl border border-slate-800 shadow-2xl space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-slate-400 text-sm font-medium ml-1">
            <span className="text-blue-500">📍</span> From
          </div>
          <StopAutocomplete
            label=""
            placeholder="Search origin stop..."
            value={origin.name}
            onChange={(name, id) => setOrigin({ name, id: id || '' })}
          />
        </div>
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-slate-400 text-sm font-medium ml-1">
            <span className="text-blue-500">🏁</span> To
          </div>
          <StopAutocomplete
            label=""
            placeholder="Search destination stop..."
            value={dest.name}
            onChange={(name, id) => setDest({ name, id: id || '' })}
          />
        </div>
      </div>
      <div className="flex items-end gap-6">
        <div className="flex-1 space-y-2">
          <div className="flex items-center gap-2 text-slate-400 text-sm font-medium ml-1">
            <span className="text-blue-500">🕒</span> Departure Time
          </div>
          <input
            type="time"
            className="w-full p-3 bg-slate-800 border border-slate-700 rounded-xl text-white outline-none focus:ring-2 focus:ring-blue-500 transition-all"
            value={time}
            onChange={(e) => setTime(e.target.value)}
          />
        </div>
        <button
          onClick={() => onSearch({
            origin_id: origin.id,
            destination_id: dest.id,
            departure_time: convertToMinutes()
          })}
          className="px-8 py-3 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-500 transition-all shadow-lg shadow-blue-900/20 h-[50px]"
        >
          Search
        </button>
      </div>
    </div>
  );
}
