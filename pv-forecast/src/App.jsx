import { useState } from "react";
import "./App.css";
import axios from "axios";
import { AreaChart, Area, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(null);
  const [error, setError] = useState(null)
  const chartData = data
  ? data.predictions.map((value, index) => ({ hour: `${index}:00`, watts: Number(value) }))
  : [];
  const maxPower = data ? Math.max(...data.predictions) : 0;


  const fetchAPI = async () => {
    setLoading(true);
    setError(null)

    try{
      const paramsResponse = await axios.get("http://localhost:5001/params");
      const predictionsResponse = await axios.get("http://localhost:5001/predict");
      const dateResponse = await axios.get("http://localhost:5001/date");

      const total = predictionsResponse.data.reduce((sum,value) => sum + value, 0)

      setData({
        longitude: paramsResponse.data.longitude,
        latitude: paramsResponse.data.latitude,
        predictions: predictionsResponse.data,
        total: total,
        date: dateResponse.data,
        pvConfig: paramsResponse.data.pv_config,
      });
  } catch (err){
  setError(`Could not load forecast data: ${err.message}.`);

  } finally{
  setLoading(false);
  }
};

  return (
    <main className="page">
      <div className="sun"></div>

      <h1>PV Forecast Dashboard</h1>
      <p>Day-ahead photovoltaic forecasting using live Open-Meteo data.</p>

      <button onClick={fetchAPI}>
        {loading ? "Loading..." : "Access Forecast Data"}
      </button>

      {error && <p className="error-message">{error}</p>}

      {data?.pvConfig &&(
        <div className="card">
          <h2>System Assumptions</h2>
          <p><strong>Capacity:</strong> {(data.pvConfig.panel_capacity_w).toFixed(2)}W</p>
          <p><strong>Tilt:</strong> {data.pvConfig.panel_tilt_deg}°</p>
          <p><strong>Azimuth:</strong> {data.pvConfig.panel_direction}°</p>
          <p><strong>Elevation:</strong> {(data.pvConfig.altitude_m).toFixed(2)}m</p>
          <p><strong>PV Watt Losses:</strong> {(data.pvConfig.pv_loss).toFixed(2)}% </p>
        </div>
      )}


      {data && (
        <div className="card">
          <h2>Daily Forecast Summary</h2>
          <p>
            <strong>Date:</strong> {data.date}
          </p>

          <p>
            <strong>Location:</strong> {data.latitude}, {data.longitude}
          </p>

        
          <p>
            <strong>Total forecast:</strong> {Number(data.total/1000).toFixed(2)}kWh
          </p>

          <h3>24-Hour Predictions</h3>
          <div className="bar-list">
            {data.predictions.map((value, index) => (
              <div className="bar-row" key={index}>
                <span className="bar-hour">{index}:00</span>
                <div className="bar-track">
                  <div
                    className="bar-fill"
                    style={{ width: `${maxPower > 0 ? (value / maxPower) * 100 : 0}%` }}
                  />
                </div>
                <span className="bar-value">{Number(value).toFixed(2)}W</span>
          </div>
        ))}
      </div>
    </div>
  )}
  




    </main>
  );
}

export default App;