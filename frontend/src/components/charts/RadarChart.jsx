import React from 'react';

const RadarChart = ({ data = [
  { label: 'DSA & Coding', value: 85, fullMark: 100 },
  { label: 'System Design', value: 65, fullMark: 100 },
  { label: 'Frontend / UI', value: 90, fullMark: 100 },
  { label: 'Backend & DB', value: 80, fullMark: 100 },
  { label: 'Communication', value: 75, fullMark: 100 },
] }) => {
  const size = 280;
  const center = size / 2;
  const radius = center - 45;
  const total = data.length;

  // Helper to calculate coordinates
  const getCoordinates = (index, value) => {
    const angle = (Math.PI * 2 / total) * index - Math.PI / 2;
    const distance = (value / 100) * radius;
    const x = center + distance * Math.cos(angle);
    const y = center + distance * Math.sin(angle);
    return { x, y };
  };

  // Polygon points for grid levels (20%, 40%, 60%, 80%, 100%)
  const levels = [0.2, 0.4, 0.6, 0.8, 1.0];

  const gridPolygons = levels.map((lvl) => {
    return Array.from({ length: total }, (_, i) => {
      const angle = (Math.PI * 2 / total) * i - Math.PI / 2;
      const x = center + radius * lvl * Math.cos(angle);
      const y = center + radius * lvl * Math.sin(angle);
      return `${x},${y}`;
    }).join(' ');
  });

  // Data polygon points
  const dataPoints = data.map((d, i) => {
    const coords = getCoordinates(i, d.value);
    return `${coords.x},${coords.y}`;
  }).join(' ');

  return (
    <div className="flex flex-col items-center justify-center">
      <svg width={size} height={size} className="overflow-visible">
        {/* Background Grids */}
        {gridPolygons.map((points, idx) => (
          <polygon
            key={idx}
            points={points}
            fill="none"
            stroke="#374151"
            strokeWidth="1"
            strokeDasharray={idx === levels.length - 1 ? 'none' : '3,3'}
          />
        ))}

        {/* Axis Lines */}
        {data.map((_, i) => {
          const coords = getCoordinates(i, 100);
          return (
            <line
              key={i}
              x1={center}
              y1={center}
              x2={coords.x}
              y2={coords.y}
              stroke="#374151"
              strokeWidth="1"
            />
          );
        })}

        {/* Data Area */}
        <polygon
          points={dataPoints}
          fill="rgba(59, 130, 246, 0.25)"
          stroke="#3b82f6"
          strokeWidth="2.5"
        />

        {/* Data Points */}
        {data.map((d, i) => {
          const coords = getCoordinates(i, d.value);
          return (
            <circle
              key={i}
              cx={coords.x}
              cy={coords.y}
              r="4"
              fill="#60a5fa"
              stroke="#1e3a8a"
              strokeWidth="2"
            />
          );
        })}

        {/* Labels */}
        {data.map((d, i) => {
          const angle = (Math.PI * 2 / total) * i - Math.PI / 2;
          const labelDist = radius + 25;
          const lx = center + labelDist * Math.cos(angle);
          const ly = center + labelDist * Math.sin(angle);
          return (
            <text
              key={i}
              x={lx}
              y={ly}
              textAnchor="middle"
              dominantBaseline="middle"
              className="text-[10px] font-semibold fill-gray-300"
            >
              {d.label}
            </text>
          );
        })}
      </svg>
    </div>
  );
};

export default RadarChart;
