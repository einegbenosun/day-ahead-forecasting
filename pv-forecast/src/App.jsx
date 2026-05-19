import { useState } from "react";
import "./App.css";
import axios from "axios";

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchAPI = async () => {
    setLoading(true);

    const paramsResponse = await axios.get("http://localhost:5001/params");
    const predictionsResponse = await axios.get("http://localhost:5001/predict");
    const totalResponse = await axios.get("http://localhost:5001/total");
    const dateResponse = await axios.get("http://localhost:5001/date");

    setData({
      longitude: paramsResponse.data.longitude,
      latitude: paramsResponse.data.latitude,
      predictions: predictionsResponse.data,
      total: totalResponse.data,
      date: dateResponse.data,
    
    });

    setLoading(false);
  };

  return (
    <main className="page">
      <div className="sun"></div>

      <h1>PV Forecast Dashboard</h1>
      <p>Day-ahead photovoltaic forecasting using live Open-Meteo data.</p>

      <button onClick={fetchAPI}>
        {loading ? "Loading..." : "Access Forecast Data"}
      </button>

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
            <strong>Total forecast:</strong> {Number(data.total).toFixed(2)}kWp
          </p>

          <h3>24-Hour Predictions</h3>
          <div className="prediction-grid">
            {data.predictions.map((value, index) => (
              <div className="prediction-box" key={index}>
                <span>{index}:00</span>
                <strong>{Number(value).toFixed(2)}</strong>
              </div>
            ))}
          </div>
        </div>


      )}
    </main>
  );
}

export default App;