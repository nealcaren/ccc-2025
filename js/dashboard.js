// Function to fetch JSON data
async function fetchData(url) {
    const response = await fetch(url);
    return response.json();
}

// Function to format numbers
function formatNumber(num) {
    return num ? num.toLocaleString() : 'N/A';
}

// Function to truncate long text
function truncateText(text, maxLength = 50) {
    if (!text) return 'Unknown';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
}

// Load and display summary statistics
async function loadSummaryStats() {
    try {
        const stats = await fetchData('data/summary_stats.json');
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

        // Add top claims and targets
        if (stats.top_claims) {
            const claimsHtml = `
                <div class="col-md-6 mt-3">
                    <div class="card">
                        <div class="card-header">
                            <h3>Top Claims</h3>
                        </div>
                        <div class="card-body">
                            <ul class="list-group">
                                ${Object.entries(stats.top_claims).map(([claim, count]) => 
                                    `<li class="list-group-item d-flex justify-content-between align-items-center">
                                        ${truncateText(claim, 100)}
                                        <span class="badge bg-primary rounded-pill">${count}</span>
                                    </li>`
                                ).join('')}
                            </ul>
                        </div>
                    </div>
                </div>
            `;
            statsContainer.innerHTML += claimsHtml;
        }

        if (stats.top_targets) {
            const targetsHtml = `
                <div class="col-md-6 mt-3">
                    <div class="card">
                        <div class="card-header">
                            <h3>Top Targets</h3>
                        </div>
                        <div class="card-body">
                            <ul class="list-group">
                                ${Object.entries(stats.top_targets).map(([target, count]) => 
                                    `<li class="list-group-item d-flex justify-content-between align-items-center">
                                        ${truncateText(target, 100)}
                                        <span class="badge bg-primary rounded-pill">${count}</span>
                                    </li>`
                                ).join('')}
                            </ul>
                        </div>
                    </div>
                </div>
            `;
            statsContainer.innerHTML += targetsHtml;
        }
    } catch (error) {
        console.error('Error loading summary stats:', error);
        document.getElementById('summary-stats').innerHTML = `
            <div class="col-12">
                <div class="alert alert-danger">
                    Error loading summary statistics: ${error.message}
                </div>
            </div>
        `;
    }
}

// Load and display events by day chart
async function loadEventsChart() {
    try {
        const dateCounts = await fetchData('data/date_counts.json');
        
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
                maintainAspectRatio: false,
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
                        },
                        ticks: {
                            maxRotation: 90,
                            minRotation: 45
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading events chart:', error);
    }
}

// Load and display event types chart
async function loadEventTypesChart() {
    try {
        const eventTypes = await fetchData('data/event_types.json');
        
        // Sort by count and take top 10
        const sortedTypes = Object.entries(eventTypes)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10);
        
        const labels = sortedTypes.map(item => item[0]);
        const data = sortedTypes.map(item => item[1]);
        
        // Create chart
        const ctx = document.getElementById('eventTypesChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)',
                        'rgba(255, 159, 64, 0.7)',
                        'rgba(199, 199, 199, 0.7)',
                        'rgba(83, 102, 255, 0.7)',
                        'rgba(40, 159, 64, 0.7)',
                        'rgba(210, 199, 199, 0.7)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                    },
                    title: {
                        display: true,
                        text: 'Event Types Distribution'
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading event types chart:', error);
    }
}

// Load and display states chart
async function loadStatesChart() {
    try {
        const statesData = await fetchData('data/states.json');
        
        // Sort by count and take top 15
        const sortedStates = Object.entries(statesData)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 15);
        
        const labels = sortedStates.map(item => item[0]);
        const data = sortedStates.map(item => item[1]);
        
        // Create chart
        const ctx = document.getElementById('statesChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Events by State',
                    data: data,
                    backgroundColor: 'rgba(75, 192, 192, 0.7)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
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
                            text: 'State'
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading states chart:', error);
    }
}

// Table pagination and search variables
let allEvents = [];
let currentPage = 1;
const eventsPerPage = 25;
let filteredEvents = [];

// Load and display events table with pagination
async function loadEventsTable() {
    try {
        // Fetch all events
        allEvents = await fetchData('data/events_table.json');
        filteredEvents = [...allEvents];
        
        // Set up search functionality
        const searchInput = document.getElementById('tableSearch');
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            filteredEvents = allEvents.filter(event => 
                (event.date && event.date.toLowerCase().includes(searchTerm)) ||
                (event.locality && event.locality.toLowerCase().includes(searchTerm)) ||
                (event.state && event.state.toLowerCase().includes(searchTerm)) ||
                (event.event_type && event.event_type.toLowerCase().includes(searchTerm)) ||
                (event.targets && event.targets.toLowerCase().includes(searchTerm)) ||
                (event.claims_summary && event.claims_summary.toLowerCase().includes(searchTerm))
            );
            currentPage = 1;
            displayEventsPage();
        });
        
        // Set up pagination buttons
        document.getElementById('prevPage').addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage--;
                displayEventsPage();
            }
        });
        
        document.getElementById('nextPage').addEventListener('click', () => {
            const totalPages = Math.ceil(filteredEvents.length / eventsPerPage);
            if (currentPage < totalPages) {
                currentPage++;
                displayEventsPage();
            }
        });
        
        // Display first page
        displayEventsPage();
    } catch (error) {
        console.error('Error loading events table:', error);
        const tableBody = document.querySelector('#eventsTable tbody');
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center text-danger">
                    Error loading events data: ${error.message}
                </td>
            </tr>
        `;
    }
}

// Display current page of events
function displayEventsPage() {
    const tableBody = document.querySelector('#eventsTable tbody');
    const startIndex = (currentPage - 1) * eventsPerPage;
    const endIndex = Math.min(startIndex + eventsPerPage, filteredEvents.length);
    const pageEvents = filteredEvents.slice(startIndex, endIndex);
    
    if (pageEvents.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center">No events found matching your search criteria</td>
            </tr>
        `;
    } else {
        // Create table rows
        tableBody.innerHTML = pageEvents.map(event => `
            <tr>
                <td>${event.date || 'Unknown'}</td>
                <td>${event.locality || 'Unknown'}</td>
                <td>${event.state || 'Unknown'}</td>
                <td>${event.event_type || 'Unknown'}</td>
                <td>${event.size_mean ? Math.round(event.size_mean) : 'Unknown'}</td>
                <td>${truncateText(event.targets, 30) || 'Unknown'}</td>
                <td>${truncateText(event.claims_summary, 50) || 'Unknown'}</td>
            </tr>
        `).join('');
    }
    
    // Update pagination info
    const totalPages = Math.ceil(filteredEvents.length / eventsPerPage);
    document.getElementById('pageInfo').textContent = `Page ${currentPage} of ${totalPages || 1}`;
    document.getElementById('tableInfo').textContent = 
        `Showing ${startIndex + 1}-${endIndex} of ${filteredEvents.length} events`;
    
    // Update button states
    document.getElementById('prevPage').disabled = currentPage === 1;
    document.getElementById('nextPage').disabled = currentPage >= totalPages;
}

// Initialize the dashboard
async function initDashboard() {
    try {
        await Promise.all([
            loadSummaryStats(),
            loadEventsChart(),
            loadEventTypesChart(),
            loadStatesChart(),
            loadEventsTable()
        ]);
    } catch (error) {
        console.error('Error initializing dashboard:', error);
    }
}

// Load everything when the page is ready
document.addEventListener('DOMContentLoaded', initDashboard);
