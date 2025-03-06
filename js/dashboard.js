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
                    <div class="stats-number">${formatNumber(stats.total_size)}</div>
                    <div>Total Participants</div>
                </div>
            </div>
        `;

        // Add Protest Issues section
        const protestTagsHtml = `
            <div class="col-md-12 mt-3">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h3>Protest Issues</h3>
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" id="protestIssuesViewSwitch">
                            <label class="form-check-label" for="protestIssuesViewSwitch">View by participants</label>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-12">
                                <div class="chart-container" style="height: 400px;">
                                    <canvas id="protestIssuesChart"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        statsContainer.innerHTML += protestTagsHtml;
        
        // Load the protest issues chart after a short delay to ensure the DOM is updated
        setTimeout(() => {
            loadProtestIssuesChart();
            
            // Add event listener to the second switch
            const issuesViewSwitch = document.getElementById('protestIssuesViewSwitch');
            if (issuesViewSwitch) {
                issuesViewSwitch.addEventListener('change', function() {
                    // Update the main switch to match
                    const mainSwitch = document.getElementById('protestTagsViewSwitch');
                    if (mainSwitch) {
                        mainSwitch.checked = this.checked;
                        // Trigger the change event on the main switch
                        mainSwitch.dispatchEvent(new Event('change'));
                    }
                });
            }
        }, 100);
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


// Load and display states chart
async function loadStatesChart() {
    try {
        const statesData = await fetchData('data/states.json');
        const statesSizeData = await fetchData('data/states_size.json');
        
        // Sort by count and take top 15
        const sortedStates = Object.entries(statesData)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 15);
        
        const labels = sortedStates.map(item => item[0]);
        const eventCounts = sortedStates.map(item => item[1]);
        
        // Get average sizes for the top 15 states by event count
        const avgSizes = labels.map(state => 
            statesSizeData[state] ? Math.round(statesSizeData[state]) : 0
        );
        
        // Create chart
        const ctx = document.getElementById('statesChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Events by State',
                        data: eventCounts,
                        backgroundColor: 'rgba(75, 192, 192, 0.7)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Average Protest Size',
                        data: avgSizes,
                        backgroundColor: 'rgba(255, 99, 132, 0.7)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1,
                        type: 'line',
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Number of Events'
                        }
                    },
                    y1: {
                        beginAtZero: true,
                        position: 'right',
                        grid: {
                            drawOnChartArea: false
                        },
                        title: {
                            display: true,
                            text: 'Average Protest Size'
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


// Load and display tactics analysis chart
async function loadTacticsAnalysisChart() {
    try {
        const tacticsData = await fetchData('data/tactics_analysis.json');
        
        // Create chart
        const ctx = document.getElementById('tacticsAnalysisChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: tacticsData.labels,
                datasets: [{
                    label: 'Percentage of Events',
                    data: tacticsData.percentages,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)',
                        'rgba(255, 159, 64, 0.7)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.dataset.label || '';
                                const value = context.raw.toFixed(2) + '%';
                                const count = tacticsData.counts[context.dataIndex];
                                return `${label}: ${value} (${count} events)`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Percentage of Events'
                        },
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Tactic'
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading tactics analysis chart:', error);
    }
}

// Load and display protest size over time chart
async function loadSizeTimeChart() {
    try {
        const events = await fetchData('data/events_table.json');
        
        // Group events by date and calculate average size
        const sizeByDate = {};
        const countByDate = {};
        
        events.forEach(event => {
            if (!sizeByDate[event.date]) {
                sizeByDate[event.date] = 0;
                countByDate[event.date] = 0;
            }
            
            // Use size_mean if available, otherwise use 11
            const size = event.size_mean !== 'Unknown' ? parseFloat(event.size_mean) : 11;
            sizeByDate[event.date] += size;
            countByDate[event.date]++;
        });
        
        // Calculate average size for each date
        const avgSizeByDate = {};
        Object.keys(sizeByDate).forEach(date => {
            avgSizeByDate[date] = sizeByDate[date] / countByDate[date];
        });
        
        // Sort dates
        const dates = Object.keys(avgSizeByDate).sort();
        const avgSizes = dates.map(date => avgSizeByDate[date]);
        
        // Create chart
        const ctx = document.getElementById('sizeTimeChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Average Protest Size',
                    data: avgSizes,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    tension: 0.2,
                    pointRadius: 3
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
                            text: 'Average Size'
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
        console.error('Error loading size time chart:', error);
    }
}

// Load and display protest tags chart
async function loadProtestTagsChart() {
    try {
        const tagsData = await fetchData('data/protest_tags.json');
        
        // Create chart
        const ctx = document.getElementById('protestTagsChart').getContext('2d');
        let protestTagsChart;
        
        // Function to create or update the chart
        const updateChart = (byParticipants = false) => {
            const data = byParticipants ? tagsData.percentagesByParticipants : tagsData.percentages;
            const counts = byParticipants ? tagsData.participantCounts : tagsData.counts;
            const label = byParticipants ? 'Percentage of Participants' : 'Percentage of Events';
            const tooltipLabel = byParticipants ? 'participants' : 'events';
            
            // Create arrays for sorting while preserving color mapping
            const sortedIndices = Array.from(Array(tagsData.tags.length).keys())
                .sort((a, b) => (byParticipants ? 
                    tagsData.percentagesByParticipants[b] - tagsData.percentagesByParticipants[a] : 
                    tagsData.percentages[b] - tagsData.percentages[a]));
            
            const sortedLabels = sortedIndices.map(i => tagsData.tags[i]);
            const sortedData = sortedIndices.map(i => data[i]);
            const sortedCounts = sortedIndices.map(i => counts[i]);
            
            // Original color array to maintain consistent colors
            const colorArray = [
                'rgba(255, 99, 132, 0.7)',
                'rgba(54, 162, 235, 0.7)',
                'rgba(255, 206, 86, 0.7)',
                'rgba(75, 192, 192, 0.7)',
                'rgba(153, 102, 255, 0.7)',
                'rgba(255, 159, 64, 0.7)',
                'rgba(199, 199, 199, 0.7)',
                'rgba(83, 102, 255, 0.7)',
                'rgba(40, 159, 64, 0.7)',
                'rgba(210, 199, 199, 0.7)',
                'rgba(255, 99, 132, 0.7)'
            ];
            
            // Map the original colors to the sorted indices
            const sortedColors = sortedIndices.map(i => colorArray[i % colorArray.length]);
            
            // If chart exists, destroy it first
            if (protestTagsChart) {
                protestTagsChart.destroy();
            }
            
            // Create new chart
            protestTagsChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: sortedLabels,
                    datasets: [{
                        label: label,
                        data: sortedData,
                        backgroundColor: sortedColors,
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.dataset.label || '';
                                    const value = context.raw.toFixed(2) + '%';
                                    const count = sortedCounts[context.dataIndex];
                                    return `${label}: ${value} (${count} ${tooltipLabel})`;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: label
                            },
                            ticks: {
                                callback: function(value) {
                                    return value + '%';
                                }
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Tag'
                            }
                        }
                    }
                }
            });
        };
        
        // Initial chart creation
        updateChart(false);
        
        // Add event listener to the switch
        const viewSwitch = document.getElementById('protestTagsViewSwitch');
        if (viewSwitch) {
            viewSwitch.addEventListener('change', function() {
                updateChart(this.checked);
            });
        }
    } catch (error) {
        console.error('Error loading protest tags chart:', error);
    }
}

// Load and display protest issues chart in the summary section
async function loadProtestIssuesChart() {
    try {
        const tagsData = await fetchData('data/protest_tags.json');
        
        // Create chart
        const ctx = document.getElementById('protestIssuesChart');
        if (!ctx) {
            console.error('protestIssuesChart element not found');
            return; // Exit if element doesn't exist yet
        }
        
        // Get the canvas context for 2d drawing
        const context = ctx.getContext('2d');
        let protestIssuesChart;
        
        // Function to create or update the chart
        const updateChart = (byParticipants = false) => {
            const data = byParticipants ? tagsData.percentagesByParticipants : tagsData.percentages;
            const counts = byParticipants ? tagsData.participantCounts : tagsData.counts;
            const label = byParticipants ? 'Percentage of Participants' : 'Percentage of Events';
            const tooltipLabel = byParticipants ? 'participants' : 'events';
            
            // Create arrays for sorting while preserving color mapping
            const sortedIndices = Array.from(Array(tagsData.tags.length).keys())
                .sort((a, b) => (byParticipants ? 
                    tagsData.percentagesByParticipants[b] - tagsData.percentagesByParticipants[a] : 
                    tagsData.percentages[b] - tagsData.percentages[a]));
            
            const sortedLabels = sortedIndices.map(i => tagsData.tags[i]);
            const sortedData = sortedIndices.map(i => data[i]);
            const sortedCounts = sortedIndices.map(i => counts[i]);
            
            // Original color array to maintain consistent colors
            const colorArray = [
                'rgba(255, 99, 132, 0.7)',
                'rgba(54, 162, 235, 0.7)',
                'rgba(255, 206, 86, 0.7)',
                'rgba(75, 192, 192, 0.7)',
                'rgba(153, 102, 255, 0.7)',
                'rgba(255, 159, 64, 0.7)',
                'rgba(199, 199, 199, 0.7)',
                'rgba(83, 102, 255, 0.7)',
                'rgba(40, 159, 64, 0.7)',
                'rgba(210, 199, 199, 0.7)',
                'rgba(255, 99, 132, 0.7)'
            ];
            
            // Map the original colors to the sorted indices
            const sortedColors = sortedIndices.map(i => colorArray[i % colorArray.length]);
            
            // If chart exists, destroy it first
            if (protestIssuesChart) {
                protestIssuesChart.destroy();
            }
            
            // Create new chart
            protestIssuesChart = new Chart(context, {
                type: 'bar',
                data: {
                    labels: sortedLabels,
                    datasets: [{
                        label: label,
                        data: sortedData,
                        backgroundColor: sortedColors,
                        borderWidth: 1
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.dataset.label || '';
                                    const value = context.raw.toFixed(2) + '%';
                                    const count = sortedCounts[context.dataIndex];
                                    return `${label}: ${value} (${count} ${tooltipLabel})`;
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: label
                            },
                            ticks: {
                                callback: function(value) {
                                    return value + '%';
                                }
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Issue'
                            }
                        }
                    }
                }
            });
        };
        
        // Initial chart creation
        updateChart(false);
        
        // Add event listener to the switch in the main section to also update this chart
        const viewSwitch = document.getElementById('protestTagsViewSwitch');
        if (viewSwitch) {
            viewSwitch.addEventListener('change', function() {
                updateChart(this.checked);
            });
        }
    } catch (error) {
        console.error('Error loading protest issues chart:', error);
    }
}

// Initialize the dashboard
async function initDashboard() {
    try {
        await Promise.all([
            loadSummaryStats(),
            loadEventsChart(),
            loadSizeTimeChart(),
            loadStatesChart(),
            loadTacticsAnalysisChart(),
            loadProtestTagsChart(),
            loadEventsTable()
        ]);
    } catch (error) {
        console.error('Error initializing dashboard:', error);
    }
}

// Load everything when the page is ready
document.addEventListener('DOMContentLoaded', initDashboard);
