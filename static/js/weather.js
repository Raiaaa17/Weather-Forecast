// Constants
const REFRESH_INTERVAL = 3 * 60 * 60 * 1000; // 3 hours in milliseconds

function refreshWeather() {
    const refreshBtn = document.getElementById('refresh-btn');
    const lastUpdateSpan = document.getElementById('last-update-time');
    const nextUpdateSpan = document.getElementById('next-update-time');
    
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
            // Reload the page to get fresh server-side rendered content
            window.location.reload();
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