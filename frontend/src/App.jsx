import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function App() {
  const [history, setHistory] = useState([]);
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const histRes = await fetch("http://localhost:8000/history/wti");
        const histData = await histRes.json();
        const forecastRes = await fetch("http://localhost:8000/forecast/wti");
        const forecastData = await forecastRes.json();
        
        setHistory(histData);
        setForecast(forecastData);
      } catch (e) {
        console.error("Backend not reachable. Displaying fallback UI.", e);
        setHistory([
          { date: '2026-03-01', wti_usd_per_barrel: 78.5 },
          { date: '2026-03-02', wti_usd_per_barrel: 79.2 },
          { date: '2026-03-03', wti_usd_per_barrel: 81.0 },
          { date: '2026-03-04', wti_usd_per_barrel: 83.5 },
          { date: '2026-03-05', wti_usd_per_barrel: 85.0 },
        ]);
        setForecast({
            predicted_value: 86.50,
            forecast_timestamp: '2026-03-06',
            recent_event_intensity: 45.2
        });
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div style={{padding: '2rem', fontFamily: 'sans-serif'}}>Loading forecasting data...</div>;

  const chartData = [...history];
  if (forecast) {
    chartData.push({
      date: forecast.forecast_timestamp.split('T')[0],
      forecast_value: forecast.predicted_value
    });
  }

  return (
    <div style={{ fontFamily: 'sans-serif', padding: '2rem', maxWidth: '1000px', margin: '0 auto' }}>
      <h1>🌍 Energy Price Forecasting Dashboard</h1>
      <p>Short-term predictions using market fundamentals and geopolitical shock indicators.</p>
      
      <div style={{ display: 'flex', gap: '2rem', marginBottom: '2rem', flexWrap: 'wrap' }}>
        <div style={{ padding: '1.5rem', background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '12px', flex: 1 }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#64748b' }}>Latest WTI Forecast (1d)</h3>
          <h2 style={{ color: '#0f172a', fontSize: '2.5rem', margin: 0 }}>${forecast?.predicted_value} <span style={{fontSize:'1rem', color:'#64748b'}}>/ bbl</span></h2>
          <p style={{ color: '#64748b' }}>Target Date: {forecast?.forecast_timestamp.split('T')[0]}</p>
        </div>
        <div style={{ padding: '1.5rem', background: '#fef2f2', border: '1px solid #fecaca', borderRadius: '12px', flex: 1 }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#991b1b' }}>Geopolitical Risk Score</h3>
          <h2 style={{ color: '#7f1d1d', fontSize: '2.5rem', margin: 0 }}>{forecast?.recent_event_intensity}</h2>
          <p style={{ color: '#991b1b' }}>Driven by conflict events and infra attacks</p>
        </div>
      </div>

      <div style={{ height: '450px', width: '100%', border: '1px solid #e2e8f0', padding: '1rem', borderRadius: '12px', background: 'white' }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="date" tick={{fontSize: 12}} dy={10} />
            <YAxis domain={['auto', 'auto']} tick={{fontSize: 12}} />
            <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
            <Legend wrapperStyle={{ paddingTop: '20px' }} />
            <Line type="monotone" dataKey="wti_usd_per_barrel" stroke="#3b82f6" name="Actual WTI" strokeWidth={3} dot={{r: 3}} activeDot={{r: 6}} />
            <Line type="monotone" dataKey="forecast_value" stroke="#ef4444" name="Forecast WTI" strokeWidth={3} strokeDasharray="5 5" dot={{r: 5, fill: '#ef4444'}} />
          </LineChart>
        </ResponsiveContainer>
      </div>
      
      <p style={{marginTop: '20px', fontSize: '0.85rem', color: '#94a3b8'}}>
        * Note: Recharts visualization connected to FastAPI backend. If backend unreachable, demo data shown.
      </p>
    </div>
  );
}

export default App;
