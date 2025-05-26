// Constants
const REFRESH_INTERVAL = 3 * 60 * 60 * 1000; // 3 hours in milliseconds

function refreshWeather() {
    const refreshBtn = document.getElementById('refresh-btn');
    const lastUpdateSpan = document.getElementById('last-update-time');
    
    // Add loading state
    if (refreshBtn) {
        refreshBtn.classList.add('loading');
        refreshBtn.disabled = true;
    }

    fetch('/refresh-weather')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Update the weather cards
            const weatherGrid = document.querySelector('.weather-grid');
            if (weatherGrid) {
                let newHtml = '';
                Object.entries(data.weather_data).forEach(([date, forecasts], index) => {
                    newHtml += `
                        <div class="weather-card" style="--card-index: ${index + 1}">
                            <div class="date">${date}</div>
                            <div class="forecast">`;
                    
                    forecasts.forEach(forecast => {
                        newHtml += `
                            <div class="time-slot">
                                <span class="time">${forecast.time}</span>
                                <span class="weather">
                                    <i class="fas fa-${forecast.icon}"></i>
                                    ${forecast.description}
                                </span>
                                <span class="temp">${forecast.temp}°C</span>
                            </div>`;
                    });
                    
                    newHtml += `
                            </div>
                        </div>`;
                });
                weatherGrid.innerHTML = newHtml;
            }

            // Update last update time
            if (lastUpdateSpan) {
                lastUpdateSpan.textContent = data.last_update;
            }
        })
        .catch(error => {
            console.error('Error refreshing weather:', error);
            // Only show alert if it was a manual refresh
            if (refreshBtn && refreshBtn.classList.contains('loading')) {
                alert('Failed to refresh weather data. Please try again.');
            }
        })
        .finally(() => {
            // Remove loading state
            if (refreshBtn) {
                refreshBtn.classList.remove('loading');
                refreshBtn.disabled = false;
            }
        });
}

// Initialize auto-refresh when the page loads
document.addEventListener('DOMContentLoaded', () => {
    // Initial refresh
    refreshWeather();
    
    // Set up auto-refresh interval
    setInterval(refreshWeather, REFRESH_INTERVAL);
    
    // Add visibility change handler to refresh when tab becomes visible
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') {
            refreshWeather();
        }
    });
}); 