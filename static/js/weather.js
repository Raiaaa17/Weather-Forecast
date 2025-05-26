// Constants
const REFRESH_INTERVAL = 3 * 60 * 60 * 1000; // 3 hours in milliseconds

// Function to ensure SGT is displayed in the last update time
function ensureSGTDisplay() {
    const lastUpdateSpan = document.getElementById('last-update-time');
    if (lastUpdateSpan && !lastUpdateSpan.textContent.includes('SGT')) {
        lastUpdateSpan.textContent = `${lastUpdateSpan.textContent} SGT`;
    }
}

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
                lastUpdateSpan.textContent = `${data.last_update} SGT`;
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

// Function to calculate time until next 3-hour mark
function getTimeUntilNextUpdate() {
    const now = new Date();
    const hours = now.getHours();
    const nextUpdateHour = Math.ceil(hours / 3) * 3; // Round up to next 3-hour mark
    const nextUpdate = new Date(now);
    nextUpdate.setHours(nextUpdateHour, 0, 0, 0);
    
    if (nextUpdate <= now) {
        nextUpdate.setHours(nextUpdate.getHours() + 3); // Add 3 hours if we're past the time
    }
    
    return nextUpdate - now;
}

// Auto-refresh logic
function setupAutoRefresh() {
    const timeUntilUpdate = getTimeUntilNextUpdate();
    console.log(`Next auto-refresh in ${Math.round(timeUntilUpdate / 1000 / 60)} minutes`);
    
    setTimeout(() => {
        refreshWeather();
        setupAutoRefresh(); // Set up next refresh
    }, timeUntilUpdate);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    // Ensure SGT is displayed on initial load
    ensureSGTDisplay();
    
    // Set up initial auto-refresh
    setupAutoRefresh();
    
    // Also refresh when tab becomes visible
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') {
            refreshWeather();
        }
    });
}); 