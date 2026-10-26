'use client';
import React from 'react';

interface Leg {
  trip_id: string;
  route_id: string;
  from_stop: string;
  from_stop_name: string;
  to_stop: string;
  to_stop_name: string;
  dep_time: string;
  arr_time: string;
}

interface Journey {
  total_duration: number;
  arrival_time: string;
  legs: Leg[];
}

export default function ResultsList({ journeys }: { journeys: Journey[] }) {
  if (journeys.length === 0) return null;

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold mb-4 text-slate-300 flex items-center gap-2">
        <span className="text-blue-500">✨</span> Suggested Journeys
      </h2>
      {journeys.map((journey, idx) => (
        <div key={idx} className="p-5 border border-slate-800 rounded-2xl bg-slate-900/50 backdrop-blur-sm shadow-xl hover:border-blue-500/50 transition-all group">
          <div className="flex justify-between items-center mb-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-blue-600/20 flex items-center justify-center text-blue-400 font-bold border border-blue-500/30">
                {journey.arrival_time}
              </div>
              <div className="flex flex-col">
                <span className="text-xs text-slate-400">Arrival Time</span>
                <span className="text-lg font-bold text-white">{journey.arrival_time}</span>
              </div>
            </div>
            <div className="text-right">
              <div className="text-xs text-slate-400">Duration</div>
              <div className="text-lg font-bold text-slate-200">{journey.total_duration} mins</div>
            </div>
          </div>
          <div className="space-y-4 relative before:absolute before:left-[11px] before:top-4 before:bottom-4 before:w-0.5 before:bg-slate-800">
            {journey.legs.map((leg, lIdx) => (
              <div key={lIdx} className="flex items-start gap-4 relative z-10">
                <div className="mt-2 w-6 h-6 rounded-full bg-slate-900 border-2 border-blue-500 flex items-center justify-center text-[10px] font-bold text-blue-400 shadow-lg shadow-blue-500/20">
                  {lIdx + 1}
                </div>
                <div className="flex-1 bg-slate-800/40 p-3 rounded-xl border border-slate-700 group-hover:border-slate-600 transition-colors">
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-xs font-bold uppercase tracking-wider text-blue-400">Route {leg.route_id}</span>
                    <span className="text-[10px] text-slate-500">{leg.dep_time} - {leg.arr_time}</span>
                  </div>
                  <div className="text-sm text-slate-200 font-medium">
                    {leg.from_stop_name} <span className="text-slate-500 mx-1">→</span> {leg.to_stop_name}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
