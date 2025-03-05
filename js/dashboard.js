// Function to fetch JSON data
async function fetchData(url) {
    const response = await fetch(url);
    return response.json();
}

// Function to format numbers
function formatNumber(num) {
    return num ? num.toLocaleString() : 'N/A';
}

// Load and display summary statistics
async function loadSummaryStats() {
    try {
        const stats = await fetchData('../data/summary_stats.json');
        const statsContainer = document.getElementById('summary-stats');
        
        // Create stats cards
        statsContainer.innerHTML = `
            <div class="col-md-3">
                <div class="card stats-card">
                    <div class="stats-number">${formatNumber(stats.total_events)}</div>
                    <div>Total Events</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stats-card">
                    <div class="stats-number">${formatNumber(stats.unique_locations)}</div>
                    <div>Unique Locations</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stats-card">
                    <div class="stats-number">${formatNumber(stats.unique_states)}</div>
                    <div>States/Territories</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stats-card">
                    <div class="stats-number">${Object.keys(stats.event_types).length}</div>
                    <div>Event Types</div>
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Error loading summary stats:', error);
    }
}

// Load and display events by day chart
async function loadEventsChart() {
    try {
        const dateCounts = await fetchData('../data/date_counts.json');
        
        // Prepare data for Chart.js
        const dates = Object.keys(dateCounts).sort();
        const counts = dates.map(date => dateCounts[date]);
        
        // Create chart
        const ctx = document.getElementById('eventsChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Number of Events',
                    data: counts,
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Events'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading events chart:', error);
    }
}

// Load and display events table
async function loadEventsTable() {
    try {
        const events = await fetchData('../data/events_table.json');
        const tableBody = document.querySelector('#eventsTable tbody');
        
        // Create table rows
        tableBody.innerHTML = events.map(event => `
            <tr>
                <td>${event.date}</td>
                <td>${event.locality || 'Unknown'}</td>
                <td>${event.state || 'Unknown'}</td>
                <td>${event.event_type || 'Unknown'}</td>
                <td>${event.size_mean ? Math.round(event.size_mean) : 'Unknown'}</td>
                <td>${event.targets || 'Unknown'}</td>
                <td>${event.claims_summary || 'Unknown'}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading events table:', error);
    }
}

// Initialize the dashboard
async function initDashboard() {
    await Promise.all([
        loadSummaryStats(),
        loadEventsChart(),
        loadEventsTable()
    ]);
}

// Load everything when the page is ready
document.addEventListener('DOMContentLoaded', initDashboard);
// Function to fetch JSON data
async function fetchData(url) {
    const response = await fetch(url);
    return response.json();
}

// Function to format numbers
function formatNumber(num) {
    return num ? num.toLocaleString() : 'N/A';
}

// Load and display summary statistics
async function loadSummaryStats() {
    try {
        const stats = await fetchData('../data/summary_stats.json');
        const statsContainer = document.getElementById('summary-stats');
        
        // Create stats cards
        statsContainer.innerHTML = `
            <div class="col-md-3">
                <div class="card stats-card">
                    <div class="stats-number">${formatNumber(stats.total_events)}</div>
                    <div>Total Events</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stats-card">
                    <div class="stats-number">${formatNumber(stats.unique_locations)}</div>
                    <div>Unique Locations</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stats-card">
                    <div class="stats-number">${formatNumber(stats.unique_states)}</div>
                    <div>States/Territories</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stats-card">
                    <div class="stats-number">${Object.keys(stats.event_types).length}</div>
                    <div>Event Types</div>
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Error loading summary stats:', error);
    }
}

// Load and display events by day chart
async function loadEventsChart() {
    try {
        const dateCounts = await fetchData('../data/date_counts.json');
        
        // Prepare data for Chart.js
        const dates = Object.keys(dateCounts).sort();
        const counts = dates.map(date => dateCounts[date]);
        
        // Create chart
        const ctx = document.getElementById('eventsChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Number of Events',
                    data: counts,
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Events'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading events chart:', error);
    }
}

// Load and display events table
async function loadEventsTable() {
    try {
        const events = await fetchData('../data/events_table.json');
        const tableBody = document.querySelector('#eventsTable tbody');
        
        // Create table rows
        tableBody.innerHTML = events.map(event => `
            <tr>
                <td>${event.date}</td>
                <td>${event.locality || 'Unknown'}</td>
                <td>${event.state || 'Unknown'}</td>
                <td>${event.event_type || 'Unknown'}</td>
                <td>${event.size_mean ? Math.round(event.size_mean) : 'Unknown'}</td>
                <td>${event.targets || 'Unknown'}</td>
                <td>${event.claims_summary || 'Unknown'}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading events table:', error);
    }
}

// Initialize the dashboard
async function initDashboard() {
    await Promise.all([
        loadSummaryStats(),
        loadEventsChart(),
        loadEventsTable()
    ]);
}

// Load everything when the page is ready
document.addEventListener('DOMContentLoaded', initDashboard);
