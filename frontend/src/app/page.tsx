'use client';
import React, { useState } from 'react';
import SearchForm from '../components/SearchForm';
import ResultsList from '../components/ResultsList';

export default function Home() {
  const [journeys, setJourneys] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (params: any) => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/journeys/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params),
      });
      if (!res.ok) throw new Error('No journey found');
      const data = await res.json();
      setJourneys([data]);
    } catch (e: any) {
      setError(e.message);
      setJourneys([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#0a0f1d] text-white p-4 md:p-8 font-sans">
      <div className="max-w-4xl mx-auto space-y-12">
        {/* Hero Section */}
        <header className="relative text-center py-12 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-blue-900/20 to-transparent pointer-events-none" />
          <h1 className="text-5xl md:text-6xl font-black tracking-tight mb-4 bg-clip-text text-transparent bg-gradient-to-r from-white via-blue-200 to-blue-400">
            Chennai <span className="text-blue-500">Transit</span> Planner
          </h1>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto">
            Find the fastest route across Bus, Metro, and Rail with real-time GTFS schedules.
          </p>

          {/* Mode Selectors (Visual Only) */}
          <div className="flex justify-center gap-3 mt-8">
            {['Bus', 'Metro', 'Rail'].map(mode => (
              <div key={mode} className="px-4 py-1.5 rounded-full bg-slate-800 border border-slate-700 text-xs font-medium text-slate-300 flex items-center gap-2 hover:bg-slate-700 transition-colors cursor-pointer">
                <div className={`w-2 h-2 rounded-full ${mode === 'Bus' ? 'bg-blue-500' : mode === 'Metro' ? 'bg-purple-500' : 'bg-green-500'}`} />
                {mode}
              </div>
            ))}
          </div>
        </header>

        {/* Search Area */}
        <div className="relative z-10 max-w-3xl mx-auto">
          <SearchForm onSearch={handleSearch} />
        </div>

        {loading && <div className="text-center text-blue-400 font-medium animate-pulse">Calculating best route...</div>}
        {error && <div className="text-center text-red-400 font-medium">{error}</div>}

        {/* Centered Journey Results */}
        <div className="flex justify-center">
          <div className="w-full max-w-2xl">
            <ResultsList journeys={journeys} />
          </div>
        </div>
      </div>
    </main>
  );
}

