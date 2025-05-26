// Constants
const REFRESH_INTERVAL = 3 * 60 * 60 * 1000; // 3 hours in milliseconds

function refreshWeather() {
    const refreshBtn = document.getElementById('refresh-btn');
    
    if (refreshBtn) {
        refreshBtn.disabled = true;
        refreshBtn.querySelector('i').classList.add('fa-spin');
    }

    fetch('/refresh-weather')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            // Update last update time
            const lastUpdateSpan = document.getElementById('last-update-time');
            if (lastUpdateSpan && data.last_update) {
                lastUpdateSpan.textContent = data.last_update;
            }
            
            // Update weather grid
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
        })
        .catch(error => {
            console.error('Error refreshing weather:', error);
            alert('Failed to refresh weather data. Please try again.');
        })
        .finally(() => {
            if (refreshBtn) {
                refreshBtn.disabled = false;
                refreshBtn.querySelector('i').classList.remove('fa-spin');
            }
        });
}

// Auto-refresh logic
document.addEventListener('DOMContentLoaded', () => {
    const nextUpdateSpan = document.getElementById('next-update-time');
    if (nextUpdateSpan) {
        const updateTime = nextUpdateSpan.getAttribute('data-time');
        if (updateTime) {
            const nextUpdate = new Date(updateTime);
            const now = new Date();
            const timeUntilUpdate = nextUpdate - now;
            
            if (timeUntilUpdate > 0) {
                setTimeout(() => {
                    window.location.reload();
                }, timeUntilUpdate);
            }
        }
    }
}); 