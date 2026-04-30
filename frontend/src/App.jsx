import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [addCityInput, setAddCityInput] = useState('');
  const [checkCityInput, setCheckCityInput] = useState('');

  const [cityStatuses, setCityStatuses] = useState({});

  const [weatherCache, setWeatherCache] = useState({});

  const [displayedResult, setDisplayedResult] = useState(null);
  const [inputError, setInputError] = useState('');

  const handleAddCity = async () => {
    if (!addCityInput) return;
    const city = addCityInput;

    // איפוס שגיאה קודמת בכל לחיצה חדשה
    setInputError('');

    try {
      const response = await fetch('http://localhost:8000/weather/request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ city: city }),
      });

      if (response.ok) {
        // הכל תקין, העיר נכנסה לתור
        setCityStatuses(prev => ({ ...prev, [city]: 'processing' }));
        setAddCityInput('');
      } else {
        // השרת החזיר שגיאה (למשל 400 - עיר לא קיימת)
        setInputError(`העיר "${city}" לא נמצאה, נא לנסות שוב.`);
      }
    } catch (error) {
      console.error("Error sending request:", error);
      setInputError("שגיאת רשת, השרת לא זמין.");
    }
  };

  useEffect(() => {
    const processingCities = Object.keys(cityStatuses).filter(
      city => cityStatuses[city] === 'processing'
    );

    if (processingCities.length === 0) return;

    const intervalId = setInterval(async () => {
      for (const city of processingCities) {
        try {
          const response = await fetch(`http://localhost:8001/weather/result?city=${city}`);
          const data = await response.json();

          if (data.data) {
            setWeatherCache(prev => ({ ...prev, [city]: data.data }));
            setCityStatuses(prev => ({ ...prev, [city]: 'done' }));
          }
        } catch (error) {
          console.error(`Error checking status for ${city}:`, error);
        }
      }
    }, 2000);

    return () => clearInterval(intervalId);
  }, [cityStatuses]);

  const handleCheckSaved = () => {
    if (!checkCityInput) return;

    if (weatherCache[checkCityInput]) {
      setDisplayedResult({ city: checkCityInput, data: weatherCache[checkCityInput] });
    } else {
      setDisplayedResult({ city: checkCityInput, notFound: true });
    }
  };

  return (
    <div className="dashboard-container">
      <h1>מערכת מזג אוויר אסינכרונית</h1>

      <div className="panels-container">
        <div className="panel">
          <h2>הוספת עיר למערכת (לתור)</h2>
          <div className="input-group">
            <input
              type="text"
              value={addCityInput}
              onChange={(e) => {
                setAddCityInput(e.target.value);
                setInputError('');               
              }}
              placeholder="שם עיר (למשל: Paris)"
            />
            <button onClick={handleAddCity}>שלח לעיבוד</button>
          </div>

          {inputError && <p className="input-error-msg">{inputError}</p>}

          <div className="status-list">
            <h3>סטטוס עיבוד:</h3>
            <ul>
              {Object.entries(cityStatuses).map(([city, status]) => (
                <li key={city} className="status-item">
                  <span className="city-name">{city}</span>
                  {status === 'processing'
                    ? <span className="icon processing" title="מעבד...">⏳</span>
                    : <span className="icon done" title="מוכן">✅</span>}
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="panel memory-panel">
          <h2>שליפת נתונים מהזיכרון</h2>
          <div className="input-group">
            <input
              type="text"
              value={checkCityInput}
              onChange={(e) => setCheckCityInput(e.target.value)}
              placeholder="חפש עיר בזיכרון..."
            />
            <button onClick={handleCheckSaved}>בדוק בזיכרון</button>
          </div>

          <div className="result-display">
            {displayedResult && (
              displayedResult.notFound ? (
                <p className="error">הנתונים עבור {displayedResult.city} טרם מוכנים או שלא התבקשו מעולם.</p>
              ) : (
                <div className="success-result">
                  <h3>תוצאה עבור: {displayedResult.city}</h3>
                  {displayedResult.data.status === 'Success' ? (
                    <p>טמפרטורה: {displayedResult.data.temperature}°C <br /> מצב: {displayedResult.data.condition}</p>
                  ) : (
                    <p>שגיאה בשליפה מקורית: {displayedResult.data.error}</p>
                  )}
                </div>
              )
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;