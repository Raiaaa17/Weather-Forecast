function refreshWeather() {
    const refreshBtn = document.getElementById('refresh-btn');
    const lastUpdateSpan = document.getElementById('last-update-time');
    
    // Add loading state
    refreshBtn.classList.add('loading');
    refreshBtn.disabled = true;

    fetch('/refresh-weather')
        .then(response => response.json())
        .then(data => {
            // Update the weather cards
            const weatherGrid = document.querySelector('.weather-grid');
            if (weatherGrid) {
                let newHtml = '';
                Object.entries(data.weather_data).forEach(([date, timeData], index) => {
                    newHtml += `
                        <div class="weather-card" style="--card-index: ${index + 1}">
                            <div class="date">${date}</div>
                            <div class="forecast">`;
                    
                    Object.entries(timeData).forEach(([time, [weather, temp]]) => {
                        const weatherIcon = getWeatherIcon(weather);
                        newHtml += `
                            <div class="time-slot">
                                <span class="time">${time}</span>
                                <span class="weather">
                                    <i class="fas fa-${weatherIcon}"></i>
                                    ${weather}
                                </span>
                                <span class="temp">${temp}°C</span>
                            </div>`;
                    });
                    
                    newHtml += `
                            </div>
                        </div>`;
                });
                weatherGrid.innerHTML = newHtml;
            }

            // Update last update time
            lastUpdateSpan.textContent = data.last_update;
        })
        .catch(error => {
            console.error('Error refreshing weather:', error);
            alert('Failed to refresh weather data. Please try again.');
        })
        .finally(() => {
            // Remove loading state
            refreshBtn.classList.remove('loading');
            refreshBtn.disabled = false;
        });
}

// Helper function to get the appropriate weather icon
function getWeatherIcon(weather) {
    const icons = {
        'Clear': 'sun',
        'Clouds': 'cloud',
        'Rain': 'cloud-rain',
        'Snow': 'snowflake',
        'Thunderstorm': 'bolt',
        'Drizzle': 'cloud-rain',
        'Mist': 'smog',
        'Fog': 'smog'
    };
    return icons[weather] || 'cloud';
} 